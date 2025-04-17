import requests
import time
import execjs


def gettime():
    return str(int(time.time())) + '000'

# 加载JS代码并编译一次
with open('/猿人学/5js混淆-乱码增强赛/5_2.js', 'r') as f:
    js = f.read()
ctx = execjs.compile(js)

# 使用编译好的JS上下文调用函数
def get_cookie(m,data):
    return ctx.call('getCookie',m,data)

def get_cookie_m(m):
    return ctx.call('getCookieM',m)

def get_time_m():
    return ctx.call('getTimeM')

sum = 0
for page in range(1, 6):
    m = str(int(time.time() * 1000))
    print(m)
    f = gettime()
    data = [
    "e46ae7873182926b81cf81a88c8ed2d0",
    "ea39ed5db9fa45984b7ce00a0a2e5778",
    "54f203edfb65f05f0d4da5db9762ed34",
    "007d11b26303aed47bc4cfeb5b46be5b"
    ]
    cookie_m = get_cookie_m(m)
    cookie_r = get_cookie(m,data)
    print(f + '\n' + m + '\n' + cookie_m + '\n' + cookie_r)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    url = 'http://match.yuanrenxue.com/api/match/5?page=' + str(page) + '&m=' + m + '&f=' + f
    # 字典方式传cookie值
    response = requests.get(url, headers=headers, cookies={'RM4hZBv0dDon443M': cookie_r, 'm': cookie_m})
    # print(response.text)
    for item in response.json()["data"]:
        sum += item['value']
print(sum)

