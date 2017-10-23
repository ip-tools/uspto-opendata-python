# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import json
import logging
import lxml.etree
import jsonpointer

logger = logging.getLogger(__name__)

class GenericDocument:

    def __init__(self, data=None, xml=None, json=None):
        data = data or {}
        self.xml  = xml or data.get('xml')
        self.json = json or data.get('json')
        self.identifiers = {}

    def get_identifiers(self):

        if self.xml:
            doc = lxml.etree.fromstring(self.xml)
            for number_type, xpath in self.XML_IDENTIFIER_XPATH_MAP.items():
                node = doc.xpath(xpath, namespaces=self.XML_NAMESPACES)
                if node:
                    identifier = self.sanitize_value(node[0].text)
                    if identifier:
                        self.identifiers.setdefault(number_type, identifier.decode('utf-8'))

        if self.json:
            data = json.loads(self.json)
            for number_type, jpointer in self.JSON_IDENTIFIER_JSONPOINTER_MAP.items():
                try:
                    identifier = self.sanitize_value(jsonpointer.resolve_pointer(data, jpointer))
                    if identifier:
                        self.identifiers.setdefault(number_type, identifier)
                except jsonpointer.JsonPointerException:
                    pass

        return self.identifiers

    def sanitize_value(self, value):
        # Compensate for values like "0" or " 0  "
        if not value:
            return
        value = value.strip()
        if value == '0':
            return
        return value
