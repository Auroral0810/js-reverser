import jsonpath
import requests
from hyper.contrib import HTTP20Adapter
""" 
安装 hyper 集成到requests 使其可以使用http2.0
pip install hyper -i https://pypi.douban.com/simple/
"""

""" 

hyper 文档
https://hyper.readthedocs.io/

Requests Integration 集成到 Requests
Do you like requests? Of course you do, everyone does! It’s a shame that requests doesn’t support HTTP/2 though. To rectify that oversight, hyper provides a transport adapter that can be plugged directly into Requests, giving it instant HTTP/2 support.

Using hyper with requests is super simple:

>>> import requests
>>> from hyper.contrib import HTTP20Adapter
>>> s = requests.Session()
>>> s.mount('https://http2bin.org', HTTP20Adapter())
>>> r = s.get('https://http2bin.org/get')
>>> print(r.status_code)
200
This transport adapter is subject to all of the limitations that apply to hyper, and provides all of the goodness of requests.

"""


sess = requests.Session()

def login():
    url = "https://match.yuanrenxue.com/api/login"
    payload = "username=你的账号&password=你的密码"
    headers = {
        'authority': 'match.yuanrenxue.com',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'referer': 'https://match.yuanrenxue.com/login',
    }
    response = sess.post(url, headers=headers, data=payload)
    print(response.text)
    print(response.headers)




if __name__ == '__main__':
    url_ = 'https://match.yuanrenxue.com/api/match/17?page={}'
    login()
    # 使用http2.0
    sess.mount('https://match.yuanrenxue.com', HTTP20Adapter())
    num = 0
    for i in range(5):
        # 发送请求
        json_data = sess.get(url_.format(i + 1),headers={
            'user-agent': 'yuanrenxue.project'
        }).json()
        # 提取数据
        num_list = jsonpath.jsonpath(json_data, '$..value')
        for j in num_list:
            print(j, end='\t')
            num += j
        print()
    print('num:', num)