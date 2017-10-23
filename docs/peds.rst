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
    result = client.download(type='application', number='15431686')

    # Download published application by early publication number
    result = client.download(type='publication', number='US20170293197A1')

    # Download granted patent by patent number
    result = client.download(type='patent', number='PP28532')

Asynchronous mode::

    from uspto.util.tasks import AsynchronousDownloader
    from uspto.peds.tasks import download_task
    downloader = AsynchronousDownloader(download_task)

    # Start downloading single document
    downloader.run({'type': 'patent', 'number': 'PP28532'})

    # Start downloading multiple documents
    downloader.run([{'type': 'publication', 'number': 'US20170293197A1'}, {'type': 'patent', 'number': 'PP28532'}])

    # Wait until results arrived
    result = downloader.poll()


Command line
============
::

    $ uspto-peds --help

    Usage:
      uspto-peds get  <document-number> --format=xml [--type=publication] [--pretty] [--background] [--wait] [--debug]
      uspto-peds save <document-number> --format=xml [--type=publication] [--pretty] [--directory=/var/spool/uspto] [--use-application-id] [--overwrite] [--background] [--wait] [--debug]
      uspto-peds bulk get  --numberfile=numbers.txt --format=xml,json [--pretty] [--use-application-id] [--wait] [--debug]
      uspto-peds bulk save --numberfile=numbers.txt --format=xml,json [--pretty] --directory=/var/spool/uspto [--use-application-id] [--overwrite] [--wait] [--debug]
      uspto-peds info
      uspto-peds --version
      uspto-peds (-h | --help)

    Acquisition options:
      <document-number>         Document number, e.g. 2017/0293197, US20170293197A1, PP28532, 15431686.
                                Format depends on data source.
      --type=<type>             Document type, one of "publication", "application", "patent" or "auto".
                                When using "auto", the program tries to to guess the document number type
                                (application, publication, patent) from the document number itself.
      --format=<target>         Data format, one of "xml" or "json".
                                In bulk mode, it can also be "--type=xml,json".

    Output options:
      --pretty                  Pretty-print output data. This currently applies to "--format=json" only.

    Save options:
      --directory=<directory>   Save downloaded documents to designated target directory.
      --use-application-id      Use the application identifier as filename.
      --overwrite               Overwrite already existing documents.

    Background mode:
      --background              Run the download process in the background.
      --wait                    Wait for the background download job to finish.

    Bulk options:
      --numberfile=<numberfile> Read document numbers from file. Implicitly uses "--background" mode.
                                Guess document number type by implicitly using "--type=auto".
                                Download multiple formats by specifying "--format=xml,json".

    Miscellaneous options:
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen


    Operation modes:

        "uspto-peds get"             Download one document and print the result to STDOUT.

        "uspto-peds save"            Download one document and save it to the target directory,
                                     defaulting to the current working directory.


        "uspto-peds bulk get"        Submit task for downloading multiple documents to the background job machinery.
                                     After finishing, print the results to STDOUT when using the "--wait" option.

        "uspto-peds bulk save"       Submit task for downloading multiple documents to the background job machinery.
                                     While doing so, progressively save documents to the target directory.
                                     After finishing, print the full file names to STDOUT when using the "--wait" option.


    Examples:

        # Download published application by publication number in XML format
        uspto-peds get "US20170293197A1" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        uspto-peds get "US20170293197A1" --type=publication --format=json --pretty

        # Download published application by application number
        uspto-peds get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        uspto-peds get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto/PP28532.peds.xml
        uspto-peds save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto


    Bulk examples:

        # Download all documents from numbers.txt and save them to /var/spool/uspto/$number.peds.(xml|json)
        uspto-peds bulk save --numberfile=numbers.txt --format=xml,json --pretty --directory=/var/spool/uspto --wait


******
Issues
******
- No transaction history data for ``applId:(15344906)``.

