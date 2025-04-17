import time

import requests
import json
import execjs

with open('demo.js', 'r') as f:
    js = f.read()
ctx = execjs.compile(js)

t = '1744287565240'
print(t)

data_sign = '{"searchReqFromPage":"xyPchome"}'
sign = ctx.call('getI', t,data_sign)
print(sign)
cookies = {
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '88f2b098ff083926e37dc0c27ffb004f_1744290359610',
    '_m_h5_tk_enc': '825a30a94621c1fe58c86aeeca277bd6',
    'cookie2': '14074476be78d62c2b645fe5d837f590',
    'xlly_s': '1',
    '_samesite_flag_': 'true',
    't': 'a29855ba281a4316c5c585273b8ba6ac',
    '_tb_token_': '56739836fea3e',
    'tfstk': 'gK2sw39D_reEUbY3jNIEVO14xdkbCr6ylniYqopwDAH9kEE-8PuZQiXjkP0UQVrZBtiYzyajiG0qkqa4D5SFUTrgjxDYlaWPUz79x9NXkm3ODXnihcKCszTgjxDA8HJAaTZgy3vJt5HAAvnj2EHxWK3dAmoxDx3tMedK223xHr3tv9njXKdtMVIQv2mjHqUx6fm1Wm1j7lsMt8MBDs4YX29vHRBm_4OtJDmLdcGsyX3BHDyIffg8fRolG5obw8GgywRZW7NuP0zNpda7XPN-wRLdRxqUNri7BgdSlPqLQXeO0Qmnn5F-B-_WWkU_SRV8XwRIAWEadXyRPKGg9PVoG-7FEAPz4-c8BOTo8bmbPAFCJdaR4R9rPA7DGHGkhDgPAMODiKZEUxxFPycj6Dm_nMsBWFctxDgPAMODifnnf-jCAFLG.',
}

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
    # 'cookie': 'mtop_partitioned_detect=1; _m_h5_tk=88f2b098ff083926e37dc0c27ffb004f_1744290359610; _m_h5_tk_enc=825a30a94621c1fe58c86aeeca277bd6; cookie2=14074476be78d62c2b645fe5d837f590; xlly_s=1; _samesite_flag_=true; t=a29855ba281a4316c5c585273b8ba6ac; _tb_token_=56739836fea3e; tfstk=gK2sw39D_reEUbY3jNIEVO14xdkbCr6ylniYqopwDAH9kEE-8PuZQiXjkP0UQVrZBtiYzyajiG0qkqa4D5SFUTrgjxDYlaWPUz79x9NXkm3ODXnihcKCszTgjxDA8HJAaTZgy3vJt5HAAvnj2EHxWK3dAmoxDx3tMedK223xHr3tv9njXKdtMVIQv2mjHqUx6fm1Wm1j7lsMt8MBDs4YX29vHRBm_4OtJDmLdcGsyX3BHDyIffg8fRolG5obw8GgywRZW7NuP0zNpda7XPN-wRLdRxqUNri7BgdSlPqLQXeO0Qmnn5F-B-_WWkU_SRV8XwRIAWEadXyRPKGg9PVoG-7FEAPz4-c8BOTo8bmbPAFCJdaR4R9rPA7DGHGkhDgPAMODiKZEUxxFPycj6Dm_nMsBWFctxDgPAMODifnnf-jCAFLG.',
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
# 搜索参数
content = '123'
data = {
    'data': '{"searchReqFromPage":"xyPchome"}',
}
print(data)
import pandas as pd
response = requests.post(
    'https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search.shade/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
).json()
print(response)
items = response['data']['singleShadeWords']
print(items)
# 将数据转换为DataFrame
df = pd.DataFrame(items)
# 保存为Excel文件
excel_filename = f"咸鱼搜索_singleShadeWords.xlsx"
df.to_excel(excel_filename, index=False)
print(f"数据已保存到 {excel_filename}")