import time
import execjs
import requests

with open('18.js', 'r') as f:
    js = f.read()

ctx = execjs.compile(js)
sum = 0
for i in range(1, 2):

    t = str(int(time.time() * 1000))
    print(t)
    # t = int(time.time() * 1000)
    m = ctx.call('getM', t)
    print(m)
    cookies = {
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
        'HMACCOUNT': '764A7B05229BE584',
        'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
        's': '51b351b351b351b370b0d0d010907051b03030b071',
        'v': 'QThJY3NNemxFUjdQUncwMmdCeEhaQ3ZxRmNNaGs4YXRlSmU2MFF6YjdqWGdYMng5OUNNV3ZVZ25DdVBmMTc0NDI4ODg1NTk0MQ==',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744288906',
        '_nano_fp': 'XpmYn0PJl0Uon5dbX9_GpxEBvOPtUoOpk89nTirs',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'client-version': '1.0.0',
        'm': m,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://stu.tulingpyton.cn/problem-detail/18/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'timestamp': t,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; s=51b351b351b351b370b0d0d010907051b03030b071; v=QThJY3NNemxFUjdQUncwMmdCeEhaQ3ZxRmNNaGs4YXRlSmU2MFF6YjdqWGdYMng5OUNNV3ZVZ25DdVBmMTc0NDI4ODg1NTk0MQ==; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744288906; _nano_fp=XpmYn0PJl0Uon5dbX9_GpxEBvOPtUoOpk89nTirs',
    }
    params = {
        'page': i,
    }
    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/18/data/', params=params, cookies=cookies, headers=headers).json()
    print(response)
#     res = response['data']['current_array']
#     for i in res:
#         sum += i
# print(sum)
