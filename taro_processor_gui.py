import lxml.etree as ET
import PySimpleGUI as SG
import os

def normalized_source(source):
    if source == "Library of Congress Subject Headings":
        source = "lcsh"
    if source == "naf":
        source = "lcnaf"
    if source == "":
        source = "lcnaf"
    return source


html_transform = ET.XML('''
<!-- EAD 2002 print stylesheet for the Texas State Archives, Nancy Enneking, January 2003-->
<!--  This stylesheet generates Style 4 which is intended to produce print output.  -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:ead="urn:isbn:1-931666-22-9" xmlns:xlink="http://www.w3.org/1999/xlink">
	<xsl:output omit-xml-declaration="yes" indent="yes"/>
	<xsl:strip-space elements="*"/>  

  <!-- Creates the body of the finding aid.-->
  <xsl:template match="/">
    <xsl:variable name="file">
			<xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>
    <html>
      <head>
        <style>
          h1,
          h2,
          h3{
              font-family:arial
          }</style>

        <title>
					<xsl:value-of select="normalize-space(ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:titleproper)"/>
          <xsl:text>  </xsl:text>
					<xsl:value-of select="normalize-space(ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:subtitle)"/>
        </title>
      </head>

      <body bgcolor="#FAFDD5">
        <xsl:call-template name="body"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template name="sponsor">
		<xsl:for-each select="ead:ead/ead:eadheader//ead:sponsor">
      <table width="100%">
        <tr>
					<td width="5%"/>
          <td width="25%" valign="top">
            <strong>
              <xsl:text>Sponsor: </xsl:text>
            </strong>
          </td>
          <td width="70%">						
						<xsl:apply-templates/>
          </td>
        </tr>
      </table>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="body">
    <xsl:variable name="file">
			<xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <xsl:call-template name="eadheader"/>
    <xsl:call-template name="archdesc-did"/>
		<xsl:call-template name="sponsor"/>
		<hr/>
    <xsl:call-template name="archdesc-bioghist"/>
    <xsl:call-template name="archdesc-scopecontent"/>
    <xsl:call-template name="archdesc-arrangement"/>
    <xsl:call-template name="archdesc-restrict"/>
    <xsl:call-template name="archdesc-control"/>
    <xsl:call-template name="archdesc-relatedmaterial"/>
    <xsl:call-template name="archdesc-admininfo"/>
    <xsl:call-template name="archdesc-otherfindaid"/>
    <xsl:call-template name="archdesc-index"/>
    <xsl:call-template name="archdesc-odd"/>
    <xsl:call-template name="archdesc-bibliography"/>
    <xsl:call-template name="dsc"/>
  </xsl:template>
  <xsl:template name="eadheader">
		<xsl:for-each select="ead:ead/ead:eadheader">
		<br/>
			<h2 style="text-align:center">
			    <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:titleproper"/>
      </h2>
			<h3 style="text-align:center">
			  <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:subtitle"/>
      </h3>

      <br/>
      <br/>

      <center>
        <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:author"/>
      </center>
      <br/>
      <br/>

      <center>
        <b>
          <xsl:value-of select="ead:filedesc/ead:publicationstmt/ead:publisher"/>
        </b>
      </center>
      <br/>
      <center> 
        <img 
          src="https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg"
        />
      </center>
      <br/>
      <br/>
      <br/>

      <xsl:for-each select="ead:profiledesc/ead:creation">
        <center>
          <xsl:value-of select="text()"/>
        </center>
        <xsl:for-each select="ead:date">
          <center>
            <xsl:value-of select="text()"/>
          </center>
          <br/>


        </xsl:for-each>
      </xsl:for-each>
    </xsl:for-each>


  </xsl:template>


  <!-- The following templates format the display of various RENDER attributes.-->

  <xsl:template match="*/ead:title">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*/ead:emph">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*/ead:container">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*[@altrender='reveal']">
    <xsl:value-of select="."/>
  </xsl:template>

  <xsl:template match="*[@render='bold']">
    <b>
      <xsl:value-of select="."/>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='italic']">
    <i>
      <xsl:value-of select="."/>
    </i>
  </xsl:template>

  <xsl:template match="*[@render='underline']">
    <u>
      <xsl:value-of select="."/>
    </u>
  </xsl:template>

  <xsl:template match="*[@render='sub']">
    <sub>
      <xsl:value-of select="."/>
    </sub>
  </xsl:template>

  <xsl:template match="*[@render='super']">
    <super>
      <xsl:value-of select="."/>
    </super>
  </xsl:template>

  <xsl:template match="*[@render='doublequote']">
    <xsl:text>"</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>"</xsl:text>
  </xsl:template>

  <xsl:template match="*[@render='singlequote']">
    <xsl:text>'</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>'</xsl:text>
  </xsl:template>

  <xsl:template match="*[@render='doubleboldquote']">
    <b>
      <xsl:text>"</xsl:text>
      <xsl:value-of select="."/>
      <xsl:text>"</xsl:text>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldsinglequote']">
    <b>
      <xsl:text>'</xsl:text>
      <xsl:value-of select="."/>
      <xsl:text>'</xsl:text>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldunderline']">
    <b>
      <u>
        <xsl:value-of select="."/>
      </u>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='bolditalic']">
    <b>
      <i>
        <xsl:value-of select="."/>
      </i>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldsmcaps']">
    <font style="font-variant: small-caps">
      <b>
        <xsl:value-of select="."/>
      </b>
    </font>
  </xsl:template>

  <xsl:template match="*[@render='smcaps']">
    <font style="font-variant: small-caps">
      <xsl:value-of select="."/>
    </font>
  </xsl:template>

  <!-- This template converts an "archref" element into an HTML anchor.-->

  <xsl:template match="*/ead:archref[@xlink:show='replace']">
				<a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:archref[@xlink:show='new']">
				<a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <!-- This template converts an "bibref" element into an HTML anchor.-->

  <xsl:template match="*/ead:bibref[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:bibref[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <!-- This template converts an "extptr" element into an HTML anchor.-->

  <xsl:template match="*/ead:extptr[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:extptr[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <!-- This template converts a "dao" element into an HTML anchor.-->
  <!-- <dao linktype="simple" href="http://www.lib.utexas.edu/benson/rg/atitlan.jpg" actuate="onrequest" show="new"/> -->

  <xsl:template match="*/ead:dao[@xlink:show='replace']">
    <xsl:choose>
      <xsl:when test="@xlink:title">
        <img src="{@xlink:href}" alt="{@xlink:title}"/>
      </xsl:when>
      <xsl:otherwise>
        <img src="{@xlink:href}"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="*/ead:dao[@xlink:show='new']">
    <xsl:choose>
      <xsl:when test="@xlink:title">
        <a href="{@xlink:href}" target="_blank">
          <xsl:value-of select="@xlink:title"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <a href="{@xlink:href}" target="_blank">
          <xsl:value-of select="@xlink:href"/>
        </a>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- This template converts an "extref" element into an HTML anchor.-->

  <xsl:template match="*/ead:extref[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:extref[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>
  <!--This template rule formats a list element.-->
  <xsl:template match="*/ead:list">
    <xsl:for-each select="ead:head">
      <xsl:apply-templates select="."/>
    </xsl:for-each>
    <xsl:for-each select="ead:item">
      <p style="margin-left: 60pt">
        <xsl:apply-templates/>
      </p>
    </xsl:for-each>
  </xsl:template>

  <!--Formats a simple table. The width of each column is defined by the colwidth attribute in a colspec element. Note we set our table width to 90 percent.-->
  <xsl:template match="*/ead:table">
    <xsl:for-each select="ead:tgroup">
      <table width="20%">
        <tr>
					<xsl:for-each select="ead:colspec">
            <td width="{@colwidth}"/>
          </xsl:for-each>
        </tr>
				<xsl:for-each select="ead:thead">
					<xsl:for-each select="ead:row">
            <tr>
              <xsl:for-each select="ead:entry">
                <td valign="top">
                  <b>
                    <xsl:value-of select="."/>
                  </b>
                </td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each select="ead:tbody">
          <xsl:for-each select="ead:row">
            <tr>
              <xsl:for-each select="ead:entry">
                <td valign="top">
                  <xsl:value-of select="."/>
                </td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </xsl:for-each>
      </table>
    </xsl:for-each>
  </xsl:template>



  <!--This template rule formats the top-level did element.-->
  <xsl:template name="archdesc-did">
    <xsl:variable name="file">
      <xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <!--For each element of the did, this template inserts the value of the LABEL attribute or, if none is present, a default value.-->

    <xsl:for-each select="ead:ead/ead:archdesc/ead:did">
      <table width="100%">
        <tr>
          <td width="5%"> </td>
          <td width="25%"> </td>
          <td width="70%"> </td>
        </tr>
        <tr>
          <td colspan="3">
            <h3>
              <xsl:apply-templates select="ead:head"/>
            </h3>
          </td>
        </tr>

        <xsl:if test="ead:origination[string-length(text()|*)!=0]">
          <xsl:for-each select="ead:origination">
            <xsl:choose>
              <xsl:when test="@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="@label"/>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:when>
              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:text>Creator: </xsl:text>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>
        </xsl:if>

        <!-- Tests for and processes various permutations of unittitle and unitdate.-->
        <xsl:for-each select="ead:unittitle">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="text() |* [not(self::ead:unitdate)]"/>
                </td>
              </tr>
            </xsl:when>
            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Title: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="text() |* [not(self::ead:unitdate)]"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>

          <xsl:if test="child::ead:unitdate">
            <xsl:choose>
              <xsl:when test="./ead:unitdate/@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="./ead:unitdate/@label"/>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="./ead:unitdate"/>
                  </td>
                </tr>
              </xsl:when>
              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:text>Dates: </xsl:text>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="./ead:unitdate"/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:if>
        </xsl:for-each>

        <!-- Processes the unit date if it is not a child of unit title but a child of did, the current context.-->
        <xsl:if test="ead:unitdate">
          <tr>
            <td/>
            <xsl:for-each select="ead:unitdate[@type='inclusive']">
              <xsl:choose>
                <xsl:when test="position()=1">
                  <td valign="top">
                    <strong>
                      <xsl:text>Dates: </xsl:text>
                    </strong>
                  </td>
                  <xsl:text disable-output-escaping="yes">&#60;td valign="top"&#62;</xsl:text>
                  <xsl:apply-templates/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates/>
                </xsl:otherwise>
              </xsl:choose>

            </xsl:for-each>
            <xsl:text disable-output-escaping="yes">&#60;/td&#62;</xsl:text>
          </tr>
          <tr>
            <td/>
            <xsl:for-each select="ead:unitdate[@type='bulk']">
              <xsl:choose>
                <xsl:when test="position()=1">
                  <td valign="top">
                    <strong>
                      <xsl:text>Dates (Bulk): </xsl:text>
                    </strong>
                  </td>
                  <xsl:text disable-output-escaping="yes">&#60;td valign="top"&#62;</xsl:text>
                  <xsl:apply-templates/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates/>
                </xsl:otherwise>
              </xsl:choose>

            </xsl:for-each>
            <xsl:text disable-output-escaping="yes">&#60;/td&#62;</xsl:text>
          </tr>

        </xsl:if>

        <xsl:if test="ead:abstract[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:abstract"/>
                </td>
              </tr>
            </xsl:when>
            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Abstract: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:abstract"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:physdesc[string-length(text()|*)!=0]">
		<xsl:for-each select="ead:physdesc">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Quantity: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
		  </xsl:for-each>
        </xsl:if>


        <xsl:if test="ead:unitid[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:unitid"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>TSLAC Control No.: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:unitid"/>

                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>

        <xsl:if test="ead:physloc[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:physloc"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Location: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:physloc"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:langmaterial[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:langmaterial"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Language: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:langmaterial"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:repository[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:repository"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Repository: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:repository"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:note[string-length(text()|*)!=0]">
          <xsl:for-each select="ead:note">
            <xsl:choose>
              <xsl:when test="@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="@label"/>
                    </b>
                  </td>
                </tr>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td> </td>
                    <td valign="top">
                      <xsl:apply-templates/><xsl:text>&#xa;</xsl:text>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:when>

              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>Location:</b>
                  </td>
                  <td>
                    <xsl:apply-templates select="ead:note"/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>
        </xsl:if>
      </table>
    </xsl:for-each>
  </xsl:template>

  <!--This template rule formats the top-level bioghist element.-->
  <xsl:template name="archdesc-bioghist">
    <xsl:variable name="file">
      <xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <xsl:if test="ead:ead/ead:archdesc/ead:bioghist[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:bioghist">
        <xsl:apply-templates/>
        <hr/>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:head">
    <h3>
      <xsl:apply-templates/>
    </h3>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:p">
    <p style="margin-left: 30pt">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:chronlist">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:bioghist">
    <h3>
      <xsl:apply-templates select="ead:head"/>
    </h3>
    <xsl:for-each select="ead:p">
      <p style="margin-left: 30pt">
        <xsl:apply-templates select="."/>
      </p>
    </xsl:for-each>
  </xsl:template>

  <!--This template rule formats a chronlist element.-->
  <xsl:template match="*/ead:chronlist">
    <table width="100%">
      <tr>
        <td width="5%"> </td>
        <td width="30%"> </td>
        <td width="65%"> </td>
      </tr>

      <xsl:for-each select="ead:listhead">
        <tr>
          <td>
            <b>
              <xsl:apply-templates select="ead:head01"/>
            </b>
          </td>
          <td>
            <b>
              <xsl:apply-templates select="ead:head02"/>
            </b>
          </td>
        </tr>
      </xsl:for-each>

      <xsl:for-each select="ead:chronitem">
        <tr>
          <td/>
          <td valign="top">
            <xsl:apply-templates select="ead:date"/>
          </td>
          <td valign="top">
            <xsl:apply-templates select="ead:event"/>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>



  <!--This template rule formats the scopecontent element.-->
  <xsl:template name="archdesc-scopecontent">
    <xsl:if test="ead:ead/ead:archdesc/ead:scopecontent[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:scopecontent">
        <xsl:apply-templates/>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:head">
    <h3>
      <xsl:apply-templates/>
    </h3>
  </xsl:template>

  <!-- This formats an organization list embedded in a scope content statement.-->
  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:organization">
    <xsl:for-each select="ead:p">
      <p style="margin-left: 30pt">
        <xsl:apply-templates select="."/>
      </p>
    </xsl:for-each>
    <xsl:for-each select="ead:list">
      <xsl:for-each select="ead:item">
        <p style="margin-left: 60pt">
          <xsl:value-of select="."/>
        </p>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:p">
    <p style="margin-left: 30pt">
      <xsl:apply-templates/>
    </p>
  </xsl:template>



  <!--This template rule formats the arrangement element.-->
  <xsl:template name="archdesc-arrangement">
    <xsl:if test="ead:ead/ead:archdesc/ead:arrangement[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:arrangement">
        <table width="100%">
          <tr>
            <td width="5%"/>
            <td width="5%"/>
            <td width="90%"/>
          </tr>

          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>

          <tr>
            <td/>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>

          <xsl:for-each select="ead:list">
            <tr>
              <td/>
              <td colspan="2">
                <xsl:apply-templates select="ead:head"/>
              </td>
            </tr>
            <xsl:for-each select="ead:item">
              <tr>
                <td/>
                <td/>
                <td colspan="1">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>

        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level relatedmaterial element.-->
  <xsl:template name="archdesc-relatedmaterial">
    <xsl:if
      test="ead:ead/ead:archdesc/ead:relatedmaterial[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:separatedmaterial[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:relatedmaterial | ead:ead/ead:archdesc/ead:separatedmaterial">
        <table width="100%">
          <tr>
            <td width="5%"> </td>
            <td width="5%"> </td>
            <td width="90%"> </td>
          </tr>

          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>

          <tr>
            <td/>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>

          <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
            <tr>
              <td> </td>
              <td colspan="2">
                <b>
                  <xsl:apply-templates select="ead:p"/>
                </b>
              </td>
            </tr>

            <xsl:for-each select="ead:note ">
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>

            <xsl:for-each select="ead:archref | ead:bibref ">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level otherfindaid element.-->
  <xsl:template name="archdesc-otherfindaid">
    <xsl:if test="ead:ead/ead:archdesc/ead:otherfindaid[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:otherfindaid">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="archdesc-control">
    <xsl:if test="ead:ead/ead:archdesc/ead:controlaccess[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:controlaccess">
        <table width="100%">
          <tr>
            <td width="5%"> </td>
            <td width="5%"> </td>
            <td width="90%"> </td>
          </tr>
          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>
          <tr>
            <td> </td>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>
          <xsl:for-each select="./ead:controlaccess">
            <tr>
              <td> </td>
              <td colspan="2">
                <b>
                  <xsl:apply-templates select="ead:head"/>
                </b>
              </td>
            </tr>
            <xsl:for-each
              select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats a top-level access/use/phystech retrict element.-->
  <xsl:template name="archdesc-restrict">
    <xsl:if
      test="ead:ead/ead:archdesc/ead:accessrestrict[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:userestrict[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:phystech[string-length(text()|*)!=0]">
      <h3>
        <b>
          <xsl:text>Restrictions and Requirements</xsl:text>
        </b>
      </h3>
      <xsl:for-each
        select="ead:ead/ead:archdesc/ead:accessrestrict | ead:ead/ead:archdesc/ead:userestrict | ead:ead/ead:archdesc/ead:phystech">
        <h4 style="margin-left : 15pt">
          <b>
            <xsl:value-of select="ead:head"/>
          </b>
        </h4>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level index element.-->
  <xsl:template name="archdesc-index">
    <xsl:if test="ead:ead/ead:archdesc/ead:index[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:index">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
        <xsl:for-each select="ead:indexentry">
          <p style="margin-left: 60pt">
            <xsl:value-of select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <!--This template rule formats the top-level bibliography element.-->
  <xsl:template name="archdesc-bibliography">
    <xsl:if test="ead:ead/ead:archdesc/ead:bibliography[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:bibliography">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <xsl:for-each select="ead:bibref">
            <p style="margin-left : 30pt">
              <xsl:apply-templates select="."/>
            </p>
          </xsl:for-each>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level odd element.-->
  <xsl:template name="archdesc-odd">
    <xsl:if test="ead:ead/ead:archdesc/ead:odd[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:odd">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


	<xsl:template name="archdesc-admininfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:accruals[string-length(text()|*)!=0]">
			<h3>
				<a name="adminlink">
					<xsl:text>Administrative Information</xsl:text>
				</a>
			</h3>
			<xsl:call-template name="archdesc-custodhist"/>
			<xsl:call-template name="archdesc-prefercite"/>
			<xsl:call-template name="archdesc-acqinfo"/>
			<xsl:call-template name="archdesc-processinfo"/>
			<xsl:call-template name="archdesc-appraisal"/>
			<xsl:call-template name="archdesc-accruals"/>
			<xsl:call-template name="archdesc-altform"/>
			<xsl:call-template name="archdesc-originalsloc"/>
			<hr/>
		</xsl:if>
	</xsl:template>


	<!--This template rule formats a top-level custodhist element.-->
	<xsl:template name="archdesc-custodhist">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist | ead:ead/ead:archdesc/ead:custodhist | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level altformavail element.-->
	<xsl:template name="archdesc-altform">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail | ead:ead/ead:archdesc/ead:altformavail | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level originalsloc element.-->
	<xsl:template name="archdesc-originalsloc">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc | ead:ead/ead:archdes/ead:coriginalsloc | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level prefercite element.-->
	<xsl:template name="archdesc-prefercite">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite | ead:ead/ead:archdesc/ead:prefercite | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level acqinfo element.-->
	<xsl:template name="archdesc-acqinfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo | ead:ead/ead:archdesc/ead:acqinfo | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level procinfo element.-->
	<xsl:template name="archdesc-processinfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo | ead:ead/ead:archdesc/ead:processinfo | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level appraisal element.-->
	<xsl:template name="archdesc-appraisal">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal | ead:ead/ead:archdesc/ead:appraisal | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level accruals element.-->
	<xsl:template name="archdesc-accruals">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:accruals[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals | ead:ead/ead:archdesc/ead:accruals | ead:ead/ead:archdesc/ead:descgrp/ead:accruals">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in25">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>

  <xsl:template name="dsc">
    <xsl:if test="ead:ead/ead:archdesc/ead:dsc">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:dsc">
        <xsl:call-template name="dsc-analytic"/>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <xsl:template name="dsc-analytic">
    <h2>
      <xsl:choose>
        <xsl:when test="child::ead:head">
          <xsl:value-of select="ead:head"/>
        </xsl:when>
      </xsl:choose>
    </h2>

    <p style="margin-left: 25 pt">
      <i>
        <xsl:apply-templates select="ead:p"/>
      </i>
    </p>

    <!--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx-->
    <!-- Process each c01.-->
    <xsl:for-each select="ead:c01">

      <table width="100%">
        <tr>
          <td width="15%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
        </tr>

        <xsl:for-each select="ead:did">
          <tr>
            <td colspan="14">
              <h3>
                <xsl:call-template name="component-did"/>
              </h3>
            </td>
          </tr>

          <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
            <xsl:for-each select="ead:abstract | ead:note">
              <tr>
                <td/>
                <td colspan="13" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:if>
        </xsl:for-each>


        <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:p">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:list/ead:item">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each select="ead:dao">
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="."/>
            </td>
          </tr>
        </xsl:for-each>


        <xsl:for-each select="ead:controlaccess">

          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>
          <xsl:for-each select="./ead:controlaccess">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <b>
                  <xsl:apply-templates select="ead:head"/>
                </b>
              </td>
            </tr>
            <xsl:for-each
              select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">

          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>

          <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="ead:note ">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:archref | ead:bibref">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each
          select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:p">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:archref | ead:bibref | ead:extref">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>            
          </xsl:for-each>
        </xsl:for-each>

        <!-- Proceses each c02.-->
        <xsl:for-each select="ead:c02">
          <xsl:for-each select="ead:did">


            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c02-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c02-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c02-box-only"/>
              </xsl:otherwise>
            </xsl:choose>



          </xsl:for-each>

          <!-- Process any remaining c02 elements of the type specified.-->

          <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:p">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:list/ead:item">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>

          <xsl:for-each select="ead:dao">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>

          <xsl:for-each select="ead:controlaccess">

            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="./ead:controlaccess">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <b>
                    <xsl:apply-templates select="ead:head"/>
                  </b>
                </td>
              </tr>
              <xsl:for-each
                select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                <xsl:sort select="."/>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>


          <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="ead:note ">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:archref | ead:bibref">
                <xsl:sort select="."/>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>


          <xsl:for-each
            select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:p">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>


          <!-- Processes each c03.-->
          <xsl:for-each select="ead:c03">
            <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c03-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c03-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c03-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

            </xsl:for-each>

            <!-- Process any remaining c03 elements of the type specified.-->

            <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:p">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:list/ead:item">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>

            <xsl:for-each select="ead:dao">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>

            <xsl:for-each select="ead:controlaccess">

              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="./ead:controlaccess">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <b>
                      <xsl:apply-templates select="ead:head"/>
                    </b>
                  </td>
                </tr>
                <xsl:for-each
                  select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                  <xsl:sort select="."/>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>


            <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="ead:note ">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>

                <xsl:for-each select="ead:archref | ead:bibref">
                  <xsl:sort select="."/>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>


            <xsl:for-each
              select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:p">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>


            <!-- Processes each c04.-->
            <xsl:for-each select="ead:c04">
              <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c04-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c04-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c04-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

              </xsl:for-each>

              <!-- Process any remaining c04 elements of the type specified.-->

              <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:list/ead:item">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>

              <xsl:for-each select="ead:dao">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:controlaccess">

                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="./ead:controlaccess">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <b>
                        <xsl:apply-templates select="ead:head"/>
                      </b>
                    </td>
                  </tr>
                  <xsl:for-each
                    select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                    <xsl:sort select="."/>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>


              <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>
                  <xsl:for-each select="ead:note ">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:archref | ead:bibref">
                    <xsl:sort select="."/>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>


              <xsl:for-each
                select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>


              <!-- Processes each c05-->
              <xsl:for-each select="ead:c05">
                <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c05-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c05-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c05-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                </xsl:for-each>

                <!-- Process any remaining c05 elements of the type specified.-->


                <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:p">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:list/ead:item">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>

                <xsl:for-each select="ead:dao">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>

                <xsl:for-each select="ead:controlaccess">

                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>

                  <xsl:for-each select="./ead:controlaccess">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <b>
                          <xsl:apply-templates select="ead:head"/>
                        </b>
                      </td>
                    </tr>
                    <xsl:for-each
                      select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                      <xsl:sort select="."/>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>


                <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>

                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>
                  <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>
                    <xsl:for-each select="ead:note ">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:archref | ead:bibref">
                      <xsl:sort select="."/>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>


                <xsl:for-each
                  select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:p">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>


                <!-- Processes each c06-->
                <xsl:for-each select="ead:c06">
                  <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c06-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c06-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c06-box-only"/>
              </xsl:otherwise>
            </xsl:choose>


                  </xsl:for-each>

                  <!-- Process any remaining c06 elements of the type specified.-->

                  <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:p">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:list/ead:item">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>

                  <xsl:for-each select="ead:dao">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>

                  <xsl:for-each select="ead:controlaccess">

                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>

                    <xsl:for-each select="./ead:controlaccess">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <b>
                            <xsl:apply-templates select="ead:head"/>
                          </b>
                        </td>
                      </tr>

                      <xsl:for-each
                        select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                        <xsl:sort select="."/>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>
                  </xsl:for-each>


                  <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>
                    <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="ead:note ">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:archref | ead:bibref">
                        <xsl:sort select="."/>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>
                  </xsl:for-each>


                  <xsl:for-each
                    select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:p">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>


                  <!-- Processes each c07.-->
                  <xsl:for-each select="ead:c07">
                    <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c07-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c07-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c07-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                    </xsl:for-each>

                    <!-- Process any remaining c07 elements of the type specified.-->

                    <xsl:for-each select=" ead:scopecontent | ead:bioghist | ead:arrangement">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:p">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:list/ead:item">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>

                    <xsl:for-each select="ead:dao">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>

                    <xsl:for-each select="ead:controlaccess">

                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="./ead:controlaccess">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <b>
                              <xsl:apply-templates select="ead:head"/>
                            </b>
                          </td>
                        </tr>
                        <xsl:for-each
                          select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                          <xsl:sort select="."/>
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>
                    </xsl:for-each>


                    <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="ead:note ">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:archref | ead:bibref">
                          <xsl:sort select="."/>
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>
                    </xsl:for-each>


                    <xsl:for-each
                      select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:p">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>


                    <!-- Processes each c08.-->
                    <xsl:for-each select="ead:c08">
                      <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c08-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c08-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c08-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                      </xsl:for-each>

                      <!-- Process any remaining c08 elements of the type specified.-->

                      <xsl:for-each select=" ead:scopecontent | ead:bioghist | ead:arrangement">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:p">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:list/ead:item">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>

                      <xsl:for-each select="ead:dao">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>

                      <xsl:for-each select="ead:controlaccess">

                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="./ead:controlaccess">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="5" valign="top">
                              <b>
                                <xsl:apply-templates select="ead:head"/>
                              </b>
                            </td>
                          </tr>
                          <xsl:for-each
                            select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                            <xsl:sort select="."/>
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:for-each>


                      <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="5" valign="top">
                              <xsl:apply-templates select="ead:p"/>
                            </td>
                          </tr>
                          <xsl:for-each select="ead:note ">
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                          <xsl:for-each select="ead:archref | ead:bibref">
                            <xsl:sort select="."/>
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:for-each>


                      <xsl:for-each
                        select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:p">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>


                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>
      </table>
      <hr/>
      <br/>
      <br/>

    </xsl:for-each>

  </xsl:template>


  <!-- Shows the container numbers for a c02.-->
  <xsl:template name="showbox-c02-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td colspan="10" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td colspan="9" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c02.-->
  <xsl:template name="hidebox-c02-box-only">
    <tr>
      <td> </td>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td colspan="10" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td colspan="9" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c03.-->
  <xsl:template name="showbox-c03-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="0" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td colspan="9" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td colspan="8" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c03.-->
  <xsl:template name="hidebox-c03-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="0" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td colspan="9" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td colspan="8" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the container number for a c04.-->
  <xsl:template name="showbox-c04-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td colspan="8" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="7" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c04.-->
  <xsl:template name="hidebox-c04-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td colspan="8" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="7" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c05.-->
  <xsl:template name="showbox-c05-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td colspan="7" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="6" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c05.-->
  <xsl:template name="hidebox-c05-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td colspan="7" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="6" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the container number for a c06.-->
  <xsl:template name="showbox-c06-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="6" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="5" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c06.-->
  <xsl:template name="hidebox-c06-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="6" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="5" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c07.-->
  <xsl:template name="showbox-c07-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="5" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="4" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c07.-->
  <xsl:template name="hidebox-c07-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="5" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="4" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c08.-->
  <xsl:template name="showbox-c08-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="4" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="3" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c08.-->
  <xsl:template name="hidebox-c08-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="4" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="3" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Displays unittitle and date information for a component level did.-->
  <xsl:template name="component-did">
    <xsl:if test="ead:unitid">
      <xsl:for-each select="ead:unitid">
        <xsl:apply-templates/>
        <xsl:text>: </xsl:text>
      </xsl:for-each>
    </xsl:if>

    <xsl:choose>
      <xsl:when test="ead:unittitle/ead:unitdate">
        <xsl:for-each select="ead:unittitle">
          <xsl:apply-templates select="text()|*[not(self::ead:unitdate)]"/>
          <xsl:text> </xsl:text>
          <xsl:apply-templates select="./ead:unitdate"/>
        </xsl:for-each>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="ead:unittitle"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="ead:unitdate"/>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:for-each select="ead:dao">
      <xsl:apply-templates select="."/>
    </xsl:for-each>

    <xsl:for-each select="ead:physdesc">
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
      <xsl:text> </xsl:text>
    </xsl:for-each>
    <xsl:for-each select="ead:materialspec">
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
      <xsl:text> </xsl:text>
    </xsl:for-each>
  </xsl:template>


</xsl:stylesheet>

''')

