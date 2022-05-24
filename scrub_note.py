import lxml.etree as ET
import lxml
import sys, os

xml = "20125.xml"
nsmap = {'ead':'urn:isbn:1-931666-22-9'}

levels = ['c02','c03','c04','c05']
dom = ET.parse(xml)
for level in levels:
    print(level)
    notes = dom.xpath(f'//ead:{level}/ead:did/ead:note/ead:p', namespaces=nsmap)
    for note in notes:
        emphs = note.xpath("ead:emph", namespaces=nsmap)
        text = ""
        for emph in emphs:
            if emph.text is not None:
                emph_text = emph.text
                if emph.attrib['render'] == "bolditalic":
                    emph_text = "<emph render='bolditalic'>" + emph_text + "</emph>"
                text += emph_text + " "
                print(text)
        toremove = note.getparent()
        did = toremove.getparent().getparent()
        did2 = toremove.getparent()
        toremove.getparent().remove(toremove)
        scopecontents = did.xpath("ead:scopecontent",namespaces=nsmap)
        for scopecontent in scopecontents:
            if scopecontent is not None:
                emph = scopecontent.find("ead:p/ead:emph", namespaces=nsmap)
                emph_text = emph.text
                emph_text = emph_text + " " + text + "turkey"
                emph.text = emph_text
            else:
                scopecontent = lxml.addnext()
                scopecontent = ET.SubElement(did,"ead:scopecontent")
                emphasis = ET.SubElement(scopecontent,"ead:emph")
                emphasis.attrib['render'] = "italic"
                emphasis.text = text
dom.write("20125_fixed.xml", pretty_print=True)