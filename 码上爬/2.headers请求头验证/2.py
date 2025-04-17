import requests
import time


time = str(int(time.time()))
print(time)
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': time,
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/1/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744099003',
}
sum = 0
for i in range(1,21):
    params = {
        'page': i,
    }
    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/2/data/', params=params, cookies=cookies, headers=headers).json()["current_array"]
    for item in response:
        sum+=item
print(sum)