my_input_file = "C:/Users/bthomas/Downloads/TX005697_20251217_190413_UTC__ead.xml" #input("Enter the name of the file: ")
my_output_file = "C:/Users/bthomas/Downloads/output.xml" #input("Enter the name of the output file: ")

nsmap = {'xmlns': 'urn:isbn:1-931666-22-9',
         'ead': 'urn:isbn:1-931666-22-9',
         'xlink': 'http://www.w3.org/1999/xlink'}

dom = ET.parse(my_input_file)
root = dom.getroot()

ead = root.xpath("//ead:ead", namespaces=nsmap)
for item in ead:
    item.attrib['relatedencoding'] = "MARC21"
eadhead = root.find(".//ead:eadheader", namespaces=nsmap)
eadhead.attrib['scriptencoding'] = "iso15924"
identifiers = ET.iterwalk(root, events=("start", "end"))
for action, elem in identifiers:
    if "id" in elem.attrib.keys():
        elem.attrib.pop("id")
pub_stmt = root.find(".//ead:publicationstmt", namespaces=nsmap)
pub_date = root.find(".//ead:publicationstmt/ead:p/ead:date", namespaces=nsmap)
pub_date2 = ET.SubElement(pub_stmt, "date")
pub_date2.text = pub_date.text
date_container = pub_date.getparent()
date_container.getparent().remove(date_container)
pub_stmt = root.xpath(".//ead:publicationstmt/ead:publisher", namespaces=nsmap)
for item in pub_stmt:
    item.text = "Texas State Library and Archives Commission"
    extptr = ET.SubElement(item, "extptr")
    extptr.attrib['xlink_actuate'] = "onLoad"
    extptr.attrib['xlink_href'] = "https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg"
    extptr.attrib['xlink_show'] = "embed"
    extptr.attrib['xlink_type'] = "simple"
    extptr.attrib['xmlns_xlink'] = "http://www.w3.org/1999/xlink"
