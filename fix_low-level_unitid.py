import lxml.etree as ET
import os

xml_to_fix = input("filename to fix: ")

nsmap = {'ead': "urn:isbn:1-931666-22-9"}

dom = ET.parse(xml_to_fix)
unitids = dom.xpath(".//ead:unitid", namespaces=nsmap)
tags = ['{urn:isbn:1-931666-22-9}c02','{urn:isbn:1-931666-22-9}c03','{urn:isbn:1-931666-22-9}c04','{urn:isbn:1-931666-22-9}c05',
        '{urn:isbn:1-931666-22-9}c06','{urn:isbn:1-931666-22-9}c07','{urn:isbn:1-931666-22-9}c08','{urn:isbn:1-931666-22-9}c09']
print(unitids)
for unitid in unitids:
    parent = unitid.getparent().getparent()
    print(parent.tag)
    if parent.tag in tags:
        listy = unitid.keys()
        print(listy)
        for item in listy:
            unitid.attrib.pop(item)
dom.write(xml_to_fix, pretty_print=True)