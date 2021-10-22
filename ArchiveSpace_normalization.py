import lxml.etree as ET
import sys, os, re

def spaceinator (content):
    print(content)
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
    containers = dom.xpath(".//ead:container", namespaces=nsmap)
    for container in containers:
        type = container.attrib['type']
        if type == "box":
            container.attrib['type'] = "Box"
        if type == 'folder':
            container.attrib['type'] = "Folder"
    dom.write(filename, pretty_print=True)
    with open(filename, "r") as r:
        filedata = r.read()
        filedata = filedata.replace("LadyGaga</emph>", "</emph>, ")
        filedata = filedata.replace(",  ", ", ")
        filedata = filedata.replace(", </unittitle>", "</unittitle>")
        filedata = filedata.replace('"</emph>,', ',"</emph>')
        filedata = filedata.replace("http://legacy.lib.utexas.edu/taro","https://legacy.lib.utexas.edu/taro")
        donkeykong = re.findall(r'https://\.*lib.utexas.edu/taro/\.*/\.*/\.*.html', filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                temp1 = item.split("/")[-3]
                temp2 = item.split("/")[-2]
                new_url = f'https://www.txarchives.org/{temp1}/finding_aids/{temp2}.xml'
                filedata = filedata.replace(item,new_url)
        with open(filename, "w") as w:
            w.write(filedata)
        w.close()

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
