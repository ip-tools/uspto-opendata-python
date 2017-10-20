#############################################
uspto-opendata-pair taskqueue-based downloads
#############################################

uspto-opendata-pair is prepared to use Celery_ as a task queue for scheduling
downloads in parallel. This documentation gives a rough overview about how
things work.

How to
======
Run Redis server::

    make redis-start

Run Celery in a simple way embedding the beat scheduler inside the worker daemon::

    make celery-start

Run examples::

    # Activate virtualenv
    source .venv27/bin/activate

    # Run download jobs over the Celery task queue
    python uspto/pair/download.py


.. _Celery: https://celery.readthedocs.io/
