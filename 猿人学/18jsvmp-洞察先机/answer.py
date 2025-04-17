import execjs
import requests
from loguru import logger

js_code = execjs.compile(open('answer.js', 'r', encoding='utf-8').read())
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
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1744190956',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1744190980',
}

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
nums = 0
for page in range(1, 6):
    params = js_code.call('getEncrypteddata', page)
    if page > 3:
        headers['user-agent'] = 'yuanrenxue.project'
    response = requests.get('https://match.yuanrenxue.com/match/18data', headers=headers, params=params,
                            cookies=cookies)
    res = response.json()
    logger.debug(res)
    for k in res['data']:
        nums += k['value']
logger.debug(nums)