import requests
import time


def encrypt(timestamp):
    """ 访问express启动的服务 """
    url = 'http://localhost:3000/encrypt'
    params = {
        'timestamp': timestamp
    }
    res = requests.get(url, params=params)
    return res.text


def getHtml(page):
    url = "http://match.yuanrenxue.com/api/match/1"
    # 时间戳偏移了100000
    # timestamp=Date.parse(new Date()) + 100000000
    timestamp = int(time.time()+100000)
    encrypt_timestamp = encrypt(str(timestamp)+"000")
    url += f'?page={str(page)}&m={encrypt_timestamp}丨{str(timestamp)}'
    print(url)
    headers = {
        'User-Agent': 'yuanrenxue.project',
    }

    response = requests.get(url,headers=headers)

    return response.json()


if __name__ == "__main__":
    # res_json = getHtml(1)
    # print(res_json)
    result_list = []
    for i in range(1, 6):
        res = getHtml(i)
        print(res)
        result_list += res['data']
    
    total = 0
    count = 0
    for each in result_list:
        count +=1
        total += each['value']
    print('total',total)
    print('average',total/count)
