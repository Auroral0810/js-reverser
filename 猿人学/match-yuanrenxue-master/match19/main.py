
""" 
https://mp.weixin.qq.com/s/aC0c7D08qWpQ2KG9KfmNqA
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
 
# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)
 
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'user-agent': 'yuanrenxue.project',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'sessionid=换成你的sessionid'
}
 
 
class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)
 
    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)
 
 
def get_page(s, page):
    r = s.get(f'https://match.yuanrenxue.com/api/match/19?page={page}', headers=headers)
    res = r.json()
    data = res.get('data')
    s = [int(d.get('value')) for d in data]
    print(123123,s)
    return s
 
 
def get_data(s):
    end = 0
    for i in range(1, 6):
        temp = get_page(s, i)
        print()
        end += sum(temp)
    print('end', end)
    return end
 
 
s = requests.Session()
s.mount('https://match.yuanrenxue.com', DESAdapter())
get_data(s)
