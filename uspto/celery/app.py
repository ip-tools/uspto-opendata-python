# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import celery

celery_app = celery.Celery(__name__, backend='redis://localhost', broker='redis://localhost')
celery_app.conf.update(
    task_serializer = 'pickle',
    result_serializer = 'pickle',
    accept_content = ['pickle'],
)
