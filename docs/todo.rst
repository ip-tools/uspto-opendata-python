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
- [o] Unify documentation between PBD and PEDS
- [o] Implement uspto.util.format_number_for_source
- [o] Release on PyPI using https://flit.readthedocs.io/
- [o] Add tests

Asynchronous processing
=======================
- [o] Send emails on_success, on_failure
- [o] Addon for storing results to database instead of filesystem

Celery
======
task.result and task.info contains the metadata dictionary while the task is running and then
suddenly switches to containing the result or otherwise the exception object.
This is a bit counter-intuitive.
::

    print task._get_task_meta()
    print type(task.result)
    print type(task.info)


*****
USPTO
*****
- [o] No patentTermAdjustmentData for application "15431686" @ PBD
- [o] Implement API wrappers for IBD, BDSS, PTAB, Assignment and PatentsView.