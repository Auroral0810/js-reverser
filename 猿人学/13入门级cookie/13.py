import requests
import re
 
def data(sum_data):
    session = requests.session()    #保持会话
    session.cookies.update({"sessionid": "a0san8v13c61zw435r31r0zpq62xafx5"})   #更新sessionid
    session.headers = {'user-agent': 'yuanrenxue.project'}
    response = session.get('https://match.yuanrenxue.com/match/13')
    cookies = re.findall("'([a-zA-Z0-9=_|])'",response.text)
    yuanrenxue_cookie = ''.join(cookies)
    key,value = yuanrenxue_cookie.split('=')
    cookie = {key: value}
    session.cookies.update(cookie)  #更新yuanrenxue_cookie
 
    for i in range(1,6):
        url = 'https://match.yuanrenxue.com/api/match/13?page={}'.format(i)
        response = session.get(url=url)
        values = response.json()['data']
        for v in values:
            value = v['value']
            sum_data.append(value)
    print(sum(sum_data))
 
if __name__ == '__main__':
    sum_data = []
    data(sum_data)