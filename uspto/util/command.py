# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import json
import logging
import pathvalidate
from docopt import docopt, DocoptExit
from uspto.util.common import boot_logging
from uspto.util.tasks import AsynchronousDownloader

logger = logging.getLogger(__name__)

def run_command(client, downloader, options):
    """
    Usage:
      {program} get  <document-number> --type=publication --format=xml [--pretty] [--background] [--debug]
      {program} save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--background] [--debug]
      {program} info
      {program} --version
      {program} (-h | --help)

    Options:
      --type=<type>             Document type, one of publication, application, patent
      --format=<target>         Data format, one of xml, json
      --pretty                  Pretty-print output data
      --directory=<directory>   Save downloaded to documents to designated target directory
      --overwrite               When saving documents, overwrite already existing documents
      --background              Run the download in background
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen

    Operation modes:

        "{program} get ..." will download the document and print the result to STDOUT.
        "{program} save ..." will save the document to the designated target directory, defaulting to the current path.

    """

    # Debugging
    #print('options: {}'.format(options))

    boot_logging(options)

    document_type   = options.get('--type')
    document_number = options.get('<document-number>')
    document_format = options.get('--format')

    # Build query
    query = {document_type: document_number, 'format': document_format}

    # Pre-flight checks
    if options.get('save'):
        directory = options.get('--directory') or os.path.curdir
        filename = pathvalidate.sanitize_filename('{name}.{suffix}'.format(name=document_number.upper(), suffix=document_format.lower()))
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            if not options.get('--overwrite'):
                raise KeyError('File "{}" already exists. Use --overwrite.'.format(filepath))


    # Run document acquisition

    if not options.get('--background'):
        result = client.download(**query)

    else:
        downloader.run(query)
        if options.get('get'):
            result = downloader.poll()

    if not result:
        logger.warning('Empty result')
        sys.exit(2)

    payload = result[document_format]

    # Prettify result payload
    if options.get('--pretty'):
        if document_format == 'json':
            payload = json.dumps(json.loads(payload), indent=4)

    # Operation modes

    # 1. Print to STDOUT
    if options.get('get'):
        print(payload)

    # 2. Save to filesystem
    elif options.get('save'):
        open(filepath, 'w').write(payload)
        logger.info('Saved document to {}'.format(filepath))

