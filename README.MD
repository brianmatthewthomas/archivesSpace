# ArchivesSpace tools
Note that these tools *are* specific to the needs of a specific repository so anyone wanting to use them should probably run against a single file and check the output for your needs before proceeding.

Future work may include consolidating common functionality into a module rather than having in separate scripts multiple times. Keep an eye out for that but no promises. 

## Requirements
You will need to install the following modules for this to work properly. Order of installation is not important. These modules may have dependencies as well but if you use pip it should be fine.
* csv
* daterangeparser
* datetime
* errno
* lxml
* re
* shutil

## Explanations for each of the scripts are as follows:

### ArchivesSpace_normalization.py
This is meant to normalize specific fields prior to importing a finding aid into ArchivesSpace. It does not have any embedded stylesheet. 

It will remove trailing commas, periods, and spaces from:
* ead:unittitle
* ead:unitdate

It will also de-nest specific fields which may have been nested previously.
* ead:relatedmaterial
* ead:controlaccess

Note that it will also remove the original container ead:controlaccess and relatedmaterial. Also, the controlaccess and relatedmaterial sections are output as immediate siblings the arrangement so it may not place that section exactly where it came from. This **WILL NOT** affect how data is rendered.

### normalizeDates_tocsv.py
For before ArchivesSpace ead import. This is meant to help with standardizing how dates are phrased in a finding aid. Over time it is common for different naming conventions to be used and different data entry standards to be applied. This tool works by taking the normal attribute of unitdate as the marker for a beginning and ending date. It works as a crawler and will output one spreadsheet per ead file it encounters.

It will output a spreadsheet with the following:
* filename: the name of the file that was processed
* xpath: the address in the file the data was pulled from. Used to push changed data back into the file
* date_original: The text as it exists now
* date_normal: the date normal attribute so you can see where the date is derived from
* date_computer_suggestion: the date derived from normal attribute. This can be configured but defaults to the spelled out month, numeric day including leading zeros and full year. Beginning and end date are separated by " to ". If there are 0000 in the normal attribute it will output Undated.
* date_desired: this will be where you choose which date text to keep. a future script will pair this field back to the actual ead file

Note: This is set to only handle year or year-month-day normal attributes. If the first day of a year is indicated as the start and last day as the end if will output year only. *This is only as good as your data, if there is an error in the normal attribute it will be transcribed.* 

Note: If you start this on a set of files, DO NOT change anything in the file until you are done. The xpath is sensitive to changes in structure and you might disrupt that detail.

### normalizeExtent_fromcsv.py
For before ArchivesSpace import. Takes the spreadsheet generated and people processed from normalizeExtent_tocsv.py and pairs the extent content back into the ead file. This is as a physdesc/extent. If someone was clever and tried to create a new tag within the extent you will get an &amp;lt; and &amp;gt; text you will need to address

### normalizeExtent_fromcsv_special.py
Same as above but with additional modifications for a coworker who didn't want to bother to actually change the spreadsheet like they needed to.

### normalizeExtent_to_csv.py
For before ArchivesSpace ead import. Crawls a directory and reads each ead file and spits out a spreadsheet per file with the address and text of the physdesc/extent field. Preprocesses the file by making sure extents are nested in a physdesc as much as possible. Be wary that if your data is structured weird you might lose it so check the output ead file for everything before throwing out the original.

It will output a spreadsheet with the following without headers:
* filename (for pairing to the correct file)
* xpath, for where to insert the modified data. If you decide to do this process **DO NOT** do anything else with an ead file until you are done as the xpath is very sensitive to structure changes.
* extent text. This is the field to modify

Note that the point here is to know what you have and standardize it before importing into ArchivesSpace and generating a bunch of unnecessary extent controlled value list thing. For example `2 folders` could be standardized to `2 folder` to avoid a duplicative item for the same underlying concept. Any also to catch where people decided to spell out a number so some archaic reason. ArchivesSpace will **only handle numbers** for a extent value.

### normalizeExtent_tocsv_oneCSV.py
For before ArchivesSpace ead import. Same as above but spits out to a single spreadsheet so everything can be done by one person. The fromcsv script pairs based on filename so it should work fine. I *highly* recommend using this over the individual spreadsheets for standardized approach reasons. For either, you can delete a line from the spreadsheet if it is fine. Just don't change the ead file until you are done.

### taro2processor.py
For pre-*TARO 2.0* upload prep. Also for before ArchivesSpace import if applicable but it can handle ArchivesSpace export just fine.

This tool uses a combination of embedded xsl and python processing (including text replacement) to prepare a file either exported from ArchivesSpace or handmade to be uploaded to TARO for its 2.0 iteration.

When invoked, the tool will first transform the data to be mostly TARO 2.0 compliant. 

It expects a spreadsheet with top-level unitids for inserting a control number into the finding aid, with the spreadsheet having the ead filename (without extension) in column 1 and the control number in column 2. If you don't want that comment out (`#` at the beginning of the line) lines 2818-2823 and 2848-2852 and 2874-2878. If you wish to use the function, the file should be named txNumbers.csv and modify the `label`s and `repositorycode`s part of lines 2850-2852.

