#to put modified dates back in
import lxml.etree as ET
import sys, os
import csv

nsmap = {'ead': "urn:isbn:1-931666-22-9"}
justifier = input("CSV file with the corrections: ")
theWay = input("path to xml being modified: ")
justifier = os.path.join(theWay, justifier)
with open(justifier, 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		filename = row[0]
		filename = os.path.join(theWay, filename)
		extent_path = row[1]
		extent_text = row[2]
		print(extent_text)
		ead = open(filename)
		tree = ET.parse(ead)
		extent = tree.xpath(extent_path, namespaces=nsmap)
		extent[0].text = extent_text
		outfile = open(filename, 'wb')
		outfile.write(ET.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))
		outfile.close()


