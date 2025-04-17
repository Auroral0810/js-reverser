import requests
import execjs
import time

cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744225027',
}

with open('answer.js', 'r') as f:
    js = f.read()

ctx = execjs.compile(js)
sum = 0
for page in range(1, 21):
    ts = str(int(time.time() * 1000))
    url = ctx.call('getUrl', ts,page)
    headers =  ctx.call('getHeaders', ts)
    response = requests.get(url, cookies=cookies, headers=headers)
    print(response.text)
    encrypted_data = response.json()['r']
    real_data =ctx.call('decode',encrypted_data)
    for item in real_data:
        sum += item
print(sum)