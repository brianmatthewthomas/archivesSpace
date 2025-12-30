# script to handle ead files not compliant with TARO standards of not having unitdate nested in unittitle.
# Unclear why this bad data practice was ever implemented

import lxml.etree as ET
import os

nsmap = {'xmlns': 'urn:isbn:1-931666-22-9',
         'ead': 'urn:isbn:1-931666-22-9',
         'xlink': 'http://www.w3.org/1999/xlink'}

crawl_me = input("directory of files to fix: ")

for dirpath, dirnames, filenames in os.walk(crawl_me):
    for filename in filenames:
        if filename.endswith(".xml"):
            filename = os.path.join(dirpath, filename)
            with open(filename, "r") as r:
                filedata = r.read()
                if "urn:isbn:1-931666-22-9" in filedata:
                    dom = ET.parse(filename)
                    root = dom.getroot()
                    bad_unitdate = root.xpath("//ead:unittitle/ead:unitdate", namespaces=nsmap)
                    if bad_unitdate is not None:
                        ET.indent(dom, space="\t")
                        with open(filename, "wb") as w:
                            w.write(ET.tostring(dom, pretty_print=True))
                        w.close()
                        for bad_date in bad_unitdate:
                            if bad_date.text is not None:
                                parent = bad_date.getparent()
                                parent.addnext(bad_date)
                                print(f"moved {bad_date.text}")
                        ET.indent(dom, space="\t")
                        filename2 = f"{filename[:-4]}_fixed.xml"
                        with open(filename2, "wb") as w:
                            w.write(ET.tostring(dom, pretty_print=True))
                        w.close()
print("all done!")