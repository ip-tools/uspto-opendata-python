# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import time
import json
import logging
import celery
import celery.exceptions
from collections import OrderedDict
from uspto.util.client import NoResults, UnknownDocumentType
from uspto.util.common import get_document_path, to_list
# Must import here to enable communication with Celery
import uspto.celery.app

logger = logging.getLogger(__name__)

# http://shulhi.com/class-based-celery-task/
# http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
class GenericDownloadTask(celery.Task):

    # Retry one hour after an error happened
    RETRY_COUNTDOWN = 60 * 60

    # How often to retry
    RETRY_ATTEMPTS  = 5

    def __init__(self, *args, **kwargs):
        self.client = self.client_factory()
        self.database = kwargs.get('database', None)
        self.host = kwargs.get('host', None)
        self.options = None
        self.result = None

        # TODO: Implement "storage_strategy = MongoDB"
        # http://docs.celeryproject.org/en/latest/userguide/tasks.html?highlight=retry#instantiation

    # Wrap the celery app within the web framework context
    # TODO: Does not work somehow
    #def bind(self, app):
    #    super(self.__class__, self).bind(self, celery_app)

    # Main entrypoint
    def process(self, query, options=None):
        self.query = query
        self.options = options or {}

        if isinstance(self.query, str):
            self.query = {'number': self.query}

        logger.info('Starting download process for query=%s, options=%s', query, options)
        self.result = {'metadata': {'query': self.query, 'options': self.options, 'files': []}}

        # Download and store the document
        try:
            self.download()
            self.enrich()
            self.store()

        # If this is an unrecoverable error, we reject it so that it's redelivered
        # to the dead letter exchange and we can manually inspect the situation.
        # http://docs.celeryproject.org/en/latest/userguide/tasks.html#reject
        except (NoResults, UnknownDocumentType) as ex:
            # FIXME: Task keeps being in PENDING state when rejected
            #raise celery.exceptions.Reject(reason=ex, requeue=False)

            # Workaround: Just re-raise the original exception
            raise

        # Otherwise, let's retry again after some time
        except Exception as ex:
            raise self.retry(exc=ex, countdown=self.RETRY_COUNTDOWN, max_retries=self.RETRY_ATTEMPTS)

        return self.result

    # TODO: Implement "after_return" and "on_retry"
    # # http://docs.celeryproject.org/en/latest/userguide/tasks.html#handlers

    def on_success(self, retval, task_id, *args, **kwargs):
        logger.info('DownloadTask succeeded')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('DownloadTask failed')
        logger.error(exc)

    def download(self):
        logger.info('Starting download job with query=%s', self.query)
        self.update_state(state='PROGRESS', meta={'stage': 'downloading', 'query': self.query})
        result = self.client.download_document(**self.query)
        self.result.update(result)

    def enrich(self):
        if self.options.get('use-application-id'):
            document = self.client.document_factory(data=self.result)
            document_identifiers = document.get_identifiers()
            self.result['metadata'].update(document_identifiers=document_identifiers)

    def store(self):
        self.update_state(state='PROGRESS', meta={'stage': 'finishing'})
        if self.options.get('save'):
            logger.info('Storing with options: %s', self.options)

            directory = self.options.get('directory')

            for format in to_list(self.query.get('format')):

                # Compute file name
                if self.options.get('use-application-id'):
                    filename = self.result['metadata']['document_identifiers']['application']
                else:
                    filename = self.query.get('number')

                # Compute file path
                filepath = get_document_path(directory, filename, format, self.client.DATASOURCE_NAME)

                # Pre-flight checks
                if os.path.exists(filepath):
                    if not self.options.get('overwrite'):
                        logger.warning('File "%s" already exists. Use --overwrite.', filepath)
                        continue

                # Get payload by format
                payload = self.result[format]
                if format == 'json' and self.options.get('pretty'):
                    payload = json.dumps(json.loads(payload), indent=4)

                # Save file
                logger.info('Saving document file to {}'.format(os.path.abspath(filepath)))
                open(filepath, 'w').write(payload)

                # Bookkeeping: Aggregate target files
                self.result['metadata']['files'].append(filepath)


class AsynchronousDownloader:

    def __init__(self, task_function=None):

        if task_function:
            self.task_function = task_function

        self.task = None

    def run(self, query, options=None):
        """
        https://celery.readthedocs.io/en/latest/userguide/canvas.html#groups
        """

        logger.info('Starting download with query=%s, options=%s', query, options)

        # http://docs.celeryproject.org/en/latest/userguide/calling.html

        if isinstance(query, str):
            query = {'number': query}

        if isinstance(query, dict):
            self.task = self.task_function.delay(query, options)

        elif isinstance(query, list):
            tasks = [self.task_function.s(query, options) for query in query]
            task_group = celery.group(tasks)
            self.task = task_group.delay()

        else:
            raise TypeError('Unknown type for query {}. type={}'.format(query, type(query)))

        return self.task

    def poll(self):
        if isinstance(self.task, celery.result.AsyncResult):
            return self.poll_task()
        elif isinstance(self.task, celery.result.GroupResult):
            return self.poll_group()
        else:
            raise ValueError('Unknown result type from Celery task scheduler. type=%s, value=%s', type(self.task), self.task)

    def poll_task(self):
        logger.info('Polling task with id=%s', self.task.id)
        try:
            while not self.task.ready():
                logger.info('Task with id=%s in state %s', self.task.id, self.task.state)
                time.sleep(1)

            result = self.task.get()
            logger.info('Download ready')
            return result

        except Exception as ex:
            logger.error('Download failed with exception: "%s: %s"', ex.__class__.__name__, ex)
            raise

    def poll_group(self):
        results = OrderedDict()
        errors = []
        while self.task.results:

            for subtask in self.task.results:

                if subtask.ready():
                    logger.info('Task with id=%s in state %s.', subtask.id, subtask.state)

                    try:
                        result = subtask.get()
                        logger.info('Download succeeded')

                        if result['metadata']['options'].get('use-application-id'):
                            key = result['metadata']['document_identifiers']['application']
                        else:
                            key = result['metadata']['query']['number']

                        results[key] = result

                    except Exception as ex:
                        logger.error('Download failed with exception: "%s: %s"', ex.__class__.__name__, ex)
                        error = {
                            'message': '{}: {}'.format(ex.__class__.__name__, ex)
                        }
                        if hasattr(ex, 'more_info'):
                            error.update(ex.more_info)
                        errors.append(error)

                    self.task.results.remove(subtask)

                else:
                    logger.info('Task %s in state %s. Metadata: %s', subtask.id, subtask.state, subtask.info)

            time.sleep(1)

        response = OrderedDict()
        response['results'] = results
        response['errors']  = errors
        return response
