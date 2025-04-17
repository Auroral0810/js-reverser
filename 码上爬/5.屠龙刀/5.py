import execjs
import requests

cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744103203',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://stu.tulingpyton.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/5/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744103203',
}


sum = 0
xl = 'b2b5e02b7b8f057b6c56709d8402c21b7c54ac10d0f7de1b812e061b69f8d210'
with open('5.js', 'r') as f:
    js_code = f.read()

ctx = execjs.compile(js_code)

for i in range(1,21):
    xl = ctx.call('getxl',i)
    # print(xl)
    # token = md5(("tuling" + timestamp + str(i)).encode()).hexdigest()
    params = {
        'xl': xl,
    }
    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/5/data/', cookies=cookies, headers=headers, json=params).json()['current_array']
    for item in response:
        sum+=item
print(sum)


# print(2*16*16+8*16+1-1*16*16-9*16-4)