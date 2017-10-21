# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from celery import Celery, Task
from celery.decorators import task
from uspto.pbd.api import UsptoPairBulkDataClient

celery_app = Celery('uspto.pbd.tasks', backend='redis://localhost', broker='redis://localhost')

celery_app.conf.update(
    task_serializer = 'pickle',
    result_serializer = 'pickle',
    accept_content = ['pickle'],
)

logger = logging.getLogger(__name__)

@task
def download(query):
    # https://celery.readthedocs.io/en/latest/userguide/canvas.html#chains
    task = DownloadTask().delay(**query)
    return task


# http://shulhi.com/class-based-celery-task/
class DownloadTask(Task):

    name = 'uspto.pbd.tasks.DownloadTask'

    def __init__(self, *args, **kwargs):
        self.client = UsptoPairBulkDataClient()
        self.database = kwargs.get('database', None)
        self.host = kwargs.get('host', None)
        self.result = None

    # Main entry
    def run(self, *args, **query):
        self.download(**query)
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

    def download(self, **query):
        logger.info('Starting download job with %s', query)
        self.update_state(state='PROGRESS', meta={'stage': 'downloading', 'query': query})
        self.result = self.client.download(**query)

    def finish(self):
        self.update_state(state='PROGRESS', meta={'stage': 'finished', })

celery_app.tasks.register(DownloadTask)
