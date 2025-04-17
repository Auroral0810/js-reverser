import time

import requests
import json
import execjs

with open('demo.js', 'r') as f:
    js = f.read()
ctx = execjs.compile(js)

t = int(time.time()*1000)
# print(t)
# 搜索参数
content = '平板'
data_sign ='{"inputWords":"'+content+'","searchReqFromPage":"xyPcHome","bucketId":30,"type":0}',
sign = ctx.call('getI', t,data_sign)
# print(sign)
headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.goofish.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.goofish.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'mtop_partitioned_detect=1; _m_h5_tk=88f2b098ff083926e37dc0c27ffb004f_1744290359610; _m_h5_tk_enc=825a30a94621c1fe58c86aeeca277bd6; cookie2=14074476be78d62c2b645fe5d837f590; xlly_s=1; x5secdata=xdb060d42a37ff81bda903b70be546057de99159e2b9db4e6c1744283184a-717315356a-264295618abaad3eaaxianyuSpace_default__bx__h5api.m.goofish.com%3A443%2Fh5%2Fmtop.taobao.idlemtopsearch.pc.search%2F1.0; _samesite_flag_=true; t=a29855ba281a4316c5c585273b8ba6ac; _tb_token_=56739836fea3e; tfstk=gCvZwbAJ4tYBqH9ZoMX4aVlTj3WOnO0S3K_fmnxcfNbgCRaDTUYd5IO15oReoeC1SC_b3KW9dCwf5VB2mU6qP4MSFhKOBt0SPeyvrB6Pbi40lZ2hBiGZXTJZFhKTxlzmVBD7ul0PbhbDo1fhxGQ3IrbMovxhJiI0Si2iYHbd-G4Gmsxh-ijYnRYcnDWhJiXcjfdhzwyP21mXypqeTlfh_axG88-pdGYU6h7Un-veT17oFwy0npSMASFCfRDP-CODC9vi-r6H2BTGYTk40MRyxOjwkYeOI3xHi1JqGuQvTHA5TBEsXMJw4KSPtj4fl_JHCOdEz8_k9nvVth3zwMODVdO252ec5Q-H8_9QR86HQFJGTTjrHrInCvpv_rVVsMIFPDoFfj_A1HtF0vFYM6A1YaiscSFAsMIFPDoUMSCH1M7Sfm1..',
}
cookies = {
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '88f2b098ff083926e37dc0c27ffb004f_1744290359610',
    '_m_h5_tk_enc': '825a30a94621c1fe58c86aeeca277bd6',
    'cookie2': '14074476be78d62c2b645fe5d837f590',
    'xlly_s': '1',
    'x5secdata': 'xdb060d42a37ff81bda903b70be546057de99159e2b9db4e6c1744283184a-717315356a-264295618abaad3eaaxianyuSpace_default__bx__h5api.m.goofish.com%3A443%2Fh5%2Fmtop.taobao.idlemtopsearch.pc.search%2F1.0',
    '_samesite_flag_': 'true',
    't': 'a29855ba281a4316c5c585273b8ba6ac',
    '_tb_token_': '56739836fea3e',
    'tfstk': 'gCvZwbAJ4tYBqH9ZoMX4aVlTj3WOnO0S3K_fmnxcfNbgCRaDTUYd5IO15oReoeC1SC_b3KW9dCwf5VB2mU6qP4MSFhKOBt0SPeyvrB6Pbi40lZ2hBiGZXTJZFhKTxlzmVBD7ul0PbhbDo1fhxGQ3IrbMovxhJiI0Si2iYHbd-G4Gmsxh-ijYnRYcnDWhJiXcjfdhzwyP21mXypqeTlfh_axG88-pdGYU6h7Un-veT17oFwy0npSMASFCfRDP-CODC9vi-r6H2BTGYTk40MRyxOjwkYeOI3xHi1JqGuQvTHA5TBEsXMJw4KSPtj4fl_JHCOdEz8_k9nvVth3zwMODVdO252ec5Q-H8_9QR86HQFJGTTjrHrInCvpv_rVVsMIFPDoFfj_A1HtF0vFYM6A1YaiscSFAsMIFPDoUMSCH1M7Sfm1..',
}

params = {
    'jsv': '2.7.2',
    'appKey': '34839810',
    't': t,  # 时间戳
    'sign': sign,  # 签名
    'v': '1.0',
    'type': 'originaljson',
    'accountSite': 'xianyu',
    'dataType': 'json',
    'timeout': '20000',
    'api': 'mtop.taobao.idlemtopsearch.pc.search.suggest',
    'sessionOption': 'AutoLoginOnly',
    'spm_cnt': 'a21ybx.item.0.0',
    'spm_pre': 'widle.12011849.0.0',
}

data = {
    'data': '{"inputWords":"'+content+'","searchReqFromPage":"xyPcHome","bucketId":30,"type":0}',
}
# print(data)
import pandas as pd

response = requests.post(
    'https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search.suggest/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
).json()
print(response)
items = response['data']['items']
print(items)
# 将数据转换为DataFrame
df = pd.DataFrame(items)
# 保存为Excel文件
excel_filename = f"咸鱼搜索_{content}.xlsx"
df.to_excel(excel_filename, index=False)
print(f"数据已保存到 {excel_filename}")