import sys
import daterangeparser
import datetime
import lxml.etree as ET
import re
import PySimpleGUI as Sg
import traceback
import os

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


def subjectspace(subject):
    while subject.startswith(" "):
        subject = subject[1:]
    while subject.endswith(" "):
        subject = subject[:-1]
    if subject.endswith("."):
        subject = subject[:-1]
    subject = subject.replace(" -- ", "--")
    return subject


def subarea(subject):
    placeholder = subject.split(". ")
    placeholder2 = placeholder[0]
    if len(placeholder) != 1:
        placeholder2 = placeholder2 + ". "
        for item in placeholder[1:]:
            while item.startswith(" "):
                item = item[1:]
            placeholder2 = placeholder2 + "<subarea>" + item + ".</subarea> "
        placeholder2 = placeholder2[:-12] + "</subarea>"
    placeholder2 = placeholder2.replace("..", ".")
    return placeholder2


def timeturner(dateify):
    dateify2 = dateify
    if dateify == "undated" or dateify == "undated," or dateify == "undated, " or dateify == 'n.d.' or dateify == "Undated" or dateify == 'date unknown':
        dateify = "2021"
    dateify = dateify.replace("bulk", "").replace("(not inclusive)", "").replace("and undated", "").replace("undated",
                                                                                                            "").replace(
        ":", "").replace(" part II", "").replace(" part I", "")
    dateify = dateify.replace("about", "").replace("\n", '').replace("[", '').replace("]", '').replace("ca.",
                                                                                                       '').replace(
        'week of', '').replace(";", '').replace("thru", "-")
    dateify = dateify.replace("and", "-").replace("primarily", "").replace(" or ", "-").replace("(?),", "").replace(
        "(?)", "").replace("(", '').replace(")", '').replace("?", "").replace("filmed on ", '')
    if dateify.endswith(" - 1944"):
        dateify = dateify.replace(" - 1944", "1944")
    if dateify.endswith(" '46") or dateify.endswith(" '44"):
        dateify = dateify[:-3] + "19" + dateify[-2:]
    # process comma-separate months of the same year
    A = "January"
    B = "February"
    C = "March"
    D = "April"
    E = "May"
    F = "June"
    G = "July"
    H = "August"
    I = "September"
    J = "October"
    K = "November"
    L = "December"
    dateify = dateify.replace(A + ", " + B, A + "-" + B).replace(A + ", " + C, A + "-" + C).replace(A + ", " + D,
                                                                                                    A + "-" + D).replace(
        A + ", " + E, A + "-" + E).replace(A + ", " + F, A + "-" + F).replace(A + ", " + G, A + "-" + G).replace(
        A + ", " + H, A + "-" + H).replace(A + ", " + I, A + "-" + I).replace(A + ", " + J, A + "-" + J).replace(
        A + ", " + K, A + "-" + K).replace(A + ", " + L, A + "-" + L)
    dateify = dateify.replace(B + ", " + C, B + "-" + C).replace(B + ", " + D, B + "-" + D).replace(B + ", " + E,
                                                                                                    B + "-" + E).replace(
        B + ", " + F, B + "-" + F).replace(B + ", " + G, B + "-" + G).replace(B + ", " + H, B + "-" + H).replace(
        B + ", " + I, B + "-" + I).replace(B + ", " + J, B + "-" + J).replace(B + ", " + K, B + "-" + K).replace(
        B + ", " + L, B + "-" + L)
    dateify = dateify.replace(C + ", " + D, B + "-" + D).replace(C + ", " + E, B + "-" + E).replace(C + ", " + F,
                                                                                                    B + "-" + F).replace(
        C + ", " + G, B + "-" + G).replace(C + ", " + H, B + "-" + H).replace(C + ", " + I, B + "-" + I).replace(
        C + ", " + J, B + "-" + J).replace(C + ", " + K, B + "-" + K).replace(C + ", " + L, B + "-" + L)
    dateify = dateify.replace(D + ", " + E, D + "-" + E).replace(D + ", " + F, D + "-" + F).replace(D + ", " + G,
                                                                                                    D + "-" + G).replace(
        D + ", " + H, D + "-" + H).replace(D + ", " + I, D + "-" + I).replace(D + ", " + J, D + "-" + J).replace(
        D + ", " + K, D + "-" + K).replace(D + ", " + L, D + "-" + L)
    dateify = dateify.replace(E + ", " + F, E + "-" + F).replace(E + ", " + G, E + "-" + G).replace(E + ", " + H,
                                                                                                    E + "-" + H).replace(
        E + ", " + I, E + "-" + I).replace(E + ", " + J, E + "-" + J).replace(E + ", " + K, E + "-" + K).replace(
        E + ", " + L, E + "-" + L)
    dateify = dateify.replace(F + ", " + G, F + "-" + G).replace(F + ", " + H, F + "-" + H).replace(F + ", " + I,
                                                                                                    F + "-" + I).replace(
        F + ", " + J, F + "-" + J).replace(F + ", " + K, F + "-" + K).replace(F + ", " + L, F + "-" + L)
    dateify = dateify.replace(G + ", " + H, G + "-" + H).replace(G + ", " + I, G + "-" + I).replace(G + ", " + J,
                                                                                                    G + "-" + J).replace(
        G + ", " + K, G + "-" + K).replace(G + ", " + L, G + "-" + L)
    dateify = dateify.replace(H + ", " + I, H + "-" + I).replace(H + ", " + J, H + "-" + J).replace(H + ", " + K,
                                                                                                    H + "-" + K).replace(
        H + ", " + L, H + "-" + L)
    dateify = dateify.replace(I + ", " + J, I + "-" + J).replace(I + ", " + K, I + "-" + K).replace(I + ", " + L,
                                                                                                    I + "-" + L)
    dateify = dateify.replace(J + ", " + K, J + "-" + K).replace(J + ", " + L, J + "-" + L)
    dateify = dateify.replace(K + ", " + L, K + "-" + L)
    dateify = dateify.replace("-" + A + "-", "-").replace("-" + B + "-", "-").replace("-" + C + "-", "-").replace(
        "-" + D + "-", "-").replace("-" + E + "-", "-").replace("-" + F + "-", "-").replace("-" + G + "-", "-").replace(
        "-" + H + "-", "-").replace("-" + I + "-", "-").replace("-" + J + "-", "-").replace("-" + K + "-", "-")

    # next steps
    donkeykong = re.search(r'\d{2}-\d{2},', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        donkeykong = ", " + donkeykong
        dateify = dateify.replace(donkeykong, donkeykong[-4:])
    donkeykong = re.findall(r'\d{4}-\d{2}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = datetime.datetime.strptime(item, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong, append=True)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{4}-\d{2}-\d{1}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:-1] + "0" + item[-1:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{4}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:5] + "0" + item[5:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{4}-\d{1}-\d{1}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:5] + "0" + item[5:7] + "0" + item[-1:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}/\d{2}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = datetime.datetime.strptime(item, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}-\d{2}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = datetime.datetime.strptime(item, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            # print(dittykong)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}/\d{1}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}-\d{1}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}-\d{2}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}/\d{2}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}/\d{1}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}-\d{1}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}/\d{2}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}-\d{2}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            if dateify.startswith(item):
                dittykong = item[:-2] + "19" + item[-2:]
                dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
                dittykong = dittykong.strftime("%B %d, %Y")
                window['-OUTPUT-'].update("\n" + dittykong, append=True)
                dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}/\d{2}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}-\d{2}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}/\d{1}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{2}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}/\d{1}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.findall(r'\d{1}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item, dittykong)
    donkeykong = re.search(r'FY \d{4}-\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        placeholder = donkeykong.split("-")
        year1 = int(placeholder[0][-4:]) - 1
        year2 = placeholder[1][-4:]
        dittykong = 'September 1, ' + str(year1) + " - August 31, " + year2
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'FY \d{4} - FY \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        placeholder = donkeykong.split(" - ")
        year1 = int(placeholder[0][-4:]) - 1
        year2 = placeholder[1][-4:]
        dittykong = 'September 1, ' + str(year1) + " - August 31, " + year2
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'FY \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'FY\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'FY \d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-2:]) + 1899
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, 19" + donkeykong[-2:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'FY\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-2:]) + 1899
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, 19" + donkeykong[-2:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'\d{4}-\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        if dateify.startswith(donkeykong + ",") or dateify.startswith(donkeykong + " ") or dateify.endswith(donkeykong):
            dittykong = donkeykong[:5] + donkeykong[:2] + donkeykong[-2:]
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'd{2}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong
        dittykong = datetime.datetime.strptime(dittykong, "%m/%Y")
        dittykong = dittykong.strftime("%B, %Y")
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'd{1}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "0" + donkeykong
        dittykong = datetime.datetime.strptime(dittykong, "%m/%Y")
        dittykong = dittykong.strftime("%B, %Y")
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    dateify = dateify.replace("Summer, ", "Summer ").replace("Spring, ", "Spring ").replace("Fall, ", "Fall ").replace(
        "Winter, ", "Winter ")
    donkeykong = re.search(r'Spring \d{4}', dateify, re.IGNORECASE)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "March 1, " + donkeykong[-4:] + " to May 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'Summer \d{4}', dateify, re.IGNORECASE)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "June 1, " + donkeykong[-4:] + " to August 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'Fall \d{4}', dateify, re.IGNORECASE)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "September 1, " + donkeykong[-4:] + " to October 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'Winter \d{4}', dateify, re.IGNORECASE)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "November 1, " + donkeykong[-4:] + " to December 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'before \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = "January 1, 0000 - December 31, " + str(dittykong)
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'after \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong[-4:] + "-" + donkeykong[-4:-2] + "99"
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    donkeykong = re.search(r'\d{4} \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong[:4] + "-" + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong, dittykong)
    dateify.strip()
    while dateify.endswith(".") or dateify.endswith(". "):
        dateify = dateify[:-1]
    while dateify.endswith(", "):
        dateify = dateify[:-2]
    while dateify.endswith(" "):
        dateify = dateify[:-1]
    while dateify.endswith(","):
        dateify = dateify[:-1]
    while dateify.startswith(" "):
        dateify = dateify[1:]
    date_normal = ""
    try:
        window['-OUTPUT-'].update("\n" + "made it this far", append=True)
        # window['-OUTPUT-'].update("\n" + dateify)
        # temp_value = daterangeparser.parse(dateify)
        if "-" in dateify:
            start, end = daterangeparser.parse(dateify)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
            date_normal += start + "/" + end + "/"
        else:
            start, end = daterangeparser.parse(dateify)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
            if end != None:
                date_normal += start + "/" + end + "/"
            else:
                date_normal += start + "/" + start + "/"
        # window['-OUTPUT-'].update("\n" + dateify)
    except:
        listy = dateify.split(",")
        for item in listy:
            while item.startswith(" "):
                item = item[1:]
            if "-early" in item and item.endswith("s"):
                item = item.replace("early", "")
                item = item[:-2] + "4"
            item = item.replace("early", "")
            if item.startswith("late") or item.startswith(" late"):
                silly = item.split("-")
                temp1 = silly[0].replace(" ", "").replace("late", "")
                if "s" in temp1:
                    temp1 = temp1[:-2] + "5"
                try:
                    item = temp1 + "-" + silly[1]
                except:
                    item = temp1
            if item.endswith("0s"):
                if item.startswith("mid-late "):
                    item = item.replace("mid-late ", "")
                    tempy = item[-5:-1]
                    tempy = tempy[:-1] + "5-"
                    item = tempy + item
                item = item[:-2] + "9"
            item = item.replace("s-", " -")
            if item != '':
                try:
                    start, end = daterangeparser.parse(item)
                    start = start.strftime("%Y-%m-%d")
                    if end != None:
                        end = end.strftime("%Y-%m-%d")
                        date_normal += start + "/" + end + "/"
                    else:
                        date_normal += start + "/" + start + "/"
                except:
                    splity = item.split("-")
                    if len(splity) == 1 and len(splity[0]) == 4:
                        date_normal = splity[0] + "-01-01/" + splity[0] + "-12-31/"
                    elif len(splity) == 2 and len(splity[0]) == 4 and len(splity[-1]) == 4:
                        date_normal = splity[0] + "-01-01/" + splity[-1] + "-12-31/"
                    else:
                        window['-OUTPUT-'].update(f"\nfind and fix date at: {dateify2}", append=True)
                        window['-OUTPUT-'].update(f"\nfind and fix date at: {item}", append=True)

    date_normal = date_normal[:-1]
    if date_normal.startswith("/"):
        date_normal = date_normal[1:]
    date_normal = date_normal.split("/")
    date_normal.sort()
    date_normal = date_normal[0] + "/" + date_normal[-1]
    if "-01-01/2021" in date_normal:
        date_normal = date_normal.replace("-01-01/2021", "")
        date_normal = date_normal + "/" + date_normal
    if date_normal == "/":
        date_normal = "0000/0000"
    if date_normal == "2021-01-01/2021-12-31" or date_normal == "2021-12-31/2021-12-31":
        date_normal = "0000/0000"
    if "January 1, 0000" in dateify:
        donkeykong = re.search(r'\d{4}-\d{2}-\d{2}/', date_normal)
        donkeykong = str(donkeykong[0])
        date_normal = date_normal.replace(donkeykong, "0000/")
    return date_normal

def encodinganaloger(taglist, analog):
    top_list = ['ead:archdesc', 'ead:descgrp', 'archdesc', 'descgrp']
    for x in taglist:
        parent = x.getparent()
        if parent.tag in top_list:
            x.attrib['encodinganalog'] = analog
    return taglist

def copy_attributes(target, source):
    if source.attrib:
        for key in source.attrib.keys():
            target.attrib[key] = source.attrib[key]
def normalize_source(source):
    if source == "Library of Congress Cubject Headings":
        source = "lcsh"
    if source == "naf":
        source = "lcnaf"
    if source == "":
        source = "lcnaf"
    return source

html_transform = ET.XML('''
<!-- EAD 2002 print stylesheet for the Texas State Archives, Nancy Enneking, January 2003-->
<!--  This stylesheet generates Style 4 which is intended to produce print output.  -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:ead="urn:isbn:1-931666-22-9" xmlns:xlink="http://www.w3.org/1999/xlink">
	<xsl:output omit-xml-declaration="yes" indent="yes"/>
	<xsl:strip-space elements="*"/>  

  <!-- Creates the body of the finding aid.-->
  <xsl:template match="/">
    <xsl:variable name="file">
			<xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>
    <html>
      <head>
        <style>
          h1,
          h2,
          h3{
              font-family:arial
          }</style>

        <title>
					<xsl:value-of select="normalize-space(ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:titleproper)"/>
          <xsl:text>  </xsl:text>
					<xsl:value-of select="normalize-space(ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:subtitle)"/>
        </title>
      </head>

      <body bgcolor="#FAFDD5">
        <xsl:call-template name="body"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template name="sponsor">
		<xsl:for-each select="ead:ead/ead:eadheader//ead:sponsor">
      <table width="100%">
        <tr>
					<td width="5%"/>
          <td width="25%" valign="top">
            <strong>
              <xsl:text>Sponsor: </xsl:text>
            </strong>
          </td>
          <td width="70%">						
						<xsl:apply-templates/>
          </td>
        </tr>
      </table>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="body">
    <xsl:variable name="file">
			<xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <xsl:call-template name="eadheader"/>
    <xsl:call-template name="archdesc-did"/>
		<xsl:call-template name="sponsor"/>
		<hr/>
    <xsl:call-template name="archdesc-bioghist"/>
    <xsl:call-template name="archdesc-scopecontent"/>
    <xsl:call-template name="archdesc-arrangement"/>
    <xsl:call-template name="archdesc-restrict"/>
    <xsl:call-template name="archdesc-control"/>
    <xsl:call-template name="archdesc-relatedmaterial"/>
    <xsl:call-template name="archdesc-admininfo"/>
    <xsl:call-template name="archdesc-otherfindaid"/>
    <xsl:call-template name="archdesc-index"/>
    <xsl:call-template name="archdesc-odd"/>
    <xsl:call-template name="archdesc-bibliography"/>
    <xsl:call-template name="dsc"/>
  </xsl:template>
  <xsl:template name="eadheader">
		<xsl:for-each select="ead:ead/ead:eadheader">
		<br/>
			<h2 style="text-align:center">
			    <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:titleproper"/>
      </h2>
			<h3 style="text-align:center">
			  <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:subtitle"/>
      </h3>

      <br/>
      <br/>

      <center>
        <xsl:value-of select="ead:filedesc/ead:titlestmt/ead:author"/>
      </center>
      <br/>
      <br/>

      <center>
        <b>
          <xsl:value-of select="ead:filedesc/ead:publicationstmt/ead:publisher"/>
        </b>
      </center>
      <br/>
      <center> 
        <img 
          src="https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg"
        />
      </center>
      <br/>
      <center>
        <b>
          <xsl:value-of select="ead:filedesc/ead:publicationstmt/ead:address/ead:addressline"/>
        </b>
      </center>
      <br/>
      <br/>

      <xsl:for-each select="ead:profiledesc/ead:creation">
        <center>
          <xsl:value-of select="text()"/>
        </center>
        <xsl:for-each select="ead:date">
          <center>
            <xsl:value-of select="text()"/>
          </center>
          <br/>


        </xsl:for-each>
      </xsl:for-each>
    </xsl:for-each>


  </xsl:template>


  <!-- The following templates format the display of various RENDER attributes.-->

  <xsl:template match="*/ead:title">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*/ead:emph">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*/ead:container">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*[@altrender='reveal']">
    <xsl:value-of select="."/>
  </xsl:template>

  <xsl:template match="*[@render='bold']">
    <b>
      <xsl:value-of select="."/>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='italic']">
    <i>
      <xsl:value-of select="."/>
    </i>
  </xsl:template>

  <xsl:template match="*[@render='underline']">
    <u>
      <xsl:value-of select="."/>
    </u>
  </xsl:template>

  <xsl:template match="*[@render='sub']">
    <sub>
      <xsl:value-of select="."/>
    </sub>
  </xsl:template>

  <xsl:template match="*[@render='super']">
    <super>
      <xsl:value-of select="."/>
    </super>
  </xsl:template>

  <xsl:template match="*[@render='doublequote']">
    <xsl:text>"</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>"</xsl:text>
  </xsl:template>

  <xsl:template match="*[@render='singlequote']">
    <xsl:text>'</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>'</xsl:text>
  </xsl:template>

  <xsl:template match="*[@render='doubleboldquote']">
    <b>
      <xsl:text>"</xsl:text>
      <xsl:value-of select="."/>
      <xsl:text>"</xsl:text>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldsinglequote']">
    <b>
      <xsl:text>'</xsl:text>
      <xsl:value-of select="."/>
      <xsl:text>'</xsl:text>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldunderline']">
    <b>
      <u>
        <xsl:value-of select="."/>
      </u>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='bolditalic']">
    <b>
      <i>
        <xsl:value-of select="."/>
      </i>
    </b>
  </xsl:template>

  <xsl:template match="*[@render='boldsmcaps']">
    <font style="font-variant: small-caps">
      <b>
        <xsl:value-of select="."/>
      </b>
    </font>
  </xsl:template>

  <xsl:template match="*[@render='smcaps']">
    <font style="font-variant: small-caps">
      <xsl:value-of select="."/>
    </font>
  </xsl:template>

  <!-- This template converts an "archref" element into an HTML anchor.-->

  <xsl:template match="*/ead:archref[@xlink:show='replace']">
				<a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:archref[@xlink:show='new']">
				<a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>
  
  <!-- This template converts an "bibref" element into an HTML anchor.-->
  
  <xsl:template match="*/ead:bibref[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>
  
  <xsl:template match="*/ead:bibref[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <!-- This template converts an "extptr" element into an HTML anchor.-->

  <xsl:template match="*/ead:extptr[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:extptr[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <!-- This template converts a "dao" element into an HTML anchor.-->
  <!-- <dao linktype="simple" href="http://www.lib.utexas.edu/benson/rg/atitlan.jpg" actuate="onrequest" show="new"/> -->

  <xsl:template match="*/ead:dao[@xlink:show='replace']">
    <xsl:choose>
      <xsl:when test="@xlink:title">
        <img src="{@xlink:href}" alt="{@xlink:title}"/>
      </xsl:when>
      <xsl:otherwise>
        <img src="{@xlink:href}"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="*/ead:dao[@xlink:show='new']">
    <xsl:choose>
      <xsl:when test="@xlink:title">
        <a href="{@xlink:href}" target="_blank">
          <xsl:value-of select="@xlink:title"/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <a href="{@xlink:href}" target="_blank">
          <xsl:value-of select="@xlink:href"/>
        </a>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- This template converts an "extref" element into an HTML anchor.-->

  <xsl:template match="*/ead:extref[@xlink:show='replace']">
    <a href="{@xlink:href}" target="_self">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="*/ead:extref[@xlink:show='new']">
    <a href="{@xlink:href}" target="_blank">
      <xsl:apply-templates/>
    </a>
  </xsl:template>
  <!--This template rule formats a list element.-->
  <xsl:template match="*/ead:list">
    <xsl:for-each select="ead:head">
      <xsl:apply-templates select="."/>
    </xsl:for-each>
    <xsl:for-each select="ead:item">
      <p style="margin-left: 60pt">
        <xsl:apply-templates/>
      </p>
    </xsl:for-each>
  </xsl:template>

  <!--Formats a simple table. The width of each column is defined by the colwidth attribute in a colspec element. Note we set our table width to 90 percent.-->
  <xsl:template match="*/ead:table">
    <xsl:for-each select="ead:tgroup">
      <table width="20%">
        <tr>
					<xsl:for-each select="ead:colspec">
            <td width="{@colwidth}"/>
          </xsl:for-each>
        </tr>
				<xsl:for-each select="ead:thead">
					<xsl:for-each select="ead:row">
            <tr>
              <xsl:for-each select="ead:entry">
                <td valign="top">
                  <b>
                    <xsl:value-of select="."/>
                  </b>
                </td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each select="ead:tbody">
          <xsl:for-each select="ead:row">
            <tr>
              <xsl:for-each select="ead:entry">
                <td valign="top">
                  <xsl:value-of select="."/>
                </td>
              </xsl:for-each>
            </tr>
          </xsl:for-each>
        </xsl:for-each>
      </table>
    </xsl:for-each>
  </xsl:template>



  <!--This template rule formats the top-level did element.-->
  <xsl:template name="archdesc-did">
    <xsl:variable name="file">
      <xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <!--For each element of the did, this template inserts the value of the LABEL attribute or, if none is present, a default value.-->

    <xsl:for-each select="ead:ead/ead:archdesc/ead:did">
      <table width="100%">
        <tr>
          <td width="5%"> </td>
          <td width="25%"> </td>
          <td width="70%"> </td>
        </tr>
        <tr>
          <td colspan="3">
            <h3>
              <xsl:apply-templates select="ead:head"/>
            </h3>
          </td>
        </tr>

        <xsl:if test="ead:origination[string-length(text()|*)!=0]">
          <xsl:for-each select="ead:origination">
            <xsl:choose>
              <xsl:when test="@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="@label"/>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:when>
              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:text>Creator: </xsl:text>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>
        </xsl:if>

        <!-- Tests for and processes various permutations of unittitle and unitdate.-->
        <xsl:for-each select="ead:unittitle">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="text() |* [not(self::ead:unitdate)]"/>
                </td>
              </tr>
            </xsl:when>
            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Title: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="text() |* [not(self::ead:unitdate)]"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>

          <xsl:if test="child::ead:unitdate">
            <xsl:choose>
              <xsl:when test="./ead:unitdate/@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="./ead:unitdate/@label"/>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="./ead:unitdate"/>
                  </td>
                </tr>
              </xsl:when>
              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:text>Dates: </xsl:text>
                    </b>
                  </td>
                  <td>
                    <xsl:apply-templates select="./ead:unitdate"/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:if>
        </xsl:for-each>

        <!-- Processes the unit date if it is not a child of unit title but a child of did, the current context.-->
        <xsl:if test="ead:unitdate">
          <tr>
            <td/>
            <xsl:for-each select="ead:unitdate[@type='inclusive']">
              <xsl:choose>
                <xsl:when test="position()=1">
                  <td valign="top">
                    <strong>
                      <xsl:text>Dates: </xsl:text>
                    </strong>
                  </td>
                  <xsl:text disable-output-escaping="yes">&#60;td valign="top"&#62;</xsl:text>
                  <xsl:apply-templates/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates/>
                </xsl:otherwise>
              </xsl:choose>
              
            </xsl:for-each>
            <xsl:text disable-output-escaping="yes">&#60;/td&#62;</xsl:text>
          </tr>
          <tr>
            <td/>
            <xsl:for-each select="ead:unitdate[@type='bulk']">
              <xsl:choose>
                <xsl:when test="position()=1">
                  <td valign="top">
                    <strong>
                      <xsl:text>Dates (Bulk): </xsl:text>
                    </strong>
                  </td>
                  <xsl:text disable-output-escaping="yes">&#60;td valign="top"&#62;</xsl:text>
                  <xsl:apply-templates/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:apply-templates/>
                </xsl:otherwise>
              </xsl:choose>
              
            </xsl:for-each>
            <xsl:text disable-output-escaping="yes">&#60;/td&#62;</xsl:text>
          </tr>
          
        </xsl:if>

        <xsl:if test="ead:abstract[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:abstract"/>
                </td>
              </tr>
            </xsl:when>
            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Abstract: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:abstract"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:physdesc[string-length(text()|*)!=0]">
		<xsl:for-each select="ead:physdesc">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Quantity: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
		  </xsl:for-each>
        </xsl:if>


        <xsl:if test="ead:unitid[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:unitid"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>TSLAC Control No.: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:unitid"/>

                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>

        <xsl:if test="ead:physloc[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:physloc"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Location: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:physloc"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:langmaterial[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:langmaterial"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Language: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:langmaterial"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:repository[string-length(text()|*)!=0]">
          <xsl:choose>
            <xsl:when test="@label">
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:value-of select="@label"/>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:repository"/>
                </td>
              </tr>
            </xsl:when>

            <xsl:otherwise>
              <tr>
                <td> </td>
                <td valign="top">
                  <b>
                    <xsl:text>Repository: </xsl:text>
                  </b>
                </td>
                <td>
                  <xsl:apply-templates select="ead:repository"/>
                </td>
              </tr>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if>


        <xsl:if test="ead:note[string-length(text()|*)!=0]">
          <xsl:for-each select="ead:note">
            <xsl:choose>
              <xsl:when test="@label">
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>
                      <xsl:value-of select="@label"/>
                    </b>
                  </td>
                </tr>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td> </td>
                    <td valign="top">
                      <xsl:apply-templates/><xsl:text>&#xa;</xsl:text>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:when>

              <xsl:otherwise>
                <tr>
                  <td> </td>
                  <td valign="top">
                    <b>Location:</b>
                  </td>
                  <td>
                    <xsl:apply-templates select="ead:note"/>
                  </td>
                </tr>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>
        </xsl:if>
      </table>
    </xsl:for-each>
  </xsl:template>

  <!--This template rule formats the top-level bioghist element.-->
  <xsl:template name="archdesc-bioghist">
    <xsl:variable name="file">
      <xsl:value-of select="ead:ead/ead:eadheader/ead:eadid"/>
    </xsl:variable>

    <xsl:if test="ead:ead/ead:archdesc/ead:bioghist[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:bioghist">
        <xsl:apply-templates/>
        <hr/>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:head">
    <h3>
      <xsl:apply-templates/>
    </h3>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:p">
    <p style="margin-left: 30pt">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:chronlist">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:bioghist/ead:bioghist">
    <h3>
      <xsl:apply-templates select="ead:head"/>
    </h3>
    <xsl:for-each select="ead:p">
      <p style="margin-left: 30pt">
        <xsl:apply-templates select="."/>
      </p>
    </xsl:for-each>
  </xsl:template>

  <!--This template rule formats a chronlist element.-->
  <xsl:template match="*/ead:chronlist">
    <table width="100%">
      <tr>
        <td width="5%"> </td>
        <td width="30%"> </td>
        <td width="65%"> </td>
      </tr>

      <xsl:for-each select="ead:listhead">
        <tr>
          <td>
            <b>
              <xsl:apply-templates select="ead:head01"/>
            </b>
          </td>
          <td>
            <b>
              <xsl:apply-templates select="ead:head02"/>
            </b>
          </td>
        </tr>
      </xsl:for-each>

      <xsl:for-each select="ead:chronitem">
        <tr>
          <td/>
          <td valign="top">
            <xsl:apply-templates select="ead:date"/>
          </td>
          <td valign="top">
            <xsl:apply-templates select="ead:event"/>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>



  <!--This template rule formats the scopecontent element.-->
  <xsl:template name="archdesc-scopecontent">
    <xsl:if test="ead:ead/ead:archdesc/ead:scopecontent[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:scopecontent">
        <xsl:apply-templates/>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:head">
    <h3>
      <xsl:apply-templates/>
    </h3>
  </xsl:template>

  <!-- This formats an organization list embedded in a scope content statement.-->
  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:organization">
    <xsl:for-each select="ead:p">
      <p style="margin-left: 30pt">
        <xsl:apply-templates select="."/>
      </p>
    </xsl:for-each>
    <xsl:for-each select="ead:list">
      <xsl:for-each select="ead:item">
        <p style="margin-left: 60pt">
          <xsl:value-of select="."/>
        </p>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="ead:ead/ead:archdesc/ead:scopecontent/ead:p">
    <p style="margin-left: 30pt">
      <xsl:apply-templates/>
    </p>
  </xsl:template>



  <!--This template rule formats the arrangement element.-->
  <xsl:template name="archdesc-arrangement">
    <xsl:if test="ead:ead/ead:archdesc/ead:arrangement[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:arrangement">
        <table width="100%">
          <tr>
            <td width="5%"/>
            <td width="5%"/>
            <td width="90%"/>
          </tr>

          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>

          <tr>
            <td/>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>

          <xsl:for-each select="ead:list">
            <tr>
              <td/>
              <td colspan="2">
                <xsl:apply-templates select="ead:head"/>
              </td>
            </tr>
            <xsl:for-each select="ead:item">
              <tr>
                <td/>
                <td/>
                <td colspan="1">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>

        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level relatedmaterial element.-->
  <xsl:template name="archdesc-relatedmaterial">
    <xsl:if
      test="ead:ead/ead:archdesc/ead:relatedmaterial[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:separatedmaterial[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:relatedmaterial | ead:ead/ead:archdesc/ead:separatedmaterial">
        <table width="100%">
          <tr>
            <td width="5%"> </td>
            <td width="5%"> </td>
            <td width="90%"> </td>
          </tr>

          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>

          <tr>
            <td/>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>

          <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
            <tr>
              <td> </td>
              <td colspan="2">
                <b>
                  <xsl:apply-templates select="ead:p"/>
                </b>
              </td>
            </tr>

            <xsl:for-each select="ead:note ">
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>

            <xsl:for-each select="ead:archref | ead:bibref ">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level otherfindaid element.-->
  <xsl:template name="archdesc-otherfindaid">
    <xsl:if test="ead:ead/ead:archdesc/ead:otherfindaid[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:otherfindaid">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="archdesc-control">
    <xsl:if test="ead:ead/ead:archdesc/ead:controlaccess[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:controlaccess">
        <table width="100%">
          <tr>
            <td width="5%"> </td>
            <td width="5%"> </td>
            <td width="90%"> </td>
          </tr>
          <tr>
            <td colspan="3">
              <h3>
                <xsl:apply-templates select="ead:head"/>
              </h3>
            </td>
          </tr>
          <tr>
            <td> </td>
            <td colspan="2">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>
          <xsl:for-each select="./ead:controlaccess">
            <tr>
              <td> </td>
              <td colspan="2">
                <b>
                  <xsl:apply-templates select="ead:head"/>
                </b>
              </td>
            </tr>
            <xsl:for-each
              select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td>
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats a top-level access/use/phystech retrict element.-->
  <xsl:template name="archdesc-restrict">
    <xsl:if
      test="ead:ead/ead:archdesc/ead:accessrestrict[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:userestrict[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:phystech[string-length(text()|*)!=0]">
      <h3>
        <b>
          <xsl:text>Restrictions and Requirements</xsl:text>
        </b>
      </h3>
      <xsl:for-each
        select="ead:ead/ead:archdesc/ead:accessrestrict | ead:ead/ead:archdesc/ead:userestrict | ead:ead/ead:archdesc/ead:phystech">
        <h4 style="margin-left : 15pt">
          <b>
            <xsl:value-of select="ead:head"/>
          </b>
        </h4>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level index element.-->
  <xsl:template name="archdesc-index">
    <xsl:if test="ead:ead/ead:archdesc/ead:index[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:index">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
        <xsl:for-each select="ead:indexentry">
          <p style="margin-left: 60pt">
            <xsl:value-of select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>

  <!--This template rule formats the top-level bibliography element.-->
  <xsl:template name="archdesc-bibliography">
    <xsl:if test="ead:ead/ead:archdesc/ead:bibliography[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:bibliography">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <xsl:for-each select="ead:bibref">
            <p style="margin-left : 30pt">
              <xsl:apply-templates select="."/>
            </p>
          </xsl:for-each>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


  <!--This template rule formats the top-level odd element.-->
  <xsl:template name="archdesc-odd">
    <xsl:if test="ead:ead/ead:archdesc/ead:odd[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:odd">
        <h3>
          <b>
            <xsl:apply-templates select="ead:head"/>
          </b>
        </h3>
        <xsl:for-each select="ead:p">
          <p style="margin-left : 30pt">
            <xsl:apply-templates select="."/>
          </p>
        </xsl:for-each>
      </xsl:for-each>
      <hr/>
    </xsl:if>
  </xsl:template>


	<xsl:template name="archdesc-admininfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:accruals[string-length(text()|*)!=0]">
			<h3>
				<a name="adminlink">
					<xsl:text>Administrative Information</xsl:text>
				</a>
			</h3>
			<xsl:call-template name="archdesc-custodhist"/>
			<xsl:call-template name="archdesc-prefercite"/>
			<xsl:call-template name="archdesc-acqinfo"/>
			<xsl:call-template name="archdesc-processinfo"/>
			<xsl:call-template name="archdesc-appraisal"/>
			<xsl:call-template name="archdesc-accruals"/>
			<xsl:call-template name="archdesc-altform"/>
			<xsl:call-template name="archdesc-originalsloc"/>
			<hr/>
		</xsl:if>
	</xsl:template>


	<!--This template rule formats a top-level custodhist element.-->
	<xsl:template name="archdesc-custodhist">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:custodhist | ead:ead/ead:archdesc/ead:custodhist | ead:ead/ead:archdesc/ead:descgrp/ead:custodhist">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level altformavail element.-->
	<xsl:template name="archdesc-altform">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:altformavail | ead:ead/ead:archdesc/ead:altformavail | ead:ead/ead:archdesc/ead:descgrp/ead:altformavail">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level originalsloc element.-->
	<xsl:template name="archdesc-originalsloc">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:originalsloc | ead:ead/ead:archdes/ead:coriginalsloc | ead:ead/ead:archdesc/ead:descgrp/ead:originalsloc">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level prefercite element.-->
	<xsl:template name="archdesc-prefercite">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:prefercite | ead:ead/ead:archdesc/ead:prefercite | ead:ead/ead:archdesc/ead:descgrp/ead:prefercite">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level acqinfo element.-->
	<xsl:template name="archdesc-acqinfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:acqinfo | ead:ead/ead:archdesc/ead:acqinfo | ead:ead/ead:archdesc/ead:descgrp/ead:acqinfo">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level procinfo element.-->
	<xsl:template name="archdesc-processinfo">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:processinfo | ead:ead/ead:archdesc/ead:processinfo | ead:ead/ead:archdesc/ead:descgrp/ead:processinfo">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level appraisal element.-->
	<xsl:template name="archdesc-appraisal">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:appraisal | ead:ead/ead:archdesc/ead:appraisal | ead:ead/ead:archdesc/ead:descgrp/ead:appraisal">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in30">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<!--This template rule formats a top-level accruals element.-->
	<xsl:template name="archdesc-accruals">
		<xsl:if
			test="ead:ead/ead:archdesc/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals[string-length(text()|*)!=0] | ead:ead/ead:archdesc/ead:descgrp/ead:accruals[string-length(text()|*)!=0]">
			<xsl:for-each
				select="ead:ead/ead:archdesc/ead:archdescgrp/ead:accruals | ead:ead/ead:archdesc/ead:accruals | ead:ead/ead:archdesc/ead:descgrp/ead:accruals">
				<xsl:if test="child::ead:head">
					<h4 class="bod-in15">
						<a name="{generate-id(ead:head)}">
							<strong>
								<xsl:apply-templates select="ead:head"/>
							</strong>
						</a>
					</h4>
				</xsl:if>
				<xsl:for-each select="ead:p">
					<p class="bod-in25">
						<xsl:apply-templates select="."/>
					</p>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>

  <xsl:template name="dsc">
    <xsl:if test="ead:ead/ead:archdesc/ead:dsc">
      <xsl:for-each select="ead:ead/ead:archdesc/ead:dsc">
        <xsl:call-template name="dsc-analytic"/>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <xsl:template name="dsc-analytic">
    <h2>
      <xsl:choose>
        <xsl:when test="child::ead:head">
          <xsl:value-of select="ead:head"/>
        </xsl:when>
      </xsl:choose>
    </h2>

    <p style="margin-left: 25 pt">
      <i>
        <xsl:apply-templates select="ead:p"/>
      </i>
    </p>

    <!--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx-->
    <!-- Process each c01.-->
    <xsl:for-each select="ead:c01">

      <table width="100%">
        <tr>
          <td width="15%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
          <td width="7%"> </td>
        </tr>

        <xsl:for-each select="ead:did">
          <tr>
            <td colspan="14">
              <h3>
                <xsl:call-template name="component-did"/>
              </h3>
            </td>
          </tr>

          <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
            <xsl:for-each select="ead:abstract | ead:note">
              <tr>
                <td/>
                <td colspan="13" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:if>
        </xsl:for-each>


        <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:p">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:list/ead:item">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each select="ead:dao">
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="."/>
            </td>
          </tr>
        </xsl:for-each>


        <xsl:for-each select="ead:controlaccess">

          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>
          <xsl:for-each select="./ead:controlaccess">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <b>
                  <xsl:apply-templates select="ead:head"/>
                </b>
              </td>
            </tr>
            <xsl:for-each
              select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>
        
        <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">

          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <tr>
            <td/>
            <td colspan="13" valign="top">
              <xsl:apply-templates select="ead:p"/>
            </td>
          </tr>
          
          <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="ead:note ">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:archref | ead:bibref">
              <xsl:sort select="."/>
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>

        <xsl:for-each
          select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
          <xsl:for-each select="ead:head">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <b>
                  <xsl:apply-templates select="."/>
                </b>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:p">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>
          <xsl:for-each select="ead:archref | ead:bibref | ead:extref">
            <tr>
              <td/>
              <td colspan="13" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>            
          </xsl:for-each>
        </xsl:for-each>

        <!-- Proceses each c02.-->
        <xsl:for-each select="ead:c02">
          <xsl:for-each select="ead:did">


            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c02-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c02-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c02-box-only"/>
              </xsl:otherwise>
            </xsl:choose>



          </xsl:for-each>

          <!-- Process any remaining c02 elements of the type specified.-->

          <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:p">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:list/ead:item">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>

          <xsl:for-each select="ead:dao">
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="."/>
              </td>
            </tr>
          </xsl:for-each>

          <xsl:for-each select="ead:controlaccess">

            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="./ead:controlaccess">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <b>
                    <xsl:apply-templates select="ead:head"/>
                  </b>
                </td>
              </tr>
              <xsl:for-each
                select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                <xsl:sort select="."/>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>


          <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <tr>
              <td/>
              <td/>
              <td colspan="12" valign="top">
                <xsl:apply-templates select="ead:p"/>
              </td>
            </tr>
            <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="ead:note ">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:archref | ead:bibref">
                <xsl:sort select="."/>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>


          <xsl:for-each
            select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
            <xsl:for-each select="ead:head">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <b>
                    <xsl:apply-templates select="."/>
                  </b>
                </td>
              </tr>
            </xsl:for-each>
            <xsl:for-each select="ead:p">
              <tr>
                <td/>
                <td/>
                <td colspan="12" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>


          <!-- Processes each c03.-->
          <xsl:for-each select="ead:c03">
            <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c03-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c03-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c03-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

            </xsl:for-each>

            <!-- Process any remaining c03 elements of the type specified.-->

            <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:p">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:list/ead:item">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>

            <xsl:for-each select="ead:dao">
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="."/>
                </td>
              </tr>
            </xsl:for-each>

            <xsl:for-each select="ead:controlaccess">

              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="./ead:controlaccess">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <b>
                      <xsl:apply-templates select="ead:head"/>
                    </b>
                  </td>
                </tr>
                <xsl:for-each
                  select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                  <xsl:sort select="."/>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>


            <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <tr>
                <td/>
                <td/>
                <td/>
                <td colspan="11" valign="top">
                  <xsl:apply-templates select="ead:p"/>
                </td>
              </tr>
              <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="ead:note ">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>

                <xsl:for-each select="ead:archref | ead:bibref">
                  <xsl:sort select="."/>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>


            <xsl:for-each
              select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
              <xsl:for-each select="ead:head">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <b>
                      <xsl:apply-templates select="."/>
                    </b>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:p">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="11" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>


            <!-- Processes each c04.-->
            <xsl:for-each select="ead:c04">
              <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c04-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c04-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c04-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

              </xsl:for-each>

              <!-- Process any remaining c04 elements of the type specified.-->

              <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:list/ead:item">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>

              <xsl:for-each select="ead:dao">
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="."/>
                  </td>
                </tr>
              </xsl:for-each>
              <xsl:for-each select="ead:controlaccess">

                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="./ead:controlaccess">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <b>
                        <xsl:apply-templates select="ead:head"/>
                      </b>
                    </td>
                  </tr>
                  <xsl:for-each
                    select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                    <xsl:sort select="."/>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>


              <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <tr>
                  <td/>
                  <td/>
                  <td/>
                  <td/>
                  <td colspan="10" valign="top">
                    <xsl:apply-templates select="ead:p"/>
                  </td>
                </tr>
                <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>
                  <xsl:for-each select="ead:note ">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:archref | ead:bibref">
                    <xsl:sort select="."/>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>


              <xsl:for-each
                select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:appraisal | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                <xsl:for-each select="ead:head">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <b>
                        <xsl:apply-templates select="."/>
                      </b>
                    </td>
                  </tr>
                </xsl:for-each>
                <xsl:for-each select="ead:p">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="10" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>
              </xsl:for-each>


              <!-- Processes each c05-->
              <xsl:for-each select="ead:c05">
                <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c05-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c05-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c05-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                </xsl:for-each>

                <!-- Process any remaining c05 elements of the type specified.-->


                <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:p">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:list/ead:item">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>

                <xsl:for-each select="ead:dao">
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="."/>
                    </td>
                  </tr>
                </xsl:for-each>

                <xsl:for-each select="ead:controlaccess">

                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>

                  <xsl:for-each select="./ead:controlaccess">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <b>
                          <xsl:apply-templates select="ead:head"/>
                        </b>
                      </td>
                    </tr>
                    <xsl:for-each
                      select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                      <xsl:sort select="."/>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>


                <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>

                  <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td/>
                    <td colspan="9" valign="top">
                      <xsl:apply-templates select="ead:p"/>
                    </td>
                  </tr>
                  <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>
                    <xsl:for-each select="ead:note ">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:archref | ead:bibref">
                      <xsl:sort select="."/>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>


                <xsl:for-each
                  select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                  <xsl:for-each select="ead:head">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <b>
                          <xsl:apply-templates select="."/>
                        </b>
                      </td>
                    </tr>
                  </xsl:for-each>
                  <xsl:for-each select="ead:p">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="9" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>


                <!-- Processes each c06-->
                <xsl:for-each select="ead:c06">
                  <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c06-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c06-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c06-box-only"/>
              </xsl:otherwise>
            </xsl:choose>


                  </xsl:for-each>

                  <!-- Process any remaining c06 elements of the type specified.-->

                  <xsl:for-each select="ead:scopecontent | ead:bioghist | ead:arrangement">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:p">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:list/ead:item">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>

                  <xsl:for-each select="ead:dao">
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="."/>
                      </td>
                    </tr>
                  </xsl:for-each>

                  <xsl:for-each select="ead:controlaccess">

                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>

                    <xsl:for-each select="./ead:controlaccess">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <b>
                            <xsl:apply-templates select="ead:head"/>
                          </b>
                        </td>
                      </tr>

                      <xsl:for-each
                        select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                        <xsl:sort select="."/>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>
                  </xsl:for-each>


                  <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <tr>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td/>
                      <td colspan="8" valign="top">
                        <xsl:apply-templates select="ead:p"/>
                      </td>
                    </tr>
                    <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="ead:note ">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:archref | ead:bibref">
                        <xsl:sort select="."/>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>
                  </xsl:for-each>


                  <xsl:for-each
                    select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                    <xsl:for-each select="ead:head">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <b>
                            <xsl:apply-templates select="."/>
                          </b>
                        </td>
                      </tr>
                    </xsl:for-each>
                    <xsl:for-each select="ead:p">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="8" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </xsl:for-each>


                  <!-- Processes each c07.-->
                  <xsl:for-each select="ead:c07">
                    <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c07-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c07-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c07-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                    </xsl:for-each>

                    <!-- Process any remaining c07 elements of the type specified.-->

                    <xsl:for-each select=" ead:scopecontent | ead:bioghist | ead:arrangement">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:p">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:list/ead:item">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>

                    <xsl:for-each select="ead:dao">
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="."/>
                        </td>
                      </tr>
                    </xsl:for-each>

                    <xsl:for-each select="ead:controlaccess">

                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="./ead:controlaccess">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <b>
                              <xsl:apply-templates select="ead:head"/>
                            </b>
                          </td>
                        </tr>
                        <xsl:for-each
                          select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                          <xsl:sort select="."/>
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>
                    </xsl:for-each>


                    <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <tr>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td/>
                        <td colspan="7" valign="top">
                          <xsl:apply-templates select="ead:p"/>
                        </td>
                      </tr>
                      <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="ead:note ">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:archref | ead:bibref">
                          <xsl:sort select="."/>
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>
                    </xsl:for-each>


                    <xsl:for-each
                      select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                      <xsl:for-each select="ead:head">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <b>
                              <xsl:apply-templates select="."/>
                            </b>
                          </td>
                        </tr>
                      </xsl:for-each>
                      <xsl:for-each select="ead:p">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="7" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>
                    </xsl:for-each>


                    <!-- Processes each c08.-->
                    <xsl:for-each select="ead:c08">
                      <xsl:for-each select="ead:did">

            <xsl:variable name="cntr-number" select="ead:container[@type][1]"/>
            <xsl:variable name="cntr-type" select="ead:container[1]/@type"/>
			<xsl:variable name="cntr-number2" select="ead:container[2][@type]"/>
			<xsl:variable name="cntr-type2" select="ead:container[2]/@type"/>

            <xsl:choose>
              <xsl:when
                test="preceding::ead:did[1][ead:container[@type][1]=$cntr-number] and preceding::ead:did[1][ead:container[1]/@type=$cntr-type] or not(./ead:container)">
				<xsl:choose>
					<xsl:when test="preceding::ead:did[1][ead:container[2][@type]=$cntr-number2] and preceding::ead:did[1][ead:container[2]/@type=$cntr-type2] or not(./ead:container[2])">
						<xsl:call-template name="hidebox-c08-box-only"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="showbox-c08-box-only"/>
					</xsl:otherwise>
				</xsl:choose>
              </xsl:when>
              <!-- If it did appear before, hide it here.-->

              <xsl:otherwise>
                <xsl:call-template name="showbox-c08-box-only"/>
              </xsl:otherwise>
            </xsl:choose>

                      </xsl:for-each>

                      <!-- Process any remaining c08 elements of the type specified.-->

                      <xsl:for-each select=" ead:scopecontent | ead:bioghist | ead:arrangement">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:p">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:list/ead:item">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>

                      <xsl:for-each select="ead:dao">
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="."/>
                          </td>
                        </tr>
                      </xsl:for-each>

                      <xsl:for-each select="ead:controlaccess">

                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="./ead:controlaccess">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="5" valign="top">
                              <b>
                                <xsl:apply-templates select="ead:head"/>
                              </b>
                            </td>
                          </tr>
                          <xsl:for-each
                            select="ead:subject | ead:corpname | ead:persname | ead:famname | ead:genreform | ead:title | ead:geogname | ead:occupation | ead:function">
                            <xsl:sort select="."/>
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:for-each>


                      <xsl:for-each select="ead:relatedmaterial | ead:separatedmaterial">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <tr>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td/>
                          <td colspan="6" valign="top">
                            <xsl:apply-templates select="ead:p"/>
                          </td>
                        </tr>
                        <xsl:for-each select="./ead:relatedmaterial | ./ead:separatedmaterial">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="5" valign="top">
                              <xsl:apply-templates select="ead:p"/>
                            </td>
                          </tr>
                          <xsl:for-each select="ead:note ">
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                          <xsl:for-each select="ead:archref | ead:bibref">
                            <xsl:sort select="."/>
                            <tr>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td/>
                              <td colspan="5" valign="top">
                                <xsl:apply-templates select="."/>
                              </td>
                            </tr>
                          </xsl:for-each>
                        </xsl:for-each>
                      </xsl:for-each>


                      <xsl:for-each
                        select="ead:note | ead:accessrestrict | ead:userestrict | ead:phystech | ead:prefercite | ead:acqinfo | ead:originalsloc | ead:processinfo | ead:odd | ead:altformavail | ead:otherfindaid">
                        <xsl:for-each select="ead:head">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <b>
                                <xsl:apply-templates select="."/>
                              </b>
                            </td>
                          </tr>
                        </xsl:for-each>
                        <xsl:for-each select="ead:p">
                          <tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                            <td colspan="6" valign="top">
                              <xsl:apply-templates select="."/>
                            </td>
                          </tr>
                        </xsl:for-each>
                      </xsl:for-each>


                    </xsl:for-each>
                  </xsl:for-each>
                </xsl:for-each>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>
      </table>
      <hr/>
      <br/>
      <br/>

    </xsl:for-each>

  </xsl:template>


  <!-- Shows the container numbers for a c02.-->
  <xsl:template name="showbox-c02-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td colspan="10" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td colspan="9" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c02.-->
  <xsl:template name="hidebox-c02-box-only">
    <tr>
      <td> </td>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td colspan="10" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td colspan="9" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c03.-->
  <xsl:template name="showbox-c03-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="0" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td colspan="9" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td colspan="8" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c03.-->
  <xsl:template name="hidebox-c03-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="0" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td colspan="9" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td colspan="8" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the container number for a c04.-->
  <xsl:template name="showbox-c04-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td colspan="8" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="7" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c04.-->
  <xsl:template name="hidebox-c04-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="1" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td colspan="8" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="7" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c05.-->
  <xsl:template name="showbox-c05-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td colspan="7" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="6" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c05.-->
  <xsl:template name="hidebox-c05-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td colspan="7" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="6" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the container number for a c06.-->
  <xsl:template name="showbox-c06-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="6" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="5" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c06.-->
  <xsl:template name="hidebox-c06-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="6" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="5" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c07.-->
  <xsl:template name="showbox-c07-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="5" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="4" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!--Hides the container number for a c07.-->
  <xsl:template name="hidebox-c07-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="5" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="4" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!-- Shows the box number for a c08.-->
  <xsl:template name="showbox-c08-box-only">
    <tr>
      <td>
        <xsl:for-each select="ead:container[@type][1]">
          <b>
            <font size="-1">
              <xsl:value-of select="@type"/>
            </font>
          </b>
        </xsl:for-each>
        <xsl:for-each select="ead:container[@type][2]">
          <td>
            <b>
              <font size="-1">
                <xsl:value-of select="@type"/>
              </font>
            </b>
          </td>
        </xsl:for-each>
      </td>
    </tr>
    <tr>
      <xsl:if test="ead:container[@type][1]">
        <td valign="top">
          <xsl:apply-templates select="ead:container[@type][1]"/>
        </td>
      </xsl:if>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="4" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="3" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Hides the container number for a c08.-->
  <xsl:template name="hidebox-c08-box-only">
    <tr>
      <td/>
      <xsl:if test="ead:container[@type][2]">
        <td colspan="2" valign="top">
          <xsl:apply-templates select="ead:container[@type][2]"/>
        </td>
      </xsl:if>

      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td/>
      <td colspan="4" valign="top">
        <xsl:call-template name="component-did"/>
      </td>
    </tr>
    <xsl:if test="ead:abstract[string-length(text()|*)!=0] | ead:note[string-length(text()|*)!=0]">
      <xsl:for-each select="ead:abstract | ead:note">
        <tr>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td/>
          <td colspan="3" valign="top">
            <xsl:apply-templates select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>


  <!--Displays unittitle and date information for a component level did.-->
  <xsl:template name="component-did">
    <xsl:if test="ead:unitid">
      <xsl:for-each select="ead:unitid">
        <xsl:apply-templates/>
        <xsl:text>: </xsl:text>
      </xsl:for-each>
    </xsl:if>

    <xsl:choose>
      <xsl:when test="ead:unittitle/ead:unitdate">
        <xsl:for-each select="ead:unittitle">
          <xsl:apply-templates select="text()|*[not(self::ead:unitdate)]"/>
          <xsl:text> </xsl:text>
          <xsl:apply-templates select="./ead:unitdate"/>
        </xsl:for-each>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="ead:unittitle"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="ead:unitdate"/>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:for-each select="ead:dao">
      <xsl:apply-templates select="."/>
    </xsl:for-each>

    <xsl:for-each select="ead:physdesc">
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
      <xsl:text> </xsl:text>
    </xsl:for-each>
    <xsl:for-each select="ead:materialspec">
      <xsl:text> </xsl:text>
      <xsl:apply-templates/>
      <xsl:text> </xsl:text>
    </xsl:for-each>
  </xsl:template>


</xsl:stylesheet>

''')
nsmap = {'xmlns': 'urn:isbn:1-931666-22-9',
         'ead': 'urn:isbn:1-931666-22-9',
         'xlink': 'http://www.w3.org/1999/xlink'}


def processor(my_xml):
    # parse as xslt for application below
    levels = ['c01','c02','c03','c04','c05','c06','c07','c08','c09','c10','c11','c12','c13','c14','c15']
    # set exceptions to how things are to be handled here on down
    exceptions = ['class', 'collection', 'fonds', 'otherlevel', 'recordgrp', 'series', 'subfonds', 'subgrp',
                  'subseries', 'Sub-Series', 'Sub-Group', 'Series']
    high_level = ['collection', 'fonds', 'recordgrp', 'series', 'subfonds', 'subgrp', 'subseries', 'Sub-Series',
                  'Sub-Group', 'Series']
    window["-OUTPUT-"].update(
        "\nthis is supposed to fix a bunch of minor issues related to TARO 2.0 normalization, check output for correctness",
        append=True)
    # window['-OUTPUT-'].update("\n" + "this is supposed to fix a bunch of minor issues related to TARO 2.0 normalization, check output for correctness", append=True)
    temp1 = my_xml.split("/")[-1].split(".")[0]
    temp2 = f"{temp1}-DONOTUSE"
    finished_product = my_xml.replace(temp1, temp2)
    finished_product_removable = finished_product
    error_log = finished_product.replace(f"{temp2}.xml", "change_log.txt")
    # start a rolling text of changes to periodically write to the error log file
    error_text = ""
    with open(my_xml, "r", encoding='utf-8') as r:
        filedata = r.read()
        if "xmlns:ead" not in filedata:
            filedata = filedata.replace('xmlns="', 'xmlns:ead="urn:isbn:1-931666-22-9" xmlns="')
        # filedata = filedata.replace("ead:","ead:")
        with open(finished_product, "w", encoding='utf-8') as w:
            w.write(filedata)
        w.close()
    window['-OUTPUT-'].update(f"\nworking copy of the file created for transformation", append=True)
    with open(finished_product, "r", encoding='utf-8') as r:
        filedata = r.read()
        if "unitid>" not in filedata:
            if "abstract>" in filedata:
                filedata = filedata.replace("abstract>",
                                            "abstract>\n<ead:unitid label='TSLAC Control No.:' countrycode='US' repositorycode='US-tx' encodinganalog='099'></ead:unitid>")
            else:
                filedata = filedata.replace('origination>',
                                            "origination>\n<ead:unitid label='TSLAC Control No.:' countrycode='US' repositorycode='US-tx' encodinganalog='099'></ead:unitid>")
        filedata = filedata.replace('xmlns:xlink', "xmlns_xlink")
        filedata = filedata.replace('xlink:', "xlink_")
        filedata = filedata.replace(' href=""', '')
        filedata = filedata.replace('<ead:unitdate era="ce" calendar="gregorian"/>', '').replace("<unitdate/>",
                                                                                                 '').replace(
            '<unitdate><?xm-replace_text {date}?></unitdate>', '')
        filedata = filedata.replace('xmlns=""', '')
        filedata = filedata.replace("\t", '')
        filedata = filedata.replace("\n", " ")
        # filedata = filedata.replace("> <",">\n<")
        filedata = filedata.replace("><", ">\n<")
        while "  " in filedata:
            filedata = filedata.replace("  ", " ")
        filedata = filedata.replace(",, ", ", ")
    with open(finished_product, "w", encoding='utf-8') as w:
        w.write(filedata)
    w.close()
    error_text += f"initial manual text replacements applied, lxml started\n"
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    unitid_text = temp1
    dom2 = ET.parse(finished_product)
    root = dom2.getroot()
    # de-nest the unitdates from the unittiles as a first step
    myDates = root.xpath(".//ead:unittitle/ead:unitdate", namespaces=nsmap)
    for item in myDates:
        boss = item.getparent()
        boss = boss.getparent()
        boss.append(item)
    # fix the encapsulating ead tag
    header = root.xpath("//ead:ead", namespaces=nsmap)
    for item in header:
        if 'xmlns:ead' in item.attrib:
            item.attrib = item.attrib.pop('xmlns:ead')
        if 'xmlns' not in item.attrib:
            item.attrib['xmlns'] = "urn:isbn:1-931666-22-9"
        item.attrib['relatedencoding'] = "MARC21"
    error_text += f"ead:ead tag attributes addressed\n"
    # remove several things from the output
    remove_list = ["ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:titleproper/ead:num",
                   "ead:ead/ead:eadheader/ead:filedesc/ead:publicationstmt/ead:address",
                   "ead:ead/ead:archdesc/ead:dsc/ead:c01/ead:did/ead:unitid",
                   "ead:relatedmaterial/ead:head",
                   "ead:extent[@altrender='carrier']"]
    for item in remove_list:
        bumps = root.xpath(f".//{item}", namespaces=nsmap)
        if bumps is not None:
            for bump in bumps:
                bump.getparent().remove(bump)
                error_text += f"removed a {item} from the ead file\n"
    #start work on the header content
    # edit attributes for ead:eadheader
    header = root.xpath("//ead:eadheader", namespaces=nsmap)
    for item in header:
        item.attrib['langencoding'] = "iso639-2b"
        item.attrib['audience'] = "internal"
        item.attrib['findaidstatus'] = "edited-full-draft"
        item.attrib['repositoryencoding'] = "iso15511"
        item.attrib['scriptencoding'] = "iso15924"
        item.attrib['dateencoding'] = "iso8601"
        item.attrib['countryencoding'] = "iso3166-1"
        if 'id' in item.attrib:
            item.attrib = item.attrib.pop('id')
    error_text += f"eadheader attributes fixed\n"
    # assign encoding analog to sponsor tags
    sponsors = root.xpath(".//ead:sponsor", namespaces=nsmap)
    for sponsor in sponsors:
        sponsor.attrib['encodinganalog'] = "536"
    #assign encoding analog to eadid
    header = root.xpath("//ead:eadid", namespaces=nsmap)
    for item in header:
        if 'encodinganalog' in item.attrib:
            item.attrib = item.attrib.pop('encodinganalog')
        if 'publicid' in item.attrib:
            item.attrib = item.attrib.pop('publicid')
        item.attrib['countrycode'] = 'US'
        item.attrib['mainagencycode'] = 'US-tx'
    error_text += f"eadid attributes fixed\n"
    # log the actions taken thus far
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    #change ead:odd to ead:note and remove child head
    odd_heads = root.findall(".//ead:odd/ead:head", namespaces=nsmap)
    if odd_heads is not None:
        for odd in odd_heads:
            odd.getparent().remove(odd)
    odds = root.findall(".//ead:odd", namespaces=nsmap)
    if odds is not None:
        for odd in odds:
            odd.tag = "note"
            error_text += "changed an ead:off to an ead:note\n"
    # fix attribute issues with unitid
    unitids = root.xpath(".//ead:archdesc/ead:did/ead:unitid", namespaces=nsmap)
    if unitids is not None:
        for unitid in unitids:
            unitid.attrib['label'] = "TSLAC Control No.:"
            unitid.attrib['countrycode'] = "US"
            unitid.attrib['repositorycode'] = "US-tx"
            unitid.attrib['encodinganalog'] = "099"
            error_text += f"update attributes for unitid {unitid.text}"
    # fix ead:publisher stuff
    publisher = root.find(".//ead:eadheader/ead:filedesc/ead:publicationstmt/ead:publisher/ead:extptr", namespaces=nsmap)
    publisher.attrib['xmlns_xlink'] = "http://www.w3.org/1999/xlink"
    publisher.attrib['xlink_actuate'] = "onLoad"
    publisher.attrib['xlink_show'] = "embed"
    publisher.attrib['xlink_type'] = "simple"
    publisher.attrib['xlink_href'] = "https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg"
    # rephrase creation statement
    # double check that output
    creation = root.find(".//ead:eadheader/ead:profiledesc/ead:creation", namespaces=nsmap)
    author = root.find(".//ead:author", namespaces=nsmap).text
    author = author.split(" ")
    date = root.find(".//ead:publicationstmt/ead:date", namespaces=nsmap).text
    creation.text = f"Finding aid created in ArchivesSpace by {author[-2]} {author[-1]} and exported as EAD Version 2002 as part of the TARO project, "
    creation_date = ET.SubElement(creation, "date")
    creation_date.attrib['calendar'] = "gregorian"
    creation_date.attrib['era'] = "ce"
    creation_date.text = date
    creation.tail = "."
    # fix finding aid creation date issues
    create_date = root.find(".//ead:publicationstmt/ead:date", namespaces=nsmap)
    create_date_text = create_date.text
    creation = root.find(".//ead:creation", namespaces=nsmap)
    creation_text = creation.text
    creation.text = ""
    creation_text = creation_text.replace(f"{create_date_text}.",
                                          f'<date calendar="gregorian" era="ce">{create_date.text}</date>.')
    creation.text = creation_text
    error_text += f"changed ead:creation text to have a subtag and to match publication statement date\n"
    # start work on descrules standard text, add emph if not present
    descrules = root.find(".//ead:descrules", namespaces=nsmap)
    desc_emph = descrules.xpath("./ead:emph", namespaces=nsmap)
    if desc_emph is None:
        descrules.text = "Description based on "
        desc_emph = ET.SubElement(descrules, "emph")
        desc_emph.attrib['render'] = "italic"
        desc_emph.text = "DACS"
        descrules.tail = "."
    # add some attributes for the archdesc tag
    archdesc = root.find(".//ead:archdesc", namespaces=nsmap)
    archdesc.attrib['type'] = "inventory"
    archdesc.attrib['audience'] = 'external'
    #start work on the top level ead:did section
    top_head = archdesc.find("./ead:did/ead:head", namespaces=nsmap)
    if top_head is None:
        headless = archdesc.find("./ead:repository", namespaces=nsmap)
        top_head = ET.Element("head")
        top_head.text = "Overview"
        headless.addprevious(top_head)
    # fix topest-level dates
    dates = root.xpath(".//ead:archdesc/ead:did/ead:unitdate", namespaces=nsmap)
    for date in dates:
        date.attrib['label'] = "Dates:"
        if "type" in date.attrib:
            if date.attrib['type'] == "bulk":
                date.attrib['encodinganalog'] = "245$g"
            else:
                date.attrib['encodinganalog'] = "245$f"
        else:
            # when someone forgot to add date type assume it is inclusive
            date.attrib['type'] = "inclusive"
            date.attrib['encodinganalog'] = "245$f"
    # update attributes of top-level abstract
    abstracts = root.xpath(".//ead:archdesc/ead:did/ead:abstract", namespaces=nsmap)
    for abstract in abstracts:
        abstract.attrib['label'] = "Abstract:"
        abstract.attrib['encodinganalog'] = "520$a"
    # update physdesc attributes of top-level
    physdescs = root.xpath(".//ead:archdesc/ead:did/ead:physdesc", namespaces=nsmap)
    for physdesc in physdescs:
        physdesc.attrib['label'] = "Quantity:"
        physdesc.attrib['encodinganalog'] = "300$a"
    # fix top-level langmaterial attributes
    languages = root.xpath(".//ead:archdesc/ead:did/ead:langmaterial", namespaces=nsmap)
    for language in languages:
        language.attrib['label'] = "Language:"
        language.attrib['encodinganalog'] = "546$a"
        # fix a cdata issue with exported language info
        mylanguage = language.text
        mylanguage = mylanguage.replace("<![CDATA[", "").replace("]]>", "")
        language.text = mylanguage
        error_text += f"CDATA issue addressed in the langmaterial section\n"
    # fix repo attributes
    repositories = root.xpath(".//ead:archdesc/ead:did/ead:repository", namespaces=nsmap)
    for repository in repositories:
        repository.attrib['encodinganalog'] = "852$a"
        # possibility need to manually include here the extref details of the repository, but don't assume yet
        # would be the xlink stuff
    # fix extref attributes across the board
    externals = root.xpath(".//ead:extref", namespaces=nsmap)
    for external in externals:
        external.attrib['xmlns_xlink'] = "http://www.w3.org/1999/xlink"
        external.attrib['xlink_actuate'] = "onRequest"
        external.attrib['xlink_show'] = "new"
        external.attrib['xlink_type'] = "simple"
        if "href" in external.attrib.keys():
            external.attrib['xlink_href'] = external.attrib['href']
            external.attrib.pop("href")
    # add encodinganalog 245 to high level unittitles
    unittitles = root.xpath(".//ead:unittitle", namespaces=nsmap)
    for unittitle in unittitles:
        title_grandpa = unittitle.getparent().getparent()
        if "level" in title_grandpa.attrib:
            if title_grandpa.attrib['level'] in high_level:
                unittitle.attrib['encodinganalog'] = "245"
                error_text += f"added encoding analog to {unittitle.text}\n"
    # add encoding analog and label to top-level unittitle
    top_titles = root.xpath (".//ead:archdesc/ead:did/ead:unittitle", namespaces=nsmap)
    for top_title in top_titles:
        top_title.attrib['encodinganalog'] = "245"
        top_title.attrib['label'] = "Title:"
        error_text += f"label and encodinganalog added to top title {top_title.text}\n"
    # update first origination to compliant formatting
    origination = root.find(".//ead:origination", namespaces=nsmap)
    if not "label" in origination.attrib:
        origination.attrib['label'] = "Creator:"
    else:
        origination.attrib['label'] = f"{origination.attrib['label']}:"
    originator = origination[0]
    if "source" in originator.attrib:
        if originator.attrib['source'] == "Library of Congress Subject Headings":
            originator.attrib['source'] = "lcsh"
        if originator.attrib['source'] == "naf":
            originator.attrib['source'] = "lcnaf"
    else:
        originator.attrib['source'] = "local"
    if "corpname" in originator.tag:
        originator.attrib['encodinganalog'] = "110"
    if "famname" in originator.tag:
        originator.attrib['encodinganalog'] = "100"
    if "persname" in originator.tag:
        originator.attrib['encodinganalog'] = "100"
        print("something")
    error_text += "made necessary modifications to first origination entity\n"
    #start work on the top body of the text
    # nest related materials if present  is no longer necessary based on procedural changes
    relations = root.xpath(".//ead:archdesc/ead:relatedmaterial", namespaces=nsmap)
    if relations is not None:
        error_text += f"related materials sections exist, check to see if nesting is needed\n"
        for relation in relations:
            relation.attrib['encodinganalog'] = "544 1"
            error_text += f"added encoding analog to {relation.text}\n"
    # fix acquisition info attributes
    acquisitions = root.xpath(".//ead:archdesc/ead:acqinfo", namespaces=nsmap)
    if acquisitions is not None:
        for acquisition in acquisitions:
            acquisition.attrib['encodinganalog'] = "541"
            error_text += f"added encoding analog to {acquisition.text}\n"
    # fix custodial history attributes
    custodians = root.xpath(".//ead:archdesc/ead:custodhist", namespaces=nsmap)
    if custodians is not None:
        for custodian in custodians:
            custodian.attrib['encodinganalog'] = "561"
            error_text += f"added encoding analog to {custodian.text}\n"
    # fix accessrestrict attributes
    restrictions = root.xpath(".//ead:archdesc/ead:accessrestrict", namespaces=nsmap)
    if restrictions is not None:
        for restriction in restrictions:
            restriction.attrib['encodinganalog'] = "506"
            error_text += f"added encoding analog to {restriction.text}\n"
    #fix processinginfo tag
    processes = root.xpath(".//ead:archdesc/ead:processinfo", namespaces=nsmap)
    if processes is not None:
        for process in processes:
            process.attrib['encodinganalog'] = "583"
            error_text += f"added encoding analog to {process.text}\n"
    # fix encoding analog on appraisal tag
    appraisals = root.xpath(".//ead:archdesc/ead:appraisal", namespaces=nsmap)
    if appraisals is not None:
        for appraisal in appraisals:
            appraisal.attrib['encodinganalog'] = "583"
            error_text += f"added encoding analog to {appraisal.text}\n"
    # fix encoding analog on separated materials
    separations = root.xpath(".//ead:archdesc/ead:separatedmaterial", namespaces=nsmap)
    if separations is not None:
        for separation in separations:
            separation.attrib['encodinganalog'] = "544 0"
            error_text += f"added encoding analog to {separation.text}\n"
    # fix accruals encoding analog
    accruals = root.xpath(".//ead:archdesc/ead:accruals", namespaces=nsmap)
    if accruals is not None:
        for accrual in accruals:
            accrual.attrib['encodinganalog'] = "584"
            error_text += f"added encoding analog to {accrual.text}\n"
    #fix encoding analog for alternate formats
    formats = root.xpath(".//ead:archdesc/ead:altformavail", namespaces=nsmap)
    if formats is not None:
        for x in formats:
            x.attrib['encodinganalog'] = "530"
            error_text += f"added encoding analog to {x.text}\n"
    # fix originals location
    originals = root.xpath(".//ead:archdesc/ead:originalsloc", namespaces=nsmap)
    if originals is not None:
        for original in originals:
            original.attrib['encodinganalog'] = "535"
            error_text += f"added encoding analog to {original.text}\n"
    # fix encoding analog for usre restrictions
    userrestrictions = root.xpath(".//ead:archdesc/ead:userestrict", namespaces=nsmap)
    if userrestrictions is not None:
        for userrestriction in userrestrictions:
            userrestriction.attrib['encodinganalog'] = "540"
            error_text += f"added encoding analog to {userrestriction.text}\n"
    # fix encoding analog for phystech
    phystechs = root.xpath('.//ead:archdesc/ead:phystech', namespaces=nsmap)
    if phystechs is not None:
        for phystech in phystechs:
            phystech.attrib['encodinganalog'] = "340"
            error_text += f"added encoding analog to {phystech.text}\n"
    # fix enconding analog for arrangement
    arrangements = root.xpath(".//ead:archdesc/ead:arrangement", namespaces=nsmap)
    if arrangements is not None:
        for arrangement in arrangements:
            arrangement.attrib['encodinganalog'] = "351"
            error_text += f"added encoding analog to {arrangement.text}\n"
    # fix encoding analog for preferred citations
    citations = root.xpath(".//ead:archdesc/ead:prefercite", namespaces=nsmap)
    if citations is not None:
        for citation in citations:
            citation.attrib['encodinganalog'] = "524"
            error_text += f"added encoding analog to {citation.text}\n"
    # fix bioghist attributes including id numbers
    bioghistories = root.xpath(".//ead:archdesc/ead:bioghist", namespaces=nsmap)
    counter = 0
    for bioghistory in bioghistories:
        counter += 1
        bioghistory.attrib['id'] = f"bio{str(counter)}"
        bioghistory.attrib['encodinganalog'] = "545"
        error_text += f"added encoding analog to {bioghistory.text}\n"
    contents = root.xpath(".//ead:archdesc/ead:scopecontent", namespaces=nsmap)
    for content in contents:
        content.attrib['encodinganalog'] = "520$b"
        error_text += f"added encoding analog to {content.text}\n"
    # process the controlled access thing
    error_text += f"generating master controlled access section"
    master_arch = root.find(".//ead:dsc", namespaces=nsmap)
    master_control = ET.Element("controlaccess")
    master_arch.addprevious(master_control)
    master_control.attrib['construct'] = "master"
    control_head = ET.SubElement(master_control, "head")
    control_head.text = "Index Terms"
    master_control_p = ET.SubElement(master_control, "p")
    master_control_p_emph = ET.SubElement(master_control_p, "emph")
    master_control_p_emph.attrib['render'] = "italic"
    master_control_p_emph.text = "The terms listed here were used to catalog the records. The terms can be used to find similar or related records."
    # populate family name creators if applicable
    famname_flag = False
    origination_seven_hundreds = root.xpath(".//ead:origination[@label = 'Creator']/ead:famname", namespaces=nsmap)
    if origination_seven_hundreds is not None:
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                famname_flag = True
    if famname_flag is True:
        famname = ET.SubElement(master_control, "controlaccess")
        famname_head = ET.SubElement(famname, "head")
        famname_head.text = "Family Names:"
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                famname_item = ET.SubElement(famname, "famname")
                if "source" in origination_seven_hundred.attrib:
                    if origination_seven_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_seven_hundred.attrib['source'] = "lcsh"
                    if origination_seven_hundred.attrib['source'] == 'naf':
                        origination_seven_hundred.attrib['source'] = "lcnaf"
                    if origination_seven_hundred.attrib['source'] == "":
                        origination_seven_hundred.attrib['source'] = "local"
                if origination_seven_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source attribute in family name {origination_seven_hundred.text}\n"
                copy_attributes(famname_item, origination_seven_hundred)
                subjective = origination_seven_hundred.text
                origination_seven_hundred.text = subjectspace(subjective)
                error_text += f"\tFamily name: {origination_seven_hundred.text} normalized\n"
                famname_item.text = origination_seven_hundred.text
                origination_parent = origination_seven_hundred.getparent()
                origination_parent.getparent().remove(origination_parent)
                famname_item.attrib['encodinganalog'] = "700"
    # clear marker for subject terms to ensure it doesn't get repeated for later
    origination_seven_hundreds = None
    # populate personal name creators if applicable
    persname_flag = False
    origination_seven_hundreds = root.xpath(".//ead:origination[@label = 'Creator']/ead:persname", namespaces=nsmap)
    if origination_seven_hundreds is not None:
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                persname_flag = True
    if persname_flag is True:
        persname = ET.SubElement(master_control, "controlaccess")
        persname_head = ET.SubElement(persname, "head")
        persname_head.text = "Personal Names:"
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                persname_item = ET.SubElement(persname, "persname")
                if "source" in origination_seven_hundred.attrib:
                    if origination_seven_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_seven_hundred.attrib['source'] = "lcsh"
                    if origination_seven_hundred.attrib['source'] == 'naf':
                        origination_seven_hundred.attrib['source'] = "lcnaf"
                    if origination_seven_hundred.attrib['source'] == "":
                        origination_seven_hundred.attrib['source'] = "local"
                if origination_seven_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source in personal name {origination_seven_hundred.text}\n"
                copy_attributes(persname_item, origination_seven_hundred)
                subjective = origination_seven_hundred.text
                origination_seven_hundred.text = subjectspace(subjective)
                error_text += f"\tPersonal name: {origination_seven_hundred.text} normalized\n"
                persname_item.text = origination_seven_hundred.text
                origination_parent = origination_seven_hundred.getparent()
                origination_parent.getparent().remove(origination_parent)
                persname_item.attrib['encodinganalog'] = "700"
    origination_seven_hundreds = None
    # populate corporate name creators if applicable
    corpname_flag = False
    origination_seven_hundreds = root.xpath(".//ead:origination[@label = 'Creator']/ead:corpname", namespaces=nsmap)
    if origination_seven_hundreds is not None:
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                corpname_flag = True
    if corpname_flag is True:
        corpname = ET.SubElement(master_control, "controlaccess")
        corpname_head = ET.SubElement(corpname, "head")
        corpname_head.text = "Corporate Names:"
        for origination_seven_hundred in origination_seven_hundreds:
            if "encodinganalog" not in origination_seven_hundred.attrib:
                corpname_item = ET.SubElement(corpname, "corpname")
                if "source" in origination_seven_hundred.attrib:
                    if origination_seven_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_seven_hundred.attrib['source'] = "lcsh"
                    if origination_seven_hundred.attrib['source'] == 'naf':
                        origination_seven_hundred.attrib['source'] = "lcnaf"
                    if origination_seven_hundred.attrib['source'] == "":
                        origination_seven_hundred.attrib['source'] = "local"
                if origination_seven_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source attribute for corporate name {origination_seven_hundred.text}\n"
                copy_attributes(corpname_item, origination_seven_hundred)
                #corpname_item.attrib = origination_seven_hundred.attrib
                subjective = origination_seven_hundred.text
                subjective = subjectspace(subjective)
                error_text += f"\tcorporate name: {origination_seven_hundred.text} normalized\n"
                origination_seven_hundred.text = subarea(subjective)
                error_text += f"\tcorporate name: {origination_seven_hundred.text} had subarea rules applied to it\n"
                corpname_item.text = origination_seven_hundred.text
                origination_parent = origination_seven_hundred.getparent()
                origination_parent.getparent().remove(origination_parent)
                corpname_item.attrib['encodinganalog'] = "710"
    origination_seven_hundreds = None
    # populate family name subjects if applicable
    famname_flag = False
    origination_six_hundreds = root.xpath(".//ead:archdesc/ead:controlaccess/ead:famname", namespaces=nsmap)
    if origination_six_hundreds is not None:
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                famname_flag = True
    if famname_flag is True:
        famname = ET.SubElement(master_control, "controlaccess")
        famname_head = ET.SubElement(famname, "head")
        famname_head.text = "Subjects (Families):"
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                famname_item = ET.SubElement(famname, "famname")
                if "source" in origination_six_hundred.attrib:
                    if origination_six_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_six_hundred.attrib['source'] = "lcsh"
                    if origination_six_hundred.attrib['source'] == 'naf':
                        origination_six_hundred.attrib['source'] = "lcnaf"
                    if origination_six_hundred.attrib['source'] == "":
                        origination_six_hundred.attrib['source'] = "local"
                if origination_six_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source attribute in {origination_six_hundred.text}\n"
                copy_attributes(famname_item, origination_six_hundred)
                subjective = origination_six_hundred.text
                origination_six_hundred.text = subjectspace(subjective)
                error_text += f"\tFamily name: {origination_six_hundred.text} normalized\n"
                famname_item.text = origination_six_hundred.text
                origination_six_hundred.getparent().remove(origination_six_hundred)
                famname_item.attrib['encodinganalog'] = "600"
    origination_six_hundreds = None
    # populate personal name subjects if applicable
    persname_flag = False
    origination_six_hundreds = root.xpath(".//ead:archdesc/ead:controlaccess/ead:persname", namespaces=nsmap)
    if origination_six_hundreds is not None:
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                persname_flag = True
    if persname_flag is True:
        persname = ET.SubElement(master_control, "controlaccess")
        persname_head = ET.SubElement(persname, "head")
        persname_head.text = "Subjects (Persons):"
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                persname_item = ET.SubElement(persname, "persname")
                if "source" in origination_six_hundred.attrib:
                    if origination_six_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_six_hundred.attrib['source'] = "lcsh"
                    if origination_six_hundred.attrib['source'] == 'naf':
                        origination_six_hundred.attrib['source'] = "lcnaf"
                    if origination_six_hundred.attrib['source'] == "":
                        origination_six_hundred.attrib['source'] = "local"
                if origination_six_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source attribute in {origination_six_hundred.text}\n"
                copy_attributes(persname_item, origination_six_hundred)
                subjective = origination_six_hundred.text
                origination_six_hundred.text = subjectspace(subjective)
                error_text += f"\tcorporate name: {origination_six_hundred.text} normalized\n"
                persname_item.text = origination_six_hundred.text
                origination_six_hundred.getparent().remove(origination_six_hundred)
                persname_item.attrib['encodinganalog'] = "600"
    origination_six_hundreds = None
    # populate corporate name subjects if applicable
    corpname_flag = False
    origination_six_hundreds = root.xpath(".//ead:archdesc/ead:controlaccess/ead:corpname", namespaces=nsmap)
    if origination_six_hundreds is not None:
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                corpname_flag = True
    if corpname_flag is True:
        corpname = ET.SubElement(master_control, "controlaccess")
        corpname_head = ET.SubElement(corpname, "head")
        corpname_head.text = "Subjects (Organizations):"
        for origination_six_hundred in origination_six_hundreds:
            if "encodinganalog" not in origination_six_hundred.attrib:
                corpname_item = ET.SubElement(corpname, "corpname")
                if "source" in origination_six_hundred.attrib:
                    if origination_six_hundred.attrib['source'] == "Library of Congress Subject Headings":
                        origination_six_hundred.attrib['source'] = "lcsh"
                    if origination_six_hundred.attrib['source'] == 'naf':
                        origination_six_hundred.attrib['source'] = "lcnaf"
                    if origination_six_hundred.attrib['source'] == "":
                        origination_six_hundred.attrib['source'] = "local"
                if origination_six_hundred.attrib['source'] == "local":
                    error_text += f"\tlocal source attribute in {origination_six_hundred.text}\n"
                copy_attributes(corpname_item, origination_six_hundred)
                #corpname_item.attrib = origination_seven_hundred.attrib
                subjective = origination_six_hundred.text
                subjective = subjectspace(subjective)
                error_text += f"\tcorporate name: {origination_six_hundred.text} normalized\n"
                origination_six_hundred.text = subarea(subjective)
                error_text += f"\tcorporate name: {origination_six_hundred.text} had subarea rules applied to it\n"
                corpname_item.text = origination_six_hundred.text
                origination_six_hundred.getparent().remove(origination_six_hundred)
                corpname_item.attrib['encodinganalog'] = "610"
    origination_six_hundreds = None
    # populate subject terms if applicable
    subject_flag = False
    subjects = root.xpath(".//ead:archdesc/ead:controlaccess/ead:subject", namespaces=nsmap)
    if subjects is not None:
        for subject in subjects:
            subject_flag = True
            window['-OUTPUT-'].update(f"\n{subject.text}\n", append=True)
    if subject_flag is True:
        subject_section = ET.SubElement(master_control, "controlaccess")
        subjective_head = ET.SubElement(subject_section, "head")
        subjective_head.text = "Subjects:"
        for subject in subjects:
            subject_item = ET.SubElement(subject_section, "subject")
            if "source" in subject.attrib:
                if subject.attrib['source'] == "Library of Congress Subject Headings":
                    subject.attrib['source'] = "lcsh"
                if subject.attrib['source'] == 'naf':
                    subject.attrib['source'] = "lcnaf"
                if subject.attrib['source'] == "":
                    subject.attrib['source'] = "local"
            if subject.attrib['source'] == "local":
                error_text += f"\tlocal source for subject {subject.text}\n"
            copy_attributes(subject_item, subject)
            subjective = subject.text
            subject.text = subjectspace(subjective)
            error_text += f"\tSubject: {subject.text} normalized\n"
            subject_item.text = subject.text
            subject_item.attrib['encodinganalog'] = "650"
            subject.getparent().remove(subject)

    # populate geographic terms if applicable
    geo_flag = False
    geonames = root.xpath(".//ead:controlaccess/ead:geogname", namespaces=nsmap)
    window["-OUTPUT-"].update(f"{geonames}\n", append=True)
    if geonames is not None:
        for geoname in geonames:
            if "encodinganalog" not in geoname.attrib:
                geo_flag = True
    if geo_flag is True:
        geode = ET.SubElement(master_control, "controlaccess")
        geode_head = ET.SubElement(geode, "head")
        geode_head.text = "Places:"
        for geoname in geonames:
            geo_item = ET.SubElement(geode, "geogname")
            if "source" in geoname.attrib:
                if geoname.attrib['source'] == "Library of Congress Subject Headings":
                    geoname.attrib['source'] = "lcsh"
                if geoname.attrib['source'] == 'naf':
                    geoname.attrib['source'] = "lcnaf"
                if geoname.attrib['source'] == "":
                    geoname.attrib['source'] = "local"
            if geoname.attrib['source'] == "local":
                error_text += f"\tlocal source listed for {geoname.text}\n"
            copy_attributes(geo_item, geoname)
            subjective = geoname.text
            geoname.text = subjectspace(subjective)
            error_text += f"\tGeogname: {geoname.text} normalized\n"
            geo_item.text = geoname.text
            geo_item.attrib['encodinganalog'] = "651"
            geoname.getparent().remove(geoname)

    # populate genreform terms if applicable
    genre_flag = False
    genreforms = root.xpath(".//ead:controlaccess/ead:genreform", namespaces=nsmap)
    window["-OUTPUT-"].update(f"{genreforms}\n", append=True)
    if genreforms is not None:
        for genreform in genreforms:
            if "encodinganalog" not in genreform.attrib:
                genre_flag = True
    if genre_flag is True:
        genre = ET.SubElement(master_control, "controlaccess")
        forms_head = ET.SubElement(genre, "head")
        forms_head.text = "Document Types:"
        for formation in genreforms:
            form_item = ET.SubElement(genre, "genreform")
            if "source" in formation.attrib:
                if formation.attrib['source'] == "Library of Congress Subject Headings":
                    formation.attrib['source'] = "lcsh"
                if formation.attrib['source'] == 'naf':
                    formation.attrib['source'] = "lcnaf"
                if formation.attrib['source'] == "":
                    formation.attrib['source'] = "local"
            if formation.attrib['source'] == "local":
                error_text += f"\tlocal source for genreform {formation.text}\n"
            copy_attributes(form_item, formation)
            subjective = formation.text
            formation.text = subjectspace(subjective)
            error_text += f"\tGenreform: {formation.text} normalized\n"
            form_item.text = formation.text
            form_item.attrib['encodinganalog'] = "655"
            formation.getparent().remove(formation)
    # populate title terms if applicable
    title_flag = False
    titles = root.xpath(".//ead:controlaccess/ead:title", namespaces=nsmap)
    if titles is not None:
        for title in titles:
            if "encodinganalog" not in title.attrib:
                title_flag = True
    if title_flag is True:
        control_title = ET.SubElement(master_control, "controlaccess")
        control_title_head = ET.SubElement(control_title, "head")
        control_title_head.text = "Titles:"
        for x in titles:
            titles_item = ET.SubElement(control_title, "title")
            if "source" in x.attrib:
                if x.attrib['source'] == "Library of Congress Subject Headings":
                    x.attrib['source'] = "lcsh"
                if x.attrib['source'] == 'naf':
                    x.attrib['source'] = "lcnaf"
                if x.attrib['source'] == "":
                    x.attrib['source'] = "local"
            copy_attributes(titles_item, x)
            titles_item.text = x.text
            titles_item.attrib['encodinganalog'] = "630"
            x.getparent().remove(x)
    # populate function statement terms if applicable
    function_flag = False
    functionals = root.xpath(".//ead:controlaccess/ead:function", namespaces=nsmap)
    if functionals is not None:
        for functional in functionals:
            if "encodinganalog" not in functional.attrib:
                function_flag = True
    if function_flag is True:
        control_functions = ET.SubElement(master_control, "controlaccess")
        control_functions_head = ET.SubElement(control_functions, "head")
        control_functions_head.text = "Functions:"
        for x in functionals:
            functions_item = ET.SubElement(control_functions, "function")
            if "source" in x.attrib:
                if x.attrib['source'] == "Library of Congress Subject Headings":
                    x.attrib['source'] = "lcsh"
                if x.attrib['source'] == 'naf':
                    x.attrib['source'] = "lcnaf"
                if x.attrib['source'] == "":
                    x.attrib['source'] = "local"
            copy_attributes(functions_item, x)
            functions_item.text = x.text
            functions_item.attrib['encodinganalog'] = "657"
            x.getparent().remove(x)
    # remove not empty control access sections
    controlaccesses = root.xpath(".//ead:controlaccess", namespaces=nsmap)
    for controlaccess in controlaccesses:
        parent = controlaccess.getparent()
        if "construct" not in parent.attrib:
            parent.remove(controlaccess)
        if 'construct' in controlaccess.attrib:
            controlaccess.attrib.pop('construct')
    # sorts subjects, but causes head to sort into the middle so adding a preceding space to get it sort on top, then removing afterwards
    subjects = root.xpath(".//ead:head", namespaces=nsmap)
    for subject in subjects:
        subject.text = " " + subject.text
    for node in root.xpath(".//ead:controlaccess/ead:controlaccess", namespaces=nsmap):
        if node.tag == "head":
            node.text = " " + node.text
        node[:] = sorted(node, key=lambda ch: ch.text)
    subjects = root.xpath(".//ead:head", namespaces=nsmap)
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
    error_text += f"Control access terms sorted alphabetically\n"
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # start subjects tags handling
    flag = 0
    error_text += f"Subjects handled:\n"
    subjects = root.xpath(".//ead:subject", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        # pass subject through subject handler
        subject.text = subjectspace(subjective)
        # strip subject from ead if already handled, otherwise add it to a list to be compared with for other subjects
        error_text += f"\tSubject: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
            error_text += f"\tlocal source attribute in subject {subject.text}\n"
    # start genreform tags handling
    subjects = root.xpath(".//ead:controlaccess/ead:genreform", namespaces=nsmap)
    error_text += f"Genreforms handled:\n"
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        error_text += f"\tGenreform: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
            error_text += f"\tlocal source attribute in genreform {subject.text}\n"
    # start geogname tags handling
    subjects = root.xpath(".//ead:geogname", namespaces=nsmap)
    error_text += f"Geognames handled:\n"
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        error_text += f"\tGeogname: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
            error_text += f"\tlocal source attribute in geogname {subject.text}\n"
    # start function statement handling
    subjects = root.xpath(".//ead:function", namespaces=nsmap)
    error_text += f"Function statements handled:\n"
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        while subjective.endswith("."):
            subjective = subjective[:-1]
        subject.text = subjectspace(subjective)
        error_text += f"\tfunction: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
    # start personal name tag handling
    subjects = root.xpath(".//ead:persname", namespaces=nsmap)
    error_text += f"Personal names handled:\n"
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        error_text += f"\tPersonal name: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
            error_text += f"\tlocal source or lcsh source attribute in {subject.text}\n"
    # start family name handling
    error_text += f"Family names handled:\n"
    subjects = root.xpath(".//ead:famname", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        error_text += f"\tFamily name: {subject.text} normalized\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
            error_text += f"\tlocal source or lcsh source attribute in {subject.text}\n"
    # being corpname handling
    error_text += f"Corporate names handled:\n"
    subjects = root.xpath(".//ead:corpname", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        error_text += f"\tcorporate name: {subject.text} normalized\n"
        if 'encodinganalog' in subject.attrib:
            corp_analog = ['710', '110', '610']
            if subject.attrib['encodinganalog'] in corp_analog:
                subject.text = subarea(subjective)
                error_text += f"\tcorporate name: {subject.text} had subarea rules applied to it\n"
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
            error_text += f"\tlocal source or lcsh source attribute in {subject.text}\n"
    # fix dsc attribute
    dsc = root.find(".//ead:archdesc/ead:dsc", namespaces=nsmap)
    if dsc is not None:
        dsc.attrib['type'] = "combined"
    # add series IDs
    series_counter = 0
    serieses = root.xpath(".//ead:c01", namespaces=nsmap)
    for series in serieses:
        series_counter += 1
        series.attrib['id'] = f"ser{str(series_counter)}"

    # fix unittitle issues
    # remove trailing commas in nested ead:emph
    error_text += f"Titles fixed:\n"
    titles = root.xpath(".//ead:unittitle/ead:emph", namespaces=nsmap)
    if titles is not None:
        for title in titles:
            titliest = title.text
            while titliest.endswith(" "):
                titliest = titliest[:-1]
            while titliest.endswith(","):
                titliest = titliest[:-1]
            if titliest != title.text:
                error_text += f"\t{titliest} punctuation updated\n"
            title.text = titliest
    # now check for and insert trailing comma where appropriate
    titles = root.xpath(".//ead:unittitle", namespaces=nsmap)
    if titles is not None:
        for title in titles:
            parent = title.getparent()
            dates = parent.xpath('./ead:unitdate', namespaces=nsmap)
            window['-OUTPUT-'].update(f"\n{title.text}", append=True)
            if dates is not None:
                if len(dates) > 0:
                    emphatic = title.xpath('./ead:emph', namespaces=nsmap)
                    if emphatic is not None:
                        if len(emphatic) > 0:
                            window['-OUTPUT-'].update("\nemphasis being dealt with", append=True)
                            emphatic[-1].tail = f'{emphatic[-1].tail},'
                        else:
                            title.text = f"{title.text},"
                            error_text += f"\ttrailing comma added to {title.text}\n"
                    else:
                        #my_title = title.text_content()
                        your_title = title.text
                        title.text = f'{title.text},'
    # fix date issues
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    error_text += f"Date issues addressed:\n"
    # handle dates within a unitdate/emph tag
    dates = root.xpath("//ead:unitdate/ead:emph", namespaces=nsmap)
    for date in dates:
        # strip out unnecessary trailing spaces
        dateify = date.text
        dateify = dateify.replace("\n", ' ')
        while dateify.endswith(" "):
            dateify = dateify[:-1]
        while '  ' in dateify:
            dateify = dateify.replace('  ', ' ')
        date.text = dateify
        # add trailing comma if next sibling is a unitdate
        nexty = date.getparent().getnext()
        if nexty is not None:
            if nexty.tag == '{urn:isbn:1-931666-22-9}unitdate':
                if not dateify.endswith(","):
                    dateify = f"{dateify},"
                    error_text += f"\ttrailing comma added to {dateify} because of sibling unitdate\n"
        my_children = date.getparent().getparent().getchildren()
        my_grandparent = date.getparent().getparent().getparent()
        # add trailing comma if next sibiling is a physdesc
        my_children_flag = False
        if my_children is not None:
            for my_child in my_children:
                if my_child.tag == '{urn:isbn:1-931666-22-9}physdesc':
                    my_children_flag = True
        if my_children_flag is True and my_grandparent.tag != "{urn:isbn:1-931666-22-9}archdesc":
            dateify = f"{dateify},"
            error_text += f"\ttrailing comma added to {dateify} due to sibling physdesc\n"
        if dateify.endswith(","):
            dateify = f"{dateify} "
        # change text of date tag if manipulated date text is different than original
        if date.text != dateify:
            error_text += f"\t{date.text} updated to {dateify}"
        date.text = dateify
        date = date.getparent()
        # address date normal attribute specifically
        if "normal" not in date.attrib:
            date.attrib['normal'] = timeturner(dateify)
            error_text += f"\tdate normal attribute added to {date.text}\n"
        # address missing date type/calendar/era issues
        if "type" not in date.attrib:
            if "bulk" not in dateify:
                date.attrib['type'] = "inclusive"
                error_text += f"\ttype attribute added to {date.text}\n"
            else:
                date.attrib['type'] = ""
        if date.attrib['type'] == "":
            window['-OUTPUT-'].update("\n" + dateify, append=True)
            date.attrib['type'] = "inclusive"
            error_text += f"\ttype attribute added to {date.text}\n"
        if 'era' not in date.attrib:
            date.attrib['era'] = 'ce'
            error_text += f"\tera attribute added to {date.text}\n"
        if date.attrib['era'] == "":
            date.attrib['era'] = 'ce'
            error_text += f"\tera attribute added to {date.text}\n"
        if 'calendar' not in date.attrib:
            date.attrib['calendar'] = 'gregorian'
            error_text += f"\tcalendar attribute added to {date.text}\n"
        if date.attrib['calendar'] == "":
            date.attrib['calendar'] = 'gregorian'
            error_text += f"\tcalendar attribute added to {date.text}\n"
    # handle dates without the child emph tag
    dates = root.xpath("//ead:unitdate", namespaces=nsmap)
    for date in dates:
        # strip out unnecessary trailing spaces
        dateify = date.text
        dateify = dateify.replace("\n", ' ')
        while dateify.endswith(" "):
            dateify = dateify[:-1]
        while '  ' in dateify:
            dateify = dateify.replace('  ', ' ')
        # add trailing comma if next sibling is a unitdate
        date.text = dateify
        nexty = date.getnext()
        if nexty is not None:
            if nexty.tag == '{urn:isbn:1-931666-22-9}unitdate':
                if not dateify.endswith(","):
                    dateify = f"{dateify},"
                    error_text += f"\ttrailing comma added to {dateify} because of sibling unitdate\n"
        my_children = date.getparent().getchildren()
        my_grandparent = date.getparent().getparent()
        # add trailing comma if next sibling is a physdesc
        my_children_flag = False
        if my_children is not None:
            for my_child in my_children:
                if my_child.tag == '{urn:isbn:1-931666-22-9}physdesc':
                    my_children_flag = True
        if my_children_flag is True and my_grandparent.tag != "{urn:isbn:1-931666-22-9}archdesc":
            dateify = f"{dateify},"
            error_text += f"\ttrailing comma added to {dateify} due to sibling physdesc\n"
        if dateify.endswith(","):
            dateify = f"{dateify} "
        # change text of date tag if manipulated date text is different than original
        if date.text != dateify:
            error_text += f"\t{date.text} updated to {dateify}"
        date.text = dateify
        # address date normal attribute specifically
        if "normal" not in date.attrib:
            date.attrib['normal'] = timeturner(dateify)
            error_text += f"\tdate normal attribute added to {date.text}\n"
        # address missing date type/calendar/era issues
        if "type" not in date.attrib:
            if "bulk" not in dateify:
                date.attrib['type'] = "inclusive"
                error_text += f"\ttype attribute added to {date.text}\n"
            else:
                date.attrib['type'] = ""
        if date.attrib['type'] == "":
            window['-OUTPUT-'].update("\n" + dateify, append=True)
            date.attrib['type'] = "inclusive"
            error_text += f"\ttype attribute added to {date.text}\n"
        if 'era' not in date.attrib:
            date.attrib['era'] = 'ce'
            error_text += f"\tera attribute added to {date.text}\n"
        if date.attrib['era'] == "":
            date.attrib['era'] = 'ce'
            error_text += f"\tera attribute added to {date.text}\n"
        if 'calendar' not in date.attrib:
            date.attrib['calendar'] = 'gregorian'
            error_text += f"\tcalendar attribute added to {date.text}\n"
        if date.attrib['calendar'] == "":
            date.attrib['calendar'] = 'gregorian'
            error_text += f"\tcalendar attribute added to {date.text}\n"
    # address the date tag
    dates = root.xpath("//ead:date", namespaces=nsmap)
    for date in dates:
        date.attrib['calendar'] = "gregorian"
        date.attrib['era'] = "ce"
        error_text += f"\tcalendar and era added to ead:date at {date.text}\n"
    # log changes before moving on
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # remove ead:note header if it exists
    notes = root.xpath("//ead:note/ead:head", namespaces=nsmap)
    for note in notes:
        note.getparent().remove(note)
        error_text += f"an ead:note header was removed\n"
    error_text += f"Containers dealt with:\n"
    containers = root.xpath(".//ead:container", namespaces=nsmap)
    ## strip leading zeros from individual box numbers
    for container in containers:
        type = container.attrib['type']
        container.attrib['type'] = type.capitalize()
        container_text = container.text
        if "-" in container_text:
            container_temp = container_text.split("-")[-1]
            while container_temp.startswith("0"):
                container_temp = container_temp[1:]
            container_list = container_text.split("-")[:-1]
            replacement_text = ""
            for container_listy in container_list:
                replacement_text = f"{replacement_text}{container_listy}-"
            container.text = f"{replacement_text}{container_temp}"
    # target containers on a per-did basis
    container_dids = root.xpath(".//ead:did", namespaces=nsmap)
    for container_did in container_dids:
        container_type = set()
        containers = container_did.xpath("ead:container", namespaces=nsmap)
        # get container types so like types get handled together
        for container in containers:
            window['-OUTPUT-'].update("\n" + container.text, append=True)
            container_type.add(container.attrib['type'])
        container_type = list(container_type)
        # handle containers by type
        for item in container_type:
            window['-OUTPUT-'].update("\n" + item, append=True)
            # create dictionaries with sets where the key is the accession reference and set is all of the box numbers
            container_list = {}
            container_set = set()
            containers = container_did.xpath(f"ead:container[@type='{item}']", namespaces=nsmap)
            # create a list of accession references by isolating the box number and removing it from the container text
            for container in containers:
                container_text = container.text
                container_number = container_text.split("-")[-1].split("/")[-1]
                container_prefix = container_text.replace(container_number, "")
                container_set.add(container_prefix)
            container_set = list(container_set)
            container_set.sort()
            # add accession references to the dictionary as keys
            for my_container in container_set:
                container_list[my_container] = list()
            # assign
            for container in containers:
                container_text = container.text
                # isolate container number
                container_number = container_text.split("-")[-1].split("/")[-1]
                container_prefix = container_text.replace(container_number, "")
                # exclude things like subcontainers by keying on that those won't have / or -
                if len(container_number) > 1:
                    container_list[container_prefix].append(container_number)
            # now that the dictionary exists, process the containers
            for key in container_list.keys():
                top = 0
                bottom = 10000
                my_list = container_list[key]
                if len(my_list) > 1:
                    my_list.sort()
                    # isolate first and last box numbers
                    for integer in my_list:
                        my_integer = list(integer)
                        for character in my_integer:
                            try:
                                int(character)
                            except:
                                my_integer.remove(character)
                        new_integer = ""
                        for character in my_integer:
                            new_integer = f"{new_integer}{str(character)}"
                        integer = new_integer
                        if int(integer) >= top:
                            top = int(integer)
                        if int(integer) <= bottom:
                            bottom = int(integer)
                    # special handling for only two containers
                    if len(my_list) == 2:
                        container_text = f"{key}{str(bottom)} and {str(top)}"
                    if len(my_list) > 2:
                        container_text = f"{key}-{str(bottom)} thru {str(top)}"
                    # set container text to be the full range for every occurence that applies
                    for container in containers:
                        temp = container.text
                        if temp.startswith(key):
                            container.text = container_text
            # remove second+ instances where the containers are identical, which anything from a given accession should be at this point
            container_list = []
            for container in containers:
                if container.text not in container_list:
                    container_list.append(container.text)
                else:
                    error_text += f"\tseveral containers were merged into {container.text}\n"
                    container.getparent().remove(container)
    # log container actions
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # work on extents
    extents = root.xpath(".//ead:extent", namespaces=nsmap)
    error_text += "Extent issues addressed:\n"
    # if there's an extent and the next tag is genreform assume it is the type of extent and merge the two bits of text into extent
    for extent in extents:
        temp = extent.text
        other_tag = extent.getnext()
        if other_tag is not None and other_tag.tag == '{urn:isbn:1-931666-22-9}genreform':
            temp = temp + other_tag.text
            extent.text = temp
            other_tag.getparent().remove(other_tag)
            error_text += f"\textent and  sibling genreform merged to become {temp}\n"
    # log extent fixes implemented
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # now process in the brackets for physdesc inner content
    # set singulars for thins that would be exported as plurals
    extent_types = {'45 rpm records': '45 rpm record',
                    '78 rpm records': '78 rpm record',
                    '8-track cartridges': '8-track cartridge',
                    'Beta (Betamax)': 'Beta (Betamax)',
                    'Betacam (TM)': 'Betacam (TM)',
                    'Betacam-SP': 'Betacam-SP',
                    'DVDs': 'DVD',
                    'Digital Betacam (TM)': 'Digital Betacam (TM)',
                    'GB': 'GB',
                    'KB': 'KB',
                    'MB': 'MB',
                    'Mini-DV': 'Mini-DV',
                    'Super-VHS (TM)': 'Super-VHS (TM)',
                    'TB': 'TB',
                    'VHS': 'VHS',
                    'advertising cards': 'advertising card',
                    'aerial photographs': 'aerial photograph',
                    'albumen prints': 'albumen prints',
                    'aluminum discs': 'aluminum disc',
                    'ambrotypes (photographs)': 'ambrotype (photograph)',
                    'architectural drawings (visual works)': 'architectural drawing (visual work)',
                    'architectural models': 'architectural model',
                    'artifact_(object_genres)': 'artifact (object genre)',
                    'artifacts (object genre)': 'artifact (object genre)',
                    'artifacts_(object_genres)': "artifact (object genre)",
                    'audiocassettes': 'audiocassette',
                    'audiotapes': 'audiotape',
                    'black-and-white negatives': 'black-and-white negative',
                    'black-and-white photographs': 'black-and-white photograph',
                    'black-and-white prints (prints on paper)': 'black-and-white print (prints on paper)',
                    'black-and-white slides': 'black-and-white slide',
                    'black-and-white transparencies': 'black-and-white transparency',
                    'blueline prints': 'blueline print',
                    'blueprints (reprographic copies)': 'blueprint (reprographic copy)',
                    'booklets': 'booklet',
                    'books': 'book',
                    'boudoir photographs': 'boudoir photograph',
                    'broadsides (notices)': 'broadside (notice)',
                    'brochures': 'brochure',
                    'building plans': 'build plan',
                    'cabinet photographs': 'cabinet photograph',
                    'cartes-de-visite (card photographs)': 'cartes-de-visite (card photograph)',
                    'cartoons (humorous images)': 'cartoon (humorous image)',
                    'charcoal drawings': 'charoal drawing',
                    'charts (graphic documents)': 'chart (graphic docuent)',
                    'chromogenic color prints': 'chromogenic color print',
                    'chromolithographs': 'chromolithograph',
                    'clippings (information artifacts)': 'clipping (informtation artifact)',
                    'collodion prints': 'collodion print',
                    'collodion transfers': 'collodion transfer',
                    'collotypes (prints)': 'collotype (print)',
                    'color negatives': 'color negative',
                    'color photographs': 'color photograph',
                    'color slides': 'color slide',
                    'color transparencies': 'color transparency',
                    'compact discs': 'compact disc',
                    'composite photographs': 'composite photograph',
                    'contact sheets': 'contact sheet',
                    'contour maps': 'contour map',
                    'copy prints': 'copy print',
                    'crystoleums (photographs)': 'crystoleums (photograph)',
                    'cubic ft.': 'cubic ft.',
                    'cyanotypes (photographic prints)': 'cyanotype (photographic print)',
                    'cylinders (sound recordings)': 'cylinder (sound recording)',
                    'daguerreotypes (photographs)': 'daguerreotype (photograph)',
                    'data cards': 'data card',
                    'design drawings': 'design drawing',
                    'detail drawings (drawings)': 'detail drawing (drawing)',
                    'diaries': 'diary',
                    'diazotypes (copies)': 'diazotype (copy)',
                    'dictation belt': 'dictation belt',
                    'diffusion transfer prints': 'diffusion transfer print',
                    'digital audio tapes': 'digital audio tapes',
                    'digital images': 'digitam image',
                    'digital photographs': 'digital photograph',
                    'drawings (visual works)': 'drawing (visual work)',
                    'dry collodion negatives': 'dry collodion negative',
                    'dye transfer prints': 'dye transfer print',
                    'electrical drawings': 'electrical drawing',
                    'electrical plans': 'electrical plan',
                    'electronic files': 'electronic file',
                    'engravings (prints)': 'engraving (print)',
                    'envelopes': 'envelope',
                    'etchings (prints)': 'etchings (print)',
                    'filmstrips': 'filmstrip',
                    'fire insurance maps': 'fire insurance map',
                    'flags': 'flag',
                    'flash drives': 'flash drive',
                    'floppy disks': 'floppy disk',
                    'folders': 'folder',
                    'gelatin silver negatives': 'gelatin silver negative',
                    'gelatin silver prints': 'gelatin silver print',
                    'gelatin silver transparencies': 'gelatin silver transparency',
                    'gem photographs': 'gen photograph',
                    'geological maps': 'geological map',
                    'glass plate negatives': 'glass plate negative',
                    'greeting cards': 'greeting card',
                    'hard drives': 'hard drive',
                    'historical maps': 'historical map',
                    'identifying cards': 'identifying card',
                    'images': 'image',
                    'imperial photographs': 'imperial photograph',
                    'index maps': 'index map',
                    'inkjet prints': 'inkjet print',
                    'instantaneous recordings': 'instantaneous recording',
                    'internegatives': 'internegative',
                    'isoline maps': 'isoline map',
                    'issues': 'issue',
                    'items': 'item',
                    'lacquer discs': 'lacquer disc',
                    'land surveys': 'land survey',
                    'land use maps': 'land use maps',
                    'lantern slides': 'lantern slide',
                    'laser prints': 'laser print',
                    'leaves': 'leaf',
                    'ledgers (account books)': 'ledger (account book)',
                    'letter books': 'letter book',
                    'letterpress copybooks': 'letterpress copybook',
                    'linear ft.': 'linear ft.',
                    'lithographs': 'lithograph',
                    'long-playing records': 'long-playing record',
                    'magazines_(periodicals)': 'magazine (periodical)',
                    'magnetic disks': 'magnetic disk',
                    'magnetic tapes': 'magnetic tape',
                    'manuscript maps': 'manuscript map',
                    'maps (documents)': 'map (document)',
                    'mechanical drawings (building systems drawings)': 'mechanical drawing (building systems drawing)',
                    'microcassettes': 'microcassette',
                    'microfiche': 'microfiche',
                    'microfilms': 'microfilm',
                    'military maps': 'military map',
                    'mineral resource maps': 'mineral resource map',
                    'miniatures (paintings)': 'miniature (painting)',
                    'motion picture components': 'motion picture component',
                    'motion pictures (visual works)': 'motion picture (visual work)',
                    'moving images': 'moving image',
                    'muster rolls': 'muster roll',
                    'national maps': 'national map',
                    'offset lithographs': 'offset lithograph',
                    'open reel audiotapes': 'open reel audiotape',
                    'optical disks': 'optical disk',
                    'paintings (visual works)': 'painting (visual work)',
                    'panel photographs': 'panel photograph',
                    'panoramas (visual works)': 'panorama (visual work)',
                    'panoramic photographs': 'panoramic photograph',
                    'pastels (visual works)': 'pastel (visual work)',
                    'pen and ink drawings': 'pen and ink drawing',
                    'photocopies': 'photocopy',
                    'photoengravings (prints)': 'photoengraving',
                    'photograph albums': 'photograph album',
                    'photographic postcards': 'photographic postcard',
                    'photographic prints': 'photographic print',
                    'photographs': 'photograph',
                    'photogravures (prints)': 'photogravure (print)',
                    'photomechanical prints': 'photomechanical print',
                    'picture postcards': 'picture postcard',
                    'plans (maps)': 'plan (map)',
                    'plats (maps)': 'plat (map)',
                    'population maps': 'population map',
                    'postcards': 'postcard',
                    'posters': 'poster',
                    'presentation drawings (proposals)': 'presentation drawing (proposal)',
                    'prints (visual works)': 'print (visual work)',
                    'promenade midget photographs': 'promenade midget photograph',
                    'promenade photographs': 'promenade photograph',
                    'public utility maps': 'public utility map',
                    'quadrangle maps': 'quadrangle map',
                    'reels': 'reel',
                    'regional maps': 'regional map',
                    'relief halftones (prints)': 'relief halftone',
                    'reports': 'report',
                    'road maps': 'road map',
                    'scrapbooks': 'scrapbook',
                    'sheets (paper artifacts)': 'sheet (paper artifact)',
                    'ships plans': 'ships plan',
                    'sketchbooks': 'sketchbook',
                    'sound recordings': 'sound recording',
                    'sound tracks': 'sound track',
                    'stained glass (visual works)': 'stained glass',
                    'stats (copies)': 'stat (copy)',
                    'steel engravings (visual works)': 'steel engraving (visual work)',
                    'stereographs': 'stereograph',
                    'street maps': 'street map',
                    'structural drawings': 'structural drawing',
                    'tintypes (prints)': 'tintype (print)',
                    'topographic maps': 'topographic map',
                    'topographic surveys': 'topographic survey',
                    'transportation maps': 'transportation map',
                    'victoria cards (photographs)': 'victoria card (photograph)',
                    'videocassettes': 'videocassette',
                    'videotapes': 'videotape',
                    'volumes': 'volume',
                    'wallets': 'wallet',
                    'watercolors (paintings)': 'watercolor (painting)',
                    'watershed maps': 'watershed map',
                    'wet collodion negatives': 'wet collodion negative',
                    'wire recordings': 'wire recording',
                    'wood engravings (prints)': 'wood engraving (print)',
                    'woodcuts (prints)': 'woodcut (print)',
                    'working drawings': 'working drawing',
                    'works of art': 'work of art',
                    'zoning maps': 'zoning map'}
    # begin work on scope notes
    scopenotes = root.xpath(".//ead:scopecontent", namespaces=nsmap)
    for scopenote in scopenotes:
        parent = scopenote.getparent()
        parent_attrib = parent.attrib['level']
        # if scope note isn't in the exceptions proceed, meant for lower level emphasis of text
        if parent.attrib != None and parent_attrib not in exceptions:
            paragraphs = scopenote.xpath("./ead:p", namespaces=nsmap)
            if paragraphs != None:
                for paragraph in paragraphs:
                    emphasis = paragraph.xpath("./ead:emph", namespaces=nsmap)
                    # if the emph wrapper has already been applied skip this one
                    if emphasis != []:
                        continue
                    # add missing emph tags
                    else:
                        myText = paragraph.text
                        emphatic = ET.SubElement(paragraph, 'emph')
                        emphatic.attrib['render'] = 'italic'
                        emphatic.text = myText
                        window['-OUTPUT-'].update("\nmanual fix to scopenote is needed in ArchivesSpace", append=True)
                        window['-OUTPUT-'].update(f"\ncheck text around: {paragraph.text[0:50]}", append=True)
                        error_text += f"manual check of paragraph italicization around this text: {paragraph.text[:50]}\n"
                        paragraph.text = ""
            else:
                emphasis = scopenote.xpath("./ead:emph", namespaces=nsmap)
                if emphasis != []:
                    continue
                else:
                    myText = scopenote.text
                    emphatic = ET.SubElement(scopenote, 'emph')
                    emphatic.attrib['render'] = 'italic'
                    emphatic.text = myText
                    window['-OUTPUT-'].update("\nmanual fix to scopenote may be needed", append=True)
                    window['-OUTPUT-'].update(f"\ncheck text around: {scopenote.text[0:50]}", append=True)
                    error_text += f"manual check of paragraph italicization needed around this text: {scopenote.text[:50]}\n"
                    scopenote.text = ""
                window['-OUTPUT-'].update("\n" + scopenote.text, append=True)
    # log paragraph emph work before moving on
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # deal with ead:note tags
    notes = root.xpath(".//ead:note", namespaces=nsmap)
    for note in notes:
        parent = note.getparent()
        if "level" in parent.attrib:
            parent_attrib = parent.attrib['level']
            if parent.attrib != None and parent_attrib not in exceptions:
                paragraphs = note.xpath("./ead:p", namespaces=nsmap)
                if paragraphs != None:
                    for paragraph in paragraphs:
                        emphasis = paragraph.xpath("./ead:emph", namespaces=nsmap)
                        if emphasis != []:
                            continue
                        else:
                            myText = paragraph.text
                            emphatic = ET.SubElement(paragraph, 'emph')
                            emphatic.attrib['render'] = 'italic'
                            emphatic.text = myText
                            window['-OUTPUT-'].update("\nmanual fix to note may be needed", append=True)
                            window['-OUTPUT-'].update(f"\ncheck text around: {paragraph.text[0:50]}", append=True)
                            error_text += f"manual check of paragraph italicization around this text: {paragraph.text[:50]}\n"
                            paragraph.text = ""
                else:
                    emphasis = note.xpath("./ead:emph", namespaces=nsmap)
                    if emphasis != []:
                        continue
                    else:
                        myText = note.text
                        emphatic = ET.SubElement(scopenote, 'emph')
                        emphatic.attrib['render'] = 'italic'
                        emphatic.text = myText
                        window['-OUTPUT-'].update("\nmanual fix to note may be needed", append=True)
                        window['-OUTPUT-'].update(f"\ncheck text around: {note.text[0:50]}", append=True)
                        error_text += f"manual check of paragraph italicization around this text: {scopenote.text[:50]}\n"
                        scopenote.text = ""
                    window['-OUTPUT-'].update("\n" + scopenote.text, append=True)


    # being handling physdesc/extent companion elements if they exist
    extents = root.xpath(".//ead:extent", namespaces=nsmap)
    error_text += f"Extent physfacet and dimensions addressed:\n"
    for extent in extents:
        parent = extent.getparent().getparent().getparent()
        next_phys = extent.getnext()
        parent_attrib = parent.attrib['level']
        if parent_attrib != None and parent_attrib not in exceptions:
            preceding = extent.getparent()
            extent.text = f"[{extent.text}"
            if next_phys is not None:
                if next_phys.tag == "{urn:isbn:1-931666-22-9}physfacet" or next_phys.tag == "{urn:isbn:1-931666-22-9}dimensions":
                    next_phys.text = f", {next_phys.text}"
                    next_next_phys = next_phys.getnext()
                    if next_next_phys is not None:
                        if next_next_phys.tag == "{urn:isbn:1-931666-22-9}physfacet" or next_next_phys.tag == "{urn:isbn:1-931666-22-9}dimensions":
                            next_next_phys.text = f", {next_next_phys.text}]"
                        else:
                            next_phys.text = f"{next_phys.text}]"
                    else:
                        next_phys.text = f"{next_phys.text}]"
                else:
                    extent.text = f"{extent.text}]"
            else:
                extent.text = f"{extent.text}]"
            if 'altrender' in extent.attrib:
                if extent.attrib['altrender'] == "materialtype spaceoccupied":
                    del extent.attrib['altrender']
            # window['-OUTPUT-'].update("\n" + parent.attrib['level'], append=True)
            '''if physfacet != None:
                prior_auth = physfacet.getprevious()
                later_auth = physfacet.getnext()
                if prior_auth.tag is not None:
                    if prior_auth.tag == 'genreform' or prior_auth.tag == 'dimensions' or prior_auth.tag == 'extent':
                        physfacet.text = f", {physfacet.text}"
                    else:
                        physfacet.text = f'[{physfacet.text}'
                else:
                    physfacet.text = f"[{physfacet.text}"
                if later_auth is not None:
                    if later_auth.tag != 'genreform' or later_auth.tag != 'dimensions':
                        physfacet.text = f'{physfacet.text}]'
                else:
                    physfacet.text = f'{physfacet.text}]'
                error_text += f"\tupdated to {physfacet.text}\n"
            if dimension != None:
                dimension.text = "[" + dimension.text + "]"
                error_text += f"\tupdated to {dimension.text}\n"'''
        # do parenthetical for high level electronic records count in extent
        if parent_attrib in exceptions:
            if "electronic files" in extent.text:
                extent.text = f"({extent.text})"
                error_text += f"added parenthetical part to {extent.text}\n"
    # update saved erorr log
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # process the singularity of extents
    error_text += f"Singularized the following extents:\n"
    extents = root.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        tempstring = extent.text
        if "[" in tempstring:
            tempstring = tempstring[1:]
        if "]" in tempstring:
            tempstring = tempstring[:-1]
        window['-OUTPUT-'].update("\n" + tempstring, append=True)
        var = tempstring.split(" ")[0]
        if var == "1":
            tempstring = tempstring.replace("1 ", "")
            window['-OUTPUT-'].update("\n" + tempstring, append=True)
            tempy = extent.text
            tempy = tempy.replace(tempstring, extent_types[tempstring])
            extent.text = tempy
            error_text += f"\t{tempy}\n"
    # process partial extents as 'includes'
    extents = root.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        tempstring = extent.text
        parental = extent.getparent()
        if 'altrender' in parental.attrib:
            parent_part = parental.attrib['altrender']
            if "part" in parent_part:
                if not tempstring.startswith("("):
                    tempstring = f"includes {tempstring}"
                    tempstring = tempstring.replace("includes [", "includes ")
                    extent.text = f"({tempstring})"
    # reprocess header stuff
    title = root.find(".//ead:archdesc/ead:did/ead:unittitle", namespaces=nsmap)
    my_title = title.text
    while my_title.endswith(","):
        my_title = my_title[:-1]
    title.text = my_title
    dates = root.xpath(".//ead:archdesc/ead:did/ead:unitdate", namespaces=nsmap)
    if len(dates) > 0:
        my_date = dates[-1]
        date_text = my_date.text
        while date_text.endswith(" ") or date_text.endswith(","):
            date_text = date_text[:-1]
        my_date.text = date_text
    # reprocess a date issue
    dids = root.xpath(".//ead:did", namespaces=nsmap)
    for did in dids:
        dates = did.xpath("./ead:unitdate", namespaces=nsmap)
        if len(dates) > 0:
            for date in dates:
                date_text = date.text
                while date_text.endswith(",, "):
                    date_text = date_text.replace(",, ", ", ")
                date.text = date_text
    # reprocess a trailing comma with brackets issue
    for level in levels:
        # first remove head tag from any scopenote
        scopes = root.xpath(f".//ead:{level}/ead:scopecontent/ead:head", namespaces=nsmap)
        if scopes is not None:
            for scope in scopes:
                scope.getparent().remove(scope)
        my_dids = root.xpath(f".//ead:{level}/ead:did", namespaces=nsmap)
        for my_did in my_dids:
            c_tag = my_did.getparent()
            c_level = c_tag.attrib["level"]
            if c_level == "Heading":
                c_tag.attrib['level'] = "otherlevel"
                c_tag.attrib['otherlevel'] = "Heading"
                error_text += f"a level of heading was updated to include otherlevel element"
            physdescs = my_did.xpath("./ead:physdesc/ead:extent", namespaces=nsmap)
            if len(physdescs) > 0:
                for physdesc in physdescs:
                    physdesc_text = physdesc.text
                    # deal with superfluous altrender and labels in physdesc
                    parent_phys = physdesc.getparent()
                    if "altrender" in parent_phys.attrib:
                        parent_phys.attrib.pop("altrender")
                        error_text += f"removed altrender from phydesc at {physdesc_text}\n"
                    if "label" in parent_phys.attrib:
                        parent_phys.attrib.pop("label")
                        error_text += f"removed label from physdesc at {physdesc_text}\n"
                    # deal with altrender on extent
                    if "altrender" in physdesc.attrib:
                        physdesc.attrib.pop("altrender")
                        error_text += f"removed altrender from extent at {physdesc_text}\n"
                    # deal with trailing punctuation on extent
                    if physdesc_text.startswith('['):
                        unitdates = my_did.xpath("./ead:unitdate", namespaces=nsmap)
                        if len(unitdates) > 0:
                            specific_date = unitdates[-1]
                            specific_text = specific_date.text
                            while specific_text.endswith(",") or specific_text.endswith(" "):
                                specific_text = specific_text[:-1]
                            specific_date.text = specific_text

    # pull out access restrict with audience = internal if still there
    restrictions = root.xpath("//ead:accessrestrict[@audience = 'internal']", namespaces=nsmap)
    if restrictions is not None:
        for restriction in restrictions:
            restriction.getparent().remove(restriction)
            error_text += f"removed internal accessrestrict notes\n"
    ET.indent(dom2, space="\t")
    with open(finished_product, "wb") as w:
        w.write(ET.tostring(dom2, pretty_print=True))
    w.close()
    #dom2.write(finished_product, pretty_print=True)
    # write final bits to error log file
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    # fix the crap that seems to not be fixed via xsl manipulation
    with open(finished_product, "r", encoding='utf-8') as r:
        filedata = r.read()
        filedata = filedata.replace("xmlns_xlink", "xmlns:xlink").replace("xlink_", "xlink:")
        filedata = filedata.replace("</creation>.<langusage>", ".</creation><langusage>").replace("</creation>.<descrules>", ".</creation><descrules>")
        filedata = filedata.replace(' construct="master">', ">")
        filedata = filedata.replace('<ead:archref href',
                                    '<ead:archref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
        filedata = filedata.replace('<ead:bibref href',
                                    '<ead:bibref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
        filedata = filedata.replace(", , <", ", <")
        filedata = filedata.replace("..", ".").replace(". .", ".")
        filedata = filedata.replace("\n<ead:descgrp>\n<head>Administrative Information</head>", "")
        filedata = filedata.replace('\n<ead:descgrp type="admininfo">\n<head>Administrative Information</head>', '')
        filedata = filedata.replace("\n<ead:descgrp>", "")
        filedata = filedata.replace('\n<ead:descgrp type="admininfo">', '')
        filedata = filedata.replace("\n</ead:descgrp>", "")
        filedata = filedata.replace("ead:", "")
        filedata = filedata.replace("\n<physfacet>", "<physfacet>").replace("\n<dimensions>", "<dimensions>").replace(
            "\n</physdesc>", "</physdesc>")
        filedata = filedata.replace("<extent>[", "[<extent>").replace("]</extent>", "</extent>]")
        filedata = filedata.replace("])</extent>", ")</extent>")
        filedata = filedata.replace("<physfacet>[", "[<physfacet>, ").replace("]</physfacet>", "</physfacet>]")
        filedata = filedata.replace("<dimensions>[", "[<dimensions>, ").replace("]</dimensions>", "</dimensions>]")
        filedata = filedata.replace("][<physfacet>", "<physfacet>").replace("][<dimensions>", "<dimensions>")

        if "852$a" not in filedata:
            filedata = filedata.replace("</abstract>",
                                        '</abstract>\n<repository encodinganalog="852$a">\n<extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href="http://www.tsl.texas.gov/arc/index.html">Texas State Archives</extref>\n</repository>')
        filedata = filedata.replace(
            '<repository encodinganalog="852$a">\n<extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href="http://www.tsl.texas.gov/arc/index.html">Texas State Archives</extref>\n</repository>\n<unitid label="TSLAC Control No.:" countrycode="US" repositorycode="US-tx" encodinganalog="099">\n</unitid>\n',
            '')
        filedata = filedata.replace(
            '\n<unitid label="TSLAC Control No.:" countrycode="US" repositorycode="US-tx" encodinganalog="099">\n</unitid>',
            '')
        filedata = filedata.replace(
            '<controlaccess>\n<head>Index Terms</head>\n<p>\n<emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</emph>\n</p>\n</controlaccess>',
            '')
        filedata = filedata.replace('<controlaccess>\n</controlaccess>\n', '').replace(" , ", ", ").replace(
            ", </unitdate>, ", "</unitdate>, ").replace(",</unitdate>, ", "</unitdate>, ").replace(", </emph>, ",
                                                                                                   "</emph>, ").replace(
            ",</emph>, ", "</emph>, ").replace(" </unitdate>, ", "</unitdate>, ")
        filedata = filedata.replace("</unitdate>, </unittitle>\n<physdesc>", ", </unitdate></unittitle>\n<physdesc>")
        if 'xmlns="urn:isbn:1-931666-22-9" xsi:' in filedata and 'relatedencoding="MARC21" xmlns="urn:isbn:1-931666-22-9">' in filedata:
            filedata = filedata.replace('relatedencoding="MARC21" xmlns="urn:isbn:1-931666-22-9">', '>')
        filedata = filedata.replace("[[", "[").replace("]]", "]").replace("[ [", "[").replace("] ]", "]").replace(
            ",</emph>\n, </unitdate>", "</emph>, </unitdate>")
        filedata = filedata.replace("\n<unittitle>, </unittitle>", "")
        filedata = filedata.replace('<container type="box">', '<container type="Box">').replace('Texas-digital-archive',
                                                                                                'Texas-Digital-Archive')
        filedata = filedata.replace('<container type="folder">', '<container type="Folder">').replace("&lt;",
                                                                                                      "<").replace(
            "&gt;", ">")
        filedata = filedata.replace("English.</langusage>",
                                    '<language langcode="eng" scriptcode="Latn">English</language>.</langusage>')
        filedata = filedata.replace('type="inclusive">, <emph', 'type="inclusive"><emph').replace('type="bulk">, <emph',
                                                                                                  'type="bulk"><emph')
        filedata = filedata.replace('list type="ordered">', 'list>')
        filedata = filedata.replace(
            '\n<!--Remove the ead.xsl and ead.css statements above before uploading to TARO.-->', '')
        filedata = filedata.replace("etc", "etc.").replace("etc..", "etc.")
        donkeykong = re.findall(']</physdesc>\n<unitdate *.*, </unitdate>\n</did>', filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                dittykong = item.replace(", </unitdate>", " </unitdate>")
                filedata = filedata.replace(item, dittykong)
        donkeykong = re.findall(r'\n*.*<\?*.*xml-stylesheet*.*\?>*.*', filedata)
        if donkeykong:
            for item in donkeykong:
                filedata = filedata.replace(item, "")
        donkeykong = re.findall(r'\n*.*Remove the ead*.*xsl and ead*.*.css statements*.*>\n', filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                filedata = filedata.replace(item, "")
        if ' xmlns="urn:isbn:1-931666-22-9" ' in filedata and ' xmlns="urn:isbn:1-931666-22-9">' in filedata:
            filedata = filedata.replace('xmlns="urn:isbn:1-931666-22-9">', '>')
        filedata = filedata.replace(
            'xsi:schemaLocation="urn:isbn:1-931666-22-9 ead.xsd" xmlns="urn:isbn:1-931666-22-9"',
            'xsi:schemaLocation="urn:isbn:1-931666-22-9 ead.xsd"')
        filedata = filedata.replace("</emph>\n,</unittitle>", "</emph>,</unittitle>")
        filedata = filedata.replace('",</unittitle>', ',"</unittitle>').replace("</emph>,</unittitle>", ",</emph></unittitle>").replace(",,", ",")
    finished_product = finished_product.replace("-DONOTUSE", "-done")
    with open(finished_product, "w", encoding='utf-8') as w:
        w.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<!--Remove the ead.xsl and ead.css statements above before uploading to TARO.-->\n<!-- <?xml-stylesheet type="text/xsl" href="ead.xsl"?> <?xml-stylesheet type="text/css" href="ead.css"?> -->\n' + filedata)
    w.close()
    os.remove(finished_product_removable)
    error_text += f"A number of manual text changes added to the ead file to make it compliant/clean-up before html generation\n"
    error_text += f"attempting to parse file to make sure the ead is valid\n"
    html_file = f"{finished_product[:-3]}html"
    my_html = ET.XSLT(html_transform)
    try:
        dom = ET.parse(finished_product)
        error_text += f"parsing of ead file successful\n"
    except Exception as e:
        error_text += f"Parsing failed because of:\n{str(e)}\n"
        error_text += f"{traceback.format_exc()}\n"
        error_text += f"try using a web browser to see if there is malformed xml somewhere\n"
        with open(error_log, "w") as w:
            w.write(error_text)
        w.close()
        sys.exit()
    newdom = my_html(dom)
    newdom.write(html_file, pretty_print=True)
    with open(html_file, "r") as r:
        filedata = r.read()
        filedata = filedata.replace("<b/>", "")
        with open(html_file, "w") as w:
            w.write(filedata)
        w.close()
    error_text += f"html file generated, done with file"
    if flag > 0:
        window['-OUTPUT-'].update("\n" + f"potential subject term issue in {unitid_text} check it manually",
                                  append=True)
        error_text += f"potential subject term issue, check it manually to be sure everything is okay"
    with open(error_log, "w") as w:
        w.write(error_text)
    w.close()
    window['-OUTPUT-'].update("\n" + f'{unitid_text} finished', append=True)
    window['-OUTPUT-'].update("\n" + "all done!", append=True)
    window['-DONE_message-'].update(visible=True)


Sg.theme('DarkGreen')
layout = [[
    Sg.Push(),
    Sg.Text("EAD file"),
    Sg.In(size=(50, 1), enable_events=True, key="-EAD-"),
    Sg.FileBrowse(file_types=(("xml text files only", "*.xml"),)), ],
    [
        Sg.Push(),
        Sg.Button("Execute", tooltip="This will start the program running"),
        Sg.Push()
    ],
    [
        Sg.Button("Close", tooltip="Close this window. Won't work while XML is being processed", bind_return_key=True)
    ],
    [
        Sg.Multiline(
            default_text="Look here for information about various data points as the file processes. Your processed file will end in '-done'",
            size=(70, 5), auto_refresh=True, reroute_stdout=False, key="-OUTPUT-", autoscroll=True,
            border_width=5)
    ],
    [
        Sg.Text("IF YOU HAD MULTIPLE CONTAINERS of the SAME PREFIX on an DID, especially \nif there was letters in the container identifier, CHECK THE OUTPUT", visible=False, key="-DONE_message-", font=("Arial", "10", "bold italic"))
    ]
]

window = Sg.Window(
    "TARO EAD processor",
    layout,
    icon=my_icon
)

event, values = window.read()
while True:
    event, values = window.read()
    my_xml = values['-EAD-']
    if event == "Execute":
        processor(my_xml)
    if event == "Close" or event == Sg.WIN_CLOSED:
        break
window.close()
