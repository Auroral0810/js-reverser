import requests
import execjs
import time
with open('8.js', 'r') as f:
    js = f.read()

ctx = execjs.compile(js)
"""
cookies里面的s需要加密
hearders里面的M和T需要加密
"""
sum = 0
for i in range(1,21):
    t = int(time.time()*1000)
    s = str(ctx.call('getS', t))
    M = str(ctx.call('getM', t,i))
    T = str(ctx.call('getT', t))
    # print(s + '\n'+ M + '\n'+ T)
    cookies = {
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
        'HMACCOUNT': '764A7B05229BE584',
        'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744261730',
        's': s,
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'm': M,
        'origin': 'https://stu.tulingpyton.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://stu.tulingpyton.cn/problem-detail/8/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        't': T,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744258844; s=51b351b351b351b370b0d0d010f05151d0d0f010d0',
    }

    json_data = {
        'page': i,
    }
    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/8/data/', cookies=cookies, headers=headers, json=json_data)
    data = response.json()['current_array']
    for res in data:
        sum +=res
print(sum)