# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
from celery.loaders.base import autodiscover_tasks

autodiscover_tasks(['uspto.pbd', 'uspto.peds'])
