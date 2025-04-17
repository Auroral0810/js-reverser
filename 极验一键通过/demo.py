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

cookies = {
    'captcha_v4_user': '5836b5c14b11451184bd8e20546413cb',
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
    # 'Cookie': 'captcha_v4_user=5836b5c14b11451184bd8e20546413cb',
}


success_count = 0
total_tests = 30

for test_num in range(1, total_tests + 1):
    logger.info(f"开始第{test_num}次验证测试")
    
    callback = 'geetest_'+str(int(round(time.time() * 1000)))
    captcha_id = '54088bb07d2df3c46b79f80300b0abbe'
    params = {
        'captcha_id': captcha_id,
        'challenge': '293a1297-29d9-4d39-ae5f-fa0f1216f7ab',
        'client_type': 'web',
        'risk_type': 'ai',
        'lang': 'zho',
        'callback': callback,
    }

    response = requests.get('https://gcaptcha4.geetest.com/load', params=params, cookies=cookies, headers=headers)

    pattern = re.compile(r'geetest_\d+\((.*)\)')  # 修改正则表达式，移除非贪婪匹配

    result = pattern.search(response.text)
    json_str = result.group(1)
    res = json.loads(json_str)['data']

    lot_number = res['lot_number']
    feedback = res['feedback']
    captcha_mode = res['captcha_mode']
    payload = res['payload']
    process_token = res['process_token']
    call_time = res['pow_detail']['datetime']

    callback = 'geetest_'+str(int(round(time.time() * 1000)))

    with open('demo.js', 'r',encoding='utf-8') as f:
        js = f.read()
    ctx = execjs.compile(js)
    # 使用新的数组格式的answer
    w = ctx.call('getW', lot_number, captcha_id)
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
