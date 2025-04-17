import requests
import time
import execjs

# 加载JS代码并编译一次
with open('5_1.js', 'r') as f:
    js = f.read()
ctx = execjs.compile(js)

# 使用编译好的JS上下文调用函数
def get_cookie():
    return ctx.call('getCookie')

def get_cookie_m():
    return ctx.call('getCookieM')

def get_time_m():
    return ctx.call('getTimeM')

def get_cookies():
    return ctx.call('get_cookies')

# 使用获取的cookies发送请求
res = []
for page in range(1, 6):
    cookies = get_cookies()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    url = f'http://match.yuanrenxue.com/api/match/5?page={page}&m={cookies["m"]}&f={cookies["f"]}'
    
    # 使用cookies字典发送请求
    response = requests.get(url, headers=headers, cookies={
        'RM4hZBv0dDon443M': cookies['RM4hZBv0dDon443M'], 
        'm': cookies['m_cookie']
    }).json()['data']
    for item in response:
        res.append(item['value'])
res.sort()
print(sum(res[-5:]))

