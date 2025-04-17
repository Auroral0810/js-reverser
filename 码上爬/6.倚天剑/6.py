import requests
import execjs
# 关闭SSL警告
import urllib3
import json
urllib3.disable_warnings()

with open('/Users/超级无敌巨重要的资料/爬虫/码上爬/6.倚天剑/6.js','r') as f:
    json_data = f.read()


ctx = execjs.compile(json_data)
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744200225',
}





sum = 0;
for i in range(1,21):
    params = {
        'page': str(i)
    }
    headers = ctx.call('s')
    # 创建一个Session对象
    session = requests.Session()
    # 设置Session的cookies和headers
    session.cookies.update(cookies)
    session.headers.update(headers)
    # 设置Session的verify和timeout默认值
    session.verify = False
    session.timeout = 10
    # 使用session发送请求
    response = session.get(
        'https://stu.tulingpyton.cn/api/problem-detail/6/data/',
        params=params
    ).json()['t']
    # print(response)
    res = ctx.call('xxxxoooo',response)['current_array']
    # res = json.dumps(res)
    # print(res['current_array'])
    for num in res:
        sum += num
#
print(sum)