###############################
USPTO PAIR Bulk Data API Client
###############################


Introduction
============
uspto-opendata-pair is a Python client for accessing the USPTO PAIR Bulk Data API (PBD) at https://pairbulkdata.uspto.gov/.

The Patent Application Information Retrieval (PAIR) Bulk Data API lets customers retrieve and download
multiple records of USPTO patent application or patent filing status at no cost.

The API was conceived as part of the `USPTO Open Data initiative`_, please also visit the `Open Data Portal`_
and its `API catalog`_ for other new API offers by the US Patent and Trademark Office.

.. _USPTO Open Data initiative: https://www.uspto.gov/learning-and-resources/open-data-and-mobility
.. _Open Data Portal: https://developer.uspto.gov/
.. _API catalog: https://developer.uspto.gov/api-catalog


Setup
=====
Prepare directory for Redis and Celery::

    mkdir -p var/lib

Create Python virtualenv::

    virtualenv --no-site-packages .venv27


Run
===

Run Redis server::

    echo 'dir ./var/lib' | redis-server -

Run Celery in a simple way embedding the beat scheduler inside the worker daemon::

    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler
    celery worker --app uspto.pair.tasks --beat --schedule-filename var/lib/celerybeat-schedule --loglevel=info

Run examples::

    # Activate virtualenv
    source .venv27/bin/activate

    # Directly access the API
    python uspto/pair/api.py

    # Run download jobs over the Celery job queue
    python uspto/pair/download.py


Contribute
==========
If you’d like to contribute you’re most welcome!


License
=======
``uspto-opendata-pair`` is released under the MIT license,
the code lives on `GitHub <https://github.com/ip-tools/uspto-opendata-pair>`_.
