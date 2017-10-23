####
Todo
####

*******
Program
*******

Core
====
- [x] Use "uscom:ApplicationNumberText" for identifying/storing documents, even across PBD/PEDS boundaries.
- [x] Provide "type=auto" parameter for auto-guessing type
- [x] Unify documentation between PBD and PEDS
- [x] Retrieve more advanced search results than numbers only
- [o] When using "--background" option, check for Celery availability (ping?)
- [o] Send PR to "clint" re. empty_char/filled_char
- [o] Send PR to "maya" re. "TypeError: 'encoding' is an invalid keyword argument for this function" on Python2
- [o] Implement uspto.util.format_number_for_source
- [o] Release on PyPI using https://flit.readthedocs.io/
- [o] Add tests


Asynchronous processing
=======================
- [o] Send emails on_success, on_failure
- [o] Addon for storing results to database instead of filesystem

Celery
======
1. task.result and task.info contains the metadata dictionary while the task is running and then
   suddenly switches to containing the result or otherwise the exception object.
   This is a bit counter-intuitive.
   ::

        print task._get_task_meta()
        print type(task.result)
        print type(task.info)

2. Task keeps being in PENDING state when rejected, see also:

- https://github.com/celery/celery/issues/2944
- https://github.com/celery/celery/issues/4222


*****
USPTO
*****
- [o] No patentTermAdjustmentData for application "15431686" @ PBD
- [o] Anomaly regarding number formats. PBD:2017/0293197 vs. PEDS:US2017293197A1
- [x] When requesting packages with more than one file inside zip, zip file seems broken.
  => Just when using ancient vanilla "unzip" from Mac OSX (unzip -v: UnZip 5.52 of 28 February 2005).
  ==> Better use "7z x <zipfile>" or "unzzip <zipfile>"
- [o] Implement API wrappers for IBD, BDSS, PTAB, Assignment and PatentsView
- [o] No transaction history data for ``applId:(15344906)`` @ PEDS.