address = root.xpath(".//ead:publicationstmt/ead:address", namespaces=nsmap)
paragraph = root.xpath(".//ead:publicationstmt/ead:p", namespaces=nsmap)
if paragraph is not None:
    for item in paragraph:
        item.getparent().remove(item)
if address is not None:
    for addres in address:
        parental = addres.getparent()
        parental.remove(addres)
revisions = root.xpath(".//ead:revisiondesc/ead:change", namespaces=nsmap)
if revisions is not None:
    test_date = 0
    for revision in revisions:
        var1 = revision.find("./ead:item", namespaces=nsmap).text
        var1 = var1.replace("R", "r")
        var2 = revision.find("./ead:date", namespaces=nsmap).text
        var2_date = int(var2.split(" ")[0])
        if var2_date > test_date:
            test_date = var2_date
            constructed = f", most recently {var1} {var2}"
    authorial = root.find(".//ead:author", namespaces=nsmap)
    authorial.text = f"{authorial.text}{constructed}"
creation_date = root.find(".//ead:profiledesc/ead:creation/ead:date", namespaces=nsmap)
creation_date.text = creation_date.text[:10]
archdesc = root.find(".//ead:archdesc", namespaces=nsmap)
archdesc.attrib['type'] = "inventory"
archdesc.attrib['audience'] = "external"
main_did = root.find(".//ead:archdesc/ead:did/ead:head", namespaces=nsmap)
main_did.text = "Overview"
repository = root.find(".//ead:archdesc/ead:did/ead:repository/ead:corpname", namespaces=nsmap)
repository_text = repository.text
repo_extref = root.find(".//ead:archdesc/ead:did/ead:repository/ead:extref", namespaces=nsmap)

