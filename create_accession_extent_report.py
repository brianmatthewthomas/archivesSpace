# Use this to harvest down accession data not previously harvested
# (will not re-download something that has since been updated)
# and generate a report with
# (1) accession number
# (2) accession date (as date received)
# (3) transfer type
# (4) resource type
# (5) for each extent/value pair compile a column for each
# GB/MB will be converted to KB which will yield inexact figures but can be summed easier
import json
import asnake
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD
import os
import PySimpleGUI as SG

my_icon = b'iVBORw0KGgoAAAANSUhEUgAAAHgAAABsCAQAAAALKr7UAAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAALEsAACxLAaU9lqkAAAAHdElNRQ' \
          b'fmAhQHBBtCNNv6AAANwUlEQVR42u2ca3hV5ZXHf0lObgRz4WK4WmpAEFFHFBTkMQWUoTyoiIpDrajcpGOFWsaOtCqgraIdO8pDp7VF' \
          b'awtVKlSpoigXUZDLYBlCRCAkJCEhIUDIhYSEJOec/3zYSdg7yd7nJDlJSJ78z6ez93r3Xuustde7bvtAJzrRiU50ohOd6EQnOtGJTv' \
          b'iBoA4kSyRdCKKc8x1f4K6M4naGcznBFJLCVrZxquPaaCIbKEWmTxX7mEd0R9RwBPN4mngq+YZdpFFFP0YyghjcrGcRaR1Lu+EsoRyR' \
          b'zEP0qD0axVjeowKxg6s7krjBLKAMsZ6r6p2L4kkKEVvp13EE/lfOID6kt83PMZdziN8T3jHE7c0exD4G2lK4eB43JUzuGOa8GA+FTH' \
          b'Kk6sFXiI/ocqmw7SK0iSuHkYVY4XP9DCop5jbzLdsO/fglPcgigwyyyaOAMjx+rQxhFv3J5LdU+aD8jMNcx93sQG0t8PX8svbp8nCe' \
          b'AvLIIp1jZJJDPueosF17FfchVnHE511Os5HrGE938ttS4HCm8wwJMUyilBxOhRRFl0VrALcAcIFiznCCDNJJJ4s8Cimr0RAA99OXE7' \
          b'xjOdYwxFbmk8DgthT4OyxiBpFDWMy9QClnya1W7nFyORtRElEVzzAA3JRylhwySSONTHI5SxzTCOJ9Uvy622FySeAadraNwMFMZCk3' \
          b'hTKFxVwDQBxx1XuLKKeIU5wgnXQyyOaUqzi2LJYEbgO8nOcsOVQwmAqO0IcCyn3e8SyZJDC4bWLpHszncbr15j+Yw2U+iKsoIZ8cMk' \
          b'ir1n0h52usWJzjDNmkksJRMkmnzDa5WMWDrOJhPx6AAGMUm/AEaay2q7Fwq1jHtEN/0bN6QCPVT10u5kYVnOKPRNnedyXibwS3rkl3' \
          b'ZSZP0S+Wx3iS+EYvDyGaaK5kDOChhEKyOUoKR8kgK6z4csYRY5P4BxEKuFt3WxrGM0wl9AYWM5mQZlwolQ0cwMMQJjEbqKKYl/gNnL' \
          b'Wtc4QQAxS3nkFH8DApKFKzdEzNgUfv6KpaQ47XMpVLkuYL8TFhtra1E7G4tcRNYCVlaJD+VM1e07FRPYS6Klgh6iEUruXyyq37hXjL' \
          b'1v324xhiZmsIG8q9JKFQTVOymosS3SE0XH9WvFz6je4RSlC6ypUoxK9subiVEspIbI3wYjnnUH8tV4maj32KU5jWqEQ3CL2iJPVUsN' \
          b'aoQNcI8bgtH08iUi+WAYJbSLf38D5PhFw2iXU8QdcAXPI0pURzLVEMBvbRj/54yaWIQvBw0mZZJBOAr8lrSYG/w6v8meF9eInVjAzY' \
          b'vhZKOacIYjjwLakUATHkUwLlFwWql6LcjJuNuFvKkMO4j30oRN/XLgUSebpWaJoK9JWi1FUT5VJ3JWm9XCKXQTaB7OuIQ/RtKXEH8Q' \
          b'YlqI9eVoECC69ek0vBmqhfKb56a5qnKr0uxDemmqUZ/0IOXpa0TAAdycN8i1y6U7t9sn9BVU3w0wsUUbsPB+suZUtaKMRmIhpMQt9G' \
          b'pNlov5m4ltWUowF6XUU+GD+h5zRB92udKhspcpn+qskapP5yyaW3pZpd+E8N6nA6pbhZGHj9xvA4aShcD2i/T6YLdHe1jqL1dhNM+4' \
          b'JylKLxQmNVqBKNkk0cdR1HEJvpHlhhg7iVj6hEg7VSpX4wvFahtWZ5i09rsMPf1UUuLVOWrhReHq7H12C2I04wOrDi9mIJJ1FXzdJh' \
          b'P9O8maam13eV3USBy/SIUE89rThRxrg6fN3ILkQRjwTSnMOYwi68aITWqcJPRrNN4T9KbEYMlq4RQi4FiZMWtxTBAxxBFDCvWYlZHQ' \
          b'xlJSXGb5wtqUzfKEnnfLK5zmTQ6HmTB35fS/WHRml8r25WkBCnuZeehBNBLyazhlJEFtMDF1R1Yz6pKFST9IU8kg5rqnqquyZqn48E' \
          b'b45J3BjtrD5erDkKFwrSKB1qhMgZGmNcq5RkNrGZQ5QjPGxhTOCi5IlswY0G6bfVLqek1u+i7+msA4M5GmIS+FYVVx9/16T3mY3YrK' \
          b'o02Ysoprz2qiV8xTwnz9y4iscQ5jOd2Bims4Ah1Qe3samWYC8HzX2NOthLuunb7bUt+v2mBsKHzOVmP9kpqDwKYfw3uxhGPJBLEgco' \
          b'Coxu43iCoyhE4/SJSQtlmmLSWqQ+dzDoeSbKy7Sj9sx/mccV9JjfUdj/poYVU8n3WyLdm8hmqtBAvVbHaLco2sTs9Tppy95JDTVRjj' \
          b'LtwQfVz3QmXv/np0W/9hkXOMXQwIeNf6AIxeixei6lQg+aWA3WKw78fahwE+0zFt3/xKLjBXL7I3DBlI8Q+4gLbGjxNBnIpfEWQ67B' \
          b'LnUzMXqVMhyynR+bKLvqC8vZ/eplOttXB/0JYk4M3Y14N3C7bRf+jT140dVa0aD3rdJcE5tBek5eH/lszWdknfTRrR9ZdPwzeXwKnH' \
          b'+6by7iF4HqAY1mLWWopxYqzeaWVr1coSMO7H1sSu3Q0/UdkHqYzg9Qik+Bk9xxbiq5KxDidmcZp1CEpmqH7W/t0U8tWlnooBWvFpgo' \
          b'o7S1HkWlHvXbWgy8oxCRe7FN1pzndg3eYI3UO475z2FdYWKxl5IcaE/rehPtjQ0+IDsUZ6IZ6LNsv1CIHYGoEH6PC8Gar1wfJZfnjE' \
          b'jWr93zU0WaaJ9qUHsV+oFFxy863v+8xgqxvLH5UEMBdhrHRR+b8acaHOddU7umG484BG1ik6mR24U7GuQyjFmm8UiximyH+58gBTzs' \
          b'bWzPqCGBc9khNlLquPA9jpm+TWK4UwjINktufoMN3WjuMH1LYa3DNZM5DQUcaLw3rg8vn1KVzCGHZbmsxlv7LZpHbXtZRqxsnk4Yax' \
          b'vbRzDL1Ob18hfb+jrsxg2pZAZCYNhDZiFbHJatt/wc4xnlQCs2m9rzkTYGbSCRsaZvB/nQhq6EvUY2UhoYgU+yHT6jxGZRGR+YBqqi' \
          b'mEmkwy0K+dxSur7RMdaZYxqb87DdZEdmHOMwVLGz8V3fhgX28DGVSSTbLLpQMwMEwMDqaSM7HOCwZQvo4aMEGmGxDrtEsxDy2N+UiM' \
          b'ruEUk7x6e2yVOExamvsdGDgc2m5nwEExz3keP8nAJLdT+4ARezkRV4IZkTgSy/Lkc32dQvKnWvJcbqqQ22+2WhbjZRDlOew956zpJ7' \
          b'IZf+WI+mWC8ZQWg+DwU2KZzA+Uh9YsPaBsVaWBtiG2d9qa4muscdAsYqLZXLctWp9TpURzTNoPmaCYGeT4ljD5pnEx+7tUxhFubGKa' \
          b'dBymdMNOH6h2NsHG254nAdrXPPfxgZVwVv892W6Bc9iwbquA17pZptCS2DNKuByLvIaIVUf4Y6hKu7NcAibp86xaICLTZi7ZP8xGEm' \
          b'q1m4kfwQvWnLYq5ut7AYqhfrVSp2WLQ2zzafytRoy7WitNJi/Em6S8FC7K7XZQggIliPJqnMVuQDutrCZqzW1KFYYjobpvdtrlNcx1' \
          b'mF6GemXkaFVmuQEOW8wRUtO5jyEFVxjt3ej9XTwuoAC3VxTaFcCA22ecqrtKSOs7rH5KxytEBRQhxnboNd4ICiL4fskrmaJHGFJfFD' \
          b't5jqWrsUYzozu0GD9jo4K6+2GT+Zl81+F6ubuRu/jAYry7Ff+6TxdNV+flDbInvB8oSvtSkjJNg4q2L92ighFbGMy2kljCA/RG84F9' \
          b'NMrRajGL+pugWTaDo6yKZRttzGWR3QVMPQk5namlPd4axFiT4a10c13ML2G9VlOXNw8qhNrXlZA86qTG8aer/AqgbeOmthTKE8Uut9' \
          b'1Je+UF+ThjdLkl60GPQam5XbTT+LEVmlaqZR4czkRy214zqnL1+iqT5HQ1dVl1lDNFulkkqNmlP1J8E2gKnUq+qtYEVqsjJUqfd0nR' \
          b'BuPuIm2gizqYrRNp/DvVv07/qhfqdCSdLXlp7EDIfmiUdJWqNNOqfj+rEReeexKLANlMYhnn3oh36NNVzcwF42BZ4u/dWPlR8YnsDL' \
          b'5yS29XvN8/F001eN6M1X6E7L8EqGD/pMPWHsxmd4vvW2IKcAJBk95PfoilSu8SaBH3SsWVdoXY1uv+T2FprvbTQW4I71+RybDXRprb' \
          b'gRWudAmap5uszQ7QtNePujxdCLfeg+h0Sifvt7uqIUpG76uc7bTlut0jAhPGxj/KWi2xrMpbKLbb7T8DDoVq3WHtshlYOaYcThJ3mW' \
          b'nlxyiGMbSnSc0vEf5/R7I+Vz8wljLtX/mribUpdWBEDcvbrHKBBlsbAt91tfiORdNFipzRI2Xy8bIywVrHOsyV8SGEEuWtCE4e6aMt' \
          b'wWjVeIECnMCci7Hy2MYF7A2606OWgssvSUuhuDgm+1nz8U6cs/0VjlN1LYcq2pSSH/ybT29c8a91Eaohf9mLK5iGTNMF5/zecV+tPO' \
          b'EM6bqJffkXWhXtOVxga0iXGBnGBuPQziWzReZ/x4H/QLTTQKNRn8lG60W0ynNFi/8OGts7XIKOKWsZrradcIYwXeWH3gUMtcqxGGk0' \
          b'riQcd+eTtBP3aia2xm7w5pllG5OMurDKCDIJGT6P7aqfaLUfLvjBc5PGzljvbppOyK9AuocGmpqVrl1S7dbYzzZ/OfPmYb2iGieAvF' \
          b'1qb3eVqq3kY1eW3bVRxbFv3ZiQZpv6q0QWOMst23zGyLanJrYTTHUaIeM9pmxfxPy7zLeSlhRvV/SnrZxZ1N/kOwdoRQFlFIHs/7mE' \
          b'btQHBxGzd1qH+57UQ7xv8DgC8wraZy+5gAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjItMDItMjBUMDc6MDQ6MjcrMDA6MDBxXqaVAAAA' \
          b'JXRFWHRkYXRlOm1vZGlmeQAyMDIyLTAyLTIwVDA3OjA0OjI3KzAwOjAwAAMeKQAAACZ0RVh0aWNjOmNvcHlyaWdodABObyBjb3B5cm' \
          b'lnaHQsIHVzZSBmcmVlbHmnmvCCAAAAIXRFWHRpY2M6ZGVzY3JpcHRpb24Ac1JHQiBJRUM2MTk2Ni0yLjFXrdpHAAAAInRFWHRpY2M6' \
          b'bWFudWZhY3R1cmVyAHNSR0IgSUVDNjE5NjYtMi4xa5wU+QAAABt0RVh0aWNjOm1vZGVsAHNSR0IgSUVDNjE5NjYtMi4xhWT+PAAAAA' \
          b'BJRU5ErkJggg=='

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_access_extent_report(to_crawl, repo, logs_folder):
    step_count = 4
    current_step = 0
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    logging.setup_logging(filename=f'{logs_folder}/container_type_changer_' + str(today_date) + '.log')
    logger = logging.get_logger('container_type_changes_log')
    logging.setup_logging(filename=f"{logs_folder}/aris_container.log", filemode="a")
    client = ASnakeClient()
    crawled_accessions = []
    window['-stepwise-'].update("getting list of accession files harvested")
    create_directory(f"{to_crawl}/something.txt")
    for dirpath, dirnames, filenames in os.walk(to_crawl):
        for filename in filenames:
            if filename.startswith("accession_") and filename.endswith(".json"):
                crawled_accessions.append(filename)
    print("compiled list of harvested accession files")
    current_step += 1
    window['-Step_progress-'].update_bar(current_step, step_count)
    window['-stepwise-'].update("getting any missing accession data")
    print("starting re-crawl of data")
    accession_repo = f"repositories/{repo}/accessions"
    accessions = (client.get(accession_repo, params={'all_ids': True})).json()
    print(accessions)
    print("pulled accessions list, verifying everything crawled")
    instep_count = len(accessions)
    instep_progress = 0
    for item in accessions:
        accession_filename = str(item)
        while len(accession_filename) < 5:
            accession_filename = f"0{accession_filename}"
        accession_filename = f"accession_{accession_filename}.json"
        if accession_filename not in crawled_accessions:
            temp_data = client.get(f"{accession_repo}/{item}").json()
            with open(f'{to_crawl}/{accession_filename}', 'w') as accession_file:
                json.dump(temp_data, accession_file)
            accession_file.close()
            crawled_accessions.append(accession_filename)
            print(f"harvested {accession_filename} accession file")
        instep_progress += 1
        window['-Instep_progress-'].update_bar(instep_progress, instep_count)
    current_step += 1
    window['-Step_progress-'].update_bar(current_step, step_count)
    window['-stepwise-'].update("getting controlled list of extents in the repository")
    extent_type_list = set()
    instep_count = len(crawled_accessions)
    instep_progress = 0
    for item in crawled_accessions:
        with open(f"{to_crawl}/{item}", "r") as r:
            filedata = json.load(r)
            if "extents" in filedata.keys():
                for extent in filedata["extents"]:
                    extent_type_list.add(extent["extent_type"])
        instep_progress += 1
        window['-Instep_progress-'].update_bar(instep_progress, instep_count)
    print("compiled list of extent types")
    extent_type_list = list(extent_type_list)
    extent_type_list.sort()
    print("compiling column list")
    columns_list = ["accession_number", "accession_title", "accession_date", "transfer_type", "resource_type"]
    for item in extent_type_list:
        columns_list.append(f"{item}_value")
    bare_dataframe = PD.DataFrame(columns = columns_list)
    print(bare_dataframe)
    current_step += 1
    window['-Step_progress-'].update_bar(current_step, step_count)
    window['-stepwise-'].update("crawling data to compile spreadsheet")
    instep_progress = 0
    for item in crawled_accessions:
        with open(f"{to_crawl}/{item}", "r") as r:
            filedata = json.load(r)
            blank_dict = 0
            blank_dict = {}
            accession_number = filedata["id_0"]
            if "id_1" in filedata.keys():
                accession_number = f"{accession_number}-{filedata['id_1']}"
            if "id_2" in filedata.keys():
                accession_number = f"{accession_number}-{filedata['id_2']}"
            if "id_3" in filedata.keys():
                accession_number = f"{accession_number}-{filedata['id_3']}"
            blank_dict["accession_number"] = accession_number
            blank_dict["accession_title"] = filedata["title"]
            blank_dict["accession_date"] = filedata["accession_date"]
            blank_dict["transfer_type"] = filedata["acquisition_type"]
            blank_dict["resource_type"] = filedata["resource_type"]
            if "extents" in filedata.keys():
                for extent in filedata["extents"]:
                    blank_dict[f'{extent["extent_type"]}_value'] = extent["number"]
            bare_dataframe = bare_dataframe._append(blank_dict, ignore_index=True)
        instep_progress += 1
        window['-Instep_progress-'].update_bar(instep_progress, instep_count)
    print(bare_dataframe)
    current_step += 1
    window['-Step_progress-'].update_bar(current_step, step_count)
    accessions_report = bare_dataframe.to_excel(f"{to_crawl}/accessions_report.xlsx", index=False)
    window['-stepwise-'].update("spreadsheet generated")
    print('all done')

