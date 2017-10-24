# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
import json
import logging
import zipfile
import requests
from io import BytesIO
from pprint import pprint
from bs4 import BeautifulSoup
from clint.textui import progress
from uspto.util.common import to_list, SmartException
from uspto.util.numbers import guess_type_from_number

logger = logging.getLogger(__name__)

class UsptoGenericBulkDataClient:

    def __init__(self):
        self.session = requests.Session()
        self.downloader = None

    def query(self, expression, filter=None, sort=None, start=None, rows=None, default_field=None):

        # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html

        # Set defaults
        default_field = default_field or 'patentTitle'
        filter = filter or []
        sort = sort or 'applId asc'

        # Filter must be a list
        filter = to_list(filter)

        logger.info('Querying for expression=%s, filter=%s, sort=%s', expression, filter, sort)
        solr_query = {
            'searchText': expression,
            'df': default_field,
            'facet': True,
            'fl': '*',
            'fq': filter,
            'mm': '100%',
            'qf': 'appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber '
                  'appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor '
                  'firstNamedApplicant appExamName appExamPrefrdName appAttrDockNumber appPCTNumber appIntlPubNumber '
                  'wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList',
            'sort': sort,
        }

        if start is not None:
            solr_query.update(start=str(start))

        if rows is not None:
            solr_query.update(rows=str(rows))

        #pprint(solr_query)

        # Submit the query to the Solr search service
        response = self.session.post(self.QUERY_URL, json=solr_query)
        #print(response.text)

        # Check response and scrape appropriate error message from HTML on failure
        if response.status_code != 200:
            logger.error('Error while querying for %s\n%s', expression, response.text)
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
            else:
                raise ValueError('Search error with response of unknown Content-Type')

        return response.json()

    def search(self, *args, **kwargs):
        total_response = self.query(*args, **kwargs)
        search_response = total_response['queryResults']['searchResponse']

        # Main result payload
        result = search_response['response']

        # Pick some other important information
        metadata = {
            'indexLastUpdatedDate': total_response['queryResults']['indexLastUpdatedDate'],
            'queryId': total_response['queryResults']['queryId'],
            'responseHeader': search_response['responseHeader']
        }
        result.update(metadata=metadata)
        return result

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

    def download_package(self, query_id, format, progressbar=False):
        url = self.PACKAGE_DOWNLOAD_URL.format(query_id=query_id, format=format)
        logger.info('Downloading package for queryId=%s with format=%s. url=%s', query_id, format, url)
        response = self.session.get(url, stream=progressbar)
        assert response.status_code in [200, 302], 'No download package. status={}'.format(response.status_code)
        assert response.headers['Content-Type'] == 'application/zip'
        if not progressbar:
            return response.content
        else:
            # https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads/20943461#20943461
            total_length = int(response.headers.get('Content-Length'))
            buffer = BytesIO()
            for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1, filled_char='='):
                if chunk:
                    buffer.write(chunk)

            buffer.seek(0)
            return buffer.read()

    def unzip_package(self, payload_zip):

        # Decode zip file
        zip = zipfile.ZipFile(BytesIO(payload_zip), 'r')
        filenames = zip.namelist()
        logger.info('Zip package contains filenames: %s', filenames)
        assert filenames, 'Zip file is empty'

        # Read first file from zip
        payload_file = zip.read(filenames[0])
        return payload_file

    def download(self, query_id, format=None, progressbar=False):

        format = format or []
        formats = to_list(format)

        # Which formats are requested?
        if not formats:
            do_xml = True
            do_json = True
        else:
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
            result['xml'] = self.download_package(query_id, 'XML', progressbar=progressbar)

        if do_json:
            result['json'] = self.download_package(query_id, 'JSON', progressbar=progressbar)

        return result

    def download_document(self, *args, **kwargs):

        if kwargs:
            query = kwargs
        elif args:
            query = {'number': args[0]}

        # Defaults
        query['type'] = query.get('type', 'auto') or 'auto'
        if query['type'] == 'auto':
            query['type'] = guess_type_from_number(query['number'])

        query['format'] = query.get('format', ['xml', 'json'])

        if query['type'] == 'application':
            response = self.query_application(query['number'])
        elif query['type'] == 'publication':
            response = self.query_publication(query['number'])
        elif query['type'] == 'patent':
            response = self.query_patent(query['number'])
        else:
            raise UnknownDocumentType('Unknown document type for {}'.format(query), query=query)

        if response['queryResults']['searchResponse']['response']['numFound'] == 0:
            raise NoResults('No results when searching for {}.'.format(query), query=query)

        query_id = response['queryId']

        result = self.download(query_id, query['format'])

        for format, package_zip in result.items():
            payload = self.unzip_package(package_zip)
            result[format] = payload

        return result

    def query_application(self, applicationId):
        expression = 'applId:({})'.format(applicationId)
        return self.query(expression)

    def query_publication(self, appEarlyPubNumber):
        expression = 'appEarlyPubNumber:({})'.format(appEarlyPubNumber)
        return self.query(expression)

    def query_patent(self, patentNumber):
        expression = 'patentNumber:({})'.format(patentNumber)
        return self.query(expression)


class NoResults(SmartException):
    pass

class UnknownDocumentType(SmartException):
    pass

def download_and_print(client, **query):

    result = client.download_document(**query)

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
