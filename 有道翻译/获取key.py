import time
from hashlib import md5

import requests
cookies = {
    'OUTFOX_SEARCH_USER_ID': '2050097210@112.2.255.96',
    'OUTFOX_SEARCH_USER_ID_NCOO': '321865632.90403944',
    'DICT_DOCTRANS_SESSION_ID': 'YmE5MTAzZTUtYmUwOC00YWYwLWExNjQtYzhkYzhlYTY0YWJm',
    '_uetsid': 'b9e330a0186811f0babf29c79671995d',
    '_uetvid': 'b9e32f80186811f080ab59a404edf487',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://fanyi.youdao.com',
    'Pragma': 'no-cache',
    'Referer': 'https://fanyi.youdao.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'OUTFOX_SEARCH_USER_ID=2050097210@112.2.255.96; OUTFOX_SEARCH_USER_ID_NCOO=321865632.90403944; DICT_DOCTRANS_SESSION_ID=YmE5MTAzZTUtYmUwOC00YWYwLWExNjQtYzhkYzhlYTY0YWJm; _uetsid=b9e330a0186811f0babf29c79671995d; _uetvid=b9e32f80186811f080ab59a404edf487',
}


d = "fanyideskweb"
u = "webfanyi"
t = 'asdjnjfenknafdfsdfsd'
mysticTime = int(time.time() * 1000)
sign = md5((f'client={d}&mysticTime={mysticTime}&product={u}&key={t}').encode('utf-8')).hexdigest()
# print(sign)
params = {
    'keyid': 'webfanyi-key-getter',
    'sign': sign,
    'client': 'fanyideskweb',
    'product': 'webfanyi',
    'appVersion': '1.0.0',
    'vendor': 'web',
    'pointParam': 'client,mysticTime,product',
    'mysticTime': str(mysticTime),
    'keyfrom': 'fanyi.web',
    'mid': '1',
    'screen': '1',
    'model': '1',
    'network': 'wifi',
    'abtest': '0',
    'yduuid': 'abcdefg',
}


response = requests.get(
    'https://dict.youdao.com/webtranslate/key',
    params=params,
    cookies=cookies,
    headers=headers,
).json()

data = response['data']
secretKey = data['secretKey']
aesKey = data['aesKey']
aesIv = data['aesIv']

print(secretKey)
print(aesKey)
print(aesIv)