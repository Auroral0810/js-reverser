import os
import time
import execjs
import requests
import jsonpath

os.environ["EXECJS_RUNTIME"] = "Node"
headers = {
    'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

o = 1
q = ''
sum = 0
for index in range(1, 6):
    t = int(time.time()) * 1000
    # 使用 RPC 远程过程调用解决（该题失败）：var demo = new Hlclient("ws://127.0.0.1:12080/ws?group=yrx&name=q6");
    # url = 'http://localhost:12080/execjs'
    # data = {
    #     'group': 'yrx',
    #     'name': "q6",
    #     'jscode': f'z({t}, {o})'
    # }
    # m = requests.post(url, data=data).json()['data']
    # 正常逆向 JavaScript 解决
    js = open('demo.js', 'r', encoding='utf-8').read()
    # from execjs._external_runtime import ExternalRuntime
    # ExternalRuntime.Context._exec_with_pipe 中 p = Popen(..., encoding='utf8')
    m = execjs.compile(js).eval(f'z({t}, {o})')
    q = f'{o}-{t}|'
    url = "https://match.yuanrenxue.cn/api/match/6"
    # values.extend(v['value'] for v in requests.get(url, headers=headers, params={'page': index, 'm': m, 'q': q}).json()['data'])
    response = requests.get(url, headers=headers, params={'page': index, 'm': m, 'q': q}).json()
    o += 1
    res = response['data']
    for i in res:
        sum += i['value']
print(sum * 24)
# print(sum(values) * 24)
