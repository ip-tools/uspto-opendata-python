# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import logging
from uspto.util.document import GenericDocument

logger = logging.getLogger(__name__)

class UsptoPatentExaminationDataSystemDocument(GenericDocument):

    XML_NAMESPACES = {
        'pat': 'http://www.wipo.int/standards/XMLSchema/ST96/Patent',
        'uscom': 'urn:us:gov:doc:uspto:common',
        'uspat': 'urn:us:gov:doc:uspto:patent',
        'com': 'http://www.wipo.int/standards/XMLSchema/ST96/Common',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    XML_IDENTIFIER_XPATH_MAP = {
        'application': '/uspat:PatentBulkData/uspat:PatentData/uspat:PatentRecordBag/uspat:PatentRecord/uspat:PatentCaseMetadata'
                       '/uscom:ApplicationNumberText',
        'publication': '/uspat:PatentBulkData/uspat:PatentData/uspat:PatentRecordBag/uspat:PatentRecord/uspat:PatentCaseMetadata'
                       '/uspat:RelatedPatentPublicationIdentification/pat:PublicationNumber',
        'patent':      '/uspat:PatentBulkData/uspat:PatentData/uspat:PatentRecordBag/uspat:PatentRecord/uspat:PatentCaseMetadata'
                       '/uspat:PatentGrantIdentification/pat:PatentNumber',
    }

    JSON_IDENTIFIER_JSONPOINTER_MAP = {
        'application': '/PatentBulkData/0/patentRecordBag/patentRecord/0/patentCaseMetadata'
                       '/applicationNumberText/value',
        'publication': '/PatentBulkData/0/patentRecordBag/patentRecord/0/patentCaseMetadata'
                       '/relatedPatentPublicationIdentification/publicationNumber',
        'patent':      '/PatentBulkData/0/patentRecordBag/patentRecord/0/patentCaseMetadata'
                       '/patentGrantIdentification/patentNumber',
    }


if __name__ == '__main__':

    import sys
    format = sys.argv[1]
    payload = open(sys.argv[2], 'r').read()

    data = {format: payload}
    document = UsptoPatentExaminationDataSystemDocument(data=data)
    print('identifiers:', document.get_identifiers())

