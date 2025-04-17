import requests
import execjs
import time
# my_spider.py
def get_m():
    with open('origin.js', 'r', encoding='utf8') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    m = ctx.call('getCookie')
    return m

m = get_m()
# print(m)
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
    'yuanrenxue_cookie': '1744041254|Ner3meWTenBw8QgzAc9RirHc6wchy9E0GqnkH3Onu85nbN49ZmfnoNlp7QxScahQbhzXHbaayOEmlwxI0wYAlFwYI6vFTGJH36CYvovfuIJ4U9F5LHBfMmUd0uf1UVaMfNaQmk1OFw8kQdym0eZS2zdTWQElNlrQi0dCdiMAXdILz0Cmc',
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1744073542',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1744073724',
    'm': m,
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/2',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1744004527; HMACCOUNT=764A7B05229BE584; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; HMACCOUNT=764A7B05229BE584; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1744004555; no-alert3=true; tk=-6834914907875830726; yuanrenxue_cookie=1744041254|Ner3meWTenBw8QgzAc9RirHc6wchy9E0GqnkH3Onu85nbN49ZmfnoNlp7QxScahQbhzXHbaayOEmlwxI0wYAlFwYI6vFTGJH36CYvovfuIJ4U9F5LHBfMmUd0uf1UVaMfNaQmk1OFw8kQdym0eZS2zdTWQElNlrQi0dCdiMAXdILz0Cmc; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1744073542; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1744073724; m=7f6b3087dc95a84f503d9cb0c60a3062|1744073802000',
}
sum = 0
for i in range(1,6):
    params = {
        'page' : i
    }
    response = requests.get('https://match.yuanrenxue.cn/api/match/2', cookies=cookies, headers=headers, verify=False,params=params).json()["data"]
    print(response)
    for item in response:
        sum+=item['value']
print(sum)