repo_extref.text = repository_text
repository.getparent().remove(repository)
top_title = root.find(".//ead:archdesc/ead:did/ead:unittitle", namespaces=nsmap)
top_title.attrib['label'] = "Title:"
originator = root.xpath(".//ead:origination", namespaces=nsmap)
if originator is not None:
    for item in originator:
        if "label" not in item.attrib.keys():
            item.attrib['label'] = "Creator:"
        else:
            if not item.attrib['label'].endswith(":"):
                item.attrib['label'] = f'{item.attrib["label"]}:'
head_id = root.find("ead:archdesc/ead:did/ead:unitid", namespaces=nsmap)
head_id.attrib['label'] = "TSLAC Control No.:"
langmaterial = root.xpath(".//ead:langmaterial", namespaces=nsmap)
if langmaterial is not None:
    langmaterial[0].attrib['label'] = "Language:"
    if len(langmaterial) > 1:
        while len(langmaterial) > 1:
            langmaterial[-1].getparent().remove(langmaterial[-1])
            langmaterial = root.xpath(".//ead:langmaterial", namespaces=nsmap)
top_physdesc = root.xpath(".//ead:archdesc/ead:did/ead:physdesc", namespaces=nsmap)
if top_physdesc is not None:
    for item in top_physdesc:
        item.attrib['label'] = "Quantity:"
    if len(top_physdesc) > 1:
        for physdesc in top_physdesc[1:]:
            if physdesc.attrib['altrender'] == "part":
                extent = physdesc.find("./ead:extent", namespaces=nsmap)
                extent.text = f"(includes {extent.text})"
