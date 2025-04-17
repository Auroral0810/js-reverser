import requests

# 创建一个Session对象
session = requests.Session()

headers = {
    's': '27f892589649333c82b25b9ef4e52e4f',
    'tt':  '1744200595725',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744200225',
}

# 设置Session的headers
session.headers.update(headers)

params = {
    'page': '1',
}

# 使用session发送请求
response = session.get('https://stu.tulingpyton.cn/api/problem-detail/6/data/', params=params).json()
print(response)