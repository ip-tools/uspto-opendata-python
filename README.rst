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

Create Python virtualenv::

    virtualenv --no-site-packages .venv27

Setup in development mode:

    # Activate virtualenv
    source .venv27/bin/activate

    # Install Python package
    python setup.py develop


Run
===

Prepare::

    # Activate virtualenv
    source .venv27/bin/activate

Run some example acquisitions::

    # Download published application by publication number in XML format
    pairclient get "2017/0293197" --type=publication --format=xml

    # ... same in JSON format, with pretty-printing
    pairclient get "2017/0293197" --type=publication --format=json --pretty

    # Download published application by application number
    pairclient get "15431686" --type=application --format=xml

.. note::
    # Download granted patent by patent number
    pairclient get "PP28532" --type=patent --format=xml

    uspto-opendata-pair is prepared to use Celery_ as a task queue for scheduling
    downloads in parallel. Please refer to the `taskqueue documentation`_.


.. _taskqueue documentation: docs/taskqueue.rst


Project Information
===================
``uspto-opendata-pair`` is released under the MIT license,
the code lives on `GitHub <https://github.com/ip-tools/uspto-opendata-pair>`_.

It's tested on Python 2.7 and Python 3.6.

If you’d like to contribute you’re most welcome!

