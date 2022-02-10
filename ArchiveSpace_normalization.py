import lxml.etree as ET
import sys, os, re

pairing = {}
'''with open("/media/sf_D_DRIVE/working_electronicRecords/ASpace/TARO 2.0 data requirement fixes/problems/map-drawers.csv", "r") as f:
    for line in f:
        line = line[:-1]
        pairing[line.split(",")[-1]] = line.split(",")[0]
    print(pairing)'''
def spaceinator (content):
    #print(content)
    if content != None:
        while content.startswith(" "):
            content = content[1:]
        while content.endswith(" "):
            content = content[:-1]
        while content.endswith(","):
            content = content[:-1]
    return content

nsmap = {'ead': "urn:isbn:1-931666-22-9"}

def aspace_processor (file_name):
    filename = file_name
    ead_name = file_name.split("/")[-1].split(".")[0]
    filename2 = filename[:-4] + "-01.xml"
    dom = ET.parse(filename)
    print(f"fixing dates in {ead_name}")
    extents = dom.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        extentText = extent.text
        temp = extentText.split(" ")[0]
        temptation = extentText.replace(temp + " ","")
        temptation2 = temptation.replace(" ","_")
        extentText = extentText.replace(temptation,temptation2)
        while extentText.endswith(" "):
            extentText = extentText[:-1]
        if extentText.endswith(":") or extentText.endswith(","):
            extentText = extentText[:-1]
        if extentText.endswith(" ft."):
            extentText = extentText.replace(" ft.","_feet")
        if extentText.endswith("_ft."):
            extentText = extentText.replace("_ft.","_feet")
        if extentText.endswith("_ft"):
            extentText = extentText.replace("_ft","_feet")
        if extentText.endswith("KB") or extentText.endswith("MB") or extentText.endswith("GB") or extentText.endswith("TB"):
            extentText = extentText.replace(" KB"," kilobytes").replace(" MB"," megabytes").replace(" GB"," gigabytes").replace(" TB"," terabytes")
        if extentText.endswith(")") and not extentText.endswith("s)"):
            extentText = extentText.replace(")","s)")
        if not extentText.endswith("s") and not extentText.endswith("s)") and not extentText.endswith("_feet"):
            extentText = extentText + "s"
        if extentText.endswith("ys") or extentText.endswith("ys)"):
            extentText = extentText.replace("ys","ies")
        extent.text = extentText
    extents = dom.xpath(".//ead:extent/ead:emph", namespaces=nsmap)
    for extent in extents:
        extentText = extent.text
        temp = extentText.split(" ")[0]
        temptation = extentText.replace(temp + " ","")
        temptation2 = temptation.replace(" ","_")
        extentText = extentText.replace(temptation,temptation2)
        while extentText.endswith(" "):
            extentText = extentText[:-1]
        if extentText.endswith(":") or extentText.endswith(","):
            extentText = extentText[:-1]
        if extentText.endswith(" ft."):
            extentText = extentText.replace(" ft.","_feet")
        if extentText.endswith("_ft."):
            extentText = extentText.replace("_ft.","_feet")
        if extentText.endswith("_ft"):
            extentText = extentText.replace("_ft","_feet")
        if extentText.endswith("KB") or extentText.endswith("MB") or extentText.endswith("GB") or extentText.endswith("TB"):
            extentText = extentText.replace(" KB"," kilobytes").replace(" MB"," megabytes").replace(" GB"," gigabytes").replace(" TB"," terabytes")
        if extentText.endswith(")") and not extentText.endswith("s)"):
            extentText = extentText.replace(")","s)")
        if not extentText.endswith("s") and not extentText.endswith("s)") and not extentText.endswith("_feet"):
            extentText = extentText + "s"
        if extentText.endswith("ys") or extentText.endswith("ys)"):
            extentText = extentText.replace("ys","ies")
        extent.text = extentText
    dates = dom.xpath(".//ead:unitdate", namespaces=nsmap)
    for date in dates:
        dateText = date.text
        dateText = spaceinator(dateText)
        if dateText != None and dateText.endswith(","):
            dateText = dateText[:-1]
        date.text = dateText
    title_emph = dom.xpath(".//ead:unittitle/ead:emph", namespaces=nsmap)
    for title in title_emph:
        titleText = title.text
        if titleText.endswith(", "):
            titleText = titleText[:-2] + '"LadyGaga'
            title.text = titleText
        if titleText.endswith(","):
            titleText = titleText[:-1] + '"LadyGaga'
            title.text = titleText
        if titleText.endswith(',"'):
            titleText = titleText[:-2] + '"LadyGaga'
            title.text = titleText
        if titleText.endswith(', "'):
            titleText = titleText[:-3] + '"LadyGaga'
            title.text = titleText
    titles = dom.xpath(".//ead:unittitle", namespaces=nsmap)
    for title in titles:
        titleText = title.text
        titleText = spaceinator(titleText)
        title.text = titleText
    turkey = dom.find(".//ead:archdesc/ead:did", namespaces=nsmap)
    myRelatives = dom.xpath(".//ead:relatedmaterial/ead:relatedmaterial", namespaces=nsmap)
    if myRelatives != None:
        for item in myRelatives:
            boss = item.getparent()
            turkey.addnext(item)
            if boss != None:
                bossy = boss.getparent()
                if bossy != None:
                    boss.getparent().remove(boss)
    mySubjects = dom.xpath(".//ead:controlaccess/ead:controlaccess", namespaces=nsmap)
    for item in mySubjects:
        boss = item.getparent()
        turkey.addnext(item)
        if boss != None:
            bossy = boss.getparent()
            if bossy != None:
                boss.getparent().remove(boss)
    containers = dom.xpath(".//ead:container", namespaces=nsmap)
    for container in containers:
        type = container.attrib['type']
        container.attrib['type'] = type.capitalize()
    headings = dom.xpath(".//ead:c01[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c02[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c03[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c04[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c05[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c06[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c07[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c08[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    headings = dom.xpath(".//ead:c09[@otherlevel='Heading']/ead:did/ead:container", namespaces=nsmap)
    if headings != None:
        for heading in headings:
            print(heading.text)
            heading.getparent().remove(heading)
    scripts = dom.xpath(".//ead:language", namespaces=nsmap)
    if scripts != None:
        for script in scripts:
            print(script.text)
            if 'langcode' not in script.attrib:
                if "English" in script.text:
                    script.attrib['langcode'] = "eng"
            if script.attrib['langcode'] == "eng":
                script.attrib['scriptcode'] = "Latn"
    idents = dom.xpath(".//ead:unitid", namespaces=nsmap)
    for ident in idents:
        turkey = ident.getparent().getparent()
        if turkey.tag != "{urn:isbn:1-931666-22-9}archdesc":
            ident.attrib.pop('label')
            ident.attrib.pop('repositorycode')
            ident.attrib.pop('encodinganalog')
            ident.attrib.pop('countrycode')
    maps = dom.xpath(".//ead:did/ead:container[1]", namespaces=nsmap)
    for map in maps:
        if map.attrib['type'] == "Map":
            print(map.text)
            turkey = ET.Element("container")
            turkey.attrib['type'] = "Map-drawer"
            if map.text in pairing:
                turkey.text = pairing[map.text]
            else:
                turkey.text = "placeholder"
            map.addprevious(turkey)
    containerslist = []
    containerslength = {}
    containers = dom.xpath(".//ead:did/ead:container[1]", namespaces=nsmap)
    for container in containers:
        temp = container.text
        if "-" in temp:
            temp2 = temp.split("-")[0]
            if len(temp2) == 8:
                if temp2 not in containerslist:
                    containerslist.append(temp2)
                    containerslength[temp2] = 0
                temp3 = len(temp.split("-")[-1])
                if temp3 > containerslength[temp2]:
                    containerslength[temp2] = temp3
            if "LR" in temp2:
                if temp2 not in containerslist:
                    containerslist.append(temp2)
                    containerslength[temp2] = 0
                temp3 = len(temp.split("-")[-1])
                if temp3 > containerslength[temp2]:
                    containerslength[temp2] = temp3
    for container in containers:
        temp = container.text
        if "-" in temp:
            temp2 = temp.split("-")[0]
            if len(temp2) == 8:
                temp3 = temp.split("-")[-1]
                temp4 = temp3
                while len(temp4) < containerslength[temp2]:
                    temp4 = "0" + temp4
                temp = temp[:-len(temp3)] + temp4
                print(temp)
                container.text = temp
            if "LR" in temp2:
                temp3 = temp.split("-")[-1]
                temp4 = temp3
                while len(temp4) < containerslength[temp2]:
                    temp4 = "0" + temp4
                temp = temp[:-len(temp3)] + temp4
                print(temp)
                container.text = temp
    containers = dom.xpath(".//ead:container", namespaces=nsmap)
    for container in containers:
        temptext = container.text
        print(temptext)
        while temptext.endswith(" "):
            temptext = temptext[:-1]
        while temptext.endswith("."):
            temptext = temptext[:-1]
        container.text = temptext
    dom.write(filename2, pretty_print=True)
    with open(filename2, "r") as r:
        filedata = r.read()
        filedata = filedata.replace("LadyGaga</emph>", "</emph>, ")
        filedata = filedata.replace(",  ", ", ")
        filedata = filedata.replace(", </unittitle>", "</unittitle>")
        filedata = filedata.replace('"</emph>,', ',"</emph>')
        filedata = filedata.replace("http://legacy.lib.utexas.edu/taro","https://legacy.lib.utexas.edu/taro")
        filedata = filedata.replace("http://www.lib.utexas.edu/taro","https://legacy.lib.utexas.edu/taro")
        donkeykong = re.findall(r'https://.*lib.utexas.edu/taro/.*\/.*\/.*.html', filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                temp1 = item.split("/")[-3]
                temp2 = item.split("/")[-2]
                new_url = f'https://www.txarchives.org/{temp1}/finding_aids/{temp2}.xml'
                filedata = filedata.replace(item,new_url)
        filedata = filedata.replace("&apos;",";")
        with open(filename2, "w") as w:
            w.write(filedata)
        w.close()
        print(filename,"finished")

print("run against a directory to get broadscale changes in place for files before they get imported into the system")
print("or run against a discreet file")
print("run against a copy please")
switch = input("run against a directory or file: ")
while switch != "directory" and switch != "file":
    print("please type either 'directory' or 'file'")
    switch = input("run against a directory or file?: ")
if switch == "file":
    file_name = input("filename  to normalize including full filepath: ")
    aspace_processor(file_name)
    print(file_name.split("/")[-1],"processed")
if switch == "directory":
    directory = input("Directory to crawl: ")
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".xml"):
                filename = os.path.join(dirpath, filename)
                aspace_processor(filename)
                print(filename.split("/")[-1],"processed")
print("all done")
