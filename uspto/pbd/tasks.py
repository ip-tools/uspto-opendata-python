# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
from celery import Celery
from celery.result import GroupResult
from celery.schedules import crontab
from celery.decorators import task

app = Celery('uspto.pbd.tasks', backend='redis://localhost', broker='redis://localhost')

app.conf.update(
    task_serializer = 'pickle',
    result_serializer = 'pickle',
    accept_content = ['pickle'],
)

@task
def submit_query(arg):
    print('submit_query:', arg)
    return '82917889-f8ec-4a5c-bf27-ddf7a3ed1e05'

@task
def request_package(query_id, arg):
    print('request_package:', arg)
    print('query id:', query_id)
    return query_id

@task
def wait_for_package(query_id, arg):
    print('wait_for_package:', arg)
    time.sleep(10)
    return query_id

@task
def download_package(query_id, arg):
    print('download_package:', arg)
    return 'BLOB'

@task
def download(query):
    # https://celery.readthedocs.io/en/latest/userguide/canvas.html#chains
    chain = submit_query.s(query) | request_package.s(query) | wait_for_package.s(query) | download_package.s(query)
    result = chain()
    return result
