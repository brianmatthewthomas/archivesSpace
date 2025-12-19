import lxml.etree as ET
import PySimpleGUI as Sg
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

my_icon2 = b'iVBORw0KGgoAAAANSUhEUgAAAH0AAAB9CAYAAACPgGwlAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABZdSURBVHhe7Z0JXJVlvsf/z/Oec9gVRFFxA0FQM7XAjWqIyaZULG+Lad5sZspMu5PNtHk/c0utW41tc/NOOpZzb9Pk2nQrRatrjS0uEGpiCgiIimuIgOzLOe8z///LAwIeDmfnHA7fFs7zPyznfX/Pf3mW930ZdBPu3SKU/cYf+wqoj2I6XSwXECdUEQOgDgEQEQA8VAgRDEIEMAaKUl8DuqpyVQAz4kmoB84rBYgyfK9YqHCWMX4cX+cBUwp0QexkvP/lSx/Onm2Sf86r8VrRE7aeDSyt+ekapsIUFDZJAIxFcYfiAQUBqtUZSh2KXl0uWxYQ2BWAVeGZKsKOcJhxtoczSPdjpuwDC++okd/lVXiP6EKw2A8yBgm94ecoQyp6cRIDNRJQBfkdNmG16GbADqbil3MYPfZhB0vz435fZT16yzl8jW95Ph4vevSGff1B8UtlJnUOij2FMRYk33IIR0RvD6aNasb5Xjybm/TBhrTD828rlm95JB4pevKuXbpzF0KmmBgswOiaih8yTL7lNJwpemvw85YBZ2lcp7zT71xA+jcrUozyLY/Bo0QfuHV/oH81n8VAPA5CnYDhksu3nI6rRG8GvV/lnGViIbgqQDF94kn53yNET0Cxy6tgnmDwJCbMeHd8KleL3gK6PtYdx/D/bwTpB64/sDCxy8XvUtET9u/Xl+WJe/Dlc+jVo5qs7sFtorclRwB/MUg/4O8ofqO0uZ2uER0r8ZhNmVNUYCvRs2/A4sztn6OLRKewj7rzPTpF98yRhbend0XF7/aTHfuXb/uJgIAVOOZ5CLU2SLPb6SrRm0HtG7iiW2dUApflLUwpkWa34D7Rybs3Zs4UwN7C3h0lrV1GV4veipOMsyXZi1K3ucvr3SL68C37ezOjuhLDOXm3Tpq7FA8SnbzeyBVlXZ3it7Rw4a2XpdlluFz0ER9kjDcp/K/4p8ZKk0fgSaI3g25+WFEM848uuj1LmlyCy8bBFM5jN2XMM3H2tacJ7qmgB441mRq+Hr1mxzw6f9LsdFzyi0dv2WKoM0Yvw/z9DNblHhHO2+OJnt6MAAz3THkVimtWZK+Y3SDNTsPposev2x1iDPJfi3lqLhYm0up5eLLoGjSpw/lG1c+08NjDsyql1Sk4NbyP/GtGeEOA4WP8uB4tuFdA5w8dh9UrH4/8753h0uoUnCY6rYY16Nh2xvkt0tSDE2CqwPNZu33Mu1/2lyaHcYro2vIn06VhOJokTT04C3R4/HeSsb42zVnCOyw6hXQmlE8ZsERp6sHZkPBCTTQ21HzqjFDvkOhUtNXr+OYeD3cDmOOZCpOA122KX/dJiLTahd2i07DMGGBYyzjryeHuQvN4MZXXK2tHL9ti97qFfaILwRoahi0TnM+Vlh7ciarOhYjAZfZO4Cjyq03Exk2fZ+L8NebCnS2uhhsbgTfWyZaXgaFeCHVKxMH84xe3b/xRWq3G5p4yYlP6OJOqfI1/OFSavBIPW3DRvuo4B9rb26gKzdbZNgP8qXJFMdxs61y9TaIPX7uzNwT3/hYLN6+fS+9q0UlnHSp8TURvSB7WHxIi+0BkSKBmO11RA3/clwOHLpTJ7+4Y/DVZQfqA5AM2rM5ZLzqth2/IWC247lFp8Wq6SnTy4FB/A9w5cgjcPWooxPQJRu++IsPpimp44rMDkH2xvFNPbwbr+j9nP5a6GH+gKWR0gtWix/xt3x2qovvIU9bDHaUrRA/UK3D/tdEwf9xw6BvoJ61XyC2pgMXbM+BClW21hrZAw/nd2YtnbpUmi1gletz6XX2NEJSJYb3Ld7w4C3eKTif5luED4Kmk0TC0t/lrNXJLLsOCrRlwqbZeWmzmpEkfMsGarVdWVd8mEfBCdxLcXVCsJY9+47YE+K/bEzsUPP9SJSzc5pDgRJTSWLVCvrZIp54es373FJX57cKwfnU88mJc7emUu1OiB8Cy5LHQP9hfWq/mRHkVPPTpPptDunlEvdAZUnIfnbZPGsxi0dMT1u7XCzCs7G6Cuxo9Dr2exFC+atoEi4KfRMEfwZDuHMEJ1MnYuJJ0kwazWBS9IrD+HqwIb5TNHqygT4ABVs+YCA9fH6sNvzqCBF+wNR3OVjr3ghcmxI3VpuK7ZdMsHX4q7C2BZcHqfszlbr3yxF04O7xT/o7rEwJvTUuEqNDgJmMHHC+thEcwh5+vqpUW54KfJSdID4kdXT/XoaeXBzbc310FdzaUv5MG94X3/iWpU8GpSn8IPdxVghPoyaOqTXC/bF6FWdET1m4NFFx5SjZ7sAAJnho3GP40fSKE+Vte+Dp4vhQeRsGLq90w56+yJydv3hsgW20wK/rloP6zgCvxstmDBeaOiYKXbxkPAXrLa1e7i4q1YVlprdM3t5qFgRhZUXp5lmy24SrRk5ft0qmMPS6bPVjg19fFwO9/di3oFYv1MGSeuwS//Xw/VDe6+f4ExsYlpKdstXDVpz0/3H8yVuwTZLOHDliA1fnvpowCpZNb3uRdqoAnPiPB3X9jKhXEhIv9aifLZgtXiW7UwSMouuWu6+OQ4Esmj2yzUGKOn7BY+82OTCirc09Ibw9DHVVhekQ2W2gj7tj390QAU1Jlswcz/Gp8jFWCVzUY4YnPD2jLpF2Lmjp29RcRsqHRRvQahc8Axp1+U5/uAFXpVLRRSO9McKMqYNmuLDh0oVRaug709jCjMM6QTY3WojMheva8mYMEvyN+CCy96ZpOczixOvMY7Mg/SydcWroWIVTU9cp+uhbRR7y3N1LlLEk2e5DQTNvNUf1hRcpYbU69M9LyzsI7Bwo8RnACRU8atyYtUjaviK4y/nPM+065MV93Ynz/MHj1F9eDv67zPaRHisth+ddZoGJk8CSwAwY1qEqKbF4RXejYTPmyB0lUaBCsmpYIIQaLi1YaJTX18LsvDkBNFwzNrIGBqUVfTXRaXBGMT9EsPWiEBxjgT9MnQL+gjpdGm6k3qbB050EPqNQ7BqNPEk2v02tN9OpgIy2stMR8X4dC+Zu3J8LwsM6vHqJA/lZ6Duw5fbHzHSldioisNjUtoGmiY0SiG+22hHpfhoZjy28eCxMirbtOcAcWbu9nFXpU4WYOhmNxrgotmjcJrfRU7QQNzRYmjsDh2WBpsQxNsa745jCGTmnwcHDQpunM792yRRHAxmlWH4YEnzZiECxKjJMWy1TUN8LT/39Qm3nzFrBvjiW9+bG6QeHYA4ZKu89yTUSoNha3tMWpGRqSvfTtj5qnexWqOuxYSe9wXquyKIz3lrd7dHPCA/zgzdsSrBqaEZuPnIJtmMs9PY+3Bz9tsEkxDeOg8Bj89NLse9As2x9uva7DPentoQmY1/Zmy5aXgTqbVDWWqyB8d4cMhuknJo+EG4b0kwbLXMY8/uyXP0Cd0Ysf2iQgjgsOw2XTpxD4z/S4QTB/vHWHT3n85W+PQGGpU2/p5n6EiMEhGx8imz5FXHgveD55LI5WrUttn+Sexjx+xuvyeHuwfhtC4/Q2C+y+QLCew5s3xUMvP+sKN9qn/ofdR2XLuxFCjeAovU9tmiA/XZ4wFOJDze4OvgrK37//xyGvGo9bgjEeyoXwneEapmWYG9sXZkVZfyu2NZl5kGXFHSG8BlUNofDuMxcnXtsnEJaOH6J5uzVknCmB/z103OvzeGuw3/txBsK6xOblhOgVeGNyFATprFtXKq9rgOd3ZWn73boT2H/xDHSnbtwBdIDPXz8EYntbl8dJ5tf3ZkPR5eomQ/eCc22loRtDR3dXdLhNefzL4+fh45zT3dUfVC6Aue2hcCRAsE6BxH7BmhD3Dg+HsZhnXUlsL3/4j+sGgxXrKBq07eml745o3t4dQQ2MLHr99xWMc4duMNsZJHZsb394OL4/TB0cCn38rlxeZcI3PywsgRcOnIZ6J+dPP4XB+pQ4uK6vdQMUCnrP7PxB29HaXZMeHmIlbRSpkm2XEKBwrJgHwdZfjILZMX3bCE7QjNicmH7wx6RoMFjrjlZAAi4ZE2m14MTOwgtyv7o0dEPQwSspp7tkEEo+Gx3iB5umxsMjowaAfydV822Dw7Riy1nn+4YBveDXGFmspbS2Hl7pxmG9GSHUclRCOP0B7xTOJ2He3nRLPIwJsz5nz4ntBw/E9dN+3hHCDDp4ecIw0FsZOejPvbkvx4k3/PFcGOPFJPpp2XYKFFanDwmFdckjoK+/bVMAJNEzYwdjSHbsmovnrh8MQ4Ktn3PaW3RRW1DpzmG9BQZFnAt2XDYdhgS/O7ovvJk03OpJkPYE4M+9OikKQvS2/zxFiDuG9YGZw6wfntU0GuGV3Ue8ZnOjowhQCzkTkCfbDkEnfPrQMHhp4jCHC7IYHGYtHWfdjtTWDAoy4PBsiNXDM+IvB49rq2g+g8rz8PyYChxOogid8DCszOd+dQwe230cMoorHSqK7sVKPyWyt2x1Dgn9YuJQCPe3/n7FJHZ3m1u3COqsMF7A/QWcwrDs0LCNPLus3gjr80vg0KVq+PxMOfzrrjx4PvMU1BhV+V22QUO55QlDoLeh8wsHqc/OxU5ysw2dhHbCvLon27u3PtkInqYqvT+c5PH+Zy9hPz8l7TZD3kxj7xqT2qYQohy5vqAEHv42Hy7buRY9OMgPC7tBnUaM6F5+8BQWgLbw5Ymf4Lsipw9cPBvOT40IqSrlH86ebWJCHJZmmyGdL6GXmwuQ1AnSi6sw3Bfa7fH3DO8LN/bveMJQh3/kPxOHQS8rIkIzdNOf138oki3fAeXIIr1liSz2NH21D3rmSEdQZ9j7UyUsP1CkhVRboYsPaKeLudEA/Toa10+x0CnM8X5+MZyo7P5j8vYIxvfS16YzaWxMx7xunytaAXn8Rycuwd/yL0qLbQzHav43YwaiyG07Dc3nPzHGtottz9c0wDs5P2FnNBebui8CUF/OtVuCa6KH1pfloPkcvXYlKw+dgcyL9tWM80dEtJlHp7BO1XpwJ3dqbM/qo+exxvCd4u0K7FwQa8ylV5rodLdgpqqa67sSWkV7Ov0ElGINYCt+CsfcPRT88Ss5/IMY1idF2BbW8y/Xwt8x4rQuOH0GxvY23xW6JVFyzrfJly6lqKoBVmj5XRpsYFRYIFbpkRAX6q+toNnKqiPnocFXpt7agemsRd8W0VmDcRemdZfvDyIvSysqg62nLkmLbcyPi4D3b46DIBvD+o+l1fDFGfc/kssToHkYIxe7ZPOK6Pm/TDrHVOHyEN/Myz+cgQtYVNkKTdpEBNi2kEO+/fbRC9qGDV+EYdWevyi1pWZrER0RCqgb5GuXU4J5/RUs7Nwhw9HSGvjHOasfUNjtUBW2EaVvOdWtRYcAVd2Blb1bdvZTLbUdw/w3bhDjnVzf9XI86lI/od8hmxptRD88/4ZiEKY02XQ5JAN5u72zddZQWFEHO300lxMMeNrhxbe1mW9uIzqhE2ItZn7XqdCO/Mt1sL7AdXPgNCFUb/JRL0cducLekc0WrhJ9YH59Bn7397Lpcqia/3P2BSiudf5ObFr5o1GCT47LESzgvu97ITBDNlu4SvRvVqQYFVVdJZtuoazeBGtQeGez43SZ9rt9FQFsFekpmy1cJToRblA/wdyuTdm5A/LELYUXnboIQoXb5uMlPuvlAkRuaL8+n8hmG8yKnn5fUi03ml6XTbdQi3l3NY6lnUVOWS1kl3nuvVpdDWPK66SjbLbBrOhE71rDRhy+ue02SuSQaUWl2vy4M6Df5aMzrhTWswN1Ko7NzdOh6AcWJtYoxsYXqQSUJpdDCzJrcxz3drq8mIZpPhnaUS/GxAsdPXKT6FB0olet30fo7btl0+WQRjRhU+hgbs/DaHGqyqFnkXst6OXfBeoi/082zWJRdPT2Rq6KZ7DzuO0Mkrf/T+5PsmUfuy9U+GhoR50U3bOkmzSYxaLoRMEDk9MVoa6TTZdD3v7pqVI4Z8diTDO0PcsnQzvj63IXT0+XrQ7pVHSCQ81yUNWTsulyqhtV2GDn1qqqRhMc8c2q/YRJJ5bL1xaxSvS8eSklHIyPY5h3y321msbtJXZtnT5YUgWldW67z4JHQLqoTLckb+EdJdJkEatEJwrun5LGVdO7sulySuqM8Nlp2xf8miZkfCy2c+XdY4unWb1QZrXoeCYFE7AUw3yWtLgU0u0DDPG23N3pWHktfOVj6+YCRJaxF19K+khTp1gvOoJFXYViqn8Q44lb1ipzUMSvz1snIk27rsw6Y3EPfncDj7RcUfiDBQ9Mt+lpAzaJTuTPvymLq+pj7srvr2Wd1YqzznjvWDF8c97LnrTgAHT+OVceO7pops2R12bRiYJ5EzcyMK2UTZdC6+3//v0pqO1gowXNF24suAivHj4rLT4AHjRX+MrsRdM7nGq1hF2iU/4Iq9StYKrr99RRbt+OBd19X+XCl2fLoaLBpF0e1WBStQWV3+47Ac/tL+p2d3a0COcbApSBK2zJ461xqMwdveVIcL2x+mPBlKnS5FIwpEEvg067SrYORb+IQzPaFGPPQSh1NaCr9rJtVCQxZzuZCL4r+99S7L683OGxzejNe/vUGXXbsfdNliavwOtEbxJ8HzPoU7MX3O7Qg9ntC++tyL4vqRRMjXeiG2ZKUw8uQDCWqQ8xzHJUcMJh0YlC2kXr15AKQu103rcHG2nK2umGXobUw/Pb7mq1F6eIThTefUOxv2KcwUDdKU09OAOGOdzPMMNZghNOE52gUO+nVN/FBFb1NJbqwX7o/HG+ngEWbU4I6a1xquhE9uyUqtA4/kv81C+5awKnu0HnjSn8pUBlwK8cqdI7wuHqvUOEYNGbvp/LBH8bQ1SotHoMnlq9o4OXcx1fnP3ojE32jsM7w+me3gJ+4BNzJ23QAU/GI3HLIo23gwpn6fx1ydmLUje6SnDCdaJL8u5POAw6lox5fk1PuDcPnRfB+JoGfUDykQXT7b7Tl7W4Lry3B8N97IbMVJWxt7AXR0trl+FB4f2E4MrjuYumb3eld7fG5Z7eAh5QwbyJ23SCTcQe8Db2bt/crtoCHj9jb5v0MDF38Yw0dwlOuM/T28JiN6VPUlVlJR7pTawLtrp0ladjZ8dD5t+Bojybu3haBp4Kt4ndjPs8vS2iYM7k9LBKNpUzMRfPg5c+kNw2UN1sptfNDTIMnNq0a9X9ghNd5eltSNi6P7C0ls1hqvo0fqSR0uxS3Obp6NiCsRzGda8HKsZNlq48cRceIXozgzfvDTAIvztBVZdgcyLmOZdFIleLjtFLZZxnCKasCg0P/bSjiwm7Ao8SvZnkZbt0p0eFTsJh3gJViJmY8fvIt5yGq0THeF2Kn3cb58q7dEMAc9eHdzUeKXprYjcf7IfCp+LLOUJVk7Dmc8pToJ0pOnp1Fd22i+7iFGDotf3QQz+z70oNN+HxoreA4/wRWw5FClBTVBVmYqZMQlskdgK7UoAjolPoxtRzDjjbw5myzaTX7Tr20K3n3TnscgTvEb0dVPyV1+hHgjAmqdQBAMahGkPxgILx5Dd9kwWsFp2GWIxVYZ8rwu6Vpd0+m/N9dHNdTyjK7MFrRW/PvVuEckDJChdGEQWqiMWhYDyqFY2qDcX/IrCEDkP9glHEAOwTilKPoleVq/g9RjwJ9ShkJUaPMvTVYvz+0yhwoQq6Y4qA4/QIDHoiAt0gX/45Lwbgn72UwrVV92ChAAAAAElFTkSuQmCC'
def normalized_source(source):
    if source == "Library of Congress Subject Headings":
        source = "lcsh"
    if source == "naf":
        source = "lcnaf"
    if source == "":
        source = "lcnaf"
    return source

