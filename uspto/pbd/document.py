# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from uspto.util.document import GenericDocument

logger = logging.getLogger(__name__)

class UsptoPairBulkDataDocument(GenericDocument):

    XML_NAMESPACES = {
        'pat': 'http://www.wipo.int/standards/XMLSchema/ST96/Patent',
        'uscom': 'urn:us:gov:doc:uspto:common',
        'uspat': 'urn:us:gov:doc:uspto:patent',
        'com': 'http://www.wipo.int/standards/XMLSchema/ST96/Common',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    XML_IDENTIFIER_XPATH_MAP = {
        'application': '/uspat:PatentBulkData/uspat:PatentData'
                       '/uspat:ApplicationData/uscom:ApplicationNumberText',
        'publication': '/uspat:PatentBulkData/uspat:PatentData'
                       '/uspat:PublishedDocumentData/uspat:ApplicationPublication/uspat:PatentPublicationIdentification/pat:PublicationNumber',
        'patent':      '/uspat:PatentBulkData/uspat:PatentData'
                       '/uspat:ApplicationData/uspat:PatentGrantIdentification/pat:PatentNumber',
    }

    JSON_IDENTIFIER_JSONPOINTER_MAP = {
        'application': '/PatentBulkData/0/applicationDataOrProsecutionHistoryDataOrPatentTermData/0'
                       '/applicationNumberText/value',
        'publication': '/PatentBulkData/0/applicationDataOrProsecutionHistoryDataOrPatentTermData/2'
                       '/applicationPublication/patentPublicationIdentification/publicationNumber',
        'patent':      '/PatentBulkData/0/applicationDataOrProsecutionHistoryDataOrPatentTermData/0'
                       '/patentGrantIdentification/patentNumber',
    }


if __name__ == '__main__':

    import sys
    format = sys.argv[1]
    payload = open(sys.argv[2], 'r').read()

    data = {format: payload}
    document = UsptoPairBulkDataDocument(data=data)
    print('identifiers:', document.get_identifiers())

