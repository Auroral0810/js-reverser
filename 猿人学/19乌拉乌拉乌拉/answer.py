# -*- coding: utf-8 -*-
import random

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

ORIGIN_CIPHERS = ('AESGCM')

class DESAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        """
        A TransportAdapter that re-enables 3DES support in Requests.
        """
        CIPHERS = ORIGIN_CIPHERS.split(':')
        random.shuffle(CIPHERS)
        CIPHERS = ':'.join(CIPHERS)
        self.CIPHERS = CIPHERS + ':!aNULL:!eNULL:!MD5'
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

headers = {
    'authority': 'match.yuanrenxue.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5; qpfccr=true; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1656682096,1656746681,1656921073,1656998602; no-alert3=true; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1656746689,1656921076,1656926887,1656998604; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1657003555; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1657003582',
    'pragma': 'no-cache',
    'referer': 'https://match.yuanrenxue.com/match/19',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'yuanrenxue.project',
    'x-requested-with': 'XMLHttpRequest',
}

session = requests.session()
session.headers.update(headers)
session.mount('https://match.yuanrenxue.com', DESAdapter())
session.verify = False

# 禁用相关警告（可选）
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

result = 0
for page in range(1,6):
    response = session.get(f'https://match.yuanrenxue.com/api/match/19?page={page}')
    data = response.json()
    print(data)
    for i in data.get('data'):
        result += i.get('value')
print(result)