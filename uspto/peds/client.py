# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from uspto.util.client import UsptoGenericBulkDataClient, download_and_print

logger = logging.getLogger(__name__)

class UsptoPatentExaminationDataSystemClient(UsptoGenericBulkDataClient):
    """
    Python client for accessing the USPTO Patent Examination Data System API (https://ped.uspto.gov/).
    See also: https://ped.uspto.gov/peds/#/apiDocumentation
    """
    QUERY_URL            = 'https://ped.uspto.gov/api/queries'
    PACKAGE_REQUEST_URL  = 'https://ped.uspto.gov/api/queries/{query_id}/package?format={format}'
    PACKAGE_STATUS_URL   = 'https://ped.uspto.gov/api/queries/{query_id}?format={format}'
    PACKAGE_DOWNLOAD_URL = 'https://ped.uspto.gov/api/queries/{query_id}/download?format={format}'

    FILENAME_SOURCE      = 'peds'


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    client = UsptoPatentExaminationDataSystemClient()

    # Published applications by publication number
    # US2017293197A1: appEarlyPubNumber:(US2017293197A1)
    download_and_print(client, publication='US2017293197A1')
    #download_and_print(client, publication='US2017293197A1')
    #download_and_print(client, publication='2017/0293197')  # No results

    # Published applications by application number
    # US2017293197A1: applId:(15431686)
    #download_and_print(client, application='15431686')

    # Granted patents by patent number
    #download_and_print(client, patent='PP28532')
    #download_and_print(client, patent='9788906')
    #download_and_print(client, patent='D799980')
    #download_and_print(client, patent='RE46571')
    #download_and_print(client, patent='3525666')           # No results

    # Deleted: US11673P
    #download_and_print(client, patent='PP11673')           # No results
