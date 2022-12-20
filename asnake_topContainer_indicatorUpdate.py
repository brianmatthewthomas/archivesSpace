from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import json
import time
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

#logging.setup_logging(filename="../../.config/JetBrains/PyCharmCE2021.3/scratches/aris.log", filemode="a")

client = ASnakeClient()
responses = (client.get('repositories/2/top_containers/search?q=223-').json())
print(responses)
responses2 = responses['response']['docs']
for response in responses2:
    if "223-" in response['title']:
        container = client.get(response['id']).json()
        indicator = container['indicator']
        if indicator.startswith("223-"):
            print(container['indicator'])
            temp = container['indicator']
            temp2 = temp.split("-")[1]
            while len(temp2) < 4:
                temp2 = "0" + temp2
            temp = temp.replace(temp.split("-")[1], temp2)
            print(temp)
            container['indicator'] = temp
            submission = client.post(container['uri'], json=container).json()
            print(f"update status: {submission}")
'''
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
'''