SG.theme("DarkGreen5")
layout = [
    [
        SG.Push(),
        SG.Text("folder with accession data:"),
        SG.In("", size=(50, 1), visible=True, key="-accession_folder-", tooltip="Folder with accession data, if none exists data will be harvested and placed in this folder"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Text("Choose the repository"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Radio("Zavala", group_id="repo", key="-zavala-", tooltip="For the Zavala Building"),
        SG.Radio("Sam Houston Center", group_id="repo", key="-shc-", tooltip="For the Sam Houston Center"),
        SG.Radio("Review", group_id="repo", key="-review-", tooltip="For the Review"),
        SG.Radio("Legislative records", group_id="repo", key="-leg-", tooltip="For legislative records, currently in custody of the LRL"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("folder to put the log files"),
        SG.In("", size=(50, 1), visible=True, key="-log_folder-", tooltip="Folder to put the log files in"),
        SG.FolderBrowse()
    ],
    [
        SG.Button("Close", tooltip="Close the application")
    ],
    [
        SG.Push(),
        SG.Button("Execute", tooltip="Execute the application"),
        SG.Push()
    ],
    [
        SG.Text("Progress by step count: "),
        SG.Text("Will update on execute", key="-stepwise-"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(1, orientation="h", size=(50, 20), bar_color="dark green", key="-Step_progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Progress within Step"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(1, orientation="h", size=(50, 20), bar_color="dark red", key="-Instep_progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Click execute to start it up, return to close\n----------------", size=(90, 5), auto_refresh=True, key="-OUTPUT-", border_width=5),
        SG.Push()
    ]
]
window = SG.Window("Accession Extent Report", layout, icon=my_icon)

event, values = window.read()
while True:
    event, value = window.read()
    to_crawl = values["-accession_folder-"]
    repo = "2"
    if values["-zavala-"] is True:
        repo = "2"
    if values['-shc-'] is True:
        repo = '11'
    if values["-review-"] is True:
        repo = '12'
    if values['-leg-'] is True:
        repo = "13"
    log_folder = values["-log_folder-"]
    if event == "Execute":
        generate_access_extent_report(to_crawl=to_crawl, repo=repo, logs_folder=log_folder)
        window['-stepwise-'].update("Will update on execute")
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()
