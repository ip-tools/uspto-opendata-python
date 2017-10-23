# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from docopt import docopt, DocoptExit
from uspto import __version__
from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.util.command import run_command
from uspto.util.common import boot_logging
"""
Python command line client for accessing the USPTO Patent Examination Data System API (https://ped.uspto.gov/peds/).
See also: https://ped.uspto.gov/peds/#/apiDocumentation
"""

logger = logging.getLogger(__name__)

APP_NAME = 'uspto-peds'

def run():
    """
    Examples:

        # Display published application by publication number in XML format
        {program} get "US20170293197A1" --type=publication --format=xml

        # ... same in JSON format, with pretty-printing
        {program} get "US20170293197A1" --type=publication --format=json --pretty

        # Display published application by application number
        {program} get "15431686" --type=application --format=xml

        # Display granted patent by patent number
        {program} get "PP28532" --type=patent --format=xml

        # Display granted patent by automatically guessing document type
        {program} get "PP28532" --format=xml

        # Download granted patent by patent number and save to /var/spool/uspto/PP28532.peds.xml
        {program} save "PP28532" --type=patent --format=xml --directory=/var/spool/uspto

    Bulk example:

        # Download all documents from numbers.txt and save them /var/spool/uspto/$number.peds.(xml|json)
        {program} bulk save --numberfile=numbers.txt --format=xml,json --pretty --directory=/var/spool/uspto --wait

    Search examples:

        # Search for documents matching "applicant=nasa" and display polished JSON response
        {program} search 'firstNamedApplicant:(nasa)' --filter='appFilingDate:[2000-01-01T00:00:00Z TO 2017-12-31T23:59:59Z]'

        # Search for documents matching "applicant=grohe" filed between 2010 and 2017
        {program} search 'firstNamedApplicant:(*grohe*)' --filter='appFilingDate:[2010-01-01T00:00:00Z TO 2017-12-31T23:59:59Z]'

        # Search for documents matching "applicant=nasa" and download zip archives containing bundles in XML and JSON formats
        {program} search 'firstNamedApplicant:(nasa)' --download --format=xml,json --directory=/tmp

    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run_command.__doc__ + run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Start logging subsystem
    boot_logging(options)

    # An instance of the API client
    client = UsptoPatentExaminationDataSystemClient()

    # An instance of the background downloader
    try:
        from uspto.peds.tasks import UsptoPatentExaminationDataSystemDownloader
        client.downloader = UsptoPatentExaminationDataSystemDownloader()
    except Exception as ex:
        logger.warning('Could not bootstrap Celery. Asynchronous downloading disabled. Exception:\n%s', ex)

    # Finally, run the command core implementation
    run_command(client, options)

