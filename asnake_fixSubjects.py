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

functions = (client.get('/subjects', params={'all_ids': True})).json()
for record in tqdm(functions):
    subject_id = '/subjects/' + str(record)
    subject = client.get(subject_id).json()
    if subject['source'] == "Library of Congress Subject Headings":
        print(subject)
        subject['source'] = 'lcsh'
        response = client.post(subject_id, json=subject)
        logger.info('Subject change successfully pushed', rec=subject_id, response=response)
print("all done")

