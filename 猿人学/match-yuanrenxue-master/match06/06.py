import time
import execjs
import requests
import os
""" 
2021.7.2测试可用
服务器端增加了q的校验
使用方法
1. 启动服务
```
node server06.js
```
2. 运行06.py获取数据

其他
1. execjs 调用06.js会有编码问题
2. os.popen 调用06.js只有第一次可以拿到数据
3. express 服务调用06.js 每5次需要重启服务才可以拿到数据
    - 猜测 这个魔改版的 RSA 每次加密有改变全局变量，5次后，加密结果就不正确

"""
headers = {
    # 'Host': 'match.yuanrenxue.com',
    'Referer': 'http://match.yuanrenxue.com/match/6',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# express 服务调用
def get_m(timestamp, count):
    """ express 服务调用 """
    return requests.post('http://localhost:3000/encrypt', data={
        'timestamp': str(timestamp),
        'count': count
    }).text


# execjs 调用
with open('06.js', encoding='utf-8') as f:
    jstext = f.read()
    f.close()

getSign = execjs.compile(jstext)


q = ''
count = 0

all_data = []
for page in range(1, 6):
    count += 1
    timestamp = int(time.time()) * 1000
    # m = get_m(timestamp,str(count))
    # m = getSign.call('get_m', timestamp, count)
    nodejs = os.popen('node 06 '+str(timestamp)+' '+str(count))
    m = nodejs.read().replace('\n', '')
    q += f'{str(count)}-{timestamp}|'
    params = {
        'page': page,
        'm': m,
        'q': q
    }
    # print(params)
    url = 'http://match.yuanrenxue.com/api/match/6'
    response = requests.get(url, headers=headers, params=params)
    print(response.json())
    all_data += response.json()['data']
    time.sleep(10)

total = 0
for each in all_data:
    num3 = int(each['value'])
    total += num3*(1+8+15)

print(total)
# 6883344

