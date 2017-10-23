# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from uspto.pbd.document import UsptoPairBulkDataDocument
from uspto.util.client import UsptoGenericBulkDataClient, download_and_print

logger = logging.getLogger(__name__)

class UsptoPairBulkDataClient(UsptoGenericBulkDataClient):
    """
    Python client for accessing the USPTO PAIR Bulk Data API (https://pairbulkdata.uspto.gov/).
    See also: https://pairbulkdata.uspto.gov/#/api-documentation
    """
    DATASOURCE_NAME      = 'pbd'

    QUERY_URL            = 'https://pairbulkdata.uspto.gov/api/queries'
    PACKAGE_REQUEST_URL  = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/package?format={format}'
    PACKAGE_STATUS_URL   = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}?format={format}'
    PACKAGE_DOWNLOAD_URL = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/download?format={format}'

    document_factory     = UsptoPairBulkDataDocument


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    client = UsptoPairBulkDataClient()

    # Published applications by publication number
    # US2017293197A1: appEarlyPubNumber:(2017/0293197)
    download_and_print(client, number='2017/0293197', type='publication')
    #download_and_print(client, number='2017-0293197')
    #download_and_print(client, number='20170293197')  # No results

    # Published applications by application number
    # US2017293197A1: applId:(15431686)
    #download_and_print(client, number='15431686')

    # Granted patents by patent number
    #download_and_print(client, number='PP28532')
    #download_and_print(client, number='9788906')
    #download_and_print(client, number='D799980')
    #download_and_print(client, number='RE46571')
    #download_and_print(client, number='3525666')           # No results

    # Deleted: US11673P
    #download_and_print(client, number='PP11673')           # No results
