from tqdm import tqdm
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD

today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='H:/container_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('container_type_changes_log')

logging.setup_logging(filename="H:/aris_container.log", filemode="a")

client = ASnakeClient()
def row_converter(row, columns):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in columns:
        pictionary[item] = str(row[count])
        count += 1
    return pictionary

def container_changer(container_ids, repo_number, container_dict):
    found_records = set([])
    for container_id in tqdm(container_ids):
        address= f"repositories/{repo_number}/top_containers/{container_id}"
        container_record = client.get(address).json()
        updated_record = deepcopy(container_record)
        try:
            my_type = container_record['type']
            if my_type in container_dict.keys():
                updated_record['indicator'] = updated_record['indicator'].replace(my_type, container_dict[my_type])
                updated_record['type'] = container_dict[my_type]
                with open("H:/log2.csv", "a") as w:
                    w.write(f"{container_record['indicator']}|{container_record['type']}\n")
                w.close()
            for key in container_dict.keys():
                if key in updated_record['indicator']:
                    updated_record['indicator'] = updated_record['indicator'].replace(key, container_dict[key])
                if key in updated_record['display_string']:
                    updated_record['display_string'] = updated_record['display_string'].replace(key, container_dict[key])
                if key in updated_record['long_display_string']:
                    updated_record['long_display_string'] = updated_record['long_display_string'].replace(key, container_dict[key])
            if container_record != updated_record:
                response = client.post(address, json=updated_record)
                if response.status_code == 200:
                    logger.info('Container type changed successfully', rec=container_id,response=response )
                    found_records.add(container_record['indicator'])
                else:
                    print(response.content)
                    logger.error(f"container type update failed for {container_record['indicator']}")
            else:
                pass
        except:
            pass

def secondary_container_changer(records, record_type, repo_number, container_dict):
    found_records = set([])
    for record in tqdm(records):
        address = f"repositories/{repo_number}/{record_type}/{record}"
        container_record = client.get(address).json()
        updated_record = deepcopy(container_record)
        try:
            if "instances" in updated_record.keys():
                if len(updated_record["instances"]) > 0:
                    for instance in updated_record["instances"]:
                        if "sub_container" in instance.keys():
                            if "type_2" in instance["sub_container"].keys():
                                if instance["sub_container"]["type_2"] in container_dict.keys():
                                    instance['sub_container']['type_2'] = container_dict[instance["sub_container"]["type_2"]]
                            if "type_3" in instance["sub_container"].keys():
                                if instance["sub_container"]["type_3"] in container_dict.keys():
                                    instance['sub_container']['type_3'] = container_dict[instance["sub_container"]["type_3"]]
            if container_record != updated_record:
                response = client.post(address, json=updated_record)
                if response.status_code == 200:
                    print(f"container type updated for {container_record['ref_id']}")
                    logger.info('Container type changed successfully', rec=container_record,response=response )
                    found_records.add(container_record['ref_id'])
                else:
                    print(response.status_code)
                    print(response.text)
                    logger.error(f"container type update failed for {container_record['ref_id']}")
            else:
                pass
        except:
            pass


print("adapter from work by Scott Carlson with his work at Rice")
#cvl = input("full path to excel spreadsheet with data: ")
cvl = "F:/Archives/Collections_management/ArchivesSpace/Administration/controlled value list normalization.xlsx"
df = PD.read_excel(cvl, dtype=object, sheet_name="container_type")
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

container_records = (client.get('repositories/13/top_containers', params={'all_ids': True})).json()
print("\nchecking containers in legislative")
container_changer(container_records, repo_number="13", container_dict=extent_dict)
accessions = (client.get("repositories/13/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in legislative')
secondary_container_changer(accessions, repo_number="13", record_type="accessions", container_dict=extent_dict)
resource_records = (client.get('repositories/13/resources', params={'all_ids': True})).json()
print("\nchecking resources in legislative")
secondary_container_changer(resource_records, repo_number="13", record_type="resources", container_dict=extent_dict)
archival_objects = (client.get("repositories/13/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in legislative')
secondary_container_changer(archival_objects, repo_number="13", record_type="archival_objects", container_dict=extent_dict)
container_records = (client.get('repositories/12/top_containers', params={'all_ids': True})).json()
print("\nchecking containers in review")
accessions = (client.get("repositories/12/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in review')
secondary_container_changer(accessions, repo_number="12", record_type="accessions", container_dict=extent_dict)
container_changer(container_records, repo_number="12", container_dict=extent_dict)
resource_records = (client.get('repositories/12/resources', params={'all_ids': True})).json()
print("\nchecking resources in review")
secondary_container_changer(resource_records, repo_number="12", record_type="resources", container_dict=extent_dict)
archival_objects = (client.get("repositories/12/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in review')
secondary_container_changer(archival_objects, repo_number="12", record_type="archival_objects", container_dict=extent_dict)
container_records = (client.get('repositories/11/top_containers', params={'all_ids': True})).json()
print("\nchecking container in SHC")
container_changer(container_records, repo_number="11", container_dict=extent_dict)
accessions = (client.get("repositories/11/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in SHC')
secondary_container_changer(accessions, repo_number="11", record_type="accessions", container_dict=extent_dict)
resource_records = (client.get('repositories/11/resources', params={'all_ids': True})).json()
print("\nchecking resources in SHC")
secondary_container_changer(resource_records, repo_number="11", record_type="resources", container_dict=extent_dict)
archival_objects = (client.get("repositories/11/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in SHC')
secondary_container_changer(archival_objects, repo_number="11", record_type="archival_objects", container_dict=extent_dict)
container_records = (client.get('repositories/2/top_containers', params={'all_ids': True})).json()
print("\nchecking containers in Zavala")
container_changer(container_records, repo_number="2", container_dict=extent_dict)
accessions = (client.get("repositories/2/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in Zavala')
secondary_container_changer(accessions, repo_number="2", record_type="accessions", container_dict=extent_dict)
resource_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
print("\nchecking resources in Zavala")
secondary_container_changer(resource_records, repo_number="2", record_type="resources", container_dict=extent_dict)
archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in Zavala')
secondary_container_changer(archival_objects, repo_number="2", record_type="archival_objects", container_dict=extent_dict)
print("all done")

