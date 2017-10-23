# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
# Must import here to enable communication with Celery
from uspto.celery.app import celery_app
from celery.loaders.base import autodiscover_tasks

# Register application tasks
autodiscover_tasks(['uspto.pbd', 'uspto.peds'])
