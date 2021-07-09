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
                turkey.addnext(item)
            if boss != None:
                boss.getparent().remove(boss)
            mySubjects = dom.xpath(".//ead:controlaccess/ead:controlaccess", namespaces=nsmap)
            for item in mySubjects:
                boss = item.getparent()
                turkey.addnext(item)
            if boss != None:
                boss.getparent().remove(boss)
            dom.write(filename, pretty_print=True)
