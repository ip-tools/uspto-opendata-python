# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import json
import logging
import pathvalidate
from docopt import docopt, DocoptExit
from uspto.pair.api import UsptoPairClient
from uspto.pair.version import __VERSION__

APP_NAME = 'pairclient ' + __VERSION__

logger = logging.getLogger(__name__)

def run():
    """
    Usage:
      pairclient get <document-number> --type=publication --format=xml [--pretty] [--debug]
      pairclient save <document-number> --type=publication --format=xml [--pretty] [--directory=/var/spool/uspto-pair] [--overwrite] [--debug]
      pairclient info
      pairclient --version
      pairclient (-h | --help)

    Options:
      --type=<type>             Document type, one of publication, application, patent
      --format=<target>         Data format, one of xml, json
      --pretty                  Pretty-print output data
      --directory=<directory>   Save downloaded to documents to designated target directory
      --overwrite               When saving documents, overwrite already existing documents
      --debug                   Enable debug messages
      --version                 Show version information
      -h --help                 Show this screen

    Operation modes:

        "pairclient get ..." will download the document and print the result to STDOUT.
        "pairclient save ..." will save the document to the designated target directory, defaulting to the current path.

    Examples:

        # Download published application by publication number in XML format
        pairclient get "2017/0293197" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        pairclient get "2017/0293197" --type=publication --format=json --pretty

        # Download published application by application number
        pairclient get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        pairclient get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto-pair/PP28532.xml
        pairclient save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto-pair

    """
    options = docopt(run.__doc__, version=APP_NAME)
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
    client = UsptoPairClient()
    result = client.download(**query)
    payload = result[document_format]

    # Prettify result payload
    if options.get('--pretty'):
        if document_format == 'json':
            payload = json.dumps(json.loads(payload), indent=4)

    # Operation mode: Print to STDOUT or save to filesystem
    if options.get('get'):
        print(payload)

    elif options.get('save'):
        open(filepath, 'w').write(payload)
        logger.info('Saved document to {}'.format(filepath))


def boot_logging(options=None):
    log_level = logging.INFO
    if options and options.get('--debug'):
        log_level = logging.DEBUG
    setup_logging(level=log_level)

def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

