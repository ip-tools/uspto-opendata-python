###############
Getting started
###############


Install
=======

Create Python virtualenv::

    # Either use Python 2.7 ...
    virtualenv --no-site-packages .venv27

    # ... or Python 3.6
    virtualenv --no-site-packages --python python3.6 .venv36

Setup in development mode::

    # Activate virtualenv
    source .venv27/bin/activate

    # Install Python package
    python setup.py develop


Synopsis
========
::

    $ uspto-pbd --help

    Usage:
      uspto-pbd get  <document-number> --type=publication --format=xml [--pretty] [--debug]
      uspto-pbd save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--debug]
      uspto-pbd info
      uspto-pbd --version
      uspto-pbd (-h | --help)

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

        "uspto-pbd get ..." will download the document and print the result to STDOUT.
        "uspto-pbd save ..." will save the document to the designated target directory, defaulting to the current path.

    Examples:

        # Download published application by publication number in XML format
        uspto-pbd get "2017/0293197" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        uspto-pbd get "2017/0293197" --type=publication --format=json --pretty

        # Download published application by application number
        uspto-pbd get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        uspto-pbd get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto-pair/PP28532.xml
        uspto-pbd save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto-pair


Asynchronous operation
======================
The software can also operate asynchronously by using Celery_
as a task queue for scheduling downloads in the background.
Please refer to the `taskqueue documentation`_.

.. _Celery: https://celery.readthedocs.io/
.. _taskqueue documentation: docs/taskqueue.rst

