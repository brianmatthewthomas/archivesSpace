import json
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime

today_date = datetime.datetime.today().strftime('%Y-%m-%d')

logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="../../.config/JetBrains/PyCharmCE2021.3/scratches/aris.log", filemode="a")

client = ASnakeClient()

this_container = {'jsonmodel_type': 'top_container',
                  'active_restrictions': [],
                  'series': [],
                  'collection': [],
                  'indicator': 'turkey-002',
                  'type': 'Box',
                  'barcode': '',
                  'repository': {'ref': '/repositories/2'},
                  'restricted': 'false',
                  'container_profile': {'ref': '/container_profiles/3'},
                  'container_locations': [{'ref': '/locations/2960', 'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': '2021-11-09'}]}
#this_container = json.dumps(this_container)
print(this_container)
response = client.post('/repositories/2/top_containers', json=this_container)
print(response.status_code)