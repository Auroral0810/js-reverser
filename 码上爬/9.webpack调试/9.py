import requests
import json
import time
import execjs

cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    's': '51b351b351b351b370b0d0d010907051b03030b071',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744261892',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://stu.tulingpyton.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/9/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; s=51b351b351b351b370b0d0d010907051b03030b071; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744261892',
}

with open('9.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
sum = 0
for i in range(1,21):
    t = int(time.time() * 1000)
    m = str(ctx.call('get_m', t))
    tt = str(ctx.call('get_tt', t))
    json_data = {
        'page': i,
        'm': m,
        'tt': tt,
    }
    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/9/data/', cookies=cookies, headers=headers, json=json_data).json()['current_array']
    for item in response:
        sum += item
print(sum)