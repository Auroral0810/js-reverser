import requests

cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    's': '51b351b351b351b370b0d0d010907051b03030b071',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744278456',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/11/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1744098732; HMACCOUNT=764A7B05229BE584; sessionid=94q4ek0xqrop8nhln9ndop819vwea79m; s=51b351b351b351b370b0d0d010907051b03030b071; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744278456',
}
sum = 0
for i in range(1, 2):
    params = {
        'page': i,
        'm': '581442511', # 加密参数
        '_ts': '1744278456',# 时间戳
    }
    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/11/data/', params=params, cookies=cookies, headers=headers).json()
    print(response)
#     for i in response['current_array']:
#         sum += i
# print(sum)