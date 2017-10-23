# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import logging
import slugify
import pathvalidate
from datetime import datetime

def to_list(obj):
    """Convert an object to a list if it is not already one"""
    # stolen from cornice.util
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj

def read_list(data, separator=u','):
    if data is None:
        return []
    result = list(map(lambda x: x.strip(), data.split(separator)))
    if len(result) == 1 and not result[0]:
        result = []
    return result

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

def normalize_options(options):
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    return normalized

def get_document_path(directory, name, format, source=None):
    if source:
        source = source.lower() + '.'
    filename = pathvalidate.sanitize_filename('{name}.{source}{suffix}'.format(
        name=name.upper(), source=source.lower(), suffix=format.lower()))
    filepath = os.path.join(directory, filename)
    return filepath

def get_archive_path(directory, name, format, source=None):

    if source:
        source = '-' + source.lower()

    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S')

    name = pathvalidate.sanitize_filename(name)
    name = slugify.slugify_filename(name)

    filename = 'uspto{source}_{timestamp}_{name}.{format}.zip'.format(
        name=name, timestamp=timestamp, source=source.lower(), format=format.lower())

    filepath = os.path.join(directory, filename)
    return filepath

def read_numbersfile(filename):
    numbers = open(filename, 'r').readlines()
    numbers = map(str.strip, numbers)
    numbers = filter(lambda number: not number.startswith('#'), numbers)
    return numbers

class SmartException(Exception):

    def __init__(self, message, **kwargs):

        # Call the base class constructor with the parameters it needs
        super(SmartException, self).__init__(message)

        # Stuff more things into the exception object
        self.more_info = kwargs
