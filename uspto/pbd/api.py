# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import requests

class UsptoPbdClient:

    # https://pairbulkdata.uspto.gov/#/api-documentation
    QUERY_URL            = 'https://pairbulkdata.uspto.gov/api/queries'
    PACKAGE_REQUEST_URL  = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/package'
    PACKAGE_STATUS_URL   = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}'
    PACKAGE_DOWNLOAD_URL = 'https://pairbulkdata.uspto.gov/api/queries/{query_id}/download'
