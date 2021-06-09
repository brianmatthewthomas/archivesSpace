# to put modified dates back in
import lxml.etree as ET
import sys, os
import csv

nsmap = {'ead': "urn:isbn:1-931666-22-9"}
justifier = input("CSV file with the corrections: ")
theWay = input("path to xml being modified: ")
fixFile = input("file to fix: ")
justifier = os.path.join(theWay, justifier)
fixFile = os.path.join(theWay, fixFile)
with open(justifier, 'r') as f:
    reader = csv.reader(f)
    with open(fixFile, "r") as r:
        filedata = r.read()
        for row in reader:
            filename = row[0]
            extent_text = row[2]
            extentList = extent_text.split("; ")
            extentValue = ""
            extentValue2 = ""
            extentValue3 = ""
            if len(extentList) == 1:
                extentValue = extentList[0]
                if extentValue.endswith("cm"):
                    extentValue2 = extentValue
                    extentValue = '1 SOMETHING'
                elif extentValue == "0.05 cubic ft., 1 artifact":
                    extentValue = '<extent>0.05 cubit ft.</extent></physdesc><physdesc><extent>1 artifact</extent>'
                elif extentValue == "1.65 cubic ft., 626 architectural drawings, 21 prints and photographs, 1 artifact":
                    extentValue2 = '<extent>1.65 cubic ft.</extent></physdesc><physdesc><extent>626 architectural drawings</extent></physdesc><physdesc><extent>21 prints and photographs</extent></physdesc><physdesc><extent>1 artifact<extent>'
                elif extentValue == "paper 93 cm x 107 cm":
                    extentValue = '1 drawing'
                    extentValue3 = 'paper'
                    extentValue2 = '93cm x 107cm'
                elif extentValue == 'blueprints':
                    extentValue = '1 blueprints'
                elif extentValue == 'linen':
                    extentValue = '1 drawing'
                    extentValue3 = 'linen'
                elif extentValue == 'rotogravure, 8 x 10, 2 copies':
                    extentValue = '1 rotogravure'
                    extentValue2 = '8 x 10'
                    extentValue3 = '2 copies'
                elif 'albumen' in extentValue:
                    tempy = extentValue.split(" (")
                    extentValue = '1 ' + tempy[0]
                    temptation = tempy[1].replace(")", " ")
                    extentValue2 = temptation
                elif extentValue == "paper 86.5 cm x 95 cm":
                    extentValue2 = '86.5 cm x 95 cm'
                    extentValue3 = 'paper'
                elif extentValue == "linen":
                    extentValue3 = extentValue
                    extentValue = "1 drawing"
            if len(extentList) == 2:
                extentValue = extentList[0]
                extentValue2 = extentList[1]
                if 'linen' in extentValue:
                    extentValue3 = extentValue
                    extentValue = '1 drawing'
                elif 'albumen' in extentValue:
                    tempy = extentValue.split(" (")
                    extentValue = '1 ' + tempy[0]
                    extentValue3 = extentValue2
                    extentValue2 = tempy[1][:-1]
                elif extentValue2 == 'paper':
                    tempy = extentValue3
                    extentValue3 = extentValue2
                    extentValue2 = tempy
                elif "paper" in extentValue:
                    tempy = extentValue
                    extentValue = "1 drawing"
                    extentValue3 = tempy
                elif 'tissue' in extentValue:
                    tempy = extentValue
                    extentValue = "1 drawing"
                    extentValue3 = tempy
                elif extentValue.startswith("blue"):
                    extentValue = "1 " + extentValue
            if len(extentList) == 3:
                extentValue = extentList[0]
                extentValue2 = extentList[1]
                extentValue3 = extentList[2]
                if extentValue.startswith("blue"):
                    extentValue = "<extent>1 " + extentValue + "</extent>"
                elif extentValue == "2 copies":
                    tempy = extentValue
                    extentValue = "1 " + extentValue2
                    extentValue2 = extentValue3
                    extentValue3 = tempy
                elif extentValue == "paper":
                    tempy = extentValue
                    extentValue = "1 drawing"
                    extentValue3 = tempy + " " + extentValue3
                elif extentValue == "part missing":
                    tempy = extentValue
                    extentValue = "1 " + extentValue2
                    extentValue2 = extentValue3
                    extentValue3 = tempy
                elif 'tissue' in extentValue:
                    if extentValue3 == "5 drawings":
                        extentValue = extentValue3
                        extentValue3 = "tissue"
                    else:
                        extentValue = "1 drawing"
                        extentValue3 = "tissue " + extentValue3
            if extentValue != "" and not extentValue.startswith("<extent>"):
                extentValue = "<extent>" + extentValue + '</extent>'
            if extentValue2 != "" and not extentValue2.startswith("<dimensions>"):
                extentValue2 = "<dimensions>" + extentValue2 + "</dimensions>"
            if extentValue3 != "" and not extentValue3.startswith("<physfacet>"):
                extentValue3 = "<physfacet>" + extentValue3 + "</physfacet>"
            filedata = filedata.replace('<extent>' + extent_text + '</extent>',
                                        extentValue + extentValue2 + extentValue3)
    with open(fixFile, "w") as w:
        w.write(filedata)
    w.close()
print("all done")


