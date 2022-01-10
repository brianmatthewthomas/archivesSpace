from tqdm import tqdm
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")

client = ASnakeClient()

changes = {'blueprints_(reprographic_copies)':['blueprints (reprographic copies)','blueprint (reprographic copy)','blueprint (reprographic copies)'],
           'albumen_prints':['albumen print','albumen prints'],
           'architectural_drawings_(visual_works)':['architectural drawing (visual work)','architectural drawing (visual works)','architectural drawings (visual work)','architectural drawings (visual works)'],
           'artifacts_(object_genre)':['artifact (object genre)','artifacts','artifacts (object genre)'],
           'audiocassettes':['audiocassette'],
           'black-and-white_negatives':['black-and-white negative','black-and-white negatives'],
           'black-and-white_prints_(prints_on_paper)':['black-and-white print (visual work)','black-and-white prints (prints on paper)'],
           'blueline_prints':['blueline print','blueline prints'],
           'boudoir_photographs':['boudoir photograph'],
           'broadsides_(notices)':['broadside (notice)'],
           'clippings_(information_artifacts)':['clipping (information artifact)'],
           'compact_discs':['compact discs'],
           'contact_sheets':['contact sheet'],
           'cubic_feet':['cubic ft.,','cubic ft.'],
           'diazotypes_(copies)':['diazotype (copy)','diazotypes (copies)'],
           'drawings_(visual_works)':['drawings'],
           'DVDs':['DVD'],
           'electronic_files':['electronic file','electronic files'],
           'envelopes':['envelope'],
           'folders':['folder','folder)','of 3 folders'],
           'gelatin_silver_prints':['gelatin silver print'],
           'gigabytes':['GB (1,797 files)','GB (2,865 files)'],
           'instantaneous_recordings':['instantaneous recordings'],
           'kilobytes':['KB','KB (11 files)','KB (13 files)','KB (2 files)','KB (24 files)','KB (26 files)','KB (3 files)','KB (34 files)','KB (4 files)','KB (6 files)'],
           'ledgers_(account_books)':['ledger (account book)','ledgers (account books)'],
           'letter_books':['letter book'],
           'lithographs':['lithograph'],
           'mechanical_drawings_(building_systems_drawings)':['mechanical drawings (building systems drawings)'],
           'megabytes':['MB','MB (11 files)','MB (152 files)','MB (18 files)','MB (20 files)','MB (26 files)','MB (380 files)','MB (39 files)','MB (57 files)','MB (69 files)','MB (76 files)','MB (89 files)','MB (90 files)'],
           'microfilms':['microfilm'],
           'motion_picture_components':['motion picture component','motion picture components'],
           'motion_pictures_(visual_works)':['motion picture (visual work)'],
           'open_reel_audiotapes':['open reel audiotape','open reel audiotapes'],
           'paintings_(visual_works)':['painting (visual work)'],
           'photoengravings_(prints)':['photoengraving (print)'],
           'photographic_postcards':['photographic postcard','photographic postcards'],
           'photographs':['photograph'],
           'photomechanical_prints':['photomechanical print'],
           'postcards':['postcard'],
           'posters':['poster'],
           'scrapbooks':['scrapbook'],
           'sheets_(paper_artifacts)':['(paper artifacts)','sheet (paper artifact)'],
           'stats_(copies)':['stat (copy)'],
           'tintypes_(prints)':['tintype (prints)'],
           'videocassettes':['videocassette'],
           'videotapes':['videotape'],
           'volumes':['volume'],
           'wallets':['wallet','wallet:'],
           'woodcuts_(prints)':['woodcut (print)']}

def extent_changer(resource_records, repo_number, type):
    found_records = set([])
    address = f'repositories/{repo_number}/{type}/' + "{0}"
    for record in tqdm(resource_records):
        rec_uri = address.format(record)
        res_record = client.get(rec_uri).json()
        updated_record = deepcopy(res_record)
        try:
            extents = res_record['extents']
            for ext_index, extent in enumerate(extents):
                for key, value in changes.items():
                    if extent['extent_type'] in value:
                        print(extent['extent_type'])
                        updated_record['extents'][ext_index]['extent_type'] = key
                        break
                    else:
                        pass
            if res_record['extents'] != updated_record['extents']:
                response = client.post(rec_uri, json=updated_record)
                if response.status_code == 200:
                    logger.info('Extent change successfully pushed', rec=record, response=response)
                    found_records.add(record)
                else:
                    logger.info('Extent change failed', rec=record, response=response)
            else:
                pass
        except:
            pass
    print('{0} resource records checked; {1} records updated.'.format(len(resource_records), len(found_records)))
print("adapter from work by Scott Carlson with his work at Rice")
print("this is going to take a while, take a coffee break")
resource_records = (client.get('repositories/11/resources', params={'all_ids': True})).json()
print("checking resources in SHC")
extent_changer(resource_records, "11", "resources")
archival_objects = (client.get("repositories/11/archival_objects", params={'all_ids': True})).json()
print('checking archival objects in SHC')
extent_changer(archival_objects, "11", "archival_objects")
resource_records = (client.get('repositories/12/resources', params={'all_ids': True})).json()
print("checking resources in review")
extent_changer(resource_records, "12", "resources")
archival_objects = (client.get("repositories/12/archival_objects", params={'all_ids': True})).json()
print('checking archival objects in review')
extent_changer(archival_objects, "12", "archival_objects")
resource_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
print("checking resources in Zavala")
extent_changer(resource_records, "2", "resources")
archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
print('checking archival objects in Zavala')
extent_changer(archival_objects, "2", "archival_objects")

