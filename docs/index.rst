.. uspto-opendata-python documentation master file, created by
   sphinx-quickstart on Tue Oct 31 04:25:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://img.shields.io/badge/Python-2.7,%203.6-green.svg
    :target: https://pypi.org/project/uspto-opendata-python/

.. image:: https://img.shields.io/pypi/v/uspto-opendata-python.svg
    :target: https://pypi.org/project/uspto-opendata-python/

.. image:: https://img.shields.io/github/tag/ip-tools/uspto-opendata-python.svg
    :target: https://github.com/ip-tools/uspto-opendata-python

|

USPTO Open Data API client
==========================
``uspto-opendata-python`` is a client library for accessing the USPTO Open Data APIs,  It is written in Python.

Currently, it implements API wrappers for the

- `PAIR Bulk Data (PBD)`_ system
- `Patent Examination Data System (PEDS)`_

Both systems contain bibliographic, published document and patent term extension data in Public PAIR from 1981 to present.
There is also some data dating back to 1935.

The PEDS system provides additional information concerning the transaction activity that has occurred for each patent.
The transaction history includes the transaction date, transaction code and transaction description for each transaction activity.

.. _PAIR Bulk Data (PBD): https://pairbulkdata.uspto.gov/
.. _Patent Examination Data System (PEDS): https://ped.uspto.gov/peds/


.. toctree::
    :maxdepth: 1
    :caption: About

    README <README>

.. toctree::
    :maxdepth: 1
    :caption: Documentation

    pbd
    peds
    taskqueue
    virtualenv

.. toctree::
    :maxdepth: 1
    :caption: Development

    Releasing <releasing>
    Changelog <CHANGES>
    Todo <todo>

.. toctree::
    :maxdepth: 1
    :caption: See also

    other-software

