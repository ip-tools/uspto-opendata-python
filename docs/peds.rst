###############################################
USPTO Patent Examination Data System API client
###############################################

The USPTO Patent Examination Data System (PEDS) contains bibliographic, published document and patent term extension data
in Public PAIR from 1981 to present. There is also some data dating back to 1935.

The PEDS system provides additional information concerning the transaction activity that has occurred for each patent.
The transaction history includes the transaction date, transaction code and transaction description for each transaction activity.


********
Synopsis
********

API
===
The API has two different modes, synchronous and asynchronous.

Synchronous mode::

    from uspto.peds.api import UsptoPatentExaminationDataSystemClient
    client = UsptoPatentExaminationDataSystemClient()

    # Download application by application number
    result = client.download(application='15431686')

    # Download published application by early publication number
    result = client.download(publication='US20170293197A1')

    # Download granted patent by patent number
    result = client.download(patent='PP28532')

Asynchronous mode::

    from uspto.util.tasks import AsynchronousDownloader
    from uspto.peds.tasks import download_task
    downloader = AsynchronousDownloader(download_task)

    # Start downloading single document
    downloader.run({'patent': 'PP28532'})

    # Start downloading multiple documents
    downloader.run([{'publication': 'US20170293197A1'}, {'patent': 'PP28532'}])

    # Wait until results arrived
    result = downloader.poll()


Command line
============
::

    $ uspto-peds --help

    Usage:
      uspto-peds get  <document-number> --type=publication --format=xml [--pretty] [--background] [--wait] [--debug]
      uspto-peds save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--background] [--wait] [--debug]
      uspto-peds info
      uspto-peds --version
      uspto-peds (-h | --help)

    Options:
      --type=<type>             Document type, one of publication, application, patent
      --format=<target>         Data format, one of xml, json
      --pretty                  Pretty-print output data
      --directory=<directory>   Save downloaded to documents to designated target directory
      --overwrite               When saving documents, overwrite already existing documents
      --background              Run the download process in background
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen

    Output modes:

        "uspto-peds get ..."  will download the document and print the result to STDOUT.
        "uspto-peds save ..." will save the document to the designated target directory, defaulting to the current path.


    Examples:

        # Download published application by publication number in XML format
        uspto-peds get "US20170293197A1" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        uspto-peds get "US20170293197A1" --type=publication --format=json --pretty

        # Download published application by application number
        uspto-peds get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        uspto-peds get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto-pair/PP28532.xml
        uspto-peds save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto-pair


******
Issues
******
- No transaction history data for ``applId:(15344906)``.

