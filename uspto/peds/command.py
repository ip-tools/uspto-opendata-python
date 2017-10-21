# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from docopt import docopt, DocoptExit
from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.util.command import run_command
from uspto.util.common import boot_logging
from uspto.version import __VERSION__
"""
Python command line client for accessing the USPTO Patent Examination Data System API (https://ped.uspto.gov/).
See also: https://ped.uspto.gov/peds/#/apiDocumentation
"""

logger = logging.getLogger(__name__)

APP_NAME = 'uspto-peds'

def run():
    """
    Examples:

        # Download published application by publication number in XML format
        {program} get "US20170293197A1" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        {program} get "US20170293197A1" --type=publication --format=json --pretty

        # Download published application by application number
        {program} get "15431686" --type=application --format=xml

        # Download granted patent by patent number
        {program} get "PP28532" --type=patent --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto-pair/PP28532.xml
        {program} save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto-pair

    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run_command.__doc__ + run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = docopt(commandline_schema, version=APP_NAME + ' ' + __VERSION__)

    # Start logging subsystem
    boot_logging(options)

    # An instance of the API client
    client = UsptoPatentExaminationDataSystemClient()

    # An instance of the background downloader
    try:
        from uspto.util.tasks import AsynchronousDownloader
        from uspto.peds.tasks import download_task
        downloader = AsynchronousDownloader(download_task)
    except Exception as ex:
        logger.warning('Could not bootstrap Celery. Asynchronous downloading disabled. Exception:\n%s', ex)
        downloader = None

    # Finally, run the command core implementation
    run_command(client, downloader, options)

