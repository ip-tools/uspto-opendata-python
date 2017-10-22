###############################
USPTO PAIR Bulk Data API client
###############################

The USPTO PAIR Bulk Data (PBD) system contains bibliographic, published document and patent term extension data
in Public PAIR from 1981 to present. There is also some data dating back to 1935.


********
Synopsis
********

API
===
The API has two different modes, synchronous and asynchronous.

Synchronous mode::

    from uspto.pbd.api import UsptoPairBulkDataClient
    client = UsptoPairBulkDataClient()

    # Download application by application number
    result = client.download(type='application', number='15431686')

    # Download published application by early publication number
    result = client.download(type='publication', number='2017/0293197')

    # Download granted patent by patent number
    result = client.download(type='patent', number='PP28532')

Asynchronous mode::

    from uspto.util.tasks import AsynchronousDownloader
    from uspto.peds.tasks import download_task
    downloader = AsynchronousDownloader(download_task)

    # Start downloading single document
    downloader.run({'type': 'patent', 'number': 'PP28532'})

    # Start downloading multiple documents
    downloader.run([{'type': 'publication', 'number': '2017/0293197'}, {'type': 'patent', 'number': 'PP28532'}])

    # Wait until results arrived
    result = downloader.poll()


Command line
============
::

    $ uspto-pbd --help

    Usage:
      uspto-pbd get  <document-number> --format=xml [--type=publication] [--pretty] [--background] [--wait] [--debug]
      uspto-pbd save <document-number> --format=xml [--type=publication] [--pretty] [--directory=/var/spool/uspto] [--use-application-id] [--overwrite] [--background] [--wait] [--debug]
      uspto-pbd bulk get  --numberfile=numbers.txt --format=xml,json [--pretty] [--wait] [--debug]
      uspto-pbd bulk save --numberfile=numbers.txt --format=xml,json [--pretty] --directory=/var/spool/uspto [--use-application-id] [--overwrite] [--wait] [--debug]
      uspto-pbd info
      uspto-pbd --version
      uspto-pbd (-h | --help)

    General options:
      <document-number>         Document number, e.g. 2017/0293197, US20170293197A1, PP28532, 15431686.
                                Format depends on data source.
      --type=<type>             Document type, one of "publication", "application", "patent" or "auto".

    Output options:
      --format=<target>         Data format, one of "xml" or "json".
      --pretty                  Pretty-print output data. Currently applies to "--format=json" only.

    Save options:
      --directory=<directory>   Save downloaded to documents to designated target directory.
      --use-application-id      When saving documents, use the application identifier as filename.
      --overwrite               When saving documents, overwrite already existing documents.

    Operation mode:
      --background              Run the download process in the background.
      --wait                    Wait for the background download to finish.

    Bulk options:
      --numberfile=<numberfile> Read document numbers from file.
                                Apply heuristics to determine document number type (application, publication, patent).
                                Download multiple formats by specifying "--format=xml,json".
                                Implicitly uses background mode.

    Miscellaneous options:
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen

    Output modes:

        "uspto-pbd get ..."        will download the document and print the result to STDOUT.
        "uspto-pbd save ..."       will save the document to the target directory, defaulting to the current path.
        "uspto-pbd bulk get ..."   will download multiple documents and print the result to STDOUT.
        "uspto-pbd bulk save ..."  will download multiple documents and save them to the target directory.


    Examples:

        # Download published application by publication number in XML format
        uspto-pbd get "2017/0293197" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        uspto-pbd get "2017/0293197" --type=publication --format=json --pretty

        # Download published application by application number
        uspto-pbd get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        uspto-pbd get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto/PP28532.pbd.xml
        uspto-pbd save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto


    Bulk examples:

        # Download all documents from numbers.txt and save them to /var/spool/uspto/$number.pbd.(xml|json)
        uspto-pbd bulk save --numberfile=numbers.txt --format=xml,json --pretty --directory=/var/spool/uspto --wait

