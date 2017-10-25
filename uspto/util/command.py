# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import json
import logging
from uspto.util.common import get_document_path, read_list, normalize_options, read_numbersfile, get_archive_path
from uspto.util.numbers import guess_type_from_number, format_number_for_source

logger = logging.getLogger(__name__)

ASYNC_RESULT = -1

def run_command(client, options):
    """
    Usage:
      {program} get  <document-number> --format=xml [--type=publication] [--pretty] [--background] [--wait] [--debug]
      {program} save <document-number> --format=xml [--type=publication] [--pretty] [--directory=/var/spool/uspto] [--use-application-id] [--overwrite] [--background] [--wait] [--debug]
      {program} bulk get  --numberfile=numbers.txt --format=xml,json [--pretty] [--use-application-id] [--wait] [--debug]
      {program} bulk save --numberfile=numbers.txt --format=xml,json [--pretty] --directory=/var/spool/uspto [--use-application-id] [--overwrite] [--wait] [--debug]
      {program} search [<expression>] [--filter=filter] [--start=0] [--rows=20] [--download] [--format=xml,json] [--directory=/var/spool/uspto] [--debug]
      {program} info
      {program} --version
      {program} (-h | --help)

    Document acquisition options:
      <document-number>         Document number, e.g. 2017/0293197, US20170293197A1, PP28532, 15431686.
                                Format depends on data source.
      --type=<type>             Document type, one of "publication", "application", "patent" or "auto".
                                When using "auto", the program tries to to guess the document number type
                                (application, publication, patent) from the document number itself.
      --format=<target>         Data format, one of "xml" or "json".
                                In bulk mode, it can also be "--type=xml,json".

    Search options:
      <expression>              Search expression for generic querying.
                                Examples:

                                - firstNamedApplicant:(nasa)
                                - patentTitle:(network AND security) AND appStatus_txt:(patented)
                                - appCls:(701) AND appStatus_txt:(patented)

      --filter=<filter>         Filter expression.
                                Example:

                                - appFilingDate:[2000-01-01T00:00:00Z TO 2005-12-31T23:59:59Z]

      --start=<start>           Start record. Default: 0
      --rows=<rows>             Number of records returned. Default: 20 (which is also the limit).


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

        "{program: <10} get"             Download one document and print the result to STDOUT.

        "{program: <10} save"            Download one document and save it to the target directory,
                                     defaulting to the current working directory.


        "{program: <10} bulk get"        Submit task for downloading multiple documents to the background job machinery.
                                     After finishing, print the results to STDOUT when using the "--wait" option.

        "{program: <10} bulk save"       Submit task for downloading multiple documents to the background job machinery.
                                     While doing so, progressively save documents to the target directory.
                                     After finishing, print the full file names to STDOUT when using the "--wait" option.

    """

    # Debugging
    #print('options: {}'.format(options))

    if options.get('search'):
        expression = options.get('<expression>') or '*:*'
        filter = options.get('--filter')
        result = client.search(expression, filter=filter, start=options.get('--start'), rows=options.get('--rows'))

        if options.get('--download'):
            query_id = result['metadata']['queryId']
            document_format = read_list(options.get('--format'))
            result = client.download(query_id, format=document_format, progressbar=True)
            for format, payload_zip in result.items():

                directory = options.get('--directory') or os.path.curdir
                filename = expression
                if filter:
                    filename += '-' + filter
                filepath = get_archive_path(directory, filename, format=format, source=client.DATASOURCE_NAME)

                # FIXME: Honor --overwrite option
                logger.info('Saving archive file to {}'.format(os.path.abspath(filepath)))
                open(filepath, 'wb').write(payload_zip)

        else:
            print(json.dumps(result, indent=4))

        #pprint(result)

    else:

        # A. Single document acquisition
        if not options.get('bulk'):

            # 1. Run document acquisition
            result = acquire_single_document(client, options)

            # 2. Process result
            if result == ASYNC_RESULT:
                pass
            elif result:
                process_single_result(client, result, options)
            else:
                logger.error('No results.')
                sys.exit(1)

        # B. Bulk document acquisition
        else:
            acquire_multiple_documents(client, options)


def acquire_single_document(client, options):

    document_type   = options.get('--type')
    document_number = options.get('<document-number>')
    document_format = options.get('--format')

    # Build query
    query = {'type': document_type, 'number': document_number, 'format': document_format}

    # Operation mode

    # 1. Synchronous mode
    if not options.get('--background'):
        result = client.download_document(**query)

    # 2. Asynchronous mode
    else:
        task = client.downloader.run(query)
        logger.info('Started background download task with id=%s', task.id)

        if options.get('--wait'):
            result = client.downloader.poll()
        else:
            logger.info('Results will not be printed to STDOUT, '
                        'add option "--wait" to wait for the background download to finish.')
            return ASYNC_RESULT

    return result

def process_single_result(client, result, options):

    document_number = options.get('<document-number>')
    document_format = options.get('--format')

    # A. Choose output format from user selection
    payload = result[document_format]

    # B. Compute document identifiers
    document = client.document_factory(data=result)
    document_identifiers = document.get_identifiers()
    logger.info('Document identifiers: %s', document_identifiers)


    # C. Output

    # 1. Prettify result payload
    if options.get('--pretty'):
        if document_format == 'json':
            payload = json.dumps(json.loads(payload), indent=4)

    # 2. Print to STDOUT
    if options.get('get'):
        print(payload)

    # 3. Save to filesystem
    elif options.get('save'):

        # Compute file name
        if options.get('--use-application-id'):
            filename = document_identifiers['application']
        else:
            filename = document_number

        # Compute file path
        directory = options.get('--directory') or os.path.curdir
        filepath = get_document_path(directory, filename, document_format, source=client.DATASOURCE_NAME)

        # Pre-flight checks
        if os.path.exists(filepath):
            if not options.get('--overwrite'):
                raise KeyError('File "{}" already exists. Use --overwrite.'.format(filepath))

        # Save file
        logger.info('Saving document file to {}'.format(os.path.abspath(filepath)))
        open(filepath, 'w').write(payload)


def acquire_multiple_documents(client, options):

    # Evaluate multiple document formats
    document_format = read_list(options.get('--format'))

    # Propagate some options to background task
    task_options = normalize_options(options)

    # Read numbers from file and compute list of queries
    numbers = read_numbersfile(options.get('--numberfile'))
    logger.info('Requesting numbers: %s', numbers)
    queries = []
    for number in numbers:
        document_type = guess_type_from_number(number)
        document_number = format_number_for_source(number, document_type)
        query = {'type': document_type, 'number': document_number, 'format': document_format}
        queries.append(query)

    #pprint(queries)
    #return

    # Run acquisition
    task = client.downloader.run(queries, task_options)

    # Wait for acquisition being ready
    if options.get('--wait'):
        result = client.downloader.poll()

        # When in "save" mode, accumulate and print filenames only
        if options.get('save'):
            files = []
            for key, entry in result.items():
                files += entry['metadata']['files']
            result = files

        result = json.dumps(result, indent=4)
        print(result)
