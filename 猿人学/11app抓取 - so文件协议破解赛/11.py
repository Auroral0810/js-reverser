import requests


def get_res(page):
    global s
    url = 'http://localhost:8080/getSign/' + str(page)

    sign = requests.get(url=url).text

    new_url = 'https://match.yuanrenxue.com/api/match/11/query'
    params = {
        'id': str(page),
        'sign': sign
    }
    res = requests.get(url=new_url, params=params).json()
    s += res['data']
    print(res)


if __name__ == '__main__':
    s = 0
    for i in range(0, 100):
        get_res(i)
    print(s)
