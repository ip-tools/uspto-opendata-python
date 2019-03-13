##################################
USPTO Open Data API client CHANGES
##################################

development
===========


2019-03-14 0.8.3
================
- Fix ``uspto-peds search`` command. Thanks, Rahul!

2018-10-24 0.8.2
================
- Fix regression re. proper charset decoding

2018-10-24 0.8.1
================
- Improve tooling (Makefile)
- Fix regression when decoding the document identifier
- Disable the PBD subsystem as it has been decommissioned by the USPTO. Thanks, Mohamed and Andy!

2018-10-03 0.8.0
================
- Upgrade to lxml 4.2.5 to satisfy libxml2 compilation on recent Homebrew
- Improve error reporting when upstream API is defunct
  with e.g. ``Service Unavailable: Back-end server is at capacity``. Thanks, Mohamed!

2017-11-20 0.7.4
================
- Replace non ASCII-compatible quotation marks in CHANGES to address #1. Thanks again, Rahul.

2017-11-17 0.7.3
================
- Replace non ASCII-compatible quotation marks in README to address #1. Thanks, Rahul.

2017-10-31 0.7.1
================
- Update documentation

2017-10-31 0.7.0
================
- Add documentation infrastructure (Sphinx) and tooling

2017-10-25 0.6.0
================
- Add commandline options ``--start`` and ``--rows`` for paging through search results
- Update documentation

2017-10-24 0.5.6
================
- Fix search command
- Update documentation
- Improve .bumpversion.cfg

2017-10-24 0.5.5
================
- Fix bumpversion woes

2017-10-24 0.5.4
================
- Fix "clint" dependency
- Update Makefile re. release process

2017-10-24 0.5.3
================
- Release on PyPI using "twine"

2017-10-24 0.5.2
================
- Release on PyPI using "flit"

2017-10-24 0.5.1
================
- Update documentation

2017-10-24 0.5.0
================
- When saving documents, optionally use the application identifier as filename
- Make "--type" argument optional by guessing document type from number
- Improve command line option juggling and documentation
- Properly retry failing tasks with Celery
- Honor "--use-application-id" also when printing results to STDOUT in bulk mode
- Fix Celery task reject behavior
- Don't use number from "--numberfile" when prefixed with "#"
- Improve exception handling and error response for bulk acquisition mode
- Improve Celery bootstrapping again
- Add API search mode, refactoring and cleanups, update API and command line documentation

2017-10-22 0.4.0
================
- Improve Celery bootstrapping
- Add "--poll" option to wait for results when running in "--background" mode
- Improve command line argument handling
- Rename command line option "--poll" to "--wait"
- Introduce bulk mode based on task queue: ``uspto-{pbd,peds} bulk {get,save} ...``

2017-10-21 0.3.0
================
- Implement access to the USPTO Patent Examination Data System (PEDS), including command line program ``uspto-peds``
- Generalize Celery-based background downloads between PBD and PEDS

2017-10-20 0.2.1
================
- Minor fixes and Python3 compatibility

2017-10-20 0.2.0
================
- Python3 compatibility
- Add command line program ``uspto-pbd`` for printing and saving documents from the USPTO PAIR Bulk Data API

2017-10-20 0.1.0
================
- Implement the basic query and download parts of the USPTO PAIR Bulk Data API
- Implement Celery-based downloader infrastructure

2017-10-19 0.0.0
================
- Basic framework for asynchronous and parallel API interaction based on Celery
