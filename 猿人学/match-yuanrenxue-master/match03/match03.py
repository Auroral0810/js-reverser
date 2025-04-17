""" 参考https://blog.csdn.net/qq_38017966/article/details/110355191 """

import requests
from collections import Counter


HEADERS = {
    # 'Host': 'match.yuanrenxue.com',
    # 'Connection': 'keep-alive'必要
    'Connection': 'keep-alive',
    'user-agent': 'yuanrenxue.project',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': '*/*',
    'Origin': 'http://match.yuanrenxue.com',
    'Referer': 'http://match.yuanrenxue.com/match/3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
}

session = requests.Session()
# 只有这种传递headers的方式可行 
session.headers = HEADERS
# session.headers.update(HEADERS)
# cookie_url = "http://match.yuanrenxue.com/logo"
# 改动设置cookie的url
cookie_url = "http://match.yuanrenxue.com/jssm"

Registration = []
for page in range(1, 6):
    # 此处传递Headers不行
    # r = session.post(cookie_url,headers=HEADERS) 
    r = session.post(cookie_url)
    print(r.cookies)
    api_url = f"http://match.yuanrenxue.com/api/match/3?page={page}"
    response = session.get(api_url)
    print(response.text)
    for each in response.json()['data']:
        Registration.append(each['value'])

print(Counter(Registration))
print(Counter(Registration).most_common(1)[0][0])
