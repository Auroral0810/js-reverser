import time
import execjs
import requests
import os
os.environ["EXECJS_RUNTIME"] = "Node"
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
    'm': 'a39cf1a67b614599915b6528290e86ab',
    'RM4hZBv0dDon443M': 'WE5gncA7M7Z3lGdzbmrwP3QE4ncG/6YtdA0Qk5Uw3mRdPI4A9yQ5aebuFC1tnR6ZgwksMHFkoBuh1xSsFeVjkoaC8a7EDxOIlQvP+Nb7/rt2qai5mf4fUZIB7oK8N01QlAxPv7bv0DdyhJCMJn+orFwC31+SU/SOOqCmK4nN18msSoF7tXdCPOKTJEjHanzNiLYH99RxTeuzHuDOGtZ5cfc55A4NKCYYdrl1wbVUOew=',
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1744135749',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1744135827',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/6',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1744004527; HMACCOUNT=764A7B05229BE584; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; HMACCOUNT=764A7B05229BE584; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1744004555; no-alert3=true; tk=-6834914907875830726; yuanrenxue_cookie=1744041254|Ner3meWTenBw8QgzAc9RirHc6wchy9E0GqnkH3Onu85nbN49ZmfnoNlp7QxScahQbhzXHbaayOEmlwxI0wYAlFwYI6vFTGJH36CYvovfuIJ4U9F5LHBfMmUd0uf1UVaMfNaQmk1OFw8kQdym0eZS2zdTWQElNlrQi0dCdiMAXdILz0Cmc; m=a39cf1a67b614599915b6528290e86ab; RM4hZBv0dDon443M=WE5gncA7M7Z3lGdzbmrwP3QE4ncG/6YtdA0Qk5Uw3mRdPI4A9yQ5aebuFC1tnR6ZgwksMHFkoBuh1xSsFeVjkoaC8a7EDxOIlQvP+Nb7/rt2qai5mf4fUZIB7oK8N01QlAxPv7bv0DdyhJCMJn+orFwC31+SU/SOOqCmK4nN18msSoF7tXdCPOKTJEjHanzNiLYH99RxTeuzHuDOGtZ5cfc55A4NKCYYdrl1wbVUOew=; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1744135749; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1744135827',
}
o = 1
sum =0
with open('demo.js', 'r') as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
for page in range(1,2):
    # q就是第一页就是几-时间戳|合在一起。
    t = str(int(time.time()) * 1000)
    oo = 1
    m = execjs.compile(js_code).eval(f'z({t}, {o})')
    print(m)
    params = {
        'page':str(page),
        'm': str(m),
        'q': str(f'{o}-{t}|'),
    }
    o += 1
    response = requests.get('https://match.yuanrenxue.cn/api/match/6', params=params, cookies=cookies, headers=headers)
    print(response.text)
    time.sleep(1)