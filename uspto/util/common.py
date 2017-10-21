# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import os
import sys
import logging
import pathvalidate

def to_list(obj):
    """Convert an object to a list if it is not already one"""
    # stolen from cornice.util
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj

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

def get_document_path(directory, number, format, source=None):
    if source:
        source = source.lower() + '.'
    filename = pathvalidate.sanitize_filename('{name}.{source}{suffix}'.format(name=number.upper(), source=source, suffix=format.lower()))
    filepath = os.path.join(directory, filename)
    return filepath
