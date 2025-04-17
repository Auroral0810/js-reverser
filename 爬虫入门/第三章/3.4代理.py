import requests
proxies = {
    'https': 'https://proxy.toolip.io:31113',
}

url = 'http://www.baidu.com'
resp = requests.get(url, proxies=proxies)
resp.encoding='utf-8'
print(resp.text)