from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import json
import time
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="../../.config/JetBrains/PyCharmCE2021.3/scratches/aris.log", filemode="a")

client = ASnakeClient()
temp2 = "PP12345-micro"
responses = (client.get('repositories/2/resources/568/top_containers').json())
print(responses)
counter = 0
for response in responses:
    container = client.get(response['ref']).json()
    if "type" in container:
        if container['type'] == "Reel":
            container['type'] = "Microfilm"
            container['container_profile'] = {}
            container['container_profile']['ref'] = '/container_profiles/9'
            submission = client.post(response['ref'], json=container).json()
            print(container)
            print("update status:",submission)
            counter += 1
    output = open("./sample.json", "w")
    output.write(json.dumps(response))
    output.close()
print(counter,"items updated")