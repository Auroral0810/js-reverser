import requests
url ="http://www.baidu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
rsp = requests.get(url,headers=headers)
print(rsp)

rsp.encoding='utf-8'
print(rsp.text)