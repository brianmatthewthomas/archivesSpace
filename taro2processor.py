import os
import shutil
import daterangeparser
import datetime
import locale
import lxml.etree as ET
import re

def subjectspace (subject):
    while subject.startswith(" "):
        subject = subject[1:]
    while subject.endswith(" "):
        subject = subject[:-1]
    return subject

def timeturner (dateify):
    if dateify == "undated" or dateify == "undated," or dateify == "undated, " or dateify == 'n.d.':
        dateify = "2021"
    dateify = dateify.replace("bulk", "").replace("(not inclusive)", "").replace("and undated", "").replace("undated","").replace(":","")
    dateify = dateify.replace("about", "").replace("\n", '').replace("[", '').replace("]", '').replace("ca.",'').replace('week of','').replace(";",'')
    dateify = dateify.replace("and", "-").replace("primarily", "").replace(" or ", "-").replace("(?),", "").replace("(?)", "").replace("(", '').replace(")",'').replace("?","")
    # process comma-separate months of the same year
    A = "January"
    B = "February"
    C = "March"
    D = "April"
    E = "May"
    F = "June"
    G = "July"
    H = "August"
    I = "September"
    J = "October"
    K = "November"
    L = "December"
    dateify = dateify.replace(A+", "+B,A+"-"+B).replace(A+", "+C,A+"-"+C).replace(A+", "+D,A+"-"+D).replace(A+", "+E,A+"-"+E).replace(A+", "+F,A+"-"+F).replace(A+", "+G,A+"-"+G).replace(A+", "+H,A+"-"+H).replace(A+", "+I,A+"-"+I).replace(A+", "+J,A+"-"+J).replace(A+", "+K,A+"-"+K).replace(A+", "+L,A+"-"+L)
    dateify = dateify.replace(B+", "+C,B+"-"+C).replace(B+", "+D,B+"-"+D).replace(B+", "+E,B+"-"+E).replace(B+", "+F,B+"-"+F).replace(B+", "+G,B+"-"+G).replace(B+", "+H,B+"-"+H).replace(B+", "+I,B+"-"+I).replace(B+", "+J,B+"-"+J).replace(B+", "+K,B+"-"+K).replace(B+", "+L,B+"-"+L)
    dateify = dateify.replace(C+", "+D,B+"-"+D).replace(C+", "+E,B+"-"+E).replace(C+", "+F,B+"-"+F).replace(C+", "+G,B+"-"+G).replace(C+", "+H,B+"-"+H).replace(C+", "+I,B+"-"+I).replace(C+", "+J,B+"-"+J).replace(C+", "+K,B+"-"+K).replace(C+", "+L,B+"-"+L)
    dateify = dateify.replace(D+", "+E,D+"-"+E).replace(D+", "+F,D+"-"+F).replace(D+", "+G,D+"-"+G).replace(D+", "+H,D+"-"+H).replace(D+", "+I,D+"-"+I).replace(D+", "+J,D+"-"+J).replace(D+", "+K,D+"-"+K).replace(D+", "+L,D+"-"+L)
    dateify = dateify.replace(E+", "+F,E+"-"+F).replace(E+", "+G,E+"-"+G).replace(E+", "+H,E+"-"+H).replace(E+", "+I,E+"-"+I).replace(E+", "+J,E+"-"+J).replace(E+", "+K,E+"-"+K).replace(E+", "+L,E+"-"+L)
    dateify = dateify.replace(F+", "+G,F+"-"+G).replace(F+", "+H,F+"-"+H).replace(F+", "+I,F+"-"+I).replace(F+", "+J,F+"-"+J).replace(F+", "+K,F+"-"+K).replace(F+", "+L,F+"-"+L)
    dateify = dateify.replace(G+", "+H,G+"-"+H).replace(G+", "+I,G+"-"+I).replace(G+", "+J,G+"-"+J).replace(G+", "+K,G+"-"+K).replace(G+", "+L,G+"-"+L)
    dateify = dateify.replace(H+", "+I,H+"-"+I).replace(H+", "+J,H+"-"+J).replace(H+", "+K,H+"-"+K).replace(H+", "+L,H+"-"+L)
    dateify = dateify.replace(I+", "+J,I+"-"+J).replace(I+", "+K,I+"-"+K).replace(I+", "+L,I+"-"+L)
    dateify = dateify.replace(J+", "+K,J+"-"+K).replace(J+", "+L,J+"-"+L)
    dateify = dateify.replace(K+", "+L,K+"-"+L)
    dateify = dateify.replace("-"+A+"-","-").replace("-"+B+"-","-").replace("-"+C+"-","-").replace("-"+D+"-","-").replace("-"+E+"-","-").replace("-"+F+"-","-").replace("-"+G+"-","-").replace("-"+H+"-","-").replace("-"+I+"-","-").replace("-"+J+"-","-").replace("-"+K+"-","-")

    # next steps
    donkeykong = re.search(r'\d{2}-\d{2},', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        donkeykong = ", " + donkeykong
        dateify = dateify.replace(donkeykong, donkeykong[-4:])
    donkeykong = re.search(r'\d{2}/\d{2}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = datetime.datetime.strptime(donkeykong, "%m/%d/%Y")
        dittykong = dittykong.strftime("%B %d, %Y")
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{1}/\d{2}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "0" + donkeykong
        dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
        dittykong = dittykong.strftime("%B %d, %Y")
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{2}/\d{2}/\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong[:-2] + "19" + donkeykong[-2:]
        dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
        dittykong = dittykong.strftime("%B %d, %Y")
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{1}/\d{2}/\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "0" + donkeykong[:-2] + "19" + donkeykong[-2:]
        dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
        dittykong = dittykong.strftime("%B %d, %Y")
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{1}/\d{1}/\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "0" + donkeykong[:2] + "0" + donkeykong[2:-2] + "19" + donkeykong[-2:]
        dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
        dittykong = dittykong.strftime("%B %d, %Y")
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, " + donkeykong[-4:]
        print(dittykong)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{4}-\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        if dateify.startswith(donkeykong + ",") or dateify.startswith(donkeykong + " ") or dateify.endswith(donkeykong):
            dittykong = donkeykong[:5] + donkeykong[:2] + donkeykong[-2:]
            print(dittykong)
            dateify = dateify.replace(donkeykong,dittykong)
    dateify.strip()
    while dateify.endswith(".") or dateify.endswith(". "):
        dateify = dateify[:-1]
    while dateify.endswith(", "):
        dateify = dateify[:-2]
    while dateify.endswith(" "):
        dateify = dateify[:-1]
    while dateify.endswith(","):
        dateify = dateify[:-1]
    while dateify.startswith(" "):
        dateify = dateify[1:]
    date_normal = ""
    try:
        temp_value = daterangeparser.parse(dateify)
        if "-" in dateify:
            start, end = daterangeparser.parse(dateify)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
            date_normal += start + "/" + end + "/"
        else:
            start, end = daterangeparser.parse(dateify)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
            if end != None:
                date_normal += start + "/" + end + "/"
            else:
                date_normal += start + "/" + start + "/"
        # print(dateify)
    except:
        listy = dateify.split(",")
        for item in listy:
            while item.startswith(" "):
                item = item[1:]
            if "-early" in item and item.endswith("s"):
                item = item.replace("early", "")
                item = item[:-2] + "4"
            item = item.replace("early", "")
            if item.startswith("late") or item.startswith(" late"):
                silly = item.split("-")
                temp1 = silly[0].replace(" ", "").replace("late", "")
                if "s" in temp1:
                    temp1 = temp1[:-2] + "5"
                try:
                    item = temp1 + "-" + silly[1]
                except:
                    item = temp1
            if item.endswith("0s"):
                if item.startswith("mid-late "):
                    item = item.replace("mid-late ", "")
                    tempy = item[-5:-1]
                    tempy = tempy[:-1] + "5-"
                    item = tempy + item
                item = item[:-2] + "9"
            item = item.replace("s-", " -")
            if item != '':
                try:
                    start, end = daterangeparser.parse(item)
                    start = start.strftime("%Y-%m-%d")
                    if end != None:
                        end = end.strftime("%Y-%m-%d")
                        date_normal += start + "/" + end + "/"
                    else:
                        date_normal += start + "/" + start + "/"
                except:
                    print(listy)
                    print(item)
                    newDate = input("manually enter date normal attribute above using YYYY-MM-DD/YYYY-MM-DD: ")
                    if not newDate.endswith("/"):
                        newDate += "/"
                    date_normal += newDate
    date_normal = date_normal[:-1]
    if date_normal.startswith("/"):
        date_normal = date_normal[1:]
    date_normal = date_normal.split("/")
    date_normal.sort()
    date_normal = date_normal[0] + "/" + date_normal[-1]
    if "-01-01/2021" in date_normal:
        date_normal = date_normal.replace("-01-01/2021", "")
        date_normal = date_normal + "/" + date_normal
    if date_normal == "/":
        date_normal = "0000/0000"
    if date_normal == "2021-01-01/2021-12-31" or date_normal == "2021-12-31/2021-12-31":
        date_normal = "0000/0000"
    return date_normal

catalyst = ET.XML('''
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ead="urn:isbn:1-931666-22-9" xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="xs" version="1.0">

<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
<!-- copy everything -->
<xsl:template match="node()|@*">
	<xsl:copy>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:copy>
</xsl:template>
<!-- insert namespace prefix into everything so there are no errors in xml transform application -->
<xsl:template match="*">
	<xsl:element name="ead:{name()}" namespace="urn:isbn:1-931666-22-9">
		<xsl:copy-of select="namespace::*"/>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:element>
</xsl:template>
<!-- stuff that needs to be weeded out -->
<xsl:template match="@id"/>
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:titleproper/ead:num"/>
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:publicationstmt/ead:address"/>
<xsl:template match="ead:ead/ead:archdesc/ead:dsc/ead:c01/ead:did/ead:unitid"/>
<xsl:template match="ead:relatedmaterial/ead:head"/>
<xsl:template match="ead:extent[@altrender='carrier']"/>
<!-- update ead header info -->
<xsl:template match="ead:eadheader">
	<xsl:element name="ead:eadheader">
		<xsl:attribute name="countryencoding">iso3166-1</xsl:attribute>
		<xsl:attribute name="dateencoding">iso8601</xsl:attribute>
		<xsl:attribute name="langencoding">iso639-2b</xsl:attribute>
		<xsl:attribute name="repositoryencoding">iso15511</xsl:attribute>
		<xsl:attribute name="audience">internal</xsl:attribute>
		<xsl:attribute name="findaidstatus">edited-full-draft</xsl:attribute>
		<xsl:attribute name="scriptencoding">iso15924</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:eadid">
	<xsl:element name="ead:eadid">
		<xsl:attribute name="countrycode">US</xsl:attribute>
		<xsl:attribute name="mainagencycode">US-tx</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- make a change to the unitid to add the correct attributes -->
<xsl:template match="ead:odd">
	<xsl:element name="ead:note">
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>

<xsl:template match="ead:unitid">
	<xsl:element name="ead:unitid">
		<xsl:attribute name="label">TSLAC Control No.:</xsl:attribute>
		<xsl:attribute name="countrycode">US</xsl:attribute>
		<xsl:attribute name="repositorycode">US-tx</xsl:attribute>
		<xsl:attribute name="encodinganalog">099</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- change unit titles to generally have the marc code inserted -->
<xsl:template match="ead:unittitle">
	<xsl:element name="ead:unittitle">
		<xsl:attribute name="encodinganalog">245</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- change highest level unit title to have both marc code and title label -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:unittitle">
	<ead:unittitle>
		<xsl:attribute name="label">Title:</xsl:attribute>
		<xsl:attribute name="encodinganalog">245</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:unittitle>
</xsl:template>
<!-- modify 1storigination to match the correct encoding analog attributes in the 100s -->
<xsl:template match="ead:origination[1]">
	<xsl:element name="ead:origination">
		<xsl:choose>
			<xsl:when test="@label='creator'">
				<xsl:attribute name="label">Creator:</xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="label"><xsl:value-of select="@label"/></xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:for-each select="ead:corpname">
			<xsl:element name="ead:corpname">
				<xsl:attribute name="encodinganalog">110</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:persname">
			<xsl:element name="ead:persname">
				<xsl:attribute name="encodinganalog">100</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:famname">
			<xsl:element name="ead:famname">
				<xsl:attribute name="encodinganalog">100 3</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
	</xsl:element>
</xsl:template>
<!-- update the highest level unit date to include the label=Dates: and encodinganalog -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:unitdate">
	<ead:unitdate>
		<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
		<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
		<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
		<xsl:choose>
			<xsl:when test="@normal">
				<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>
		<xsl:attribute name="label">Dates:</xsl:attribute>
		<xsl:choose>
			<xsl:when test="@type='bulk'">
				<xsl:attribute name="encodinganalog">245$g</xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="encodinganalog">245$f</xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</ead:unitdate>
</xsl:template>
<!-- update the highest level abstract to include encodinganalog and correct label -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:abstract">
	<ead:abstract>
		<xsl:attribute name="label">Abstract:</xsl:attribute>
		<xsl:attribute name="encodinganalog">520$a</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:abstract>
</xsl:template>
<!-- update the highest level physdesc to include encodinganalog and correct label name -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:physdesc">
	<ead:physdesc>
		<xsl:attribute name="label">Quantity:</xsl:attribute>
		<xsl:attribute name="encodinganalog">300$a</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:physdesc>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:langmaterial">
	<xsl:element name="ead:langmaterial">
		<xsl:attribute name="label">Language:</xsl:attribute>
		<xsl:attribute name="encodinganalog">546$a</xsl:attribute>
		<xsl:if test="@audience">
			<xsl:attribute name="audience"><xsl:value-of select="@audience"/></xsl:attribute>
		</xsl:if>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update repository to include the encodinganalog and correct links for tslac -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:repository">
	<xsl:element name="ead:repository">
		<xsl:attribute name="encodinganalog">852$a</xsl:attribute>
		<xsl:element name="ead:extref">
            <xsl:attribute name="xlink:actuate">onRequest</xsl:attribute>
            <xsl:attribute name="xlink:show">new</xsl:attribute>
            <xsl:attribute name="xlink:href">http://www.tsl.state.tx.us/arc/index.html</xsl:attribute>
            <xsl:attribute name="xlink:type">simple</xsl:attribute>
			<xsl:text>Texas State Archives</xsl:text>
		</xsl:element>
	</xsl:element>
</xsl:template>
<!-- general extref processing -->
<xsl:template match="ead:extref">
    <xsl:element name="ead:extref">
            <xsl:attribute name="xlink:actuate">onRequest</xsl:attribute>
            <xsl:attribute name="xlink:show">new</xsl:attribute>
            <xsl:attribute name="xlink:href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
            <xsl:attribute name="xlink:type">simple</xsl:attribute>
            <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
</xsl:template>
<!-- insert correct encodinganalog in acqinfo -->
<xsl:template match="ead:acqinfo">
	<xsl:element name="ead:acqinfo">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">541</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">541</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
		</xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update custodhist to generally have correct encodinganalog -->
<xsl:template match="ead:custodhist">
	<xsl:element name="ead:custodhist">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">561</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">561</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to sponsor tag -->
<xsl:template match="ead:sponsor">
	<xsl:element name="ead:sponsor">
		<xsl:attribute name="encodinganalog">536</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- insert the logo/graphic reference in the tslac listed as publisher tag -->
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:publicationstmt/ead:publisher">
	<xsl:element name="ead:publisher">
		<xsl:value-of select="."/>
		<extptr xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onLoad" xlink:show="embed" xlink:href="https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg" xlink:type="simple"/>
	</xsl:element>
</xsl:template>
<!-- modify creation to reword the output, pull the archivists name, 
insert proper attributes in the date and keep just the date and not the whole UTC code -->
<xsl:template match="ead:ead/ead:eadheader/ead:profiledesc/ead:creation">
	<xsl:element name="ead:creation">
		<xsl:text>Finding aid created in ArchivesSpace by </xsl:text>
		<xsl:value-of select="substring(//ead:titlestmt/ead:author,15,1000)"/>
		<xsl:text> and exported as EAD Version 2002 as part of the TARO project, </xsl:text>
		<xsl:element name="ead:date">
			<xsl:attribute name="era">ce</xsl:attribute>
			<xsl:attribute name="calendar">gregorian</xsl:attribute>
			<xsl:value-of select="substring(ead:date,1,10)"/>
		</xsl:element>
		<xsl:text>.</xsl:text>
	</xsl:element>
</xsl:template>
<!-- change descrules tag content to match our standards -->
<xsl:template match="ead:ead/ead:eadheader/ead:profiledesc/ead:descrules">
	<xsl:element name="ead:descrules">Description based on 
		<xsl:element name="ead:emph">
			<xsl:attribute name="render">italic</xsl:attribute>DACS
		</xsl:element>.
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to accessrestrict -->
<xsl:template match="ead:accessrestrict">
	<xsl:element name="ead:accessrestrict">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">506</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">506</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to processing info -->
<xsl:template match="ead:processinfo">
	<xsl:element name="ead:processinfo">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to appraisal info -->
<xsl:template match="ead:appraisal">
	<xsl:element name="ead:appraisal">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to separated materials -->
<xsl:template match="ead:separatedmaterial">
	<xsl:element name="ead:separatedmaterial">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">544 0</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">544 0</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to accruals -->
<xsl:template match="ead:accruals">
	<xsl:element name="ead:accruals">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">584</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">584</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to altformavail -->
<xsl:template match="ead:altformavail">
	<xsl:element name="ead:altformavail">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">530</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">530</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to originalsloc -->
<xsl:template match="ead:originalsloc">
	<xsl:element name="ead:originalsloc">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">535</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">535</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to userestrict -->
<xsl:template match="ead:userestrict">
	<xsl:element name="ead:userestrict">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">540</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">540</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to phystech -->
<xsl:template match="ead:phystech">
	<xsl:element name="ead:phystech">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">340</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">340</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog and bio attribute to bioghist -->
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[1]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio1</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[2]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio2</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[3]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio3</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to scopecontent -->
<xsl:template match="ead:scopecontent">
	<ead:scopecontent>
		<xsl:if test="parent::ead:archdesc">
			<xsl:attribute name="encodinganalog">520$b</xsl:attribute>
		</xsl:if>
		<xsl:if test="@id">
		    <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
		</xsl:if>
		<xsl:apply-templates />
	</ead:scopecontent>
</xsl:template>
<!-- add correct encodinganalog to arrangement -->
<xsl:template match="ead:arrangement">
	<xsl:element name="ead:arrangement">
	    <xsl:choose>
	        <xsl:when test="parent::ead:descgrp">
        		<xsl:attribute name="encodinganalog">351</xsl:attribute>
        	</xsl:when>
        	<xsl:when test="parent::ead:archdesc">
        		<xsl:attribute name="encodinganalog">351</xsl:attribute>
        	</xsl:when>
        	<xsl:otherwise/>
        </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to preferred citation -->
<xsl:template match="ead:prefercite">
	<xsl:element name="ead:prefercite">
	    <xsl:choose>
	        <xsl:when test="parent::ead:descgrp">
        		<xsl:attribute name="encodinganalog">524</xsl:attribute>
        	</xsl:when>
        	<xsl:when test="parent::ead:archref">
        		<xsl:attribute name="encodinganalog">524</xsl:attribute>
        	</xsl:when>
        	<xsl:otherwise/>
        </xsl:choose>        	    
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update physdesc when not direct child of a series -->
<xsl:template match="ead:physdesc[ancestor::*[@level='file']]">
	<xsl:element name="ead:physdesc">
		<xsl:apply-templates select="@*"/>
		<xsl:text>[</xsl:text>
		<xsl:apply-templates />
		<xsl:text>]</xsl:text>
	</xsl:element>
</xsl:template>
<!-- reformat controlled access to group like tags into subheadings and nested structure -->
<!-- change source from 'library of congress subject headings' to 'lcsh' when applicable -->
<xsl:template match="ead:ead/ead:archdesc/ead:controlaccess">
	<xsl:element name="ead:controlaccess">
		<ead:head>Index Terms</ead:head>
		<ead:p>
			<ead:emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</ead:emph>
		</ead:p>
		<!-- redirect added authors into controlled access terms and add the correct encoding analog -->
		<!-- trigger on the existence of the role attribute. Won't create segments if does not exist -->
		<xsl:if test="//ead:origination/ead:famname[@role]|ead:controlaccess/ead:famname[@encodinganalog='700']">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Family Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:famname">
					<xsl:element name="ead:famname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:famname[@encodinganalog='700']">
					<xsl:element name="ead:famname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<xsl:if test="//ead:origination/ead:persname[@role]|ead:controlaccess/ead:persname[@encodinganalog='700']">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Personal Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:persname[@role]">
					<xsl:element name="ead:persname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname[@encodinganalog='700']">
					<xsl:element name="ead:persname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<xsl:if test="//ead:origination/ead:corpname[@role]|ead:controlaccess/ead:corpname[@encodinganalog='710']">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Corporate Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:corpname[@role]">
					<xsl:element name="ead:corpname">
						<xsl:attribute name="encodinganalog">710</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:corpname[@encodinganalog='710']">
					<xsl:element name="ead:corpname">
						<xsl:attribute name="encodinganalog">710</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<!-- begin rearrangement of controlled access terms into nested structure, but preserve structure if possible -->
		<xsl:if test="ead:persname[1]|ead:controlaccess/ead:persname[@encodinganalog='600']">
			<ead:controlaccess>
				<ead:head>Subjects (Persons):</ead:head>
				<xsl:for-each select="ead:persname">
					<xsl:element name="ead:persname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname[@encodinganalog='600']">
					<xsl:element name="ead:persname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:famname[1]|ead:controlaccess/ead:famname[@encodinganalog='600']">
			<ead:controlaccess>
				<ead:head>Subjects (Families):</ead:head>
				<xsl:for-each select="ead:famname">
					<xsl:element name="ead:famname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname[@encodinganalog='600']">
					<xsl:element name="ead:famname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:corpname|ead:controlaccess/ead:corpname[@encodinganalog='610']">
			<ead:controlaccess>
				<ead:head>Subjects (Organizations):</ead:head>
				<xsl:for-each select="ead:corpname">
					<xsl:element name="ead:corpname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">610</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:corpname[@encodinganalog='610']">
					<xsl:element name="ead:corpname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">610</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:subject[1]|ead:controlaccess/ead:subject">
			<ead:controlaccess>
				<ead:head>Subjects:</ead:head>
				<xsl:for-each select="ead:subject">
					<xsl:element name="ead:subject">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">650</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:subject">
					<xsl:element name="ead:subject">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@authfilenumber">
                            <xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
                        </xsl:if>
                        <xsl:attribute name="encodinganalog">650</xsl:attribute>
                        <xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:geogname[1]|ead:controlaccess/ead:geogname[@encodinganalog='651']">
			<ead:controlaccess>
				<ead:head>Places:</ead:head>
				<xsl:for-each select="ead:geogname">
					<xsl:element name="ead:geogname">
					<xsl:choose>
						<xsl:when test="@source='Library of Congress Subject Headings'">
							<xsl:attribute name="source">lcsh</xsl:attribute>
						</xsl:when>
						<xsl:when test="@source='naf'">
							<xsl:attribute name="source">lcnaf</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">651</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:geogname[@encodinganalog='651']">
					<xsl:element name="ead:geogname">
					<xsl:choose>
						<xsl:when test="@source='Library of Congress Subject Headings'">
							<xsl:attribute name="source">lcsh</xsl:attribute>
						</xsl:when>
						<xsl:when test="@source='naf'">
							<xsl:attribute name="source">lcnaf</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">651</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:genreform[1]|ead:controlaccess/ead:genreform">
			<ead:controlaccess>
				<ead:head>Document Types:</ead:head>
				<xsl:for-each select="ead:genreform">
					<xsl:element name="ead:genreform">
					    <xsl:choose>
					        <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source=''">
                                        <xsl:attribute name="source">aat</xsl:attribute>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
					        <xsl:otherwise>
					            <xsl:attribute name="source">aat</xsl:attribute>
					        </xsl:otherwise>
					    </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">655</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:genreform">
					<xsl:element name="ead:genreform">
					    <xsl:choose>
					        <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source=''">
                                        <xsl:attribute name="source">aat</xsl:attribute>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
					        <xsl:otherwise>
					            <xsl:attribute name="source">aat</xsl:attribute>
					        </xsl:otherwise>
					    </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">655</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:title[1]|ead:controlaccess/ead:title[@encodinganalog='630']">
			<ead:controlaccess>
				<ead:head>Titles:</ead:head>
				<xsl:for-each select="ead:title">
					<xsl:element name="ead:title">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:attribute name="encodinganalog">630</xsl:attribute>
						<xsl:attribute name="source">lcnaf</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:title[@encodinganalog='630']">
					<xsl:element name="ead:title">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:attribute name="encodinganalog">630</xsl:attribute>
						<xsl:attribute name="source">lcnaf</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:function[1]|ead:controlaccess/ead:function[@encodinganalog='657']">
			<ead:controlaccess>
				<ead:head>Functions:</ead:head>
				<xsl:for-each select="ead:function">
					<xsl:element name="ead:function">
						<xsl:choose>
							<xsl:when test="@source='Library of Congress Subject Headings'">
								<xsl:attribute name="source">lcsh</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='naf'">
								<xsl:attribute name="source">lcnaf</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='aat'">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source=''">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:otherwise>
								<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:attribute name="encodinganalog">657</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:function[@encodinganalog='657']">
					<xsl:element name="ead:function">
						<xsl:choose>
							<xsl:when test="@source='Library of Congress Subject Headings'">
								<xsl:attribute name="source">lcsh</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='naf'">
								<xsl:attribute name="source">lcnaf</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='aat'">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source=''">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:otherwise>
								<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:attribute name="encodinganalog">657</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
	</xsl:element>
</xsl:template>
<!-- update ead:dsc to include a generic header -->
<xsl:template match="ead:ead/ead:archdesc/ead:dsc">
	<xsl:element name="ead:dsc">
		<xsl:attribute name="type">combined</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[1]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser1</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[2]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser2</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[3]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser3</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[4]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser4</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[5]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser5</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[6]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser6</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[7]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser7</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[8]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser8</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[9]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser9</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[10]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser10</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[11]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser11</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[12]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser12</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[13]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser13</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[14]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser14</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[15]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser15</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[16]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser16</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[17]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser17</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[18]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser18</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[19]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser19</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[20]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser20</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c01/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present -->
<xsl:template match="//ead:c01/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c02 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c02/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c02/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c02[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c03 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c03/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c03/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c03[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c04 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c04/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c04/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c04[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c05 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c05/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c05/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c05[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c06 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c06/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c06/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c06[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c07 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c07/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c07/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c07[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c08 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c08/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c08/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c08[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c09 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c09/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c09/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c09[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- add some attributes to the archdesc tag -->
<!-- add a overview head tag to the top level did -->
<!-- get related materials properly nested together -->
<!-- group content belonging in the descgrp into that tag -->
<xsl:template match="ead:ead/ead:archdesc">
	<xsl:element name="ead:archdesc">
		<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		<xsl:attribute name="type">inventory</xsl:attribute>
		<xsl:attribute name="audience">external</xsl:attribute>
		<xsl:for-each select="ead:did">
			<xsl:element name="ead:did">
				<!-- <ead:head>Overview</ead:head> -->
				<xsl:apply-templates />
			</xsl:element>
		</xsl:for-each>
		<xsl:if test="ead:relatedmaterial[1]">
			<xsl:element name="ead:relatedmaterial">
				<xsl:attribute name="encodinganalog">544 1</xsl:attribute>
				<ead:head>Related Material</ead:head>
				<ead:p>
					<xsl:element name="ead:emph">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:text>The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive.</xsl:text>
					</xsl:element>
				</ead:p> 
				<xsl:for-each select="ead:relatedmaterial">
					<xsl:element name="ead:relatedmaterial">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:for-each> 
			</xsl:element>
		</xsl:if>
		<xsl:for-each select="ead:custodhist">
			<xsl:element name="ead:custodhist">
				<xsl:attribute name="encodinganalog">561</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:prefercite">
			<xsl:element name="ead:prefercite">
				<xsl:attribute name="encodinganalog">524</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:acqinfo">
			<xsl:element name="ead:acqinfo">
				<xsl:attribute name="encodinganalog">541</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:processinfo">
			<xsl:element name="ead:processinfo">
				<xsl:attribute name="encodinganalog">583</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:appraisal">
			<xsl:element name="ead:appraisal">
				<xsl:attribute name="encodinganalog">583</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:separatedmaterial">
			<xsl:element name="ead:separatedmaterial">
				<xsl:attribute name="encodinganalog">544 0</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:accruals">
			<xsl:element name="ead:accruals">
				<xsl:attribute name="encodinganalog">584</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:altformavail">
			<xsl:element name="ead:altformavail">
				<xsl:attribute name="encodinganalog">530</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:originalsloc">
			<xsl:element name="ead:originalsloc">
				<xsl:attribute name="encodinganalog">535</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<!-- now strip out the original copy of everything that was modified above -->
<xsl:template match="ead:ead/ead:archdesc/ead:did"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[2]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[3]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[4]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[5]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[6]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[7]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[8]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[9]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[10]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[11]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[12]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[13]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[14]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[15]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[16]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[17]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[18]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[19]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[20]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[21]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[22]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[23]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[24]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[25]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[26]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[27]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[28]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[29]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[1]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[2]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[3]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[4]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[5]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[6]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[7]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[8]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[9]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:custodhist"/>
<xsl:template match="ead:ead/ead:archdesc/ead:prefercite"/>
<xsl:template match="ead:ead/ead:archdesc/ead:acqinfo"/>
<xsl:template match="ead:ead/ead:archdesc/ead:processinfo"/>
<xsl:template match="ead:ead/ead:archdesc/ead:appraisal"/>
<xsl:template match="ead:ead/ead:archdesc/ead:separatedmaterial"/>
<xsl:template match="ead:ead/ead:archdesc/ead:accruals"/>
<xsl:template match="ead:ead/ead:archdesc/ead:altformavail"/>
<xsl:template match="ead:ead/ead:archdesc/ead:originalsloc"/>
<xsl:template match="ead:ead/ead:archdesc/ead:odd"/>
<xsl:template match="//ead:c01/ead:controlaccess"/>
<xsl:template match="//ead:c01/ead:scopecontent/ead:head|//ead:c02/ead:scopecontent/ead:head|//ead:c03/ead:scopecontent/ead:head|//ead:c04/ead:scopecontent/ead:head|//ead:c05/ead:scopecontent/ead:head|//ead:c06/ead:scopecontent/ead:head|//ead:c07/ead:scopecontent/ead:head|//ead:c07/ead:scopecontent/ead:head|//ead:c08/ead:scopecontent/ead:head|//ead:c09/ead:scopecontent/ead:head"/>
</xsl:stylesheet>''')
nsmap = {'xmlns': 'urn:isbn:1-931666-22-9',
         'ead': 'urn:isbn:1-931666-22-9',
         'xlink': 'http://www.w3.org/1999/xlink'}
#parse as xslt for application below
transform = ET.XSLT(catalyst)
print("this is supposed to fix a bunch of minor issues related to TARO 2.0 normalization, check output for correctness")
print("file will be spit out as its original name in a processed folder")
process = input("folder to process: ")
tx_number = "txNumbers.csv"  #input("csv file with the tx_number: ")
sourceDir = input("source directory as relative or absolute filepath: ")
process = sourceDir + "/" + process
output = sourceDir + "/processed"
exception = sourceDir + "/problems"
tx_number = sourceDir + "/" + tx_number
pairing = {}
with open(tx_number, "r") as r:
    for line in r:
        line = line[:-1]
        line = line.split(",")
        pairing[line[0]] = line[1]
print(pairing)
for dirpath, dirnames, filenames in os.walk(process):
    for filename in filenames:
        ead_file = os.path.join(dirpath, filename)
        output_file = os.path.join(output,filename)
        exception_file = os.path.join(exception,filename)
        with open(ead_file, "r") as r:
            filedata = r.read()
            if "xmlns:ead" not in filedata:
                filedata = filedata.replace('xmlns="','xmlns:ead="urn:isbn:1-931666-22-9" xmlns="')
            with open(ead_file, "w") as w:
                w.write(filedata)
            w.close()
        dom = ET.parse(ead_file)
        newdom = transform(dom)
        newdom.write(output_file, pretty_print=True)
        with open(output_file, "r") as r:
            filedata = r.read()
            if "unitid>" not in filedata:
                filedata = filedata.replace("abstract>","abstract>\n<ead:unitid label='TSLAC Control No.:' countrycode='US' repositorycode='US-tx' encodinganalog='099'></ead:unitid>")
            filedata = filedata.replace(' xmlns:xlink="http://www.w3.org/1999/xlink"',"")
            filedata = filedata.replace(' xlink:actuate="onLoad"',"")
            filedata = filedata.replace(' xlink:actuate="onRequest"',"")
            filedata = filedata.replace(' xlink:show="embed"','')
            filedata = filedata.replace(' xlink:show="new"','')
            filedata = filedata.replace(' xlink:href',' href')
            filedata = filedata.replace(' xlink:type="simple"','')
            filedata = filedata.replace(' xlink:role=""','')
            filedata = filedata.replace(' href=""','')
            filedata = filedata.replace('<ead:unitdate era="ce" calendar="gregorian"/>','')
            filedata = filedata.replace('xmlns=""','')
            filedata = filedata.replace("\t",'')
            filedata = filedata.replace("\n"," ")
            while "  " in filedata:
                filedata = filedata.replace("  "," ")
            filedata = filedata.replace("> <",">\n<")
            filedata = filedata.replace("><",">\n<")
            filedata = filedata.replace(",, ",", ")
        with open(output_file, "w") as w:
            w.write(filedata)
        w.close()
        unitid_text = filename.split(".")[0]
        print(pairing[unitid_text])
        dom2 = ET.parse(output_file)
        unitid = dom2.xpath("//ead:unitid", namespaces=nsmap)
        unitid[0].text = pairing[unitid_text]
        dates = dom2.xpath("//ead:unitdate", namespaces=nsmap)
        screwballs = []
        flag = 0
        for date in dates:
            dateify = date.text
            #TODO something
            if "normal" not in date.attrib:
                date.attrib['normal'] = timeturner(dateify)
            if "type" not in date.attrib:
                if "bulk" not in dateify:
                    date.attrib['type'] = "inclusive"
                else:
                    date.attrib['type'] = ""
            if date.attrib['type'] == "":
                print(dateify)
                date.attrib['type'] = input("date type missing, inclusive or bulk: ")
        subjects = dom2.xpath("//ead:subject", namespaces=nsmap)
        subjectlist = []
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
            if subject.attrib['source'] == "local":
                flag += 1
        subjects = dom2.xpath("//ead:controlaccess/ead:genreform", namespaces=nsmap)
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
            if subject.attrib['source'] == "local":
                flag += 1
        subjects = dom2.xpath("//ead:function", namespaces=nsmap)
        subjectlist = []
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
        subjects = dom2.xpath("//ead:persname", namespaces=nsmap)
        subjectlist = []
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
            if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
                flag += 1
        subjects = dom2.xpath("//ead:famname", namespaces=nsmap)
        subjectlist = []
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
            if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
                flag += 1
        subjects = dom2.xpath("//ead:corpname", namespaces=nsmap)
        subjectlist = []
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
            if subject.text in subjectlist:
                subject.getparent().remove(subject)
            else:
                subjectlist.append(subject.text)
            if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
                flag += 1
        # sorts subjects, but causes head to sort into the middle so adding a preceding space to get it sort on top, then removing afterwards
        subjects = dom2.xpath("//ead:head", namespaces=nsmap)
        for subject in subjects:
            subject.text = " " + subject.text
        for node in dom2.xpath("//ead:controlaccess/ead:controlaccess", namespaces=nsmap):
            if node.tag == "head":
                node.text = " " + node.text
            node[:] = sorted(node, key=lambda ch: ch.text)
        subjects = dom2.xpath("//ead:head", namespaces=nsmap)
        for subject in subjects:
            subjective = subject.text
            subject.text = subjectspace(subjective)
        dom2.write(output_file, pretty_print=True)
        with open(output_file, "r") as r:
            filedata = r.read()
            filedata = filedata.replace('<extptr href','<extptr xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onLoad" xlink:show="embed" xlink:type="simple" xlink:href')
            filedata = filedata.replace('<ead:extref href','<ead:extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
            filedata = filedata.replace('<ead:archref href','<ead:archref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
            filedata = filedata.replace('<ead:bibref href','<ead:bibref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
            filedata = filedata.replace('label="Quantity"','label="Quantity:"')
            filedata = filedata.replace('label="Creator"','label="Creator:"')
            filedata = filedata.replace('label="Collector"','label="Collector:"')
            filedata = filedata.replace('label="Title"','label="Title:"')
            filedata = filedata.replace('label="Dates"','label="Dates:"')
            filedata = filedata.replace('label="Abstract"','label="Abstract:"')
            filedata = filedata.replace(", , <",", <")
            filedata = filedata.replace("..",".").replace(". .",".")
            filedata = filedata.replace("\n<ead:descgrp>","")
            filedata = filedata.replace("\n</ead:descgrp>","")
            filedata = filedata.replace("ead:","")
            filedata = filedata.replace('\n<relatedmaterial>\n<p>\n<emph render="italic">The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive.</emph>\n</p>','')
            filedata = filedata.replace('\n<relatedmaterial>\n<p>\n<emph render="italic">The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive. </emph>\n</p>','')
            filedata = filedata.replace("\n</relatedmaterial>\n</relatedmaterial>\n</relatedmaterial>","\n</relatedmaterial>\n</relatedmaterial>")
            filedata = filedata.replace('\n<controlaccess>\n<head>Index Terms</head>\n<p>\n<emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</emph>\n</p>\n</controlaccess>','')
            if "852$a" not in filedata:
                filedata = filedata.replace("</abstract>",'</abstract>\n<repository encodinganalog="852$a">\n<extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href="http://www.tsl.state.tx.us/arc/index.html">Texas State Archives</extref>\n</repository>')
        with open(output_file, "w") as w:
            w.write('<?xml version="1.0" encoding="UTF-8"?>\n' + filedata)
        w.close()
        switch = True
        if flag > 0:
            print("potential subject term issue in",unitid_text,"moving to problem area for checking")
            shutil.move(output_file,exception_file)
            switch = False
        if switch is True:
            try:
                dom3 = ET.parse(output_file)
            except:
                print(unitid_text, "has a xml tag problem, moving to special handling area")
                shutil.move(output_file,exception_file)
        switch = "no"
        while switch != "yes":
            switch = input(f"did you verify the ead file is okay with {unitid_text}?: ")
print("all done!")
#TODO continue testing against real files