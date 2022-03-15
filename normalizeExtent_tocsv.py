import errno
import os
import lxml.etree as ET
import csv

catalyst = ET.XML('''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ead="urn:isbn:1-931666-22-9">
<xsl:output method="xml" encoding="UTF-8" version="1.0" standalone="yes"/>
<!-- For this to work you must use the python_xslt.py processor, some other processor or a webbrowser. If using the web browser, inser <?xml-stylesheet type="text/xsl" href="transform_removeAtomFeed.xsl"?> just after the xml declaration -->
<!-- WARNING: for reasons that are unclear, the template removing the Atom feed does not play well with others so adding it to another transform probably won't work. -->

	<xsl:template match="node()|@*">
		<xsl:copy>
			<xsl:apply-templates select="node()|@*"/>
		</xsl:copy>
	</xsl:template>
<xsl:template match="//ead:physdesc">
		<xsl:choose>
			<xsl:when test="ead:dimensions">
				<xsl:element name="physdesc">
					<xsl:element name="extent">
						<xsl:value-of select="normalize-space(ead:extent[1])"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="normalize-space(ead:genreform[1])"/>
					</xsl:element>
					<xsl:element name="dimensions">
						<xsl:text> </xsl:text>
						<xsl:value-of select="normalize-space(ead:dimensions)"/>
					</xsl:element>
				</xsl:element>
				<xsl:if test="ead:extent[2]">
					<xsl:element name="physdesc">
						<xsl:element name="extent">
							<xsl:value-of select="normalize-space(ead:extent[2])"/>
							<xsl:text> </xsl:text>
							<xsl:value-of select="normalize-space(ead:genreform[2])"/>
						</xsl:element>
					</xsl:element>
				</xsl:if>
				<xsl:if test="ead:extent[3]">
					<xsl:element name="physdesc">
						<xsl:element name="extent">
							<xsl:value-of select="normalize-space(ead:extent[3])"/>
							<xsl:text> </xsl:text>
							<xsl:value-of select="normalize-space(ead:genreform[3])"/>
						</xsl:element>
					</xsl:element>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="ead:genreform">
						<xsl:element name="physdesc">
							<xsl:element name="extent">
								<xsl:value-of select="normalize-space(ead:extent[1])"/>
								<xsl:text> </xsl:text>
								<xsl:value-of select="normalize-space(ead:genreform[1])"/>
							</xsl:element>
						</xsl:element>
						<xsl:if test="ead:extent[2]">
							<xsl:element name="physdesc">
								<xsl:element name="extent">
									<xsl:value-of select="normalize-space(ead:extent[2])"/>
									<xsl:text> </xsl:text>
									<xsl:value-of select="normalize-space(ead:genreform[2])"/>
								</xsl:element>
							</xsl:element>
						</xsl:if>
						<xsl:if test="ead:extent[3]">
							<xsl:element name="physdesc">
								<xsl:element name="extent">
									<xsl:value-of select="normalize-space(ead:extent[3])"/>
									<xsl:text> </xsl:text>
									<xsl:value-of select="normalize-space(ead:genreform[3])"/>
								</xsl:element>
							</xsl:element>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<xsl:choose>
							<xsl:when test="ead:extent">
								<xsl:element name="physdesc">
									<xsl:element name="extent">
										<xsl:value-of select="normalize-space(ead:extent)"/>
									</xsl:element>
								</xsl:element>
								<xsl:if test="ead:extent[2]">
									<xsl:element name="physdesc">
										<xsl:element name="extent">
											<xsl:value-of select="normalize-space(ead:extent[2])"/>
											<xsl:text> </xsl:text>
											<xsl:value-of select="normalize-space(ead:genreform[2])"/>
										</xsl:element>
									</xsl:element>
								</xsl:if>
								<xsl:if test="ead:extent[3]">
									<xsl:element name="physdesc">
										<xsl:element name="extent">
											<xsl:value-of select="normalize-space(ead:extent[3])"/>
											<xsl:text> </xsl:text>
											<xsl:value-of select="normalize-space(ead:genreform[3])"/>
										</xsl:element>
									</xsl:element>
								</xsl:if>
							</xsl:when>
							<xsl:otherwise>
								<xsl:element name="physdesc">
									<xsl:element name="extent">
										<xsl:value-of select="normalize-space(.)"/>
									</xsl:element>
								</xsl:element>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
</xsl:template>

</xsl:stylesheet>''')
transform = ET.XSLT(catalyst)
print("meant to normalize extent formatting and then spit out a spreadsheet of extents for correction, use the ..._fromcsv program to pair back the values you've updated in the csv file")
print("works as a directory crawler so be cognizant of that")
# the global variables
seriousFilepath = input("Source directory: ")
output = input("target directory: ")
nsmap = {'ead': "urn:isbn:1-931666-22-9"}
# getting down to work
for dirpath, dirnames, filenames in os.walk(seriousFilepath):
    # load directory to crawl
    for filename in filenames:
        filename2 = filename
        filename = os.path.join(dirpath, filename)
        if filename.endswith(('.xml')):
            dom = ET.parse(filename)
            #xslt = ET.parse(catalyst)
            #transform = ET.XSLT(xslt)
            newdom = transform(dom)
            newFilename = os.path.join(output, filename2)
            if not os.path.exists(os.path.dirname(newFilename)):
                try:
                    os.makedirs(os.path.dirname(newFilename), exist_ok=True)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            newdom.write(newFilename, xml_declaration=True, encoding='UTF-8', standalone='yes', pretty_print=True)
            print(newFilename + " is processed!")
            with open(newFilename, "r") as r:
                filedata = r.read()
                filedata = filedata.replace(' xmlns=""','')
                with open(newFilename, "w") as w:
                    w.write(filedata)
                w.close()
            print("creating csv file of extents to review")
            with open(newFilename[:-4] + ".csv", "a") as f:
                tree = ET.parse(newFilename)
                extents = tree.xpath("//ead:extent", namespaces=nsmap)
                for extent in extents:
                    print(extent.text)
                    if extent == None:
                        extentText = "NOTHING THERE"
                    else:
                        extentText = str(extent.text)
                    writer = csv.writer(f)
                    writer.writerow([filename2, tree.getpath(extent), extentText.encode('utf-8')])
                print(newFilename,"processed")
            f.close()
print("all done!")
# outfile = open(theFinishedProduct + "/" + filename)
# outfile.write(infile)
