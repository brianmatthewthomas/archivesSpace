import sys
import os
import lxml.etree as ET

def subjectspace (subject):
    if subject != None:
        while subject.startswith(" "):
            subject = subject[1:]
        while subject.endswith(" "):
            subject = subject[:-1]
        if subject.endswith("."):
            subject = subject[:-1]
    return subject

fileguy = input("file to process including filepath: ")
fileguy2 = input("output file name including filepath: ")

nsmap = {'marc': "http://www.loc.gov/MARC21/slim"}

dom = ET.parse(fileguy)
subjectList = []
subjects = dom.xpath("//marc:datafield", namespaces=nsmap)
for subject in subjects:
    thisTag = subject.attrib['tag']
    if thisTag == '650' or thisTag == '651':
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.attrib['tag'] == "650" and subject.attrib['ind2'] == "1":
            subject.attrib['ind2'] = "0"
        if subject in subjectList:
            subject.getparent().remove(subject)
        else:
            subjectList.append(subject)
    else:
        subject.getparent().remove(subject)
subjects = dom.xpath("//marc:datafield/marc:subfield", namespaces=nsmap)
for subject in subjects:
    subjective = subject.text
    subject.text = subjectspace(subjective)
dom.write(fileguy2, pretty_print=True)
