import json
import re
import time
import numpy as np
import pandas as pd
import requests
import execjs
import os
import sys
from loguru import logger

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# 配置 logger
logger.remove()  # 移除默认处理器
# 添加自定义格式处理器，格式与图片中一致
logger.add(
    sink=sys.stdout,  # 输出到标准输出
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,  # 启用颜色
    level="INFO"  # 设置日志级别
)

#横向检查
def check_transverse(a):
    # 检查是否为列表类型，如果是则转换为DataFrame
    if isinstance(a, list):
        a = pd.DataFrame(a)
    
    for i in range(0,a.shape[0]):
        if(np.std(a.iloc[:,i])==0):   #标准差检查所有元素是否相等
            return 1
    return -1

#纵向检查
def check_portrait(a):
    # 检查是否为列表类型，如果是则转换为DataFrame
    if isinstance(a, list):
        a = pd.DataFrame(a)
        
    for i in range(0, a.shape[1]):
        if (np.std(a.iloc[i,:]) == 0):
            return 1
    return -1

#纵向交换
def portrait_change(a):
    # 检查是否为列表类型，如果是则转换为DataFrame
    if isinstance(a, list):
        a = pd.DataFrame(a)
        
    while True:
        b = a.copy()
        x,y = b.shape
        for i in range(0,x):
            for n in range(0,y-1):
                # 使用loc进行赋值，避免链式赋值警告
                tmp = b.iloc[i,n]
                b.iloc[i,n] = b.iloc[i,n+1]
                b.iloc[i,n+1] = tmp
                result = check_transverse(b)
                if(result==1):
                    return [[i, n], [i, n+1]]
                result = check_portrait(b)
                if(result==1):
                    return [[i, n], [i, n+1]]
                b = a.copy()
        return 0

#横向交换
def transverse_change(a):
    # 检查是否为列表类型，如果是则转换为DataFrame
    if isinstance(a, list):
        a = pd.DataFrame(a)
        
    while True:
        b = a.copy()
        x,y = b.shape
        for i in range(0,x):
            for n in range(0,y-1):
                # 使用loc进行赋值，避免链式赋值警告
                tmp = b.iloc[n,i]
                b.iloc[n,i] = b.iloc[n+1,i]
                b.iloc[n+1,i] = tmp
                result = check_transverse(b)
                if(result==1):
                    return [[n, i], [n+1, i]]
                result = check_portrait(b)
                if(result==1):
                    return [[n, i], [n+1, i]]
                b = a.copy()
        return 0

cookies = {
    'captcha_v4_user': '2007ca91c1754966b5dd806c26ab3d2c',
    'language': 'zh',
    'Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744610769,1744862248',
    'HMACCOUNT': '764A7B05229BE584',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.geetest.com%2Fadaptive-captcha%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2MzJlNmMwMzFkYi0wNjUyNTAzNGQwYmJhOWMtMWE1MjU2MzYtMjAyNTAwMC0xOTYzMmU2YzAzMjFiYjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%7D',
    'Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744862278',
    '_uetsid': '1b0adaa01b4011f09ba1db5fbf437bb7',
    '_uetvid': '90299a9018f611f0943c3f2848b3a4f7',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://gt4.geetest.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'captcha_v4_user=2007ca91c1754966b5dd806c26ab3d2c; language=zh; Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744610769,1744862248; HMACCOUNT=764A7B05229BE584; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.geetest.com%2Fadaptive-captcha%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2MzJlNmMwMzFkYi0wNjUyNTAzNGQwYmJhOWMtMWE1MjU2MzYtMjAyNTAwMC0xOTYzMmU2YzAzMjFiYjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%7D; Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744862278; _uetsid=1b0adaa01b4011f09ba1db5fbf437bb7; _uetvid=90299a9018f611f0943c3f2848b3a4f7',
}
success_count = 0
total_tests = 30

for test_num in range(1, total_tests + 1):
    logger.info(f"开始第{test_num}次验证测试")
    
    callback = 'geetest_'+str(int(round(time.time() * 1000)))
    captcha_id = '54088bb07d2df3c46b79f80300b0abbe'
    params = {
        'captcha_id': captcha_id,
        'challenge': '209742de-12dc-4fe4-a1af-b07e0c26694b',
        'client_type': 'web',
        'risk_type': 'match',
        'lang': 'zho',
        'callback': callback,
    }

    response = requests.get('https://gcaptcha4.geetest.com/load', params=params, cookies=cookies, headers=headers)

    pattern = re.compile(r'geetest_\d+\((.*)\)')  # 修改正则表达式，移除非贪婪匹配

    result = pattern.search(response.text)
    json_str = result.group(1)
    res = json.loads(json_str)['data']

    lot_number = res['lot_number']
    imgs = res['imgs']
    ques = res['ques']
    feedback = res['feedback']
    captcha_mode = res['captcha_mode']
    payload = res['payload']
    process_token = res['process_token']
    call_time = res['pow_detail']['datetime']
    answer = portrait_change(ques)

    callback = 'geetest_'+str(int(round(time.time() * 1000)))

    with open('demo.js', 'r',encoding='utf-8') as f:
        js = f.read()
    ctx = execjs.compile(js)

    # 使用新的数组格式的answer
    w = ctx.call('getW', answer, lot_number, captcha_id)
    time.sleep(5)

    # 构造验证的参数
    params = {
        'callback': callback,
        'captcha_id': captcha_id,
        'client_type': 'web',
        'lot_number': lot_number,
        'risk_type': 'match',
        'payload': payload,
        'process_token': process_token,
        'payload_protocol': '1',
        'pt': '1',
        'w': w
    }

    response = requests.get('https://gcaptcha4.geetest.com/verify', params=params, cookies=cookies, headers=headers)
    pattern = re.compile(r'geetest_\d+\((.*)\)')  # 修改正则表达式，移除非贪婪匹配

    result = pattern.search(response.text)
    json_str = result.group(1)
    res = json.loads(json_str)
    
    # 判断验证是否成功
    is_success = False
    if 'data' in res and 'result' in res['data'] and res['data']['result'] == 'success':
        is_success = True
        success_count += 1
    
    logger.info(f"第{test_num}次验证结果: {res}")
    logger.info(f"第{test_num}次验证{'成功' if is_success else '失败'}")

# 计算并输出最终准确率
accuracy = (success_count / total_tests) * 100
logger.info(f"测试完成: 总共{total_tests}次测试, 成功{success_count}次, 准确率{accuracy:.2f}%")
