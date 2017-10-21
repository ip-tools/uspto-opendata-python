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


Usage
=====
Please refer to the respective documentation about which API you want to access:

- PAIR Bulk Data (PBD) system: `PBD usage`_
- Patent Examination Data System (PEDS): `PEDS usage`_

.. _PBD usage: pbd.rst
.. _PEDS usage: peds.rst


Asynchronous operation
======================
The software can also operate asynchronously by using Celery_
as a task queue for scheduling downloads in the background.
Please refer to the `taskqueue documentation`_.

.. _Celery: https://celery.readthedocs.io/
.. _taskqueue documentation: taskqueue.rst

