# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import json
import logging
from docopt import docopt, DocoptExit
from uspto.util.common import get_document_path
import uspto.celery                     # Must import here to enable communication with Celery

logger = logging.getLogger(__name__)

def run_command(client, downloader, options):
    """
    Usage:
      {program} get  <document-number> --type=publication --format=xml [--pretty] [--background] [--wait] [--debug]
      {program} save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--background] [--wait] [--debug]
      {program} info
      {program} --version
      {program} (-h | --help)

    Options:
      --type=<type>             Document type, one of publication, application, patent
      --format=<target>         Data format, one of xml, json
      --pretty                  Pretty-print output data
      --directory=<directory>   Save downloaded to documents to designated target directory
      --overwrite               When saving documents, overwrite already existing documents
      --background              Run the download process in background
      --wait                    Wait for the background download to finish
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen

    Output modes:

        "{program} get ..."  will download the document and print the result to STDOUT.
        "{program} save ..." will save the document to the designated target directory, defaulting to the current path.

    """

    # Debugging
    #print('options: {}'.format(options))

    document_type   = options.get('--type')
    document_number = options.get('<document-number>')
    document_format = options.get('--format')

    # Build query
    query = {document_type: document_number, 'format': document_format}



    # Run document acquisition

    # Operation mode

    # 1. Synchronous mode
    if not options.get('--background'):

        # Pre-flight checks
        if options.get('save'):
            directory = options.get('--directory') or os.path.curdir
            filepath = get_document_path(directory, document_number, document_format, source=client.FILENAME_SOURCE)
            if os.path.exists(filepath):
                if not options.get('--overwrite'):
                    raise KeyError('File "{}" already exists. Use --overwrite.'.format(filepath))

            options['file'] = filepath

        # Run download synchronously
        result = client.download(**query)

        # Process result
        process_single_result(result, options)

    # 2. Asynchronous mode
    else:

        # Propagate "save" options to background task
        task_options = {
            'save': options.get('save'),
            'directory': options.get('--directory'),
            'overwrite': options.get('--overwrite'),
        }

        # Run background task asynchronously
        task = downloader.run(query)
        logger.info('Started background download task with id=%s', task.id)

        if options.get('--wait'):
            result = downloader.poll()
        else:
            logger.info('Results will not be printed to STDOUT, '
                        'add option "--wait" to wait for the background download to finish.')
            return

    if not result:
        logger.warning('Empty result')
        sys.exit(2)


def process_single_result(result, options):

    document_format = options.get('--format')

    # Choose output format from user selection
    payload = result[document_format]

    # Prettify result payload
    if options.get('--pretty'):
        if document_format == 'json':
            payload = json.dumps(json.loads(payload), indent=4)

    # Output mode

    # 1. Print to STDOUT
    if options.get('get'):
        print(payload)

    # 2. Save to filesystem
    elif options.get('save'):
        filepath = options['file']
        open(filepath, 'w').write(payload)
        logger.info('Saved document to {}'.format(filepath))