top_unitdates = root.xpath(".//ead:archdesc/ead:did/ead:unitdate", namespaces=nsmap)
if top_unitdates is not None:
    for item in top_unitdates:
        item.attrib['label'] = "Dates:"
abstract = root.xpath(".//ead:archdesc/ead:did/ead:abstract", namespaces=nsmap)
if abstract is not None:
    for item in abstract:
        item.attrib['label'] = "Abstract:"
top_location = root.xpath(".//ead:archdesc/ead:did/ead:physloc", namespaces=nsmap)
if top_location is not None:
    for item in top_location:
        item.attrib['label'] = "Location:"
arrangement = root.xpath(".//ead:archdesc/ead:arrangement", namespaces=nsmap)
if arrangement is not None:
    for item in arrangement:
        item.attrib['encodinganalog'] = "351"
processinfo = root.xpath(".//ead:processinfo", namespaces=nsmap)
if processinfo is not None:
    for item in processinfo:
        item.attrib['encodinganalog'] = "583"
appraisal = root.xpath(".//ead:archdesc/ead:appraisal", namespaces=nsmap)
if appraisal is not None:
    for item in appraisal:
        item.attrib['encodinganalog'] = "583"
phystech = root.xpath(".//ead:archdesc/ead:phystech", namespaces=nsmap)
if phystech is not None:
    for item in phystech:
        item.attrib['encodinganalog'] = "340"
