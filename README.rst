.. image:: https://img.shields.io/badge/Python-2.7,%203.6-green.svg
    :target: https://pypi.org/project/uspto-opendata-python/

.. image:: https://img.shields.io/pypi/v/uspto-opendata-python.svg
    :target: https://pypi.org/project/uspto-opendata-python/

.. image:: https://img.shields.io/github/tag/ip-tools/uspto-opendata-python.svg
    :target: https://github.com/ip-tools/uspto-opendata-python

|

##########################
USPTO Open Data API client
##########################


*****
About
*****
``uspto-opendata-python`` is a client library for accessing the USPTO Open Data APIs.  It is written in Python.

Currently, it implements API wrappers for the

- `Patent Examination Data System (PEDS)`_
- `PAIR Bulk Data (PBD)`_ system (decommissioned, so defunct)

Both systems contain bibliographic, published document and patent term extension data in Public PAIR from 1981 to present.
There is also some data dating back to 1935.

The PEDS system provides additional information concerning the transaction activity that has occurred for each patent.
The transaction history includes the transaction date, transaction code and transaction description for each transaction activity.

.. _PAIR Bulk Data (PBD): https://pairbulkdata.uspto.gov/
.. _Patent Examination Data System (PEDS): https://ped.uspto.gov/peds/

.. attention::

    The USPTO PBD service (PAIR Bulk Data system) has been decommissioned,
    please use the USPTO PEDS service (Patent Examination Data System).


***************
Getting started
***************

Install
=======
If you know your way around Python, installing this software is really easy::

    pip install uspto-opendata-python

Please refer to the `virtualenv`_ page about further guidelines how to install and use this software.

.. _virtualenv: https://github.com/ip-tools/uspto-opendata-python/blob/master/docs/virtualenv.rst


Usage
=====
Please refer to the respective documentation about which API you want to access:

- PAIR Bulk Data (PBD) system: `PBD usage`_
- Patent Examination Data System (PEDS): `PEDS usage`_

.. _PBD usage: https://docs.ip-tools.org/uspto-opendata-python/pbd.html
.. _PEDS usage: https://docs.ip-tools.org/uspto-opendata-python/peds.html


*******************
Project information
*******************
``uspto-opendata-python`` is released under the MIT license.
The code lives on `GitHub <https://github.com/ip-tools/uspto-opendata-python>`_ and
the Python package is published to `PyPI <https://pypi.org/project/uspto-opendata-python/>`_.
You might also want to have a look at the `documentation <https://docs.ip-tools.org/uspto-opendata-python/>`_.

The software has been tested on Python 2.7 and Python 3.6.

If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Disclaimer
==========
The project and its authors are not affiliated with the USPTO in any way.
It is a sole project from the community for making data more accessible in the spirit of open data.


*******
Credits
*******
Thanks to the USPTO data team and all people working behind the scenes
for providing these excellent services to the community. You know who you are.


**********
Background
**********
The Patent Application Information Retrieval (PAIR) APIs let customers retrieve and download
multiple records of USPTO patent application or patent filing status at no cost.

They are part of the US Patent and Trademark Office's (USPTO) commitment to fostering a culture of open government as
described by the 2013 Executive Order 13642 to make open and machine-readable data the new default for government information
(`HTML <https://obamawhitehouse.archives.gov/the-press-office/2013/05/09/executive-order-making-open-and-machine-readable-new-default-government->`_,
`PDF <https://www.gpo.gov/fdsys/pkg/FR-2013-05-14/pdf/2013-11533.pdf>`_).

The API was conceived as part of the `USPTO Open Data Initiative`_, please also visit the `USPTO Open Data Portal`_
and its `API catalog`_ for other new APIs provided by the US Patent and Trademark Office.

The US Patent and Trademark office encourages innovators and entrepreneurs worldwide to publish their inventions
for worldwide use and adoption. They have opened their APIs to third party developers inside and outside of
government so that they can directly benefit from this data, by making and using their own apps.

For terms of use regarding their APIs and data, please visit the respective pages at `USPTO general terms`_ and
`PatentsView API terms`_. In general, the published material is in the public domain and may be freely distributed and
copied, but it is requested that in any subsequent use the United States Patent and Trademark Office (USPTO) be given
appropriate acknowledgement (e.g., "Source: United States Patent and Trademark Office, www.uspto.gov").

.. _USPTO Open Data Initiative: https://www.uspto.gov/learning-and-resources/open-data-and-mobility
.. _USPTO Open Data Portal: https://developer.uspto.gov/
.. _API catalog: https://developer.uspto.gov/api-catalog

.. _Bulk Data Products: https://www.uspto.gov/learning-and-resources/bulk-data-products
.. _Bulk search and download: https://developer.uspto.gov/api-catalog/bulk-search-and-download
.. _PAIR Bulk Data: https://developer.uspto.gov/api-catalog/pair-bulk-data

.. _USPTO general terms: https://www.uspto.gov/terms-use-uspto-websites#copyright
.. _PatentsView API terms: http://www.patentsview.org/api/faqs.html#what-api

