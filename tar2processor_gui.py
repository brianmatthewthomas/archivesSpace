import sys
import daterangeparser
import datetime
import lxml.etree as ET
import re
import PySimpleGUI as Sg

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

def subjectspace (subject):
    while subject.startswith(" "):
        subject = subject[1:]
    while subject.endswith(" "):
        subject = subject[:-1]
    if subject.endswith("."):
        subject = subject[:-1]
    subject = subject.replace(" -- ","--")
    return subject

def subarea (subject):
    placeholder = subject.split(". ")
    placeholder2 = placeholder[0]
    if len(placeholder) != 1:
        placeholder2 = placeholder2 + ". "
        for item in placeholder[1:]:
            while item.startswith(" "):
                item = item[1:]
            placeholder2 = placeholder2 + "<subarea>" + item + ".</subarea> "
        placeholder2 = placeholder2[:-12] + "</subarea>"
    placeholder2 = placeholder2.replace("..",".")
    return placeholder2

def timeturner (dateify):
    dateify2 = dateify
    if dateify == "undated" or dateify == "undated," or dateify == "undated, " or dateify == 'n.d.' or dateify == "Undated" or dateify == 'date unknown':
        dateify = "2021"
    dateify = dateify.replace("bulk", "").replace("(not inclusive)", "").replace("and undated", "").replace("undated","").replace(":","").replace(" part II", "").replace(" part I","")
    dateify = dateify.replace("about", "").replace("\n", '').replace("[", '').replace("]", '').replace("ca.",'').replace('week of','').replace(";",'').replace("thru","-")
    dateify = dateify.replace("and", "-").replace("primarily", "").replace(" or ", "-").replace("(?),", "").replace("(?)", "").replace("(", '').replace(")",'').replace("?","").replace("filmed on ",'')
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
    dateify = dateify.replace(A+", "+B,A+"-"+B).replace(A+", "+C,A+"-"+C).replace(A+", "+D,A+"-"+D).replace(A+", "+E,A+"-"+E).replace(A+", "+F,A+"-"+F).replace(A+", "+G,A+"-"+G).replace(A+", "+H,A+"-"+H).replace(A+", "+I,A+"-"+I).replace(A+", "+J,A+"-"+J).replace(A+", "+K,A+"-"+K).replace(A+", "+L,A+"-"+L)
    dateify = dateify.replace(B+", "+C,B+"-"+C).replace(B+", "+D,B+"-"+D).replace(B+", "+E,B+"-"+E).replace(B+", "+F,B+"-"+F).replace(B+", "+G,B+"-"+G).replace(B+", "+H,B+"-"+H).replace(B+", "+I,B+"-"+I).replace(B+", "+J,B+"-"+J).replace(B+", "+K,B+"-"+K).replace(B+", "+L,B+"-"+L)
    dateify = dateify.replace(C+", "+D,B+"-"+D).replace(C+", "+E,B+"-"+E).replace(C+", "+F,B+"-"+F).replace(C+", "+G,B+"-"+G).replace(C+", "+H,B+"-"+H).replace(C+", "+I,B+"-"+I).replace(C+", "+J,B+"-"+J).replace(C+", "+K,B+"-"+K).replace(C+", "+L,B+"-"+L)
    dateify = dateify.replace(D+", "+E,D+"-"+E).replace(D+", "+F,D+"-"+F).replace(D+", "+G,D+"-"+G).replace(D+", "+H,D+"-"+H).replace(D+", "+I,D+"-"+I).replace(D+", "+J,D+"-"+J).replace(D+", "+K,D+"-"+K).replace(D+", "+L,D+"-"+L)
    dateify = dateify.replace(E+", "+F,E+"-"+F).replace(E+", "+G,E+"-"+G).replace(E+", "+H,E+"-"+H).replace(E+", "+I,E+"-"+I).replace(E+", "+J,E+"-"+J).replace(E+", "+K,E+"-"+K).replace(E+", "+L,E+"-"+L)
    dateify = dateify.replace(F+", "+G,F+"-"+G).replace(F+", "+H,F+"-"+H).replace(F+", "+I,F+"-"+I).replace(F+", "+J,F+"-"+J).replace(F+", "+K,F+"-"+K).replace(F+", "+L,F+"-"+L)
    dateify = dateify.replace(G+", "+H,G+"-"+H).replace(G+", "+I,G+"-"+I).replace(G+", "+J,G+"-"+J).replace(G+", "+K,G+"-"+K).replace(G+", "+L,G+"-"+L)
    dateify = dateify.replace(H+", "+I,H+"-"+I).replace(H+", "+J,H+"-"+J).replace(H+", "+K,H+"-"+K).replace(H+", "+L,H+"-"+L)
    dateify = dateify.replace(I+", "+J,I+"-"+J).replace(I+", "+K,I+"-"+K).replace(I+", "+L,I+"-"+L)
    dateify = dateify.replace(J+", "+K,J+"-"+K).replace(J+", "+L,J+"-"+L)
    dateify = dateify.replace(K+", "+L,K+"-"+L)
    dateify = dateify.replace("-"+A+"-","-").replace("-"+B+"-","-").replace("-"+C+"-","-").replace("-"+D+"-","-").replace("-"+E+"-","-").replace("-"+F+"-","-").replace("-"+G+"-","-").replace("-"+H+"-","-").replace("-"+I+"-","-").replace("-"+J+"-","-").replace("-"+K+"-","-")

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
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{4}-\d{2}-\d{1}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:-1] + "0" + item[-1:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{4}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:5] + "0" + item[5:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{4}-\d{1}-\d{1}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:5] + "0" + item[5:7] + "0" + item[-1:]
            dittykong = datetime.datetime.strptime(dittykong, "%Y-%m-%d")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}/\d{2}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = datetime.datetime.strptime(item, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}-\d{2}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = datetime.datetime.strptime(item, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window["-OUTPUT-"].update(dittykong)
            #print(dittykong)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}/\d{1}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}-\d{1}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}-\d{2}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}/\d{2}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}/\d{1}/\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}-\d{1}-\d{4}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-5] + item[-5:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}/\d{2}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}-\d{2}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            if dateify.startswith(item):
                dittykong = item[:-2] + "19" + item[-2:]
                dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
                dittykong = dittykong.strftime("%B %d, %Y")
                window['-OUTPUT-'].update("\n" + dittykong, append=True)
                dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}/\d{2}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}-\d{2}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}/\d{1}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{2}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = item[:3] + "0" + item[3:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}/\d{1}/\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m/%d/%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.findall(r'\d{1}-\d{1}-\d{2}', dateify)
    if donkeykong:
        for item in donkeykong:
            item = str(item)
            dittykong = "0" + item[:2] + "0" + item[2:-2] + "19" + item[-2:]
            dittykong = datetime.datetime.strptime(dittykong, "%m-%d-%Y")
            dittykong = dittykong.strftime("%B %d, %Y")
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(item,dittykong)
    donkeykong = re.search(r'FY \d{4}-\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        placeholder = donkeykong.split("-")
        year1 = int(placeholder[0][-4:]) - 1
        year2 = placeholder[1][-4:]
        dittykong = 'September 1, ' + str(year1) + " - August 31, " + year2
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY \d{4} - FY \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        placeholder = donkeykong.split(" - ")
        year1 = int(placeholder[0][-4:]) - 1
        year2 = placeholder[1][-4:]
        dittykong = 'September 1, ' + str(year1) + " - August 31, " + year2
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-4:]) - 1
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY \d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-2:]) + 1899
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, 19" + donkeykong[-2:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'FY\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = int(donkeykong[-2:]) + 1899
        dittykong = 'September 1, ' + str(dittykong) + " - August 31, 19" + donkeykong[-2:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{4}-\d{2}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        if dateify.startswith(donkeykong + ",") or dateify.startswith(donkeykong + " ") or dateify.endswith(donkeykong):
            dittykong = donkeykong[:5] + donkeykong[:2] + donkeykong[-2:]
            window['-OUTPUT-'].update("\n" + dittykong, append=True)
            dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'd{2}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong
        dittykong = datetime.datetime.strptime(dittykong, "%m/%Y")
        dittykong = dittykong.strftime("%B, %Y")
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'd{1}/\d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "0" + donkeykong
        dittykong = datetime.datetime.strptime(dittykong, "%m/%Y")
        dittykong = dittykong.strftime("%B, %Y")
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
    dateify = dateify.replace("Summer, ","Summer ").replace("Spring, ","Spring ").replace("Fall, ","Fall ").replace("Winter, ","Winter ")
    donkeykong = re.search(r'Spring \d{4}', dateify, re.IGNORECASE)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = "March 1, " + donkeykong[-4:] + " to May 31, " + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
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
        dateify = dateify.replace(donkeykong,dittykong)
    donkeykong = re.search(r'\d{4} \d{4}', dateify)
    if donkeykong:
        donkeykong = str(donkeykong[0])
        dittykong = donkeykong[:4] + "-" + donkeykong[-4:]
        window['-OUTPUT-'].update("\n" + dittykong, append=True)
        dateify = dateify.replace(donkeykong,dittykong)
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
        #window['-OUTPUT-'].update("\n" + dateify)
        #temp_value = daterangeparser.parse(dateify)
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
                        window['-OUTPUT-'].update("\n" + dateify2, append=True)
                        window['-OUTPUT-'].update("\n" + item, append=True)
                        newDate = input("manually enter date normal attribute above using YYYY-MM-DD/YYYY-MM-DD: ")
                        if not newDate.endswith("/"):
                            newDate += "/"
                        date_normal += newDate
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
        date_normal = date_normal.replace(donkeykong,"0000/")
    return date_normal

catalyst = ET.XML('''
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ead="urn:isbn:1-931666-22-9" xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="xs" version="1.0">

<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
<!-- copy everything -->
<xsl:template match="node()|@*">
	<xsl:copy>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:copy>
</xsl:template>
<!-- insert namespace prefix into everything so there are no errors in xml transform application -->
<xsl:template match="*">
	<xsl:element name="ead:{name()}" namespace="urn:isbn:1-931666-22-9">
		<xsl:copy-of select="namespace::*"/>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:element>
</xsl:template>
<!-- stuff that needs to be weeded out -->
<xsl:template match="@id"/>
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:titlestmt/ead:titleproper/ead:num"/>
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:publicationstmt/ead:address"/>
<xsl:template match="ead:ead/ead:archdesc/ead:dsc/ead:c01/ead:did/ead:unitid"/>
<xsl:template match="ead:relatedmaterial/ead:head"/>
<xsl:template match="ead:extent[@altrender='carrier']"/>
<!-- update ead header info -->
<xsl:template match="ead:eadheader">
	<xsl:element name="ead:eadheader">
		<xsl:attribute name="countryencoding">iso3166-1</xsl:attribute>
		<xsl:attribute name="dateencoding">iso8601</xsl:attribute>
		<xsl:attribute name="langencoding">iso639-2b</xsl:attribute>
		<xsl:attribute name="repositoryencoding">iso15511</xsl:attribute>
		<xsl:attribute name="audience">internal</xsl:attribute>
		<xsl:attribute name="findaidstatus">edited-full-draft</xsl:attribute>
		<xsl:attribute name="scriptencoding">iso15924</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:eadid">
	<xsl:element name="ead:eadid">
		<xsl:attribute name="countrycode">US</xsl:attribute>
		<xsl:attribute name="mainagencycode">US-tx</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- make a change to the unitid to add the correct attributes -->
<xsl:template match="ead:odd">
	<xsl:element name="ead:note">
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>

<xsl:template match="ead:unitid">
	<xsl:element name="ead:unitid">
		<xsl:attribute name="label">TSLAC Control No.:</xsl:attribute>
		<xsl:attribute name="countrycode">US</xsl:attribute>
		<xsl:attribute name="repositorycode">US-tx</xsl:attribute>
		<xsl:attribute name="encodinganalog">099</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- change unit titles to generally have the marc code inserted -->
<xsl:template match="ead:unittitle">
	<xsl:element name="ead:unittitle">
		<xsl:attribute name="encodinganalog">245</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- change highest level unit title to have both marc code and title label -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:unittitle">
	<ead:unittitle>
		<xsl:attribute name="label">Title:</xsl:attribute>
		<xsl:attribute name="encodinganalog">245</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:unittitle>
</xsl:template>
<!-- modify 1storigination to match the correct encoding analog attributes in the 100s -->
<xsl:template match="ead:origination[1]">
	<xsl:element name="ead:origination">
		<xsl:choose>
			<xsl:when test="@label='creator'">
				<xsl:attribute name="label">Creator:</xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="label"><xsl:value-of select="@label"/></xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:for-each select="ead:corpname">
			<xsl:element name="ead:corpname">
				<xsl:attribute name="encodinganalog">110</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:persname">
			<xsl:element name="ead:persname">
				<xsl:attribute name="encodinganalog">100</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:famname">
			<xsl:element name="ead:famname">
				<xsl:attribute name="encodinganalog">100 3</xsl:attribute>
				<xsl:choose>
				    <xsl:when test="@source">
                        <xsl:choose>
                            <xsl:when test="@source='Library of Congress Subject Headings'">
                                <xsl:attribute name="source">lcsh</xsl:attribute>
                            </xsl:when>
                            <xsl:when test="@source='naf'">
                                <xsl:attribute name="source">lcnaf</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="source">local</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="@role">
                    <xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
                </xsl:if>
				<xsl:if test="@authfilenumber">
					<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>.</xsl:text>
			</xsl:element>
		</xsl:for-each>
	</xsl:element>
</xsl:template>
<!-- update the highest level unit date to include the label=Dates: and encodinganalog -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:unitdate">
	<ead:unitdate>
		<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
		<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
		<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
		<xsl:choose>
			<xsl:when test="@normal">
				<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>
		<xsl:attribute name="label">Dates:</xsl:attribute>
		<xsl:choose>
			<xsl:when test="@type='bulk'">
				<xsl:attribute name="encodinganalog">245$g</xsl:attribute>
			</xsl:when>
			<xsl:otherwise>
				<xsl:attribute name="encodinganalog">245$f</xsl:attribute>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</ead:unitdate>
</xsl:template>
<!-- update the highest level abstract to include encodinganalog and correct label -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:abstract">
	<ead:abstract>
		<xsl:attribute name="label">Abstract:</xsl:attribute>
		<xsl:attribute name="encodinganalog">520$a</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:abstract>
</xsl:template>
<!-- update the highest level physdesc to include encodinganalog and correct label name -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:physdesc">
	<ead:physdesc>
		<xsl:attribute name="label">Quantity:</xsl:attribute>
		<xsl:attribute name="encodinganalog">300$a</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</ead:physdesc>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:langmaterial">
	<xsl:element name="ead:langmaterial">
		<xsl:attribute name="label">Language:</xsl:attribute>
		<xsl:attribute name="encodinganalog">546$a</xsl:attribute>
		<xsl:if test="@audience">
			<xsl:attribute name="audience"><xsl:value-of select="@audience"/></xsl:attribute>
		</xsl:if>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update repository to include the encodinganalog and correct links for tslac -->
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:repository">
	<xsl:element name="ead:repository">
		<xsl:attribute name="encodinganalog">852$a</xsl:attribute>
		<xsl:element name="ead:extref">
            <xsl:attribute name="xlink:actuate">onRequest</xsl:attribute>
            <xsl:attribute name="xlink:show">new</xsl:attribute>
            <xsl:attribute name="xlink:href">http://www.tsl.state.tx.us/arc/index.html</xsl:attribute>
            <xsl:attribute name="xlink:type">simple</xsl:attribute>
			<xsl:text>Texas State Archives</xsl:text>
		</xsl:element>
	</xsl:element>
</xsl:template>
<!-- general extref processing -->
<xsl:template match="ead:extref">
    <xsl:element name="ead:extref">
            <xsl:attribute name="xlink:actuate">onRequest</xsl:attribute>
            <xsl:attribute name="xlink:show">new</xsl:attribute>
            <xsl:attribute name="xlink:href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
            <xsl:attribute name="xlink:type">simple</xsl:attribute>
            <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
</xsl:template>
<!-- insert correct encodinganalog in acqinfo -->
<xsl:template match="ead:acqinfo">
	<xsl:element name="ead:acqinfo">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">541</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">541</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
		</xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update custodhist to generally have correct encodinganalog -->
<xsl:template match="ead:custodhist">
	<xsl:element name="ead:custodhist">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">561</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">561</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to sponsor tag -->
<xsl:template match="ead:sponsor">
	<xsl:element name="ead:sponsor">
		<xsl:attribute name="encodinganalog">536</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>
<!-- insert the logo/graphic reference in the tslac listed as publisher tag -->
<xsl:template match="ead:ead/ead:eadheader/ead:filedesc/ead:publicationstmt/ead:publisher">
	<xsl:element name="ead:publisher">
		<xsl:value-of select="."/>
		<extptr xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onLoad" xlink:show="embed" xlink:href="https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg" xlink:type="simple"/>
	</xsl:element>
</xsl:template>
<!-- modify creation to reword the output, pull the archivists name, 
insert proper attributes in the date and keep just the date and not the whole UTC code 
<xsl:template match="ead:ead/ead:eadheader/ead:profiledesc/ead:creation">
	<xsl:element name="ead:creation">
		<xsl:text>Finding aid created in ArchivesSpace by </xsl:text>
		<xsl:value-of select="substring(//ead:titlestmt/ead:author,15,1000)"/>
		<xsl:text> and exported as EAD Version 2002 as part of the TARO project, </xsl:text>
		<xsl:element name="ead:date">
			<xsl:attribute name="era">ce</xsl:attribute>
			<xsl:attribute name="calendar">gregorian</xsl:attribute>
			<xsl:value-of select="//ead:publicationstmt/ead:date"/>
		</xsl:element>
		<xsl:text>.</xsl:text>
	</xsl:element>
</xsl:template> -->
<!-- change descrules tag content to match our standards -->
<xsl:template match="ead:ead/ead:eadheader/ead:profiledesc/ead:descrules">
	<xsl:element name="ead:descrules">Description based on 
		<xsl:element name="ead:emph">
			<xsl:attribute name="render">italic</xsl:attribute>DACS
		</xsl:element>.
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to accessrestrict -->
<xsl:template match="ead:accessrestrict">
	<xsl:element name="ead:accessrestrict">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">506</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">506</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to processing info -->
<xsl:template match="ead:processinfo">
	<xsl:element name="ead:processinfo">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to appraisal info -->
<xsl:template match="ead:appraisal">
	<xsl:element name="ead:appraisal">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">583</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to separated materials -->
<xsl:template match="ead:separatedmaterial">
	<xsl:element name="ead:separatedmaterial">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">544 0</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">544 0</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to accruals -->
<xsl:template match="ead:accruals">
	<xsl:element name="ead:accruals">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">584</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">584</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to altformavail -->
<xsl:template match="ead:altformavail">
	<xsl:element name="ead:altformavail">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">530</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">530</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encoding analog to originalsloc -->
<xsl:template match="ead:originalsloc">
	<xsl:element name="ead:originalsloc">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">535</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">535</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to userestrict -->
<xsl:template match="ead:userestrict">
	<xsl:element name="ead:userestrict">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">540</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">540</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog attribute to phystech -->
<xsl:template match="ead:phystech">
	<xsl:element name="ead:phystech">
	    <xsl:choose>
	        <xsl:when test="parent::ead:archdesc">
		        <xsl:attribute name="encodinganalog">340</xsl:attribute>
	        </xsl:when>
	        <xsl:when test="parent::ead:descgrp">
		        <xsl:attribute name="encodinganalog">340</xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise/>
	    </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog and bio attribute to bioghist -->
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[1]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio1</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[2]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio2</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<xsl:template match="ead:ead/ead:archdesc/ead:bioghist[3]">
	<xsl:element name="ead:bioghist">
		<xsl:attribute name="id">bio3</xsl:attribute>
		<xsl:attribute name="encodinganalog">545</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to scopecontent -->
<xsl:template match="ead:scopecontent">
	<ead:scopecontent>
		<xsl:if test="parent::ead:archdesc">
			<xsl:attribute name="encodinganalog">520$b</xsl:attribute>
		</xsl:if>
		<!--
		<xsl:if test="@id">
		    <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
		</xsl:if>
		-->
		<xsl:apply-templates />
	</ead:scopecontent>
</xsl:template>
<!-- add correct encodinganalog to arrangement -->
<xsl:template match="ead:arrangement">
	<xsl:element name="ead:arrangement">
	    <xsl:choose>
	        <xsl:when test="parent::ead:descgrp">
        		<xsl:attribute name="encodinganalog">351</xsl:attribute>
        	</xsl:when>
        	<xsl:when test="parent::ead:archdesc">
        		<xsl:attribute name="encodinganalog">351</xsl:attribute>
        	</xsl:when>
        	<xsl:otherwise/>
        </xsl:choose>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- add correct encodinganalog to preferred citation -->
<xsl:template match="ead:prefercite">
	<xsl:element name="ead:prefercite">
	    <xsl:choose>
	        <xsl:when test="parent::ead:descgrp">
        		<xsl:attribute name="encodinganalog">524</xsl:attribute>
        	</xsl:when>
        	<xsl:when test="parent::ead:archref">
        		<xsl:attribute name="encodinganalog">524</xsl:attribute>
        	</xsl:when>
        	<xsl:otherwise/>
        </xsl:choose>        	    
		<xsl:apply-templates select="@*|node()"/>
	</xsl:element>
</xsl:template>
<!-- update physdesc when not direct child of a series -->
<xsl:template match="ead:physdesc[ancestor::*[@level='file']]">
	<xsl:element name="ead:physdesc">
		<xsl:apply-templates select="@*"/>
		<xsl:text>[</xsl:text>
		<xsl:apply-templates />
		<xsl:text>]</xsl:text>
	</xsl:element>
</xsl:template>
<!-- reformat controlled access to group like tags into subheadings and nested structure -->
<!-- change source from 'library of congress subject headings' to 'lcsh' when applicable -->
<xsl:template match="ead:ead/ead:archdesc/ead:controlaccess">
	<xsl:element name="ead:controlaccess">
		<ead:head>Index Terms</ead:head>
		<ead:p>
			<ead:emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</ead:emph>
		</ead:p>
		<!-- redirect added authors into controlled access terms and add the correct encoding analog -->
		<!-- trigger on the existence of the role attribute. Won't create segments if does not exist -->
		<xsl:if test="//ead:origination/ead:famname|ead:controlaccess/ead:famname">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Family Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:famname">
					<xsl:element name="ead:famname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:famname">
					<xsl:element name="ead:famname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<xsl:if test="//ead:origination/ead:persname|ead:controlaccess/ead:persname">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Personal Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:persname[@role]">
					<xsl:element name="ead:persname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname">
					<xsl:element name="ead:persname">
						<xsl:attribute name="encodinganalog">700</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<xsl:if test="//ead:origination/ead:corpname|ead:controlaccess/ead:corpname">
			<xsl:element name="ead:controlaccess">
				<xsl:element name="ead:head">Corporate Names:</xsl:element>
				<xsl:for-each select="//ead:origination/ead:corpname">
					<xsl:element name="ead:corpname">
						<xsl:attribute name="encodinganalog">710</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:corpname">
					<xsl:element name="ead:corpname">
						<xsl:attribute name="encodinganalog">710</xsl:attribute>
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@role">
    						<xsl:attribute name="role"><xsl:value-of select="@role"/></xsl:attribute>
    					</xsl:if>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
		<!-- begin rearrangement of controlled access terms into nested structure, but preserve structure if possible -->
		<xsl:if test="ead:persname[1]|ead:controlaccess/ead:persname">
			<ead:controlaccess>
				<ead:head>Subjects (Persons):</ead:head>
				<xsl:for-each select="ead:persname">
					<xsl:element name="ead:persname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname">
					<xsl:element name="ead:persname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:famname[1]|ead:controlaccess/ead:famname">
			<ead:controlaccess>
				<ead:head>Subjects (Families):</ead:head>
				<xsl:for-each select="ead:famname">
					<xsl:element name="ead:famname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:persname">
					<xsl:element name="ead:famname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">600</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:corpname|ead:controlaccess/ead:corpname">
			<ead:controlaccess>
				<ead:head>Subjects (Organizations):</ead:head>
				<xsl:for-each select="ead:corpname">
					<xsl:element name="ead:corpname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">610</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="//ead:controlaccess/ead:corpname">
					<xsl:element name="ead:corpname">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">610</xsl:attribute>
						<xsl:value-of select="."/>
						<xsl:text>.</xsl:text>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:subject[1]|ead:controlaccess/ead:subject">
			<ead:controlaccess>
				<ead:head>Subjects:</ead:head>
				<xsl:for-each select="ead:subject">
					<xsl:element name="ead:subject">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">650</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:subject">
					<xsl:element name="ead:subject">
                        <xsl:choose>
                            <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                        <xsl:when test="@source=''">
                                            <xsl:attribute name="source">lcnaf</xsl:attribute>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="source">local</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:if test="@authfilenumber">
                            <xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
                        </xsl:if>
                        <xsl:attribute name="encodinganalog">650</xsl:attribute>
                        <xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:geogname[1]|ead:controlaccess/ead:geogname[@encodinganalog='651']">
			<ead:controlaccess>
				<ead:head>Places:</ead:head>
				<xsl:for-each select="ead:geogname">
					<xsl:element name="ead:geogname">
					<xsl:choose>
						<xsl:when test="@source='Library of Congress Subject Headings'">
							<xsl:attribute name="source">lcsh</xsl:attribute>
						</xsl:when>
						<xsl:when test="@source='naf'">
							<xsl:attribute name="source">lcnaf</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">651</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:geogname[@encodinganalog='651']">
					<xsl:element name="ead:geogname">
					<xsl:choose>
						<xsl:when test="@source='Library of Congress Subject Headings'">
							<xsl:attribute name="source">lcsh</xsl:attribute>
						</xsl:when>
						<xsl:when test="@source='naf'">
							<xsl:attribute name="source">lcnaf</xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">651</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:genreform[1]|ead:controlaccess/ead:genreform">
			<ead:controlaccess>
				<ead:head>Document Types:</ead:head>
				<xsl:for-each select="ead:genreform">
					<xsl:element name="ead:genreform">
					    <xsl:choose>
					        <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source=''">
                                        <xsl:attribute name="source">aat</xsl:attribute>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
					        <xsl:otherwise>
					            <xsl:attribute name="source">aat</xsl:attribute>
					        </xsl:otherwise>
					    </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">655</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:genreform">
					<xsl:element name="ead:genreform">
					    <xsl:choose>
					        <xsl:when test="@source">
                                <xsl:choose>
                                    <xsl:when test="@source='Library of Congress Subject Headings'">
                                        <xsl:attribute name="source">lcsh</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source='naf'">
                                        <xsl:attribute name="source">lcnaf</xsl:attribute>
                                    </xsl:when>
                                    <xsl:when test="@source=''">
                                        <xsl:attribute name="source">aat</xsl:attribute>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
					        <xsl:otherwise>
					            <xsl:attribute name="source">aat</xsl:attribute>
					        </xsl:otherwise>
					    </xsl:choose>
						<xsl:if test="@authfilenumber">
							<xsl:attribute name="authfilenumber"><xsl:value-of select="@authfilenumber"/></xsl:attribute>
						</xsl:if>
						<xsl:attribute name="encodinganalog">655</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:title[1]|ead:controlaccess/ead:title[@encodinganalog='630']">
			<ead:controlaccess>
				<ead:head>Titles:</ead:head>
				<xsl:for-each select="ead:title">
					<xsl:element name="ead:title">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:attribute name="encodinganalog">630</xsl:attribute>
						<xsl:attribute name="source">lcnaf</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:title[@encodinganalog='630']">
					<xsl:element name="ead:title">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:attribute name="encodinganalog">630</xsl:attribute>
						<xsl:attribute name="source">lcnaf</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
		<xsl:if test="ead:function[1]|ead:controlaccess/ead:function[@encodinganalog='657']">
			<ead:controlaccess>
				<ead:head>Functions:</ead:head>
				<xsl:for-each select="ead:function">
					<xsl:element name="ead:function">
						<xsl:choose>
							<xsl:when test="@source='Library of Congress Subject Headings'">
								<xsl:attribute name="source">lcsh</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='naf'">
								<xsl:attribute name="source">lcnaf</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='aat'">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source=''">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:otherwise>
								<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:attribute name="encodinganalog">657</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
				<xsl:for-each select="ead:controlaccess/ead:function[@encodinganalog='657']">
					<xsl:element name="ead:function">
						<xsl:choose>
							<xsl:when test="@source='Library of Congress Subject Headings'">
								<xsl:attribute name="source">lcsh</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='naf'">
								<xsl:attribute name="source">lcnaf</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source='aat'">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:when test="@source=''">
								<xsl:attribute name="source">local</xsl:attribute>
							</xsl:when>
							<xsl:otherwise>
								<xsl:attribute name="source"><xsl:value-of select="@source"/></xsl:attribute>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:attribute name="encodinganalog">657</xsl:attribute>
						<xsl:value-of select="."/>
					</xsl:element>
				</xsl:for-each>
			</ead:controlaccess>
		</xsl:if>
	</xsl:element>
</xsl:template>
<!-- update ead:dsc to include a generic header -->
<xsl:template match="ead:ead/ead:archdesc/ead:dsc">
	<xsl:element name="ead:dsc">
		<xsl:attribute name="type">combined</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[1]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser1</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[2]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser2</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[3]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser3</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[4]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser4</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[5]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser5</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[6]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser6</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[7]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser7</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[8]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser8</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[9]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser9</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[10]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser10</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[11]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser11</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[12]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser12</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[13]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser13</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[14]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser14</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[15]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser15</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[16]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser16</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[17]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser17</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[18]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser18</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[19]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser19</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<xsl:template match="//ead:c01[20]">
	<xsl:element name="ead:c01">
		<xsl:if test="@level">
			<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		</xsl:if>
		<xsl:attribute name="id">ser20</xsl:attribute>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c01/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present -->
<xsl:template match="//ead:c01/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c02 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c02/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c02/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c02[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c03 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c03/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c03/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c03[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c04 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c04/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c04/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c04[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c05 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c05/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c05/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c05[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c06 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c06/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c06/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c06[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c07 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c07/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c07/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c07[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c08 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c08/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c08/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c08[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- c09 mods -->
<!-- add trailing comma and space to unittitle when a date or physdesc but not when it is empty -->
<xsl:template match="//ead:c09/ead:did/ead:unittitle">
	<xsl:choose>
		<xsl:when test="text()[. = '']">
			<xsl:apply-templates/>
		</xsl:when>
		<xsl:when test="../ead:physdesc">
			<xsl:choose>
				<xsl:when test="../ead:physdesc/text()[. = '[empty folder]']">
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="ead:unittitle">
						<xsl:apply-templates/>
						<xsl:text>, </xsl:text>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:when test="../ead:unitdate">
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unittitle">
			<xsl:apply-templates/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>
<!-- add trailing comma to unitdate if a physdesc is present or the next element is a unitdate -->
<xsl:template match="//ead:c09/ead:did/ead:unitdate">
	<xsl:choose>
		<xsl:when test="../ead:physdesc">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:if test="not(ancestor::ead:c09[@level='file'])">
				<xsl:text>, </xsl:text></xsl:if>
			</xsl:element>
		</xsl:when>
		<xsl:when test="following-sibling::ead:unitdate">
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
				<xsl:text>, </xsl:text>
			</xsl:element>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="ead:unitdate">
				<xsl:if test="@era">
					<xsl:attribute name="era"><xsl:value-of select="@era"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@calendar">
					<xsl:attribute name="calendar"><xsl:value-of select="@calendar"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@normal">
					<xsl:attribute name="normal"><xsl:value-of select="@normal"/></xsl:attribute>
				</xsl:if>
				<xsl:if test="@type">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:if>
				<xsl:value-of select="."/>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- add some attributes to the archdesc tag -->
<!-- add a overview head tag to the top level did -->
<!-- get related materials properly nested together -->
<!-- group content belonging in the descgrp into that tag -->
<xsl:template match="ead:ead/ead:archdesc">
	<xsl:element name="ead:archdesc">
		<xsl:attribute name="level"><xsl:value-of select="@level"/></xsl:attribute>
		<xsl:attribute name="type">inventory</xsl:attribute>
		<xsl:attribute name="audience">external</xsl:attribute>
		<xsl:for-each select="ead:did">
			<xsl:element name="ead:did">
				<!-- <ead:head>Overview</ead:head> -->
				<xsl:apply-templates />
			</xsl:element>
		</xsl:for-each>
		<xsl:if test="ead:relatedmaterial[1]">
			<xsl:element name="ead:relatedmaterial">
				<xsl:attribute name="encodinganalog">544 1</xsl:attribute>
				<ead:head>Related Material</ead:head>
				<ead:p>
					<xsl:element name="ead:emph">
						<xsl:attribute name="render">italic</xsl:attribute>
						<xsl:text>The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive.</xsl:text>
					</xsl:element>
				</ead:p> 
				<xsl:for-each select="ead:relatedmaterial">
					<xsl:element name="ead:relatedmaterial">
						<xsl:apply-templates/>
					</xsl:element>
				</xsl:for-each> 
			</xsl:element>
		</xsl:if>
		<xsl:for-each select="ead:custodhist">
			<xsl:element name="ead:custodhist">
				<xsl:attribute name="encodinganalog">561</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:prefercite">
			<xsl:element name="ead:prefercite">
				<xsl:attribute name="encodinganalog">524</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:acqinfo">
			<xsl:element name="ead:acqinfo">
				<xsl:attribute name="encodinganalog">541</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:processinfo">
			<xsl:element name="ead:processinfo">
				<xsl:attribute name="encodinganalog">583</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:appraisal">
			<xsl:element name="ead:appraisal">
				<xsl:attribute name="encodinganalog">583</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:separatedmaterial">
			<xsl:element name="ead:separatedmaterial">
				<xsl:attribute name="encodinganalog">544 0</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:accruals">
			<xsl:element name="ead:accruals">
				<xsl:attribute name="encodinganalog">584</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:altformavail">
			<xsl:element name="ead:altformavail">
				<xsl:attribute name="encodinganalog">530</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:for-each select="ead:originalsloc">
			<xsl:element name="ead:originalsloc">
				<xsl:attribute name="encodinganalog">535</xsl:attribute>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:element>
		</xsl:for-each>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>
<!-- now strip out the original copy of everything that was modified above -->
<xsl:template match="//ead:note/ead:head"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[2]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[3]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[4]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[5]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[6]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[7]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[8]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[9]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[10]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[11]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[12]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[13]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[14]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[15]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[16]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[17]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[18]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[19]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[20]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[21]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[22]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[23]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[24]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[25]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[26]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[27]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[28]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:did/ead:origination[29]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[1]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[2]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[3]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[4]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[5]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[6]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[7]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[8]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:relatedmaterial[9]"/>
<xsl:template match="ead:ead/ead:archdesc/ead:custodhist"/>
<xsl:template match="ead:ead/ead:archdesc/ead:prefercite"/>
<xsl:template match="ead:ead/ead:archdesc/ead:acqinfo"/>
<xsl:template match="ead:ead/ead:archdesc/ead:processinfo"/>
<xsl:template match="ead:ead/ead:archdesc/ead:appraisal"/>
<xsl:template match="ead:ead/ead:archdesc/ead:separatedmaterial"/>
<xsl:template match="ead:ead/ead:archdesc/ead:accruals"/>
<xsl:template match="ead:ead/ead:archdesc/ead:altformavail"/>
<xsl:template match="ead:ead/ead:archdesc/ead:originalsloc"/>
<xsl:template match="ead:ead/ead:archdesc/ead:odd"/>
<xsl:template match="//ead:c01/ead:controlaccess"/>
<xsl:template match="//ead:accessrestrict[@ audience='internal']"/>
<xsl:template match="//ead:c01/ead:scopecontent/ead:head|//ead:c02/ead:scopecontent/ead:head|//ead:c03/ead:scopecontent/ead:head|//ead:c04/ead:scopecontent/ead:head|//ead:c05/ead:scopecontent/ead:head|//ead:c06/ead:scopecontent/ead:head|//ead:c07/ead:scopecontent/ead:head|//ead:c07/ead:scopecontent/ead:head|//ead:c08/ead:scopecontent/ead:head|//ead:c09/ead:scopecontent/ead:head"/>
</xsl:stylesheet>''')
nsmap = {'xmlns': 'urn:isbn:1-931666-22-9',
         'ead': 'urn:isbn:1-931666-22-9',
         'xlink': 'http://www.w3.org/1999/xlink'}
def processor(my_xml):
    #parse as xslt for application below
    transform = ET.XSLT(catalyst)
    window["-OUTPUT-"].update("\nthis is supposed to fix a bunch of minor issues related to TARO 2.0 normalization, check output for correctness", append=True)
    #window['-OUTPUT-'].update("\n" + "this is supposed to fix a bunch of minor issues related to TARO 2.0 normalization, check output for correctness", append=True)
    temp1 = my_xml.split("/")[-1].split(".")[0]
    temp2 = f"{temp1}-done"
    finished_product = my_xml.replace(temp1, temp2)
    with open(my_xml, "r") as r:
        filedata = r.read()
        if "xmlns:ead" not in filedata:
            filedata = filedata.replace('xmlns="','xmlns:ead="urn:isbn:1-931666-22-9" xmlns="')
        #filedata = filedata.replace("ead:","ead:")
        with open(my_xml, "w") as w:
            w.write(filedata)
        w.close()
    dom = ET.parse(my_xml)
    myDates = dom.xpath(".//ead:unittitle/ead:unitdate", namespaces=nsmap)
    for item in myDates:
        boss = item.getparent()
        boss = boss.getparent()
        boss.append(item)
    newdom = transform(dom)
    newdom.write(finished_product, pretty_print=True)

    with open(finished_product, "r") as r:
        filedata = r.read()
        if "unitid>" not in filedata:
            if "abstract>" in filedata:
                filedata = filedata.replace("abstract>","abstract>\n<ead:unitid label='TSLAC Control No.:' countrycode='US' repositorycode='US-tx' encodinganalog='099'></ead:unitid>")
            else:
                filedata = filedata.replace('origination>',"origination>\n<ead:unitid label='TSLAC Control No.:' countrycode='US' repositorycode='US-tx' encodinganalog='099'></ead:unitid>")
        filedata = filedata.replace(' xmlns:xlink="http://www.w3.org/1999/xlink"',"")
        filedata = filedata.replace(' xlink:actuate="onLoad"',"")
        filedata = filedata.replace(' xlink:actuate="onRequest"',"")
        filedata = filedata.replace(' xlink:show="embed"','')
        filedata = filedata.replace(' xlink:show="new"','')
        filedata = filedata.replace(' xlink:href',' href')
        filedata = filedata.replace(' xlink:type="simple"','')
        filedata = filedata.replace(' xlink:role=""','')
        filedata = filedata.replace(' href=""','')
        filedata = filedata.replace('<ead:unitdate era="ce" calendar="gregorian"/>','').replace("<unitdate/>",'').replace('<unitdate><?xm-replace_text {date}?></unitdate>','')
        filedata = filedata.replace('xmlns=""','')
        filedata = filedata.replace("\t",'')
        filedata = filedata.replace("\n"," ")
        #filedata = filedata.replace("> <",">\n<")
        filedata = filedata.replace("><",">\n<")
        while "  " in filedata:
            filedata = filedata.replace("  "," ")
        filedata = filedata.replace(",, ",", ")
    with open(finished_product, "w") as w:
        w.write(filedata)
    w.close()
    unitid_text = temp1
    dom2 = ET.parse(finished_product)
    create_date = dom2.find("//ead:publicationstmt/ead:date", namespaces=nsmap)
    create_date_text = create_date.text
    creation = dom2.find("//ead:creation", namespaces=nsmap)
    creation_text = creation.text
    creation_text = creation_text.replace(create_date_text, f'<date calendar="gregorian" era="ce">{create_date.text}</date>')
    creation.text = creation_text
    dates = dom2.xpath("//ead:unitdate/ead:emph", namespaces=nsmap)
    screwballs = []
    flag = 0

    for date in dates:
        dateify = date.text
        date = date.getparent()
        if "normal" not in date.attrib:
            date.attrib['normal'] = timeturner(dateify)
        if "type" not in date.attrib:
            if "bulk" not in dateify:
                date.attrib['type'] = "inclusive"
            else:
                date.attrib['type'] = ""
        if date.attrib['type'] == "":
            window['-OUTPUT-'].update("\n" + dateify, append=True)
            date.attrib['type'] = input("date type missing, inclusive or bulk: ")
        if 'era' not in date.attrib:
            date.attrib['era'] = 'ce'
        if date.attrib['era'] == "":
            date.attrib['era'] = 'ce'
        if 'calendar' not in date.attrib:
            date.attrib['calendar'] = 'gregorian'
        if date.attrib['calendar'] == "":
            date.attrib['calendar'] = 'gregorian'
    dates = dom2.xpath("//ead:unitdate", namespaces=nsmap)
    screwballs = []
    flag = 0
    for date in dates:
        dateify = date.text
        if "normal" not in date.attrib:
            date.attrib['normal'] = timeturner(dateify)
        if "type" not in date.attrib:
            if "bulk" not in dateify:
                date.attrib['type'] = "inclusive"
            else:
                date.attrib['type'] = ""
        if date.attrib['type'] == "":
            window['-OUTPUT-'].update("\n" + dateify, append=True)
            placeholder = ""
            while placeholder != "inclusive" and placeholder != "bulk":
                placeholder = input("date type missing, inclusive or bulk: ")
                date.attrib['type'] = placeholder
        if 'era' not in date.attrib:
            date.attrib['era'] = 'ce'
        if date.attrib['era'] == "":
            date.attrib['era'] = 'ce'
        if 'calendar' not in date.attrib:
            date.attrib['calendar'] = 'gregorian'
        if date.attrib['calendar'] == "":
            date.attrib['calendar'] = 'gregorian'
    dates = dom2.xpath("//ead:date", namespaces=nsmap)
    for date in dates:
        date.attrib['calendar'] = "gregorian"
        date.attrib['era'] = "ce"
    notes = dom2.xpath("//ead:note/ead:head", namespaces=nsmap)
    for note in notes:
        note.getparent().remove(note)
    subjects = dom2.xpath("//ead:subject", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
    subjects = dom2.xpath("//ead:controlaccess/ead:genreform", namespaces=nsmap)
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
    subjects = dom2.xpath("//ead:geogname", namespaces=nsmap)
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local":
            flag += 1
    subjects = dom2.xpath("//ead:function", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        while subjective.endswith("."):
            subjective = subjective[:-1]
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
    subjects = dom2.xpath("//ead:persname", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
    subjects = dom2.xpath("//ead:famname", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
    subjects = dom2.xpath("//ead:corpname", namespaces=nsmap)
    subjectlist = []
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
        if 'encodinganalog' in subject.attrib:
            if subject.attrib['encodinganalog'] == "710":
                subject.text = subarea(subject.text)
            if subject.attrib['encodinganalog'] == "110":
                subject.text = subarea(subject.text)
            if subject.attrib['encodinganalog'] == "610":
                subject.text = subarea(subject.text)
        if subject.text in subjectlist:
            subject.getparent().remove(subject)
        else:
            subjectlist.append(subject.text)
        if subject.attrib['source'] == "local" or subject.attrib['source'] == "lcsh":
            flag += 1
    # sorts subjects, but causes head to sort into the middle so adding a preceding space to get it sort on top, then removing afterwards
    subjects = dom2.xpath("//ead:head", namespaces=nsmap)
    for subject in subjects:
        subject.text = " " + subject.text
    for node in dom2.xpath("//ead:controlaccess/ead:controlaccess", namespaces=nsmap):
        if node.tag == "head":
            node.text = " " + node.text
        node[:] = sorted(node, key=lambda ch: ch.text)
    subjects = dom2.xpath("//ead:head", namespaces=nsmap)
    for subject in subjects:
        subjective = subject.text
        subject.text = subjectspace(subjective)
    header = dom2.xpath("//ead:eadheader", namespaces=nsmap)
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
    header = dom2.xpath("//ead:eadid", namespaces=nsmap)
    for item in header:
        if 'encodinganalog' in item.attrib:
            item.attrib = item.attrib.pop('encodinganalog')
        if 'publicid' in item.attrib:
            item.attrib = item.attrib.pop('publicid')
        item.attrib['countrycode'] = 'US'
        item.attrib['mainagencycode'] = 'US-tx'
    header = dom2.xpath("//ead:ead", namespaces=nsmap)
    for item in header:
        if 'xmlns:ead' in item.attrib:
            item.attrib = item.attrib.pop('xmlns:ead')
        if 'xmlns' not in item.attrib:
            item.attrib['xmlns'] = "urn:isbn:1-931666-22-9"
        item.attrib['relatedencoding'] = "MARC21"
    containers = dom2.xpath(".//ead:container", namespaces=nsmap)
    for container in containers:
        type = container.attrib['type']
        container.attrib['type'] = type.capitalize()
        container_text = container.text
        if "-" in container_text:
            container_temp = container_text.split("-")[-1]
            while container_temp.startswith("0"):
                container_temp = container_temp[1:]
            container.text = container_text.split("-")[0] + "-" + container_temp
    container_dids = dom2.xpath(".//ead:did", namespaces=nsmap)
    for container_did in container_dids:
        container_type = set()
        containers = container_did.xpath("ead:container", namespaces=nsmap)
        for container in containers:
            window['-OUTPUT-'].update("\n" + container.text, append=True)
            container_type.add(container.attrib['type'])
        container_type = list(container_type)
        for item in container_type:
            window['-OUTPUT-'].update("\n" + item, append=True)
            container_list = []
            container_count = 0
            containers = container_did.xpath(f"ead:container[@type='{item}']", namespaces=nsmap)
            for container in containers:
                container_count += 1
            window['-OUTPUT-'].update(f"\n{len(containers)}", append=True)
            if len(containers) > 1:
                for container in containers:
                    container_list.append(container.text)
                container_list.sort()
                try:
                    top = int(container_list[0].split("-")[-1])
                    bottom = int(container_list[0].split("-")[-1])
                    for item in container_list:
                        temp = int(item.split("-")[-1])
                        if temp <= top:
                            top = temp
                        if temp >= bottom:
                            bottom = temp
                    container_text = container_list[0].split("-")[0] + f"-{str(top)} thru {str(bottom)}"
                except:
                    window['-OUTPUT-'].update("\n" + f"problem with {container_list[0]}, fix that and try again", append=True)
                    sys.exit()
                window['-OUTPUT-'].update("\n" + container_text, append=True)
                containers[0].text = container_text
                containers = containers[1:]
                for container in containers:
                    window['-OUTPUT-'].update("\n" + "removing",container.text, append=True)
                    container.getparent().remove(container)
    langs = dom2.xpath("//ead:langmaterial", namespaces=nsmap)
    for lang in langs:
        lang_text = lang.text
        if lang_text.startswith("<![CDATA"):
            lang.text = lang_text.replace("<![CDATA[","").replace("]]>","")
    extents = dom2.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        temp = extent.text
        other_tag = extent.getnext()
        if other_tag is not None and other_tag.tag == '{urn:isbn:1-931666-22-9}genreform':
            temp = temp + other_tag.text
            extent.text = temp
            other_tag.getparent().remove(other_tag)
    #now process in the brackets for physdesc inner content
    window['-OUTPUT-'].update("\n" + "on the languages", append=True)
    extent_types ={'45 rpm records': '45 rpm record',
                   '78 rpm records': '78 rpm record',
                   '8-track cartridges': '8-track cartridge',
                   'Beta (Betamax)': 'Beta (Metamax)',
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
                   'artifacts (object genre)': 'artifact (object genre)',
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
                   'cartoons (humorous images)': 'cartton (humorous image)',
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
    exceptions = ['class', 'collection', 'fonds', 'otherlevel', 'recordgrp', 'series', 'subfonds', 'subgrp',
                  'subseries', 'Sub-Series', 'Sub-Group', 'Series']
    scopenotes = dom2.xpath(".//ead:scopecontent", namespaces=nsmap)
    for scopenote in scopenotes:
        parent = scopenote.getparent()
        parent_attrib = parent.attrib['level']
        if parent.attrib != None and parent_attrib not in exceptions:
            paragraphs = scopenote.xpath("./ead:p", namespaces=nsmap)
            if paragraphs != None:
                for paragraph in paragraphs:
                    emphasis = paragraph.xpath("./ead:emph", namespaces=nsmap)
                    if emphasis != []:
                        window['-OUTPUT-'].update("\n" + "manual fix to scopenote needed", append=True)
                    else:
                        myText = paragraph.text
                        emphatic = ET.SubElement(paragraph,'emph')
                        emphatic.attrib['render'] = 'italic'
                        emphatic.text = myText
                        paragraph.text = ""
            else:
                emphasis = scopenote.xpath("./ead:emph", namespaces=nsmap)
                if emphasis != []:
                    window['-OUTPUT-'].update("\n" + "manual fix to scopenote needed", append=True)
                else:
                    myText = scopenote.text
                    emphatic = ET.SubElement(scopenote,'emph')
                    emphatic.attrib['render'] = 'italic'
                    emphatic.text = myText
                    scopenote.text = ""
                window['-OUTPUT-'].update("\n" + scopenote.text, append=True)
    notes = dom2.xpath(".//ead:note", namespaces=nsmap)
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
                            window['-OUTPUT-'].update("\n" + "manual fix to note needed", append=True)
                        else:
                            myText = paragraph.text
                            emphatic = ET.SubElement(paragraph,'emph')
                            emphatic.attrib['render'] = 'italic'
                            emphatic.text = myText
                            paragraph.text = ""
                else:
                    emphasis = note.xpath("./ead:emph", namespaces=nsmap)
                    if emphasis != []:
                        window['-OUTPUT-'].update("\n" + "manual fix to note needed", append=True)
                    else:
                        myText = scopenote.text
                        emphatic = ET.SubElement(scopenote,'emph')
                        emphatic.attrib['render'] = 'italic'
                        emphatic.text = myText
                        scopenote.text = ""
                    window['-OUTPUT-'].update("\n" + scopenote.text, append=True)
    extents = dom2.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        parent = extent.getparent().getparent().getparent()
        physfacet = extent.find("../ead:physfacet", namespaces=nsmap)
        dimension = extent.find("../ead:dimensions", namespaces=nsmap)
        parent_attrib = parent.attrib['level']
        if parent_attrib != None and parent_attrib not in exceptions:
            preceding = extent.getparent()
            preceding.text = "["
            extent.text = "[" + extent.text + "]"
            if 'altrender' in extent.attrib:
                if extent.attrib['altrender'] == "materialtype spaceoccupied":
                    del extent.attrib['altrender']
            #window['-OUTPUT-'].update("\n" + parent.attrib['level'], append=True)
            if physfacet != None:
                physfacet.text = "[" + physfacet.text + "]"
            if dimension != None:
                dimension.text = "[" + dimension.text + "]"
    #process the singularity of extents
    extents = dom2.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        tempstring = extent.text
        if "[" in tempstring:
            tempstring = tempstring[1:-1]
            window['-OUTPUT-'].update("\n" + tempstring, append=True)
        var = tempstring.split(" ")[0]
        if var == "1":
            tempstring = tempstring.replace("1 ","")
            window['-OUTPUT-'].update("\n" + tempstring, append=True)
            tempy = extent.text
            tempy = tempy.replace(tempstring, extent_types[tempstring])
            extent.text = tempy
    #process partial extents as 'includes'
    extents = dom2.xpath(".//ead:extent", namespaces=nsmap)
    for extent in extents:
        tempstring = extent.text
        parental = extent.getparent()
        if 'altrender' in parental.attrib:
            parent_part = parental.attrib['altrender']
            if "part" in parent_part:
                if not tempstring.startswith("("):
                    tempstring = f"(includes {tempstring})"
                    extent.text = tempstring

    # pull out access restrict with audience = internal if still there
    restrictions = dom2.xpath("//ead:accessrestrict[@audience = 'internal']", namespaces=nsmap)
    if restrictions is not None:
        for restriction in restrictions:
            restriction.getparent().remove(restriction)
    dom2.write(finished_product)
    with open(finished_product, "r") as r:
        filedata = r.read()
        filedata = filedata.replace('<extptr href','<extptr xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onLoad" xlink:show="embed" xlink:type="simple" xlink:href')
        filedata = filedata.replace('<ead:extref href','<ead:extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
        filedata = filedata.replace('<ead:archref href','<ead:archref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
        filedata = filedata.replace('<ead:bibref href','<ead:bibref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href')
        filedata = filedata.replace('label="Quantity"','label="Quantity:"')
        filedata = filedata.replace('label="Creator"','label="Creator:"')
        filedata = filedata.replace('label="Collector"','label="Collector:"')
        filedata = filedata.replace('label="Title"','label="Title:"')
        filedata = filedata.replace('label="Dates"','label="Dates:"')
        filedata = filedata.replace('label="Abstract"','label="Abstract:"')
        filedata = filedata.replace(", , <",", <")
        filedata = filedata.replace("..",".").replace(". .",".")
        filedata = filedata.replace("\n<ead:descgrp>\n<head>Administrative Information</head>","")
        filedata = filedata.replace('\n<ead:descgrp type="admininfo">\n<head>Administrative Information</head>','')
        filedata = filedata.replace("\n<ead:descgrp>","")
        filedata = filedata.replace('\n<ead:descgrp type="admininfo">','')
        filedata = filedata.replace("\n</ead:descgrp>","")
        filedata = filedata.replace("ead:","")
        filedata = filedata.replace("\n<physfacet>","<physfacet>").replace("\n<dimensions>","<dimensions>").replace("\n</physdesc>","</physdesc>")
        filedata = filedata.replace("<extent>[","[<extent>").replace("]</extent>","</extent>]")
        filedata = filedata.replace("<physfacet>[","[<physfacet>, ").replace("]</physfacet>","</physfacet>]")
        filedata = filedata.replace("<dimensions>[","[<dimensions>, ").replace("]</dimensions>","</dimensions>]")
        filedata = filedata.replace("][<physfacet>","<physfacet>").replace("][<dimensions>","<dimensions>")
        filedata = filedata.replace('\n<relatedmaterial>\n<p>\n<emph render="italic">The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive.</emph>\n</p>','')
        filedata = filedata.replace('\n<relatedmaterial>\n<p>\n<emph render="italic">The following materials are offered as possible sources of further information on the agencies and subjects covered by the records. The listing is not exhaustive. </emph>\n</p>','')
        filedata = filedata.replace("\n</relatedmaterial>\n</relatedmaterial>\n</relatedmaterial>","\n</relatedmaterial>\n</relatedmaterial>")
        filedata = filedata.replace('\n<controlaccess>\n<head>Index Terms</head>\n<p>\n<emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</emph>\n</p>\n</controlaccess>','')
        if "852$a" not in filedata:
            filedata = filedata.replace("</abstract>",'</abstract>\n<repository encodinganalog="852$a">\n<extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href="http://www.tsl.texas.gov/arc/index.html">Texas State Archives</extref>\n</repository>')
        filedata = filedata.replace('<repository encodinganalog="852$a">\n<extref xmlns:xlink="http://www.w3.org/1999/xlink" xlink:actuate="onRequest" xlink:show="new" xlink:type="simple" xlink:href="http://www.tsl.texas.gov/arc/index.html">Texas State Archives</extref>\n</repository>\n<unitid label="TSLAC Control No.:" countrycode="US" repositorycode="US-tx" encodinganalog="099">\n</unitid>\n','')
        filedata = filedata.replace('\n<unitid label="TSLAC Control No.:" countrycode="US" repositorycode="US-tx" encodinganalog="099">\n</unitid>','')
        filedata = filedata.replace('<controlaccess>\n<head>Personal Names:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Family Names:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Corporate Names:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Subjects (Persons):</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Subjects (Families):</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Subjects (Organizations):</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Subjects:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Places:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Document Types:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Titles:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Functions:</head>\n</controlaccess>\n','')
        filedata = filedata.replace('<controlaccess>\n<head>Index Terms</head>\n<p>\n<emph render="italic">The terms listed here were used to catalog the records. The terms can be used to find similar or related records.</emph>\n</p>\n</controlaccess>','')
        filedata = filedata.replace('<controlaccess>\n</controlaccess>\n','').replace(" , ",", ").replace(", </unitdate>, ","</unitdate>, ").replace(",</unitdate>, ","</unitdate>, ").replace(", </emph>, ", "</emph>, ").replace(",</emph>, ","</emph>, ").replace(" </unitdate>, ","</unitdate>, ")
        filedata = filedata.replace("</unitdate>, </unittitle>\n<physdesc>",", </unitdate></unittitle>\n<physdesc>")
        if 'xmlns="urn:isbn:1-931666-22-9" xsi:' in filedata and 'relatedencoding="MARC21" xmlns="urn:isbn:1-931666-22-9">' in filedata:
            filedata = filedata.replace('relatedencoding="MARC21" xmlns="urn:isbn:1-931666-22-9">','>')
        filedata = filedata.replace("[[","[").replace("]]","]").replace("[ [", "[").replace("] ]","]").replace(",</emph>\n, </unitdate>","</emph>, </unitdate>")
        filedata = filedata.replace("\n<unittitle>, </unittitle>","")
        filedata = filedata.replace('<container type="box">','<container type="Box">').replace('Texas-digital-archive', 'Texas-Digital-Archive')
        filedata = filedata.replace('<container type="folder">','<container type="Folder">').replace("&lt;","<").replace("&gt;",">")
        filedata = filedata.replace("English.</langusage>", '<language langcode="eng" scriptcode="Latn">English</language>.</langusage>')
        # removed a few blank items i think, appears to create a problem so removing for now
        #filedata = filedata.replace("\n<?xm-replace_text (be sure level attribute is correct)?>","")
        #filedata = filedata.replace('\n<change>\n<date era="ce" calendar="gregorian">\n<?xm-replace_text {date}?>\n</date>\n<item>\n<?xm-replace_text {item}?>\n</item>\n</change>','')
        #filedata = filedata.replace('<unitdate era="ce" calendar="gregorian" normal="0000/0000" type="inclusive">\n<?xm-replace_text {date}?>\n</unitdate>\n','')
        #filedata = filedata.replace('\n<note>\n<p>\n<emph render="italic">\n<?xm-replace_text {Notes, if desired}?>\n</emph>\n</p>\n</note>','')
        #filedata = filedata.replace('\n<unittitle>\n<?xm-replace_text {title}?>, </unittitle>','')
        filedata = filedata.replace('\n<!--Remove the ead.xsl and ead.css statements above before uploading to TARO.-->','')
        donkeykong = re.findall(']</physdesc>\n<unitdate *.*, </unitdate>\n</did>', filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                dittykong = item.replace(", </unitdate>"," </unitdate>")
                filedata = filedata.replace(item,dittykong)
        donkeykong = re.findall(r'\n*.*<\?*.*xml-stylesheet*.*\?>*.*', filedata)
        if donkeykong:
            for item in donkeykong:
                filedata = filedata.replace(item,"")
        donkeykong = re.findall(r'\n*.*Remove the ead*.*xsl and ead*.*.css statements*.*>\n',filedata)
        if donkeykong:
            for item in donkeykong:
                item = str(item)
                filedata = filedata.replace(item,"")
        if ' xmlns="urn:isbn:1-931666-22-9" ' in filedata and ' xmlns="urn:isbn:1-931666-22-9">' in filedata:
            filedata = filedata.replace('xmlns="urn:isbn:1-931666-22-9">','>')
        filedata = filedata.replace('xsi:schemaLocation="urn:isbn:1-931666-22-9 ead.xsd" xmlns="urn:isbn:1-931666-22-9"','xsi:schemaLocation="urn:isbn:1-931666-22-9 ead.xsd"')
    with open(finished_product, "w") as w:
        w.write('<?xml version="1.0" encoding="UTF-8"?>\n<!--Remove the ead.xsl and ead.css statements above before uploading to TARO.-->\n<!-- <?xml-stylesheet type="text/xsl" href="ead.xsl"?> <?xml-stylesheet type="text/css" href="ead.css"?> -->\n' + filedata)
    w.close()
    switch = True
    if switch is True:
        try:
            dom3 = ET.parse(finished_product)
        except:
            window['-OUTPUT-'].update("\n" + unitid_text, "has a xml tag problem, check it for errors. We suggest using a web browser at minimum.", append=True)
    if flag > 0:
        window['-OUTPUT-'].update("\n" + f"potential subject term issue in {unitid_text} check it manually", append=True)
        switch = False
    window['-OUTPUT-'].update("\n" + f'{unitid_text} finished', append=True)
    window['-OUTPUT-'].update("\n" + "all done!", append=True)

Sg.theme('DarkGreen')
layout = [[
    Sg.Push(),
    Sg.Text("EAD file"),
    Sg.In(size=(50, 1), enable_events=True, key="-EAD-"),
    Sg.FileBrowse(file_types=(("xml text files only", "*.xml"),)),],
    [
        Sg.Push(),
        Sg.Button("Execute", tooltip="This will start the program running"),
        Sg.Push()
    ],
    [
        Sg.Button("Close", tooltip="Close this window. Won't work while XML is being processed", bind_return_key=True)
    ],
    [
        Sg.Multiline(default_text="Look here for information about various data points as the file processes. Your processes file will end in '-done'",
                     size=(70, 5), auto_refresh=True, reroute_stdout=False, key="-OUTPUT-", autoscroll=True,
                     border_width=5)
    ]
]

window = Sg.Window(
    "TARO EAD processor",
    layout,
    icon = my_icon
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
