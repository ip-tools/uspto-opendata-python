###########################
Taskqueue-based downloading
###########################


About
=====
It is possible to use a task queue for scheduling downloads in the background.
This documentation gives a rough overview about how things work.


Introduction
============
Celery_ is used for taskqueue-based scheduling of downloads.
It is a distributed task queue system with focus on real-time processing while also supporting task scheduling.

To operate appropriately, Celery requires a broker_ and a database for storing task results.
The default configuration setting uses Redis_ for both purposes, however you can choose from
a large number of other options.
Please refer to the Celery documentation at `broker settings`_ and `task result settings`_
to read about the details.


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
    python uspto/pbd/download.py


Operation
=========
Some quick notes about ``celery`` command line invocations.
::

    celery report --app uspto
    celery status --app uspto

    celery inspect conf --app uspto
    celery inspect report --app uspto
    celery inspect registered --app uspto

    celery inspect stats --app uspto
    celery inspect scheduled --app uspto

    celery result cbcb5866-c33a-4bb9-b9f3-0b93b87e0673 --app uspto


.. _Celery: https://celery.readthedocs.io/
.. _Redis: https://redis.io/
.. _broker: https://celery.readthedocs.io/en/latest/getting-started/brokers/
.. _broker settings: http://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-settings
.. _task result settings: http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-result-backend-settings

