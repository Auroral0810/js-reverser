import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.ishumei.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ishumei.com/trial/captcha.html',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'og': 'IxbGpVfruz0=',
    'jp': 'Wq4jwGqOHYM=',
    'captchaUuid': '202504151149433nPeWbSbpxwx7XPWf5',
    'callback': 'sm_1744689625804',
    'organization': 'd6tpAY1oV0Kv5jRSgxQr',
    'dj': '7SnISxDhfjI=',
    'rid': '2025041512001913c1f53df051d1ea51',
    'wz': 'ufdT5h7SVes=',
    'sy': 'lN908/15DcI=',
    'gp': '7kP9OL4ZRNU=',
    'aj': 'Z8JptdSbQHg=',
    'sdkver': '1.1.3',
    'protocol': '184',
    'act.os': 'web_pc',
    'ostype': 'web',
    'tb': 'Ws7zJ8pn73U=',
    'rversion': '1.0.4',
    'ly': 'CGvyx0eqAeA=',
    'tm': 'fwtwgMB82cHLivnhp9ppCGdaouY+hI+V63CwnhWWObPBniBX1IeNcWQkCXzACiWHWzuAwfdQIBUx6waGqyvAfZU7U2CjwucRzsXuDoNCIJL+me4AV7Y/ypU7U2CjwucREN3lKGqvrHi1GAQf9tz6DouEua/WugM+',
    'fc': '2VKLJM6OJCc=',
    'uc': 'b8IY1XIB1iA=',
}

response = requests.get('https://captcha1.fengkongcloud.cn/ca/v2/fverify', params=params, headers=headers)
print(response.text)