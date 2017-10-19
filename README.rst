###############################
USPTO PAIR Bulk Data API Client
###############################


************
Introduction
************
uspto-pdb is a Python client for accessing the USPTO PAIR Bulk Data API (https://pairbulkdata.uspto.gov/).


*****
Setup
*****
Prepare directory for Redis and Celery::

    mkdir -p var/lib

Create Python virtualenv::

    virtualenv --no-site-packages .venv27


***
Run
***

Run Redis server::

    echo 'dir ./var/lib' | redis-server -

Run Celery::

    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler
    celery worker --app uspto.pbd.tasks --beat --schedule-filename var/lib/celerybeat-schedule --loglevel=info

Run example::

    source .venv27/bin/activate
    python uspto/pbd/download.py
