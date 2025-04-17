import base64

import pandas as pd
import requests
import json
cookies = {
    'sessionid': 'a0san8v13c61zw435r31r0zpq62xafx5',
    'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1744004527',
    'HMACCOUNT': '764A7B05229BE584',
    'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1744004548',
    'Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3': '1744004548',
    'HMACCOUNT': '764A7B05229BE584',
    'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1744004555',
    'no-alert3': 'true',
    'tk': '-6834914907875830726',
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1744028635',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1744028641',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/12',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1744004527; HMACCOUNT=764A7B05229BE584; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; HMACCOUNT=764A7B05229BE584; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1744004555; no-alert3=true; tk=-6834914907875830726; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1744028635; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1744028641',
}
data = []
for i in range(1,6):
    # 根据i的值来计算param的值
    # 将yuanrenxue和i拼接后进行Base64编码
    str1 = 'yuanrenxue' + str(i)
    param = base64.b64encode(str1.encode('utf-8')).decode('utf-8')
    params = {
        'page': i,
        'm': param,
    }
    response = requests.get('https://match.yuanrenxue.cn/api/match/12', params=params, cookies=cookies, headers=headers)
    content = json.loads(response.text)['data']
    for item in content:
        data.append(item)

db = pd.DataFrame(data)
res = sum(db['value'])
print(res)