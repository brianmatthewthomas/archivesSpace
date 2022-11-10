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

responses = (client.get('repositories/2/resources/1087/tree').json())

output = open("./sample.json", "w")
output.write(json.dumps(responses))
output.close()

for item in utils.walk_tree('repositories/2/resources/1087', client):
    response = (client.get(item['uri']).json())
    if "instances" in response:
        if len(response['instances']) is not None:
            for instance in response['instances']:
                print(instance['instance_type'])
                if 'sub_container' in instance:
                    print(instance['sub_container']['type_2'])
                    if instance['sub_container']['type_2'] == "File":
                        instance['sub_container']['type_2'] = "Folder"
                        fixed_response = client.post(item['uri'], json=response)
'''    output = open("./sample2.json", "w")
    output.write(json.dumps(response))
    output.close()
'''