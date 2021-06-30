import lxml.etree as ET
import sys, os

def spaceinator (content):
    while content.startswith(" "):
        content = content[1:]
    while content.endswith(" "):
        content = content[:-1]
    while content.endswith(","):
        content = content[:-1]
    return content

nsmap = {'ead': "urn:isbn:1-931666-22-9"}
print("run against a directory to get broadscale changes in place for files before they get imported into the system")
print("run against a copy please")
directory = input("Directory to crawl: ")
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith(".xml"):
            ead_name = filename.split(".")[0]
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            print(f"fixing dates in {ead_name}")
            dates = dom.xpath(".//ead:unitdate", namespaces=nsmap)
            for date in dates:
                dateText = date.text
                dateText = spaceinator(dateText)
                date.text = dateText
            titles = dom.xpath(".//ead:unittitle", namespaces=nsmap)
            for title in titles:
                titleText = title.text
                titleText = spaceinator(titleText)
                title.text = titleText
            turkey = dom.find(".//ead:archdesc/ead:arrangement", namespaces=nsmap)
            myRelatives = dom.xpath(".//ead:relatedmaterial/ead:relatedmaterial", namespaces=nsmap)
            for item in myRelatives:
                boss = item.getparent()
                boss = boss.getparent()
                turkey.addnext(item)
            mySubjects = dom.xpath(".//ead:controlaccess/ead:controlaccess", namespaces=nsmap)
            for item in mySubjects:
                boss = item.getparent()
                boss = boss.getparent()
                turkey.addnext(item)
            trashRemoval = dom.xpath(".//ead:controlaccess/ead:head", namespaces=nsmap)
            for item in trashRemoval:
                if "Index Terms" in item.text:
                    myBoss = item.getparent()
                    myBoss.getparent().remove(myBoss)
            trashRemoval = dom.xpath(".//ead:relatedmaterial/ead:p/ead:emph", namespaces=nsmap)
            for item in trashRemoval:
                if "possible sources" in item.text:
                    myBoss = item.getparent()
                    myBoss = myBoss.getparent()
                    myBoss.getparent().remove(myBoss)
            dom.write(filename, pretty_print=True)
