from tqdm import tqdm
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD

today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='H:/extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="H:/aris.log", filemode="a")

client = ASnakeClient()
def row_converter(row, columns):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in columns:
        pictionary[item] = str(row[count])
        count += 1
    return pictionary

def extent_changer(resource_records, repo_number, type, extent_dict):
    found_records = set([])
    address = f"repositories/{repo_number}/{type}/" + "{0}"
    for record in tqdm(resource_records):
        record_uri = address.format(record)
        res_record = client.get(record_uri).json()
        updated_record = deepcopy(res_record)
        try:
            extents = res_record['extents']
            for ext_index, extent in enumerate(extents):
                #print(res_record)
                if extent['extent_type'] in extent_dict.keys():
                    updated_record['extents'][ext_index]['extent_type'] = extent_dict[extent['extent_type']]
                    with open("H:/log2.csv", "a") as w:
                        w.write(f"{res_record['title']}|{res_record['uri']}|{extent['extent_type']}\n")
                    w.close()
            if res_record['extents'] != updated_record['extents']:
                response = client.post(record_uri, json=updated_record)
                if response.status_code == 200:
                    print(f"extent changed for {res_record['title']}")
                    logger.info('Extent change successfully ppushed', rec=record, response=response)
                    found_records.add(record)
                else:
                    logger.info("Extent change failed", rec=record, response=response)
            else:
                pass
        except:
            pass
    print('{0} records checked; {1} records updated'.format(len(resource_records), len(found_records)))


print("adapter from work by Scott Carlson with his work at Rice")
#cvl = input("full path to excel spreadsheet with data: ")
cvl = "F:/Archives/Collections_management/ArchivesSpace/Administration/controlled value list normalization.xlsx"
df = PD.read_excel(cvl, dtype=object, sheet_name="extent_type")
columns = df.columns
df.fillna("None", inplace=True)
print(df)
extent_dict = {}
for row in df.itertuples():
    pictionary = row_converter(row, columns)
    if pictionary['Correct value'] != "None":
        extent_dict[pictionary['Value']] = pictionary['Correct value']
print("list of values to correct compiled")
print(extent_dict)

resource_records = (client.get('repositories/13/resources', params={'all_ids': True})).json()
print("\nchecking resources in legislative")
extent_changer(resource_records, repo_number="13", type="resources", extent_dict=extent_dict)
archival_objects = (client.get("repositories/13/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in legislative')
extent_changer(archival_objects, repo_number="13", type="archival_objects", extent_dict=extent_dict)
accessions = (client.get("repositories/13/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in legislative')
extent_changer(accessions, repo_number="13", type="accessions", extent_dict=extent_dict)
resource_records = (client.get('repositories/12/resources', params={'all_ids': True})).json()
print("\nchecking resources in review")
extent_changer(resource_records, repo_number="12", type="resources", extent_dict=extent_dict)
archival_objects = (client.get("repositories/12/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in review')
extent_changer(archival_objects, repo_number="12", type="archival_objects", extent_dict=extent_dict)
accessions = (client.get("repositories/12/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in review')
extent_changer(accessions, repo_number="12", type="accessions", extent_dict=extent_dict)
resource_records = (client.get('repositories/11/resources', params={'all_ids': True})).json()
print("\nchecking resources in SHC")
extent_changer(resource_records, repo_number="11", type="resources", extent_dict=extent_dict)
archival_objects = (client.get("repositories/11/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in SHC')
extent_changer(archival_objects, repo_number="11", type="archival_objects", extent_dict=extent_dict)
accessions = (client.get("repositories/11/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in SHC')
extent_changer(accessions, repo_number="11", type="accessions", extent_dict=extent_dict)
resource_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
print("\nchecking resources in Zavala")
extent_changer(resource_records, repo_number="2", type="resources", extent_dict=extent_dict)
archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in Zavala')
extent_changer(archival_objects, repo_number="2", type="archival_objects", extent_dict=extent_dict)
accessions = (client.get("repositories/2/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in Zavala')
extent_changer(accessions, repo_number="2", type="accessions", extent_dict=extent_dict)