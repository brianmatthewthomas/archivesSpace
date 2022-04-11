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
changes = {'GB (11,231 files)':['gigabytes','11231','electronic_files'],
           'MB_(4_files)':['megabytes','4','electronic_files'],
           'MB_(2_files)':['megabytes','2','electronic_files'],
           'KB_(1_files)':['kilobytes','1','electronic_files'],
           'folders_and_1_wallets':['folders','1','wallets'],
           'folders_and_4_wallets':['folders','4','wallets'],
           'folders,_1_wallets':['folders','1','wallets'],
           'folders_and_5_wallets':['folders','5','wallets'],
           'MB_(642_files)':['megabytes','642','electronic_files'],
           'folders_and_3_wallets':['folders','3','wallets'],
           'MB_(469_files)':['megabytes','469','electronic_files'],
           'folders_and_2_wallets':['folders','2','wallets'],
           'MB_(342_files)':['megabytes','342','electronic_files'],
           'MB_(152_files)':['megabytes','152','electronic_files'],
           'MB_(18_files)':['megabytes','18','electronic_files'],
           'MB_(76_files)':['megabytes','76','electronic_files'],
           'MB_(249_files)':['megabytes','249','electronic_files'],
           'GB_(1,797_files)':['gigabytes','1797','electronic_files'],
           'KB_(26_files)':['kilobytes','26','electronic_files'],
           'KB_(34_files)':['megabytes','34','electronic_files'],
           'MB_(89_files)':['megabytes','89','electronic_files'],
           'KB_(2_files)':['kilobytes','2','electronic_files'],
           'MB_(11_files)':['megabytes','11','electronic_files'],
           'KB_(11_files)':['kilobytes','11','electronic_files'],
           'MB_(69_files)':['megabytes','69','electronic_files'],
           'MB_(380_files)':['kilobytes','380','electronic_files'],
           'KB_(4_files)':['kilobytes','4','electronic_files'],
           'KB_(13_files)':['kilobytes','13','electronic_files'],
           'KB_(3_files)':['kilobytes','3','electronic_files'],
           'KB_(24_files)':['kilobytes','24','electronic_files'],
           'MB_(26_files)':['megabytes','26','electronic_files'],
           'MB_(57_files)':['megabytes','57','electronic_files'],
           'KB_(6_files)':['kilobytes','6','electronic_files'],
           'MB_(20_files)':['megabytes','20','electronic_files'],
           'MB_(90_files)':['megabytes','90','electronic_files'],
           'MB_(39_files)':['megabytes','39','electronic_files'],
           'GB_(2,865_files)':['gigabytes','2865','electronic_files'],
           'GB_(3,114_files)':['gigabytes','3114','electronic_files'],
           'MB_(425_files)':['megabytes','425','electronic_files'],
           'MB_(349_files)':['megabytes','349','electronic_files'],
           'MB_(341_files)':['megabytes','341','electronic_files'],
           'MB_(414_files)':['megabytes','414','electronic_files'],
           'MB_(16_electronic_files':['megabytes','16','electronic_files'],
           'MB_(12_electronic_files':['megabytes','12','electronic_files'],
           'MB_(22_electronic_files':['megabytes','22','electronic_files'],
           'MB_(9_electronic_files':['megabytes','9','electronic_files'],
           'MB_(5_electronic_files':['megabytes','5','electronic_files'],
           'MB_(28_electronic_files':['megabytes','28','electronic_files'],
           'MB_(90_electronic_files':['megabytes','90','electronic_files'],
           'KB_(9_electronic_files':['kilobytes','9','electronic_files'],
           'MB_(44_electronic_files':['megabytes','44','electronic_files'],
           'MB_(42_electronic_files':['megabytes','42','electronic_files'],
           'MB_(2_electronic_files':['megabytes','2','electronic_files'],
           'MB_(33_electronic_files':['megabytes','33','electronic_files'],
           'KB_(5_electronic_files':['kilobytes','5','electronic_files'],
           'MB_(29_electronic_files':['megabytes','29','electronic_files'],
           'MB_(52_electronic_files':['megabytes','52','electronic_files'],
           'MB_(20_electronic_files':['megabytes','20','electronic_files'],
           'MB_(24_electronic_files':['megabytes','24','electronic_files'],
           'MB_(88_electronic_files':['megabytes','88','electronic_files'],
           'MB,_16_files,_in_7_folders':['megabytes','16','electronic_files'],
           'MB,_45_files,_in_3_folders':['megabytes','45','electronic_files'],
           'KB,_5_files':['kilobytes','5','electronic_files'],
           'MB_(66_files)':['megabytes','66','electronic_files'],
           'folders,_172_color_slides':['folders','172','color_slides']}


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
                if extent['extent_type'] in changes:
                    print(extent['extent_type'])
                    keymaster = extent['extent_type']
                    gozer = changes[keymaster][0]
                    second_value = changes[keymaster][1]
                    second_type = changes[keymaster][2]
                    updated_record['extents'][ext_index]['extent_type'] = gozer
                    template = {"number": f"{second_value}",
                                "portion": "part",
                                "extent_type": f"{second_type}",
                                "jsonmodel_type": "extent"}
                    updated_record['extents'].append(template)
                    with open("log2.csv", "a") as w:
                        w.write(res_record['title'] + "|" + res_record['uri'] + "|" + extent['extent_type'] + "\n")
                    w.close()
                    Flag = False
            if Flag is False:
                print(updated_record['extents'])
                response = client.post(rec_uri, json=updated_record)
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
'''resource_records = (client.get('repositories/11/resources', params={'all_ids': True})).json()
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
print('\nchecking accessions in review')
extent_changer(accessions, "12", "accessions")
resource_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
print("\nchecking resources in Zavala")
extent_changer(resource_records, "2", "resources")'''
archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
print('\nchecking archival objects in Zavala')
extent_changer(archival_objects, "2", "archival_objects")
accessions = (client.get("repositories/2/accessions", params={'all_ids': True})).json()
print('\nchecking accessions in Zavala')
extent_changer(accessions, "2", "accessions")
print(counter)
