# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
import json
import logging
import zipfile
import requests
from io import BytesIO
from BeautifulSoup import BeautifulSoup

logger = logging.getLogger(__name__)

class UsptoPairClient:
    """
    Python client for accessing the USPTO PAIR Bulk Data API (https://pairbulkdata.uspto.gov/).
    See also: https://pairbulkdata.uspto.gov/#/api-documentation
    """
    QUERY_URL            = 'https://pairbulkdata.uspto.gov/api/queries'
    PACKAGE_REQUEST_URL  = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/package?format={format}'
    PACKAGE_STATUS_URL   = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}?format={format}'
    PACKAGE_DOWNLOAD_URL = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/download?format={format}'

    def __init__(self):
        self.session = requests.Session()

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
            logger.error(response.text)
            if response.headers['Content-Type'] == 'text/html':
                soup = BeautifulSoup(response.text)
                title = soup.find('title')
                message = title.string.strip()
                hr = soup.body.find('hr')
                reason =  hr.nextSibling.string.strip()
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
        logger.info('Requesting package for queryId=%s with format=%s', query_id, format)
        response = self.session.put(self.PACKAGE_REQUEST_URL.format(query_id=query_id, format=format))
        assert response.status_code == 200
        time.sleep(1)
        return response.json()

    def package_status(self, query_id, format):
        logger.debug('Checking package status for queryId=%s with format=%s', query_id, format)
        response = self.session.get(self.PACKAGE_STATUS_URL.format(query_id=query_id, format=format))
        assert response.status_code == 200
        return response.json()

    def wait_for_package(self, query_id, format):
        # TODO: Break after x seconds or react on possible "FAIL" states
        # TODO: Sometimes jobs get stuck in 'INITIATED' state
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

        if 'application' in query:
            response = self.query_application(query['application'])
        elif 'publication' in query:
            response = self.query_publication(query['publication'])
        elif 'patent' in query:
            response = self.query_patent(query['patent'])
        else:
            raise KeyError('Unknown document type for "{}"'.format(query))

        if not response['queryResults']['searchResponse']['response']['numFound'] >= 1:
            raise KeyError('No results when searching for {}.'.format(query))

        query_id = response['queryId']

        self.request_package(query_id, 'XML')
        self.wait_for_package(query_id, 'XML')

        self.request_package(query_id, 'JSON')
        self.wait_for_package(query_id, 'JSON')

        package_zip = self.download_package(query_id, 'XML')
        payload_xml = self.unzip_package(package_zip)

        package_zip = self.download_package(query_id, 'JSON')
        payload_json = self.unzip_package(package_zip)

        result = {
            'xml': payload_xml,
            'json': json.loads(payload_json),
        }

        return result

def download_and_print(**query):

    client = UsptoPairClient()

    result = client.download(**query)

    print('-' * 42)
    print(result['xml'])
    print()

    print('-' * 42)
    print(json.dumps(result['json'], indent=4))
    print()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # Published applications by publication number
    # US2017293197A1: appEarlyPubNumber:(2017/0293197)
    #download_and_print(publication='2017/0293197')
    #download_and_print(publication='2017-0293197')
    #download_and_print(publication='20170293197')  # No results

    # Published applications by application number
    # US2017293197A1: applId:(15431686)
    #download_and_print(application='15431686')

    # Granted patents by patent number
    #download_and_print(patent='PP28532')
    #download_and_print(patent='9788906')
    #download_and_print(patent='D799980')
    #download_and_print(patent='RE46571')
    #download_and_print(patent='3525666')           # No results

    # Deleted: US11673P
    #download_and_print(patent='PP11673')           # No results

