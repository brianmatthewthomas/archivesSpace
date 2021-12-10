import lxml.etree as ET
import os
nsmap = {'ead': "urn:isbn:1-931666-22-9"}
toCrawl = input("directory of files to crawl: ")
for dirpath, dirnames, filenames in os.walk(toCrawl):
    for filename in filenames:
        if filename.endswith(".xml"):
            filename = os.path.join(dirpath, filename)
            dom = ET.parse(filename)
            extents = dom.xpath(".//ead:extent", namespaces=nsmap)
            for extent in extents:
                manipulatableText = extent.text
                formats = [".aiff",".aif",".aup",".au",".avi",".bak",".bmp",
                           ".bup",".ccx",".cdr",".cr2",".crw",".db",".docx",
                           ".doc",".dot",".dv",".eps",".fcp",".flv",".gif",
                           ".html",".htm",".ifo",".jpg",".jpeg",".lay",".m2v",
                           ".m4a",".m4v",".mov",".mp3",".mp4",".mpg",".msg",
                           ".nef",".pcd",".pdf",".png",".pptx",".ppt",".psd",
                           ".rtf",".thm",".tif",".txt",".upsd",".wav",".wmv",
                           ".xlsx",".xls",".xmp",".vob",".zip"]
                sizes = ["KB","MB","GB","TB"]
                formatica = ""
                tempText = ""
                if "ft. and " in manipulatableText:
                    tempy = manipulatableText.split("ft. and ")
                    manipulatableText = manipulatableText.replace(tempy[0] + "ft. and ","")
                    tempText = tempText + tempy[0] + "ft.TURKEYTOM"
                if "(" in manipulatableText:
                    tempy = manipulatableText.split(" (")[0]
                    tempText = tempText + tempy + "TURKEYTOM"
                    manipulatableText = manipulatableText.replace(tempy + " (","")
                    manipulatableText = manipulatableText.replace(")","")
                for item in sizes:
                    item2 = item + ", "
                    if item2 in manipulatableText:
                        tempy = manipulatableText.split(item2)[0]
                        tempText = tempText + tempy + item + "TURKEYTOM"
                        manipulatableText = manipulatableText.replace(tempy + " " + item,"")
                for item in formats:
                    if item in manipulatableText:
                        formatica = formatica + item + ", "
                        manipulatableText = manipulatableText.replace(item,"")
                manipulatableText = manipulatableText.replace(",","").replace("and","")
                while "  " in manipulatableText:
                    manipulatableText = manipulatableText.replace("  "," ")
                while manipulatableText.startswith(" "):
                    manipulatableText = manipulatableText[1:]
                while manipulatableText.endswith(" "):
                    manipulatableText = manipulatableText[:-1]
                tempText = tempText + manipulatableText
                formatica = formatica[:-2]
                print(tempText)
                if len(formatica) > 0:
                    print(formatica)
                extent.text = tempText
            dom.write(filename, pretty_print=True)
            with open(filename, "r") as r:
                filedata = r.read()
                filedata = filedata.replace("TURKEYTOM","</extent></physdesc><physdesc><extent>")
                with open(filename, "w") as w:
                    w.write(filedata)
                w.close()
            logfile = filename[:-4] + "-01.txt"
            with open(logfile, "a") as w:
                dom = ET.parse(filename)
                extents = dom.xpath(".//ead:extent", namespaces=nsmap)
                for extent in extents:
                    w.write(extent.text + "\n")
