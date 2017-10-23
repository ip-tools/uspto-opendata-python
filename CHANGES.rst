##################################
USPTO Open Data API client CHANGES
##################################

development
===========
- When saving documents, optionally use the application identifier as filename
- Make "--type" argument optional by guessing document type from number
- Improve command line option juggling and documentation
- Properly retry failing tasks with Celery
- Honor "--use-application-id" also when printing results to STDOUT in bulk mode
- Fix Celery task reject behavior

2017-10-22 0.4.0
================
- Improve Celery bootstrapping
- Add “--poll” option to wait for results when running in “--background” mode
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
