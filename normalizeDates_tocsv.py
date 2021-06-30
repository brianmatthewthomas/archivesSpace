import lxml.etree as ET
import sys, os
import csv
import re
import datetime

nsmap = {'ead': 'urn:isbn:1-931666-22-9'}
directory = input("Directory to run against: ")

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith(".xml"):
            filename2 = os.path.join(dirpath, filename)
            with open(filename2[:-4] + ".csv", "a") as errorlog:
                writer = csv.writer(errorlog, dialect='excel')
                writer.writerow(['filename','xpath','date_original','date_normal','date_computer_suggestion','date_desired'])
                tree = ET.parse(filename2)
                dates = tree.xpath('.//ead:unitdate', namespaces=nsmap)
                for date in dates:
                    dateText = date.text
                    dateNormal = date.attrib['normal']
                    beginDate = date.attrib['normal'].split("/")[0]
                    endDate = date.attrib['normal'].split("/")[-1]
                    compiledDate = ""
                    print(dateNormal)
                    if len(beginDate) == 4:
                        if beginDate == "0000":
                            beginDate = 'Undated'
                    if len(beginDate) == 10:
                        if beginDate.endswith("-02-29") and int(beginDate[:4]) % 4 == 0:
                            beginDate = "February 29, " + beginDate[:4]
                        else:
                            beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
                            beginDate = datetime.datetime.strftime(beginDate, "%B %d, %Y")
                    if len(endDate) == 4:
                        if endDate == "0000":
                            endDate = 'Undated'
                    if len(endDate) == 10:
                        if endDate.endswith("-02-29") and int(endDate[:4]) % 4 == 0:
                            endDate = "February 29, " + endDate[:4]
                        else:
                            endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
                            endDate = datetime.datetime.strftime(endDate, "%B %d, %Y")
                    if beginDate == endDate:
                        compiledDate = beginDate
                    if beginDate != endDate:
                        compiledDate = beginDate + " to " + endDate
                    if beginDate.startswith("January 01,") and endDate.startswith("December 31,"):
                        if beginDate[-4:] == endDate[-4:]:
                            compiledDate = beginDate[-4:]
                        else:
                            compiledDate = beginDate[-4:] + " to " + endDate[-4:]
                    if date.attrib['type'] == "bulk":
                        compiledDate = "bulk " + compiledDate
                    writer.writerow([filename, tree.getpath(date), '="' + dateText + '"', dateNormal, '="' + compiledDate + '"','="' + dateText + '"'])
            errorlog.close()