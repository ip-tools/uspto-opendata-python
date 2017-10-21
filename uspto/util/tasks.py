# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
import json
import types
import celery
import logging

celery_app = celery.Celery('uspto.util.tasks', backend='redis://localhost', broker='redis://localhost')

celery_app.conf.update(
    task_serializer = 'pickle',
    result_serializer = 'pickle',
    accept_content = ['pickle'],
)


logger = logging.getLogger(__name__)

# http://shulhi.com/class-based-celery-task/
# http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
class GenericDownloadTask(celery.Task):

    def __init__(self, *args, **kwargs):
        self.client = self.client_factory()
        self.database = kwargs.get('database', None)
        self.host = kwargs.get('host', None)
        self.result = None

    # Main entry
    def process(self, query):
        logger.info('Starting download process for %s', query)
        self.download(query)
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

    def download(self, query):
        logger.info('Starting download job with %s', query)
        self.update_state(state='PROGRESS', meta={'stage': 'downloading', 'query': query})
        self.result = self.client.download(**query)

    def finish(self):
        self.update_state(state='PROGRESS', meta={'stage': 'finished', })
        pass



class AsynchronousDownloader:

    def __init__(self, task_function):
        self.task_function = task_function
        self.task = None

    def run(self, query):
        """
        https://celery.readthedocs.io/en/latest/userguide/canvas.html#groups
        """

        logger.info('Starting download of "%s"', query)

        # http://docs.celeryproject.org/en/latest/userguide/calling.html

        if isinstance(query, dict):
            self.task = self.task_function.delay(query)

        elif isinstance(query, list):
            tasks = map(self.task_function.s, query)
            task_group = celery.group(tasks)
            self.task = task_group.delay()

        return self.task

    def poll(self):
        if isinstance(self.task, celery.group):
            return self.poll_group()
        else:
            return self.poll_task()

    def poll_task(self):
        logger.info('Task id is "%s"', self.task.id)
        try:
            while not self.task.ready():
                logger.info('Task %s in state %s', self.task.id, self.task.state)
                time.sleep(1)

            result = self.task.get()
            logger.info('Download succeeded')
            #print(json.dumps(result, indent=4))
            return result

        except Exception as ex:
            logger.error('Download failed with exception: "%s"', ex)

    def poll_group(self):
        while self.task.results:

            for subtask in self.task.results:

                #print 'task:', task
                #print 'self.task.dir:', dir(task)

                if subtask.ready():
                    logger.info('Task %s in state %s.', subtask.id, subtask.state)

                    try:
                        result = subtask.get()
                        logger.info('Download succeeded')
                        print(json.dumps(result, indent=4))

                    except Exception as ex:
                        logger.error('Download failed with exception: "%s"', ex)

                    self.task.results.remove(subtask)

                else:
                    #print dir(result)
                    logger.info('Task %s in state %s. Metadata: %s', subtask.id, subtask.state, subtask.info)

            time.sleep(1)