This tool will do the following:
* nest all of the agents in an ASpace export that are listed as creators into a controlaccess section
* nest all of the separate related material notes  from an ASpace export into a nested relatedmaterial structure
* remove the descgroup encapsulating tags
* normalize subjects by removing trailing/predecing spaces
* insert a date normal in any unitdate if it is missing.
* push a normalized file to an error folder if the output is badly formed xml. This can happen for a few reasons but most often it has to do with nested related material
* push a normalized file to the error folder if a controlaccess term is missing its source attribute or if that attribute is set to local

***Note*** that after a file has been processed it will ask for confirmation that you have checked the ead file for accuracy/completeness before moving on to prevent forgetting what to check on.

***Note*** that the revisiondesc may be affected by the processor so you will need to check it after for possible re-insertion of the data.

***Note*** also that there may be a superfluous "." added in origination for unknown reasons, check that as well.

***Note*** archref has a specific process for modifying the native output without a xlink: prefix to have that prefix in the attributes. worth verifying that the process applied because variance in ***your*** data practices can affect whether it worked.

***Note*** if your containers have 'box' or 'folder', they will be capitalized.

#### ***Note about date normal attribute:*** 
This will most likely the most time consuming part of this tool. If you are missing the type attribute it will insert and only ask for input if it is unclear whether it is a bulk vs. inclusive date. It uses daterangeparser to guess at the date to generate the normal attribute and will prompt for input when it can't figure it out. It will ouput the following:
* The full text of the unitdate tag
* The section it cannot resolve.

You **must** provide the full normal attribute in the `yyyy-mm-dd/yyyy-mm-dd format`. If it is undated you can use `0000`. 

***Note***: dates are broken into lists if they cannot be parsed on their own based on the typical case where someone entered a proper year and then comma and then another proper year. This was the most common case during development. However, it will result in the following: `Aug 20, 21, 25 1998` being interpreted as `2021-08-20/2021-08-20`, prompt for input on what `21` and `25` means, and `1998-01-01/1998-12-31`. That is then usually split into largest and smallest to `1998-01-01/2021-08-20` or something like that. Yes, this was preferrable to the alternative options. You made the human readable (debatable) but not machine processable data so you will have to fix it.

Depending on the source data the output might be a bit scrambled, so after the file is normalized you should search using a text editor for `0000` to check that it wasn't put in the wrong place and for the current year (such as `2021`) which is what it defaults to if it can't parse the date range properly. Sometimes it has trouble with leap days. If it runs across trouble it may also default to the same beginning/ending date even if incorrect. **Always** check the date normal attributes you had to input as those are the most likely places where the error will show up. So keep notes or checkback on the terminal output to see where that happened. 

FY is interpretted as state of Texas fiscal year of Sept previous year number-Aug listed year number.

Some dates that have to get extra reconfiguration for daterangeparser to work will be printed on screen to show what was done.

### taro2processor-generic.py ###
A genericized version of the `taro2processor.py` for other archives that want to go through roughly the same process. Users will need to know their repo code. Experimental and may not work perfect so check your output.
### fix_low-level_unitid.py
Resolves an issue where TARO2 normalization had inserted the wrong attributes to lower level unitids.
### marcXML_subjects.py
Takes a dump of subject terms from SIRSI via MarcEdit API connection and removes 650/651 items. Used before mass importing Marc encoded subject terms.
### parseExtent.py
Used for normalizing errant extent types pre-import into ArchivesSpace.
# ArchiveSnake tools
These are scripts that rely on archivesnake to do API tasks. You will need to have that installed and configured to log into your system. 
## asnake_fixExtent.py
Uses a dictionary method to normalize errant extent types. The correct extent type is the dictionary key, the errant type is a text item in a list associated with the key. Crawls all repositories based on repo number.       This needs to be localized.
## asnake_fixSubjects.py
Meant to correct a problem where some LCSH subject terms were imported as `Library of Congress Subject Headings` rather than `lcsh`. Crawls entire system.
## asnake_microfilm.py
Meant to crawl repo #2  for instances where there are multiple top containers for an item, one physical item and one microfilm. Finds the microfilm container or creates a new top-container for the microfilm if that doesn't exist, makes the item pairing, removes the data for the microfilm from the original container.
Note that it has to wait for 30 seconds for a newly created container to register in the system so it can take a while. Has a feature to pick up where it left off built in so multiple full passes aren't necessary if you've added stuff and need to rerun.
## asnake_retype_top_container.py
A testing tool to change a top container type from one to another. Configured for changing "Reel" to microfilm but can be applicable to anything.
## container_test.py
The output of a container creation test, provides information on how container data is structured.
## generate_locations_csv.py
Crawls system for all generated locations and creates spreadsheet with the data points. Meant for future pairing of containers created as part of Aspace import to their correct stacks coordinates.
## topContainer_create.py
A testing tool to make sure it is possible to create top containers via the API
## topContainer_bulkGenerate.py
An API tool to take       a csv with container names and bulk generate those containers. Spreadsheet also hase informattttion parameters to link into a specific collection/accession, assign a container profile, and assign a location via the location UUID. Has a pause of 30 seconds after bulk create before trying any pairing to try to get the containers registered in the system.

***Note***: There is a known irresolvable issue where the containers do not always take in the system, or do take but there is a delay in getting recognized by the index. You may need to run, curate to what didn't get created, rerun, etc. ***and then*** check for dedupe needs.