xml_header = '''<?xml version="1.0" encoding="utf-8"?>
<!--Remove the ead.xsl and ead.css statements above before uploading to TARO.-->
<!-- <?xml-stylesheet type="text/xsl" href="ead.xsl"?> <?xml-stylesheet type="text/css" href="ead.css"?> -->'''

singularization_dict = {'45 rpm records': '45 rpm record',
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

translation_dict = {}

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
          /* Use Times New Roman for default font */
document {
  font-family: "Times New Roman";
  font-size: 12pt;
  margin-top: 5px;
  margin-left: 5px;
}

comment {
  display: block;
  color: purple;
  white-space: pre;
}
head>title {
display: none;
}
abstract, accessrestrict, accruals, acqinfo, add, address, addressline, admininfo, altformavail, appraisal, archdesc, archref, arrangement, author, bibliography, bibref, bibseries, bioghist, blockquote, c, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, change, chronitem, chronlist, container, controlaccess, corpname, creation, custodhist, dao, daodesc, daogrp, daoloc, date, defitem, did, div, dsc, ead, eadheader, eadid, edition, editionstmt, entry, event, eventgrp, extref, extrefloc, famname, filedesc, fileplan, frontmatter, function, genreform, geogname, head, head01, head02, index, indexentry, item, label, langusage, linkgrp, list, listhead, name, namegrp, note, notestmt, num, occupation, odd, organization, origination, otherfindaid, p, persname, physdesc, physloc, prefercite, processinfo, profiledesc, ptrgrp, publicationstmt, publisher, ref, refloc, relatedmaterial, repository, revisiondesc, row, runner, scopecontent, separatedmaterial, seriesstmt, sponsor, subject, subtitle, table, tbody, tfoot, tgroup, thead, title, titlepage, titleproper, titlestmt, unitdate, unitid, unittitle, userestrict {
  display: block;
}

c01 {
  display: block;
  margin-left: 10pt;
}

archdesc>did {
  display: block;
  margin-top: 5pt;
  color: black;
}

c02 {
  margin-left: 20pt;
}

c03 {
  margin-left: 20pt;
}

c01>c02>c03>scopecontent {
  margin-left: 30pt;
}

c04 {
  margin-left: 20pt;
  color: black;
}

archdesc>head {
  margin-left: 10pt;
}

scopecontent>p {
  margin-left: 10pt;
}

archdesc>p {
  margin-left: 15pt;
}

repository {
  margin-left: 10pt;
}

archdesc>did>repository {
  margin-left: 10pt;
}

archdesc>did>origination {
  margin-left: 10pt;
}

archdesc>did>unittitle {
  margin-left: 10pt;
}

archdesc>did>unitdate {
  margin-left: 10pt;
}

archdesc>did>abstract {
  margin-left: 10pt;
}

archdesc>did>physdesc {
  margin-left: 10pt;
}

archdesc>did>physloc {
  margin-left: 10pt;
}

archdesc>did>unitid {
  margin-left: 10pt;
}

controlaccess>controlaccess {
  margin-left: 20pt;
}

controlaccess>controlaccess>head {
  margin-left: 25pt;
}

controlaccess>subject {
  margin-left: 30pt;
}

controlaccess>corpname {
  margin-left: 30pt;
} 

dsc {
  display: inline;
}

dsc>scopecontent {
  margin-left: 10pt;
}

c01>did {
  margin-left: 15pt;
}

c05 {
  margin-left: 20pt;
}

c06 {
  margin-left: 20pt;
}

c07 {
  margin-left: 20pt;
}

c08 {
  margin-left: 50pt;
}

unitid {
}
          </style>
        <style>
          h1,
          h2,
          h3{
              font-family:arial
          }</style>

        <title style="display: none;">
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
def processor(my_input_file=str, singularization_dict=dict, translation_dict=dict):
    my_output_file = f"{my_input_file[:-4]}-done.xml"
    dom = ET.parse(my_input_file)
    root = dom.getroot()
    try:
        ead = root.xpath("//ead:ead", namespaces=nsmap)
        for item in ead:
            item.attrib['relatedencoding'] = "MARC21"
        eadhead = root.find(".//ead:eadheader", namespaces=nsmap)
        eadhead.attrib['scriptencoding'] = "iso15924"
        window['-OUTPUT-'].update("fupdated header information\n", append=True)
    except:
        window['-OUTPUT-'].update(f"failed while trying to modify header information\n", append=True)
    identifiers = ET.iterwalk(root, events=("start", "end"))
    for action, elem in identifiers:
        if "id" in elem.attrib.keys():
            try:
                elem.attrib.pop("id")
            except:
                window['-OUTPUT-'].update(f"failed to remove id from {elem.text}\n", append=True)
                raise
    try:
        pub_stmt = root.find(".//ead:publicationstmt", namespaces=nsmap)
        pub_date = root.find(".//ead:publicationstmt/ead:p/ead:date", namespaces=nsmap)
        pub_date2 = ET.SubElement(pub_stmt, "date")
        pub_date2.text = pub_date.text
        date_container = pub_date.getparent()
        date_container.getparent().remove(date_container)
        window['-OUTPUT-'].update(f"promoted publication date\n", append=True)
        pub_stmt = root.xpath(".//ead:publicationstmt/ead:publisher", namespaces=nsmap)
        for item in pub_stmt:
            item.text = "Texas State Library and Archives Commission"
            extptr = ET.SubElement(item, "extptr")
            extptr.attrib['xlink_actuate'] = "onLoad"
            extptr.attrib['xlink_href'] = "https://www.tsl.texas.gov/sites/default/files/public/tslac/arc/findingaids/tslac_logo.jpg"
            extptr.attrib['xlink_show'] = "embed"
            extptr.attrib['xlink_type'] = "simple"
            extptr.attrib['xmlns_xlink'] = "http://www.w3.org/1999/xlink"
        window['-OUTPUT-'].update(f"added extptr to publisher reference\n", append=True)
        address = root.xpath(".//ead:publicationstmt/ead:address", namespaces=nsmap)
        paragraph = root.xpath(".//ead:publicationstmt/ead:p", namespaces=nsmap)
        if paragraph is not None:
            for item in paragraph:
                item.getparent().remove(item)
        window['-OUTPUT-'].update(f"removed unnecessary paragraphs from publication statment\n", append=True)
        if address is not None:
            for addres in address:
                parental = addres.getparent()
                parental.remove(addres)
        window['-OUTPUT-'].update(f"removed address information from publication statement\n", append=True)
    except:
        window['-OUTPUT-'].update(f"failed while trying to update publication information\n", append=True)
        raise
    try:
        creation_date = root.find(".//ead:profiledesc/ead:creation/ead:date", namespaces=nsmap)
        creation_date.text = creation_date.text[:10]
        window['-OUTPUT-'].update(f"shortened creation date to yyyy-mm-dd\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble shortening creation date\n", append=True)
        raise
    try:
        archdesc = root.find(".//ead:archdesc", namespaces=nsmap)
        archdesc.attrib['type'] = "inventory"
        archdesc.attrib['audience'] = "external"
        main_did = root.find(".//ead:archdesc/ead:did/ead:head", namespaces=nsmap)
        main_did.text = "Overview"
        window['-OUTPUT-'].update(f"updated archdesc attributes and archdesc did descriptor\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble updating archdesc attributes and overview title\n", append=True)
        raise
    try:
        repository = root.find(".//ead:archdesc/ead:did/ead:repository/ead:corpname", namespaces=nsmap)
        repository_text = repository.text
        repo_extref = root.find(".//ead:archdesc/ead:did/ead:repository/ead:extref", namespaces=nsmap)
        repo_extref.text = repository_text
        repository.getparent().remove(repository)
        window['-OUTPUT-'].update(f"re-arranged archdesc repo tags\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble re-arranging archdesc repository tags\n", append=True)
        raise
    try:
        top_title = root.find(".//ead:archdesc/ead:did/ead:unittitle", namespaces=nsmap)
        top_title.attrib['label'] = "Title:"
        originator = root.xpath(".//ead:origination", namespaces=nsmap)
        if originator is not None:
            for item in originator:
                if "label" not in item.attrib.keys():
                    item.attrib['label'] = "Creator:"
                else:
                    if not item.attrib['label'].endswith(":"):
                        item.attrib['label'] = f'{item.attrib["label"]}:'
                window['-OUTPUT-'].update(f"handled collection title attributes\n", append=True)
        head_id = root.find("ead:archdesc/ead:did/ead:unitid", namespaces=nsmap)
        head_id.attrib['label'] = "TSLAC Control No.:"
        window['-OUTPUT-'].update(f"updated label to top unitid\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble updating labels for title or TX number\n", append=True)
        raise
    try:
        origination = root.find(".//ead:archdesc/ead:did/ead:origination", namespaces=nsmap)
        children = origination.getchildren()
        if len(children) > 1:
            print("more children than I know what to do with")
            controlaccess = root.find(".//ead:controlaccess", namespaces=nsmap)
            fams = 0
            peeps = 0
            corps = 0
            for child in children[1:]:
                if "corpname" in child.tag:
                    corps += 1
                if "famname" in child.tag:
                    fams += 1
                if "persname" in child.tag:
                    peeps += 1
                child.attrib['encodinganalog'] = f"7{child.attrib['encodinganalog'][1:]}"
            if fams > 0:
                families = ET.SubElement(controlaccess, "controlaccess")
                fam_head = ET.SubElement(families, "head")
                fam_head.text = "Family Names"
            if peeps > 0:
                peoples = ET.SubElement(controlaccess, "controlaccess")
                peep_head = ET.SubElement(peoples, "head")
                peep_head.text = "Personal Names"
            if corps > 0:
                corporate = ET.SubElement(controlaccess, "controlaccess")
                corporate_ceo = ET.SubElement(corporate, "head")
                corporate_ceo.text = "Corporate Names"
            for child in children[1:]:
                window['-OUTPUT-'].update(f"moving {child.text} to subject terms\n", append=True)
                if "corpname" in child.tag:
                    corporate.append(child)
                if "famname" in child.tag:
                    families.append(child)
                if "persname" in child.tag:
                    peoples.append(child)
    except:
        window['-OUTPUT-'].update("trouble moving extra creators to controlaccess section\n", append=True)
        raise
    try:
        langmaterial = root.xpath(".//ead:langmaterial", namespaces=nsmap)
        if langmaterial is not None:
            langmaterial[0].attrib['label'] = "Language:"
            window['-OUTPUT-'].update(f"added label to first langmaterial tag\n", append=True)
            if len(langmaterial) > 1:
                while len(langmaterial) > 1:
                    langmaterial[-1].getparent().remove(langmaterial[-1])
                    langmaterial = root.xpath(".//ead:langmaterial", namespaces=nsmap)
            window['-OUTPUT-'].update(f"removed all other langmaterial tags\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble trying to update language/langmaterial tagging\n", append=True)
        raise
    try:
        top_physdesc = root.xpath(".//ead:archdesc/ead:did/ead:physdesc", namespaces=nsmap)
        if top_physdesc is not None:
            for item in top_physdesc:
                item.attrib['label'] = "Quantity:"
            window['-OUTPUT-'].update(f"added labels to top level physdesc tags\n", append=True)
            if len(top_physdesc) > 1:
                for physdesc in top_physdesc[1:]:
                    if physdesc.attrib['altrender'] == "part":
                        extent = physdesc.find("./ead:extent", namespaces=nsmap)
                        extent.text = f"(includes {extent.text})"
            window['-OUTPUT-'].update(f"added parenthetical to partial extents if applicable\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble trying to update top physdesc tagging\n", append=True)
        raise
    try:
        top_unitdates = root.xpath(".//ead:archdesc/ead:did/ead:unitdate", namespaces=nsmap)
        if top_unitdates is not None:
            if len(top_unitdates) > 1:
                for item in top_unitdates[:-1]:
                    item.text = f"{item.text}, "
            for item in top_unitdates:
                item.attrib['label'] = "Dates:"
                window['-OUTPUT-'].update(f"added date label to {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update("trouble adding labels to top-level dates\n", append=True)
        raise
    try:
        abstract = root.xpath(".//ead:archdesc/ead:did/ead:abstract", namespaces=nsmap)
        if abstract is not None:
            for item in abstract:
                item.attrib['label'] = "Abstract:"
        window['-OUTPUT-'].update(f"added label to abstract tag\n", append=True)
    except:
        window['-OUTPUT-'].update(f"troruble adding label to abstract tag\n", append=True)
        raise
    try:
        top_location = root.xpath(".//ead:archdesc/ead:did/ead:physloc", namespaces=nsmap)
        if top_location is not None:
            for item in top_location:
                item.attrib['label'] = "Location:"
        window['-OUTPUT-'].update(f"added label to top physloc if applicable\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding label to top physloc\n", append=True)
        raise
    try:
        arrangement = root.xpath(".//ead:archdesc/ead:arrangement", namespaces=nsmap)
        if arrangement is not None:
            for item in arrangement:
                item.attrib['encodinganalog'] = "351"
                window['-OUTPUT-'].update(f"added encodinganalog to arrangement note\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding encodinganalog to arrangement note\n", append=True)
        raise
    try:
        processinfo = root.xpath(".//ead:processinfo", namespaces=nsmap)
        if processinfo is not None:
            for item in processinfo:
                item.attrib['encodinganalog'] = "583"
                window['-OUTPUT-'].update(f"added encodinganalog to processing info\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding encodinganalog to processing info\n", append=True)
        raise
    try:
        appraisal = root.xpath(".//ead:archdesc/ead:appraisal", namespaces=nsmap)
        if appraisal is not None:
            for item in appraisal:
                item.attrib['encodinganalog'] = "583"
                window['-OUTPUT-'].update(f"added encodinganalog to appraisal\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding encodinganalog to appraisal\n", append=True)
        raise
    try:
        phystech = root.xpath(".//ead:archdesc/ead:phystech", namespaces=nsmap)
        if phystech is not None:
            for item in phystech:
                item.attrib['encodinganalog'] = "340"
                window['-OUTPUT-'].update(f"added encoding analog to phystech\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding encodinganalog to phystech\n", append=True)
        raise
    try:
        controlaccess = root.find(".//ead:archdesc/ead:controlaccess/ead:controlaccess", namespaces=nsmap)
        if controlaccess is not None:
            paragraph = ET.SubElement(item, "p")
            emphasis = ET.SubElement(paragraph, "emph")
            emphasis.attrib['render'] = "italic"
            emphasis.text = "The terms listed here were used to catalog the records. The terms can be used to find similar or related records."
            controlaccess.addprevious(paragraph)
            window['-OUTPUT-'].update(f"added intro language to index terms\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble adding intro language to index terms\n", append=True)
        raise
    try:
        subject = root.xpath(".//ead:subject", namespaces=nsmap)
        if subject is not None:
            for item in subject:
                if "source" in item.attrib.keys():
                    item.attrib['source'] = normalized_source(item.attrib['source'])
                    window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble normalizing source on subject tags\n", append=True)
        raise
    try:
        corpname = root.xpath(".//ead:corpname", namespaces=nsmap)
        if corpname is not None:
            for item in corpname:
                if "source" in item.attrib.keys():
                    item.attrib['source'] = normalized_source(item.attrib['source'])
                    window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update(f'trouble normalizing source attributes for corpnames\n', append=True)
        raise
    try:
        famname = root.xpath(".//ead:famname", namespaces=nsmap)
        if famname is not None:
            for item in famname:
                if "source" in item.attrib.keys():
                    item.attrib['source'] = normalized_source(item.attrib['source'])
                    window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble normalizing source attributes for famnames\n", append=True)
        raise
    try:
        persname = root.xpath(".//ead:persname", namespaces=nsmap)
        if persname is not None:
            for item in persname:
                if "source" in item.attrib.keys():
                    item.attrib['source'] = normalized_source(item.attrib['source'])
                    window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble normalizing source attributes for persnames\n", append=True)
        raise
    try:
        geogname = root.xpath(".//ead:geogname", namespaces=nsmap)
        if geogname is not None:
            for item in geogname:
                if item.text is not None:
                    if "source" in item.attrib.keys():
                        item.attrib['source'] = normalized_source(item.attrib['source'])
                        window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update("trouble trying to update source attributes for geographic terms\n", append=True)
        raise
    try:
        functional = root.xpath(".//ead:function", namespaces=nsmap)
        if functional is not None:
            for item in functional:
                if item.text is not None:
                    if "source" in item.attrib.keys():
                        item.attrib['source'] = normalized_source(item.attrib['source'])
                        window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update("trouble trying to update source attributes for function terms\n", append=True)
    try:
        titles = root.xpath(".//ead:title", namespaces=nsmap)
        if titles is not None:
            for item in titles:
                if item.text is not None:
                    if "source" in item.attrib.keys():
                        item.attrib['source'] = normalized_source(item.attrib['source'])
                        window['-OUTPUT-'].update(f"normalized source attribute for {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update("trouble normalizing source attributes for title subjects\n", append=True)
        raise
    try:
        counter = 0
        series = root.xpath(".//ead:c01", namespaces=nsmap)
        for item in series:
            if item.attrib['level'] == "series":
                counter += 1
                item.attrib['id'] = f"ser{str(counter)}"
                window['-OUTPUT-'].update(f"added {item.attrib['id']} identifier to series {str(counter)}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble assigning series identifiers\n", append=True)
        raise
    try:
        extents = root.xpath(".//ead:physdesc/ead:extent", namespaces=nsmap)
        if extents is not None:
            for extent in extents:
                if extent.text is not None:
                    extent_text = extent.text
                    for key in translation_dict.keys():
                        if key in extent_text:
                            extent_text = extent_text.replace(key, translation_dict[key])
                            window['-OUTPUT-'].update(f"translated {extent_text}\n", append=True)
                    try:
                        extent_enumeration = float(extent_text.split(" ")[0])
                        if extent_enumeration <= 1:
                            for key in singularization_dict.keys():
                                if key in extent_text:
                                    extent_text = extent_text.replace(key, singularization_dict[key])
                                    window['-OUTPUT-'].update(f"singularized {extent_text}\n", append=True)
                    except:
                        window['-OUTPUT-'].update(f"trouble with singularization of {extent_text}, recommend checking on that\n", append=True)
                        continue
                    extent.text = extent_text
    except:
        window['-OUTPUT-'].update("trouble translating or singularizing extents\n", append=True)
        raise
    try:
        box = root.xpath(".//ead:container", namespaces=nsmap)
        if box is not None:
            for item in box:
                if "type" in item.attrib.keys():
                    if item.attrib['type'] == "box":
                        item.attrib['type'] = "Box"
                        window['-OUTPUT-'].update(f"normalized box label to {item.text}\n", append=True)
                if "parent" in item.attrib.keys():
                    item.attrib.pop('parent')
                    window['-OUTPUT-'].update(f"removed parent attribute to {item.text}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble normalizing boxes\n", append=True)
        raise
    try:
        date_normal = root.xpath(".//ead:unitdate", namespaces=nsmap)
        for item in date_normal:
            if "normal" in item.attrib.keys():
                normal = item.attrib["normal"]
                if "T" in normal:
                    normal = normal.split("/")
                    var1 = normal[0].split("T")[0]
                    var2 = normal[1].split("T")[0]
                    item.attrib['normal'] = f"{var1}/{var2}"
                    window['-OUTPUT-'].update(f"normalized out timecodes for {item.attrib['normal']}\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble normalizing out timecodes from unitdates\n", append=True)
        raise
    c_tags = ['c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12', 'c13', 'c14', 'c15']
    for c in c_tags:
        window['-OUTPUT-'].update(f"starting to process tags at {c} level\n", append=True)
        dids = root.xpath(f".//ead:{c}/ead:did", namespaces=nsmap)
        for did in dids:
            did_text = ""
            try:
                unittitle = did.find("./ead:unittitle", namespaces=nsmap)
                unittitle_emph = did.find("./ead:unittitle/ead:emph", namespaces=nsmap)
                unitdate = did.xpath("./ead:unitdate", namespaces=nsmap)
                physdesc = did.xpath("./ead:physdesc/ead:extent", namespaces=nsmap)
                if unittitle is not None and len(unitdate) > 0 or len(physdesc) > 0:
                    window['-OUTPUT-'].update(f"{unittitle}\n", append=True)
                    if unittitle is not None:
                        unittitle_text = unittitle.text
                        if unittitle_text is not None:
                            if not unittitle_text.endswith(",") or not unittitle_text.endswith(", "):
                                unittitle_text += ","
                                unittitle.text = unittitle_text
                                did_text = f"{did_text}{unittitle_text}"
                        if unittitle_text is None:
                            unittitle_text = unittitle_emph.text
                            if unittitle_text is not None:
                                if not unittitle_text.endswith(",") or not unittitle_text.endswith(", "):
                                    unittitle_text += ","
                                    unittitle_emph.text = unittitle_text
                                    did_text = f"{did_text}{unittitle_text}"
                        print(unittitle_text)
                if len(physdesc) > 0:
                    if len(unitdate) > 0:
                        for date in unitdate:
                            date_text = date.text
                            if not date_text.endswith(",") or not date_text.endswith(", "):
                                date_text += ","
                                date.text = date_text
                                did_text = f"{did_text}/{date_text}"
                if len(physdesc) == 0:
                    if len(unitdate) > 1:
                        for date in unitdate[1:]:
                            date_text = date.text
                            if not date_text.endswith(",") or not date_text.endswith(", "):
                                date_text += ","
                                date.text = date_text
                                did_text = f"{did_text}/{date_text}"
                if len(physdesc) > 1:
                    for phys in physdesc[:-1]:
                        phys_text = phys.text
                        if not phys_text.endswith(",") or not phys_text.endswith(", "):
                            phys_text += ","
                            phys.text = phys_text
                            did_text = f"{did_text}/{phys_text}"
                    phys_counter = 0
                    for phys in physdesc:
                        parental = phys.getparent()
                        if "altrender" in parental.attrib.keys():
                            if parental.attrib["altrender"] == "part":
                                phys.text = f"(includes {phys.text})"
                                physdesc[phys_counter].text = physdesc[phys_counter].text[:-1]
                                phys_counter += 1
                window['-OUTPUT-'].update(f"processed {did_text}\n", append=True)
            except:
                window['-OUTPUT-'].update(f"failed near {did_text}\n", append=True)
                raise
    try:
        unitid_list = []
        unitid = root.xpath(".//ead:unitid", namespaces=nsmap)
        if unitid is not None:
            for item in unitid:
                unit_text = item.text
                if unit_text in unitid_list:
                    item.getparent().remove(item)
                else:
                    unitid_list.append(unit_text)
        window['-OUTPUT-'].update(f"removed duplicate unitids\n", append=True)
    except:
        window['-OUTPUT-'].update(f"trouble removing duplicate unitids\n", append=True)
        raise
    ead_emph = root.xpath(".//ead:emph", namespaces=nsmap)
    if ead_emph is not None:
        for item in ead_emph:
            if "render" not in item.attrib.keys():
                window['-OUTPUT-'].update(f"\nemph tag for {item.text} missing render attribute\n", append=True)
    try:
        ET.indent(dom, space="\t")
        with open(my_output_file, "wb") as w:
            w.write(ET.tostring(dom, pretty_print=True))
        w.close()
        with open(my_output_file, "r") as r:
            filedata = r.read()
            filedata = filedata.replace("xlink_", "xlink:").replace("xmlns_", "xmlns:")
            filedata = f"{xml_header}{filedata}"
            with open(my_output_file, "w") as w:
                w.write(filedata)
            w.close()
        html_file = f"{my_output_file[:-3]}html"
        my_html = ET.XSLT(html_transform)
        dom = ET.parse(my_output_file)
        new_dom = my_html(dom)
        new_dom.write(html_file, pretty_print=True)
    except:
        window['-OUTPUT-'].update(f"trouble saving processor output and creating html page\n", append=True)
        raise
    window['-status_img-'].update(my_icon2)
    window['-status_img2-'].update(my_icon2)
    window['-OUTPUT-'].update(f"finished processing {my_output_file}\n", append=True)

Sg.theme('DarkGreen')
layout = [[
    Sg.Push(),
    Sg.Text("EAD file"),
    Sg.In(size=(50, 1), enable_events=True, key="-EAD-"),
    Sg.FileBrowse(file_types=(("xml text files only", "*.xml"),)), ],
    [
        Sg.Push(),
        Sg.Checkbox("Use taroprocessor_configfile.txt?", key="-CONFIG-", tooltip="to use the configuration file to translate extents data instead of built-in", enable_events=True),
    ],
    [
        Sg.Push(),
        Sg.Button("Execute", tooltip="This will start the program running"),
        Sg.Push()
    ],
    [
        Sg.Button("Close", tooltip="Close this window. Won't work while XML is being processed", bind_return_key=True)
    ],
    [
        Sg.Image(my_icon, key='-status_img-'),
        Sg.Multiline(
            default_text="Look here for information about various data points as the file processes. Your processed file will end in '-done'",
            size=(70, 5), auto_refresh=True, reroute_stdout=False, key="-OUTPUT-", autoscroll=True,
            border_width=5),
        Sg.Image(my_icon, key='-status_img2-')
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
        if window['-CONFIG-'] is True:
            config = configparser.ConfigParser()
            config.read("taroprocessor_configfile.txt")
            singularization_dict = ""
            singularization_dict = {}
            for (key, value) in config['extent_singular']:
                singularization_dict[key] = value
            translation_dict = ""
            translation_dict = {}
            for (key, value) in config['extent_translations']:
                translation_dict[key] = value
            window['-OUTPUT-'].update("loaded configuration file values for extent processing\n", append=True)
        processor(my_xml, singularization_dict, translation_dict)
    if event == "Close" or event == Sg.WIN_CLOSED:
        break
window.close()