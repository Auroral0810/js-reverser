



import requests
from collections import defaultdict

proxies = {
    'http': 'http://localhost:8889',
    'https': 'http://localhost:8889'

}

headers = {
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile':	'?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'origin': 'https://match.yuanrenxue.cn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://match.yuanrenxue.cn/match/3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
cookies = {
    "sessionid": "a0san8v13c61zw435r31r0zpq62xafx5",
    "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1744004527",
    "qpfccr": "true",
    "no-alert3": "true",
    "tk": "-6834914907875830726",
    "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1744004555",
    "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1744013738",
    "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1744013762",
    "HMACCOUNT": "764A7B05229BE584"
}
session = requests.session()
session.headers = headers
res = defaultdict(int)
for i in range(1, 6):
    url = "https://match.yuanrenxue.cn/jssm"
    response = session.post(url, cookies=cookies)

    url_p = 'https://match.yuanrenxue.cn/api/match/3?page={}'.format(i)
    resp = session.get(url=url_p, cookies=cookies)
    for data in resp.json()['data']:
        value = data['value']
        res[value] += 1
# print(res)
# print(dict(res))
print(max(res, key=lambda x: res[x]))