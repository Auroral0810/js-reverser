import json
from sqlite3 import Date

import requests
import execjs

def get_m():
    with open('1.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    js = execjs.compile(js_content)
    v = js.call('get_sign')
    return v

param_m = get_m()

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/1',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

import pandas as pd

# 创建一个空列表来存储所有数据
all_data = []

for i in range(1, 6):
    # 使用动态生成的m参数
    params = {
        'page': i,  # 页码，可以根据需要修改
        'm': param_m,  # 动态生成的加密参数
    }
    # 发送请求
    response = requests.get('https://match.yuanrenxue.cn/api/match/1', params=params, headers=headers).json()
    res = response['data']
    # 将当前页的数据添加到总列表中
    all_data.extend(res)

# 将列表转换为DataFrame
df = pd.DataFrame(all_data)
# 计算value列的平均值
average_value = df['value'].mean()
print(f"\n所有数据的平均值是: {average_value}")
