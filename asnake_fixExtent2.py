from tqdm import tqdm
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")
item_log = open("/home/brian/itemlog.txt", "a")
item_log.close()
itemlog = []
with open("/home/brian/itemlog.txt", "r") as r:
    for line in r:
        itemlog.append(line[:-1])
client = ASnakeClient()
counter = 0

changes = {'cubic_feet': ['staging'],
           'blueprints_(reprographic_copies)': ['staging2'],
           'architectural_drawings_(visual_works)': ['staging3'],
           'folders': ['staging4'],
           'electronic_files': ['staging5'],
           'daguerreotypes_(photographs)': ['staging6']
           }

def extent_changer(resource_records, repo_number, type):
    found_records = set([])
    address = f'repositories/{repo_number}/{type}/' + "{0}"
    for record in tqdm(resource_records):
        rec_uri = address.format(record)
        res_record = client.get(rec_uri).json()
        updated_record = deepcopy(res_record)
        Flag = True
        try:
            extents = res_record['extents']
            listy = []
            for ext_index, extent in enumerate(extents):
                #print(extent['extent_type'])
                for key in changes.keys():
                    new_list = changes[key]
                    if extent['extent_type'] in new_list:
                        print(extent['extent_type'])
                        keymaster = extent['extent_type']
                        updated_record['extents'][ext_index]['extent_type'] = key
                        with open("log2.csv", "a") as w:
                            w.write(res_record['title'] + "|" + res_record['uri'] + "|" + extent['extent_type'] + "\n")
                        w.close()
                        Flag = False
            if Flag is False:
                print(updated_record['extents'])
                response = client.post(rec_uri, json=updated_record)
                print(response)
                if response.status_code == 200:
                    logger.info('Extent change successfully pushed', rec=record, response=response)
                    found_records.add(record)
                    print("update applied")
                    counter = counter + 1
                else:
                    logger.info('Extent change failed', rec=record, response=response)
                    print(response.json())
        except:
            pass
    print('{0} records checked; {1} records updated.'.format(len(resource_records), len(found_records)))
print("adapter from work by Scott Carlson with his work at Rice")
print("this is going to take a while, take a coffee break")
resource_records = (client.get('repositories/11/resources', params={'all_ids': True})).json()
print("\nchecking resources in SHC")
extent_changer(resource_records, "11", "resources")
archival_objects = (client.get("repositories/11/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in SHC')
extent_changer(archival_objects, "11", "archival_objects")
accessions = (client.get("repositories/11/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in SHC')
extent_changer(accessions, "11", "accessions")
resource_records = (client.get('repositories/12/resources', params={'all_ids': True})).json()
print("\nchecking resources in review")
extent_changer(resource_records, "12", "resources")
archival_objects = (client.get("repositories/12/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in review')
extent_changer(archival_objects, "12", "archival_objects")
accessions = (client.get("repositories/12/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in legislative')
extent_changer(accessions, "12", "accessions")
'''
resource_records = (client.get('repositories/13/resources', params={'all_ids': True})).json()
print("\nchecking resources in review")
extent_changer(resource_records, "13", "resources")
archival_objects = (client.get("repositories/13/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in review')
extent_changer(archival_objects, "13", "archival_objects")
accessions = (client.get("repositories/13/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in review')
extent_changer(accessions, "13", "accessions")
resource_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
print("\nchecking resources in Zavala")
extent_changer(resource_records, "2", "resources")
archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in Zavala')
extent_changer(archival_objects, "2", "archival_objects")
accessions = (client.get("repositories/2/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in Zavala')
extent_changer(accessions, "2", "accessions")
'''
print(counter)
