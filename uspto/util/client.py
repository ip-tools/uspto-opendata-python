# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
import json
import logging
import zipfile
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from uspto.util.common import to_list

logger = logging.getLogger(__name__)

class UsptoGenericBulkDataClient:

    def __init__(self):
        self.session = requests.Session()
        self.downloader = None

    def query(self, searchText, df='patentTitle'):
        logger.info('Querying for %s', searchText)
        response = self.session.post(self.QUERY_URL, json={
            'searchText': searchText,
            'df': df,
            'facet': True,
            'fl': '*',
            'fq': [],
            'mm': '100%',
            'qf': 'appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber '
                  'appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor '
                  'firstNamedApplicant appExamName appExamPrefrdName appAttrDockNumber appPCTNumber appIntlPubNumber '
                  'wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList',
            'sort': 'applId asc',
            'start': '0',
        })

        if response.status_code != 200:
            logger.error('Error while querying for %s\n%s', searchText, response.text)
            if response.headers['Content-Type'].startswith('text/html'):
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                message = title.string.strip()
                hr = soup.body.find('hr')
                reason = hr.next_sibling.string.strip()
                if reason:
                    message += '. ' + reason
                message += ' (status={})'.format(response.status_code)
                raise ValueError(message)

        return response.json()

    def query_application(self, applicationId):
        searchText = 'applId:({})'.format(applicationId)
        return self.query(searchText)

    def query_publication(self, appEarlyPubNumber):
        searchText = 'appEarlyPubNumber:({})'.format(appEarlyPubNumber)
        return self.query(searchText)

    def query_patent(self, patentNumber):
        searchText = 'patentNumber:({})'.format(patentNumber)
        return self.query(searchText)

    def request_package(self, query_id, format):

        # The platform sometimes responds with "403 Forbidden" if requesting the package too fast after querying.
        # Account for that.
        time.sleep(1)

        logger.info('Requesting package for queryId=%s with format=%s', query_id, format)
        response = self.session.put(self.PACKAGE_REQUEST_URL.format(query_id=query_id, format=format))

        if response.status_code != 200:
            logger.error('Error while requesting package for queryId=%s\n%s', query_id, response.text)
            if response.headers['Content-Type'].startswith('text/html'):
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').string.strip()
                reason = soup.body.find('h1').string.strip('- ')
                reason_more = ', '.join(map(lambda item: ': '.join(item.stripped_strings), soup.body.find_all('p')))

                message = title
                if reason:
                    message += '. ' + reason
                if reason_more:
                    message += '. ' + reason_more
                message += ' (status={})'.format(response.status_code)

                raise ValueError(message)

        return response.json()

    def package_status(self, query_id, format):
        logger.debug('Checking package status for queryId=%s with format=%s', query_id, format)
        response = self.session.get(self.PACKAGE_STATUS_URL.format(query_id=query_id, format=format))
        assert response.status_code == 200
        return response.json()

    def wait_for_package(self, query_id, format):

        # The platform sometimes responds with "403 Forbidden" if checking the package status too fast after requesting it.
        # Account for that.
        time.sleep(1)

        # TODO: Break loop after x seconds, sometimes jobs get stuck in the "INITIATED" state.
        # TODO: Properly account for possible "FAIL" states.
        while True:
            response = self.package_status(query_id, format)
            status = response['jobStatus']
            logger.info('Package status for queryId=%s is %s', query_id, status)

            if response['jobStatus'] == 'COMPLETED':
                if self.check_package_url(query_id, format):
                    break

            time.sleep(1)

    def check_package_url(self, query_id, format):
        # Sometimes the platform responds with "403 Forbidden". Give it some time to breath.
        url = self.PACKAGE_DOWNLOAD_URL.format(query_id=query_id, format=format)
        logger.info('Checking package url for queryId=%s with format=%s. url=%s', query_id, format, url)
        response = self.session.get(url, allow_redirects=False)
        if response.status_code != 403:
            return True

    def download_package(self, query_id, format):
        url = self.PACKAGE_DOWNLOAD_URL.format(query_id=query_id, format=format)
        logger.info('Downloading package for queryId=%s with format=%s. url=%s', query_id, format, url)
        response = self.session.get(url)
        assert response.status_code in [200, 302], 'No download package. status={}'.format(response.status_code)
        assert response.headers['Content-Type'] == 'application/zip'
        return response.content

    def unzip_package(self, payload_zip):

        # Decode zip file
        zip = zipfile.ZipFile(BytesIO(payload_zip), 'r')
        filenames = zip.namelist()
        logger.info('Zip package contains filenames: %s', filenames)
        assert filenames, 'Zip file is empty'

        # Read first file from zip
        payload_file = zip.read(filenames[0])
        return payload_file

    def download(self, **query):

        if query['type'] == 'application':
            response = self.query_application(query['number'])
        elif query['type'] == 'publication':
            response = self.query_publication(query['number'])
        elif query['type'] == 'patent':
            response = self.query_patent(query['number'])
        else:
            raise KeyError('Unknown document type for "{}"'.format(query))

        if not response['queryResults']['searchResponse']['response']['numFound'] >= 1:
            raise KeyError('No results when searching for {}.'.format(query))

        query_id = response['queryId']

        # Which formats are requested?
        if 'format' not in query:
            do_xml = True
            do_json = True
        else:
            formats = to_list(query['format'])
            do_xml = 'xml' in formats
            do_json = 'json' in formats

        # Acquisition
        if do_xml:
            self.request_package(query_id, 'XML')
            self.wait_for_package(query_id, 'XML')

        if do_json:
            self.request_package(query_id, 'JSON')
            self.wait_for_package(query_id, 'JSON')

        # Download
        result = {}
        if do_xml:
            package_zip = self.download_package(query_id, 'XML')
            payload_xml = self.unzip_package(package_zip)
            result['xml'] = payload_xml

        if do_json:
            package_zip = self.download_package(query_id, 'JSON')
            payload_json = self.unzip_package(package_zip)
            result['json'] = payload_json

        return result

def download_and_print(client, **query):

    result = client.download(**query)

    print('-' * 42)
    print('XML format')
    print('-' * 42)
    print(result['xml'])
    print

    print('-' * 42)
    print('JSON format')
    print('-' * 42)
    print(json.dumps(json.loads(result['json']), indent=4))
    print