controlaccess = root.find(".//ead:archdesc/ead:controlaccess/ead:controlaccess", namespaces=nsmap)
if controlaccess is not None:
    paragraph = ET.SubElement(item, "p")
    emphasis = ET.SubElement(paragraph, "emph")
    emphasis.attrib['render'] = "italic"
    emphasis.text = "The terms listed here were used to catalog the records. The terms can be used to find similar or related records."
    controlaccess.addprevious(paragraph)
subject = root.xpath(".//ead:subject", namespaces=nsmap)
if subject is not None:
    for item in subject:
        if "source" in item.attrib.keys():
            item.attrib['source'] = normalized_source(item.attrib['source'])
corpname = root.xpath(".//ead:corpname", namespaces=nsmap)
if corpname is not None:
    for item in corpname:
        if "source" in item.attrib.keys():
            item.attrib['source'] = normalized_source(item.attrib['source'])
famname = root.xpath(".//ead:famname", namespaces=nsmap)
if famname is not None:
    for item in famname:
        if "source" in item.attrib.keys():
            item.attrib['source'] = normalized_source(item.attrib['source'])
persname = root.xpath(".//ead:persname", namespaces=nsmap)
if persname is not None:
    for item in persname:
        if "source" in item.attrib.keys():
            item.attrib['source'] = normalized_source(item.attrib['source'])
