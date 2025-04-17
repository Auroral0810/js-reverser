import requests
import time
import os
from urllib import parse

sess = requests.Session()

def login():
    url = "https://match.yuanrenxue.com/api/login"
    payload = "username=&password="
    headers = {
        'authority': 'match.yuanrenxue.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://match.yuanrenxue.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://match.yuanrenxue.com/login',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = sess.post(url, headers=headers, data=payload)
    print(response.text)
    print(response.headers)




def main():
    sums = 0
    headers = {
        'user-agent': 'yuanrenxue.project',
        'x-requested-with': 'XMLHttpRequest'
    }
    for page in range(1, 6):
        data = {
            'page': str(page),
            't': str(int(time.time())) + '000'
        }
        # 用gcc 编译了可执行文件 match20 用于签名
        # 用ubuntu 上的gcc 编译的match20 好像只能在Linux上用
        nodejs = os.popen('./match20 "' + data['page'] + '|' + data['t'] + '"')
        print('./match20 "' + data['page'] + '|' + data['t'] + '"')
        data['sign'] = nodejs.read().replace('\n', '')
        nodejs.close()
        print(data)
        url = 'https://match.yuanrenxue.com/api/match/20?' + parse.urlencode(data)
        response = sess.get(url, headers=headers).json()
        print(response)

        for each in response['data']:
            sums += each['value']
    print(sums)
    

if __name__ == '__main__':
    login()
    main()