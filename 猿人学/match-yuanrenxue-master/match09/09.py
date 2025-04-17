import requests
import re
import os

s = requests.session()
headers = {
	'User-Agent':'yuanrenxue.project',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://match.yuanrenxue.com/match/9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
}
s.headers.update(headers)
url = "http://match.yuanrenxue.com/match/9"
response = s.get(url)
# decrypt\,\'(\d+)\'
hasTs = re.search(r"decrypt,'(\d+)'", response.text, re.S)
if hasTs:
    ts = hasTs.group(1)
    print(ts)
    # udc.js文件必须每次都重新加载 否则生成的cookie错误
    nodejs = os.popen('node udc_2219 '+ts)
    m_cookie = nodejs.read().replace('\n', '')
    nodejs.close()
    # print(m_cookie)
    c = requests.cookies.RequestsCookieJar()  # 定义一个cookie对象
    c.set('m', m_cookie)  # 增加cookie的值
    s.cookies.update(c)  # 更新s的cookie
    # print(s.cookies)
    result_list = []

    for page in range(1, 6):
        res = s.get(
            'http://match.yuanrenxue.com/api/match/9?page={}'.format(str(page)), headers=headers)
        print(res.text)
        result_list += res.json()['data']
    
    total = 0
    count = 0
    for each in result_list:
        count +=1
        total += each['value']
    print('total',total)
    print('average',total/count)

else:
    print('no ts')
