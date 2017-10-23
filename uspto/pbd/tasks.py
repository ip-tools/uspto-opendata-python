# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import celery
from uspto.util.tasks import GenericDownloadTask, AsynchronousDownloader
from uspto.pbd.client import UsptoPairBulkDataClient

class UsptoPairBulkDataDownloadTask(GenericDownloadTask):
    name = 'uspto.pbd.tasks.UsptoPairBulkDataDownloadTask'
    client_factory = UsptoPairBulkDataClient

@celery.shared_task(bind=True, base=UsptoPairBulkDataDownloadTask)
def download_task(self, query, options=None):
    """
    https://celery.readthedocs.io/en/latest/userguide/tasks.html#basics
    http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
    """
    return self.process(query, options)

class UsptoPairBulkDataDownloader(AsynchronousDownloader):
    task_function = download_task
