import requests
import re
import base64

# 使用session保持会话
sess = requests.Session()
headers = {
    # auto delete br encoding. cos requests and scrapy can not decode it.
    # "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "user-agent": "yuanrenxue.project"
}
sess.headers.update(headers)


sum = 0

# 请求首页 
# 1.设置sessionid 
# 2.获取eval字符串中的三个变动的数字
response1 = sess.get('http://match.yuanrenxue.com/match/10')
# sessionid = re.findall('sessionid=[^;]+; ', response1.headers['Set-Cookie'])[0]
# print('sessionid', sessionid)
search_sessionid = re.search('sessionid=(.*?); ', response1.headers['Set-Cookie'])
if search_sessionid:
    sessionid = search_sessionid.group(1)
enc_int = int(re.findall(r'yuanrenxue_59 *= *(\d+)', response1.text)[0])
print('enc_int', enc_int)
response2 = sess.get('http://match.yuanrenxue.com/stati/mu/rsnkw2ksph')
b64eval = ''.join([chr(ord(i)-idx % enc_int-0x32) for idx,
                i in enumerate(response2.text.replace("$_ts['dfe1683']=", '')[1:-1])])
evalstr = base64.b64decode(b64eval.encode()).decode()
v1 = int(re.findall(
    r"_yrxC2_=(\d+) \+ _yrxCxm\['.'\+'.'\+'.'\+'.'\]", evalstr)[0])
v2 = int(re.findall(
    r"_yrxmbl=(\d+) \+ _yrxCxm\['.'\+'.'\+'.'\+'.'\]", evalstr)[0])
v3 = int(re.findall(
    r"return (\d+) \+ _yrxCxm\['.'\+'.'\+'.'\+'.'\]", evalstr)[0])


for page in range(1,6):
    # 请求 offset 值，翻页时 eval中的数字可以保持不变
    response3 = sess.get(
        'http://match.yuanrenxue.com/api/offset')
    offset = int(re.findall(r'= *(\d+)', response3.text)[0])
    print(v1, v2, v3,offset)

    # 需要先 node server.js 在本地启动服务
    response4 = requests.get(f'http://localhost:3000/m',params={
        'page':page,
        'v1':v1,
        'v2':v2,
        'v3':v3,
        'offset':offset
    })
    m = response4.text
    response5 = sess.get('https://match.yuanrenxue.com/api/match/10',params={
        'page':page,
        'm':m
    },cookies={
        # "sessionid":sessionid,
        "m":"pua"
    })
    print(response5.json())
    for each in response5.json()['data']:
        sum += each['value']

print('sum',sum)





