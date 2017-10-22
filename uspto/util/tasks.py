# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import time
import json
import celery
import logging
from collections import OrderedDict
from uspto.util.common import get_document_path, to_list

logger = logging.getLogger(__name__)

# http://shulhi.com/class-based-celery-task/
# http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
class GenericDownloadTask(celery.Task):

    def __init__(self, *args, **kwargs):
        self.client = self.client_factory()
        self.database = kwargs.get('database', None)
        self.host = kwargs.get('host', None)
        self.options = None
        self.result = None

    # Main entry
    def process(self, query, options=None):
        self.query = query
        self.options = options or {}

        logger.info('Starting download process for query=%s, options=%s', query, options)
        self.result = {'metadata': {'query': self.query, 'options': self.options, 'files': []}}
        self.download()
        self.finish()
        return self.result

    # Wrap the celery app within the Flask context
    #def bind(self, app):
    #    super(self.__class__, self).bind(self, celery_app)

    def on_success(self, retval, task_id, *args, **kwargs):
        logger.info('DownloadTask succeeded')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('DownloadTask failed')
        logger.error(exc)

    def download(self):
        logger.info('Starting download job with query=%s', self.query)
        self.update_state(state='PROGRESS', meta={'stage': 'downloading', 'query': self.query})
        result = self.client.download(**self.query)
        self.result.update(result)


    def finish(self):
        self.update_state(state='PROGRESS', meta={'stage': 'finishing'})
        if self.options.get('save'):
            logger.info('Storing with options: %s', self.options)

            document = self.client.document_factory(data=self.result)
            document_identifiers = document.get_identifiers()
            directory = self.options.get('directory')

            for format in to_list(self.query.get('format')):

                # Compute file name
                if self.options.get('use_application_id'):
                    filename = document_identifiers['application']
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
                open(filepath, 'w').write(payload)
                logger.info('Saved document to {}'.format(filepath))

                # Bookkeeping: Aggregate target files
                self.result['metadata']['files'].append(filepath)


class AsynchronousDownloader:

    def __init__(self, task_function):
        self.task_function = task_function
        self.task = None

    def run(self, query, options=None):
        """
        https://celery.readthedocs.io/en/latest/userguide/canvas.html#groups
        """

        logger.info('Starting download with query=%s, options=%s', query, options)

        # http://docs.celeryproject.org/en/latest/userguide/calling.html

        if isinstance(query, dict):
            self.task = self.task_function.delay(query, options)

        elif isinstance(query, list):
            tasks = [self.task_function.s(query, options) for query in query]
            task_group = celery.group(tasks)
            self.task = task_group.delay()

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

    def poll_group(self):
        results = OrderedDict()
        while self.task.results:

            for subtask in self.task.results:

                if subtask.ready():
                    logger.info('Task with id=%s in state %s.', subtask.id, subtask.state)

                    try:
                        result = subtask.get()
                        logger.info('Download succeeded')

                        key = result['metadata']['query']['number']
                        results[key] = result

                    except Exception as ex:
                        logger.error('Download failed with exception: "%s: %s"', ex.__class__.__name__, ex)

                    self.task.results.remove(subtask)

                else:
                    logger.info('Task %s in state %s. Metadata: %s', subtask.id, subtask.state, subtask.info)

            time.sleep(1)

        return results