counter = 0
series = root.xpath(".//ead:c01", namespaces=nsmap)
for item in series:
    if item.attrib['level'] == "series":
        counter += 1
        item.attrib['id'] = f"ser{str(counter)}"
box = root.xpath(".//ead:container", namespaces=nsmap)
if box is not None:
    for item in box:
        if "type" in item.attrib.keys():
            if item.attrib['type'] == "box":
                item.attrib['type'] = "Box"
date_normal = root.xpath(".//ead:unitdate", namespaces=nsmap)
for item in date_normal:
    if "normal" in item.attrib.keys():
        normal = item.attrib["normal"]
        if "T" in normal:
            normal = normal.split("/")
            var1 = normal[0].split("T")[0]
            var2 = normal[1].split("T")[0]
            item.attrib['normal'] = f"{var1}/{var2}"
c_tags = ['c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12', 'c13', 'c14', 'c15']
for c in c_tags:
    dids = root.xpath(f".//ead:{c}/ead:did", namespaces=nsmap)
    for did in dids:
        unittitle = did.find("./ead:unittitle", namespaces=nsmap)
        unitdate = did.xpath("./ead:unitdate", namespaces=nsmap)
        physdesc = did.xpath("./ead:physdesc/ead:extent", namespaces=nsmap)
        if unittitle is not None and len(unitdate) > 0 or len(physdesc) > 0:
            uniittitle_text = unittitle.text
            print(uniittitle_text)
            if uniittitle_text is not None:
                if not uniittitle_text.endswith(",") or not unittitle_text.endswith(", "):
                    uniittitle_text += ","
                    unittitle.text = uniittitle_text
        if len(physdesc) > 0:
            if len(unitdate) > 0:
                for date in unitdate:
                    date_text = date.text
                    if not date_text.endswith(",") or not date_text.endswith(", "):
                        date_text += ","
                        date.text = date_text
        if len(physdesc) == 0:
            if len(unitdate) > 1:
                for date in unitdate[1:]:
                    date_text = date.text
                    if not date_text.endswith(",") or not date_text.endswith(", "):
                        date_text += ","
                        date.text = date_text
        if len(physdesc) > 1:
            for phys in physdesc[:-1]:
                phys_text = phys.text
                if not phys_text.endswith(",") or not phys_text.endswith(", "):
                    phys_text += ","
                    phys.text = phys_text
            phys_counter = 0
            for phys in physdesc:
                parental = phys.getparent()
                if "altrender" in parental.attrib.keys():
                    if parental.attrib["altrender"] == "part":
                        phys.text = f"(includes {phys.text})"
                        physdesc[phys_counter].text = physdesc[phys_counter].text[:-1]
                        phys_counter += 1
unitid_list = []
unitid = root.xpath(".//ead:unitid", namespaces=nsmap)
if unitid is not None:
    for item in unitid:
        unit_text = item.text
        if unit_text in unitid_list:
            item.getparent().remove(item)
        else:
            unitid_list.append(unit_text)



ET.indent(dom, space="\t")
with open(my_output_file, "wb") as w:
    w.write(ET.tostring(dom, pretty_print=True))
w.close()

with open(my_output_file, "r") as r:
    filedata = r.read()
    filedata = filedata.replace("xlink_", "xlink:").replace("xmlns_", "xmlns:")
    with open(my_output_file, "w") as w:
        w.write(filedata)
    w.close()

html_file = f"{my_output_file[:-3]}html"
my_html = ET.XSLT(html_transform)
dom = ET.parse(my_output_file)
new_dom = my_html(dom)
new_dom.write(html_file, pretty_print=True)
