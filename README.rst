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

Setup in development mode::

    # Activate virtualenv
    source .venv27/bin/activate

    # Install Python package
    python setup.py develop


Synopsis
========
::

    $ pairclient --help
        Usage:
          pairclient get <document-number> --type=publication --format=xml [--pretty] [--debug]
          pairclient save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--debug]
          pairclient info
          pairclient --version
          pairclient (-h | --help)

        Options:
          --type=<type>             Document type, one of publication, application, patent
          --format=<target>         Data format, one of xml, json
          --pretty                  Pretty-print output data
          --directory=<directory>   Save downloaded to documents to designated target directory
          --overwrite               When saving documents, overwrite already existing documents
          --debug                   Enable debug messages
          --version                 Show version information
          -h --help                 Show this screen

        Operation modes:

            "pairclient get ..." will download the document and print the result to STDOUT.
            "pairclient save ..." will save the document to the designated target directory, defaulting to the current path.

        Examples:

            # Download published application by publication number in XML format
            pairclient get "2017/0293197" --type=publication --format=xml

            # ... same in JSON format, with pretty-printing
            pairclient get "2017/0293197" --type=publication --format=json --pretty

            # Download published application by application number
            pairclient get "15431686" --type=application --format=xml

            # Download granted patent by patent number
            pairclient get "PP28532" --type=patent --format=xml

            # Download granted patent by patent number and save to /var/spool/uspto-pair/PP28532.xml
            pairclient save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto-pair


Asynchronous operation
======================
The software can also operate asynchronously by using Celery_
as a task queue for scheduling downloads in the background.
Please refer to the `taskqueue documentation`_.

.. _Celery: https://celery.readthedocs.io/
.. _taskqueue documentation: docs/taskqueue.rst


Project information
===================
``uspto-opendata-pair`` is released under the MIT license,
the code lives on `GitHub <https://github.com/ip-tools/uspto-opendata-pair>`_.

The software is tested on Python 2.7 and Python 3.6.

If you’d like to contribute you’re most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

