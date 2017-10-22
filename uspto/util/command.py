# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import json
import logging
from docopt import docopt, DocoptExit
from uspto.util.common import get_document_path, read_list
from uspto.util.numbers import guess_type_from_number, format_number_for_source
import uspto.celery                     # Must import here to enable communication with Celery

logger = logging.getLogger(__name__)

def run_command(client, options):
    """
    Usage:
      {program} get  <document-number> --type=publication --format=xml [--pretty] [--background] [--wait] [--debug]
      {program} save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto] [--use-application-id] [--overwrite] [--background] [--wait] [--debug]
      {program} bulk get  --numberfile=numbers.txt --format=xml,json [--pretty] [--wait] [--debug]
      {program} bulk save --numberfile=numbers.txt --format=xml,json [--pretty] --directory=/var/spool/uspto [--use-application-id] [--overwrite] [--wait] [--debug]
      {program} info
      {program} --version
      {program} (-h | --help)

    General options:
      --type=<type>             Document type, one of "publication", "application" or "patent".
      --format=<target>         Data format, one of "xml" or "json".
      --pretty                  Pretty-print output data. Currently applies to "--format=json" only.
      --background              Run the download process in the background.
      --wait                    Wait for the background download to finish.

    Save options:
      --directory=<directory>   Save downloaded to documents to designated target directory.
      --use-application-id      When saving documents, use the application identifier as filename.
      --overwrite               When saving documents, overwrite already existing documents.

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

        "{program} get ..."        will download the document and print the result to STDOUT.
        "{program} save ..."       will save the document to the target directory, defaulting to the current path.
        "{program} bulk get ..."   will download multiple documents and print the result to STDOUT.
        "{program} bulk save ..."  will download multiple documents and save them to the target directory.

    """

    # Debugging
    #print('options: {}'.format(options))

    document_format = options.get('--format')

    # Single document acquisition
    if not options.get('bulk'):

        # A. Run document acquisition
        result = acquire_single_document(client, options)

        # B. Process result
        if result:
            process_single_result(client, result, options)

    # Bulk document acquisition
    else:

        document_format = read_list(document_format)

        # Propagate some options to background task
        task_options = {
            'save': options.get('save'),
            'pretty': options.get('--pretty'),
            'directory': options.get('--directory'),
            'overwrite': options.get('--overwrite'),
            'use_application_id': options.get('--use-application-id'),
        }

        query = [
            {'type': 'publication', 'number': 'US20170293197A1', 'format': document_format},
            {'type': 'patent', 'number': 'PP28532', 'format': document_format},
        ]
        numbers = map(str.strip, open(options.get('--numberfile'), 'r').readlines())
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


def acquire_single_document(client, options):

    document_type   = options.get('--type')
    document_number = options.get('<document-number>')
    document_format = options.get('--format')

    # Build query
    query = {'type': document_type, 'number': document_number, 'format': document_format}

    # Operation mode

    # 1. Synchronous mode
    if not options.get('--background'):
        result = client.download(**query)

    # 2. Asynchronous mode
    else:
        task = client.downloader.run(query)
        logger.info('Started background download task with id=%s', task.id)

        if options.get('--wait'):
            result = client.downloader.poll()
        else:
            logger.info('Results will not be printed to STDOUT, '
                        'add option "--wait" to wait for the background download to finish.')
            return

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
        open(filepath, 'w').write(payload)
        logger.info('Saved document to {}'.format(filepath))

