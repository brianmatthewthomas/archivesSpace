import json
import os
import pandas as PD
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import time

start = time.asctime()
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")
item_log = open("itemlog.txt", "a")
item_log.close()
itemlog = []
with open("itemlog.txt", "r") as r:
    for line in r:
        itemlog.append(line[:-1])
item_log = open("itemlog.txt", "a")

client = ASnakeClient()


def row_converter(row=tuple, listy=list):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = row[count]
        pictionary[item] = str(pictionary[item])
        if pictionary[item] == 'NaN' or pictionary[item] == "nan":
            pictionary[item] = ''
        count += 1
    return pictionary


my_file = "accession_tester.xlsx"

df = PD.read_excel(my_file, dtype=object)
listy = df.columns
for row in df.itertuples():
    my_data = row_converter(row, listy)
    # clear the data
    my_json = "text"
    my_json = {}
    # construct the data
    my_json['title'] = my_data['accession_title']
    my_json['display_string'] = my_data['accession_title']
    my_json['publish'] = False
    if my_data['accession_publish'] == "1":
        my_json['publish'] = True
    my_json['content_description'] = my_data['accession_content_description']
    my_json['inventory'] = f"{my_data['extent_number']} {my_data['extent_type']}"
    if my_json['inventory'] == " ":
        my_json['inventory'] = "No specific inventory information available"
    my_json[
        'general_note'] = "Information sourced from pre-ArchivesSpace electronic data sources and remixed to construct an ArchivesSpace accession record. Additional information may exist in a physical accession file."
    my_json['disposition'] = my_data['accession_disposition']
    my_json[
        'provenance'] = f"Accession of {my_data['accession_disposition']} provided as a {my_data['accession_acquisition_type']} by {my_data['delete_Creator']}."
    my_json['id_0'] = my_data['accession_number_1']
    if my_data['accession_number_2'] != "":
        my_json['id_1'] = my_data['accession_number_2']
    my_json['accession_date'] = "1836-03-02"
    if my_data['accession_accession_date'] != '':
        my_json['accession_date'] = my_data['accession_accession_date']
    my_json['acquisition_type'] = "transfer"
    if my_data['accession_acquisition_type']:
        my_json['acquisition_type'] = my_data['accession_acquisition_type']
    my_json['resource_type'] = "papers"
    if my_data['access_resource_type'] != "":
        my_json['resource_type'] = my_data['access_resource_type']
    my_json['language'] = 'eng'
    my_json['access_restrictions'] = False
    my_json['access_restrictions_note'] = "None."
    if my_data['accession_restrictions_apply'] == "true":
        my_json['access_restrictions'] = true
        my_json['access_restrictions_note'] = "Accession access restrictions apply"
    my_json['use_restrictions'] = False
    if my_data['accession_use_restriction'] == "true":
        my_json['use_restrictions'] = True
    if my_data['accession_use_restriction_note'] != "":
        my_json['use_restrictions_note'] = my_data['accession_use_restriction_note']
    my_json['jsonmodel_type'] = "accession"
    if my_data['extent_number'] != "" and my_data['extent_type'] != "":
        my_json['extent'] = []
        my_extent = "hi"
        my_extent = {"jsonmodel_type": "extent", "portion": "part", "number": my_data['extent_number'],
                     "extent_type": my_data['extent_type']}
        my_json['extent'].append(my_extent)
    if my_data['date_1_expression'] != "":
        my_json['dates'] = []
        my_date = {'jsonmodel_type': 'date', 'expression': my_data['date_1_expression']}
        if my_data['date_1_label'] != "":
            my_date['label'] = my_data['date_1_label']
        if my_data['date_1_type'] != "":
            my_date['date_type'] = my_data['date_1_type']
        my_json['dates'].append(my_date)
    my_json['repository'] = {'ref': '/repositories/2'}
    if my_data['agent_uuid'] != "":
        agent_list = my_data['agent_uuid'].split("|")
        my_json['linked_agents'] = []
        for agent in agent_list:
            agent_dict = "something"
            agent_dict = {}
            agent_dict['role'] = "source"
            if my_data['agent_role'] != "":
                agent_dict['role'] = my_data['agent_role']
            agent_dict['agent_type'] = agent.split("/")[0]
            agent = agent.replace("agent_person", "people").replace("agent_family", "families").replace(
                "agent_corporate_entity", "corporate_entities")
            agent_dict['ref'] = f"/agents/{agent.split('/')[0]}/{agent.split('/')[-1]}"
            my_json['linked_agents'].append(agent_dict)
    my_json['user_defined'] = {'boolean_1': True, 'boolean_2': False, 'boolean_3': False,
                               'date_1': my_json['accession_date'], 'jsonmodel_type': 'user_defined'}
    if my_data['user_defined_text_1---Received_by'] != "":
        my_json['user_defined']['text_1'] = my_data['user_defined_text_1---Received_by']
    if my_data['user_defined_text_2---Accessions_by'] != "":
        my_json['user_defined']['text_2'] = my_data['user_defined_text_2---Accessions_by']
    if my_data['user_defined_string_1'] != "":
        my_json['user_defined']['string_1'] = my_data['user_defined_string_1']
    print("constructed json")
    '''with open("json_tester.txt", "w") as w:
        my_data = json.dumps(my_json)
        w.write(json.dumps(my_json))
    w.close()
    os.rename("json_tester.txt", "json_tester.json")
    '''
    temp = client.post("/repositories/2/accessions", json=my_json)
    print(temp.content)
print("all done")

