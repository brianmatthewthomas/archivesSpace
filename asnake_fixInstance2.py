from tqdm import tqdm
from copy import deepcopy
# meant to fix issues with faulty second instance types, default setting for converting file to folder
from asnake.client import ASnakeClient
import asnake.logging as logging
import asnake.utils as utils
import datetime
import json
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")

client = ASnakeClient()

responses = (client.get('repositories/2/resources/1141/tree').json())

output = open("./sample.json", "w")
output.write(json.dumps(responses))
output.close()

for item in utils.walk_tree('repositories/2/resources/1141', client):
    response = (client.get(item['uri']).json())
    if "instances" in response:
        if len(response['instances']) is not None:
            for instance in response['instances']:
                print(instance['instance_type'])
                if 'sub_container' in instance:
                    if 'type_2' in instance['sub_container']:
                        del instance['sub_container']['type_2']
                        if 'indicator_2' in instance['sub_container']:
                            del instance['sub_container']['indicator_2']
                        fixed_response = client.post(item['uri'], json=response)
                        output = open("./sample3.json", "w")
                        output.write(json.dumps(response))
                        output.close()