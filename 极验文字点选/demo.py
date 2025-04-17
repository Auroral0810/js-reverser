import json
import re
import time
import urllib

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
    'sensorsdata2015jssdkcross': '%7B%22%24device_id%22%3A%2219642a7e5cc1791-0d48ee46d4bfc6-1a525636-2025000-19642a7e5cd25e9%22%7D',
    'Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744610769,1744862248,1744875022',
    'Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744875022',
    'HMACCOUNT': 'DDF927EE5DF25454',
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
    # 'Cookie': 'captcha_v4_user=5836b5c14b11451184bd8e20546413cb; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%2219642a7e5cc1791-0d48ee46d4bfc6-1a525636-2025000-19642a7e5cd25e9%22%7D; Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744610769,1744862248,1744875022; Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744875022; HMACCOUNT=DDF927EE5DF25454',
}

# 打码狗平台配置
DAMAGOU_API_URL = "http://api.damagou.top/apiv1/jiyan4CustomRecognize.html"
DAMAGOU_USERKEY = "DAMAGOU_USERKEY"  # 替换为你的userkey


def get_w_from_damagou(load_response, captcha_id, referer=None, user_agent=None):
    """
    从打码狗平台获取w参数

    Args:
        load_response: load请求的原始响应内容
        captcha_id: 极验四代参数captcha_id
        referer: 请求的Referer头
        user_agent: 请求的User-Agent头

    Returns:
        str: w参数
    """
    # 准备请求参数
    data = {
        'userkey': DAMAGOU_USERKEY,
        'captchaId': captcha_id,
        'loadRes': urllib.parse.quote(load_response),
    }

    # 添加可选参数
    if referer:
        data['referer'] = referer
    if user_agent:
        data['userAgent'] = user_agent

    # 发送请求到打码狗平台
    try:
        response = requests.post(DAMAGOU_API_URL, data=data)
        logger.info(f"打码狗平台响应: {response.text[:100]}...")  # 只打印前100个字符

        # 检查响应格式，可能是纯文本或JSON
        if response.text.startswith('{'):
            result = json.loads(response.text)
            if result['status'] == '0':
                return result['data']
            else:
                logger.error(f"打码狗平台返回错误: {result['msg']}")
                return None
        else:
            # 纯文本格式，如果不是错误信息，则为w参数
            if not response.text.startswith('错误'):
                return response.text
            else:
                logger.error(f"打码狗平台返回错误: {response.text}")
                return None
    except Exception as e:
        logger.error(f"请求打码狗平台出错: {str(e)}")
        return None
success_count = 0
total_tests = 30

for test_num in range(1, total_tests + 1):
    logger.info(f"开始第{test_num}次验证测试")
    
    callback = 'geetest_'+str(int(round(time.time() * 1000)))
    captcha_id = '54088bb07d2df3c46b79f80300b0abbe'
    params = {
        'captcha_id': captcha_id,
        'challenge': '60b9fd96-e868-4298-ab37-9a4b35562c6c',
        'client_type': 'web',
        'risk_type': 'word',
        'lang': 'zho',
        'callback': callback,
    }

    response = requests.get('https://gcaptcha4.geetest.com/load', params=params, cookies=cookies, headers=headers)
    load_response_text = response.text
    pattern = re.compile(r'geetest_\d+\((.*)\)')  # 修改正则表达式，移除非贪婪匹配

    result = pattern.search(response.text)
    json_str = result.group(1)
    res = json.loads(json_str)['data']

    lot_number = res['lot_number']
    imgs = res['imgs'] #主体图片
    ques = res['ques'] # 三个小的需要识别找到的图片
    feedback = res['feedback']
    captcha_mode = res['captcha_mode']
    payload = res['payload']
    process_token = res['process_token']
    call_time = res['pow_detail']['datetime']
    # 从打码狗平台获取w参数
    w = get_w_from_damagou(
        load_response_text,
        captcha_id,
        referer='https://gt4.geetest.com/',
        user_agent=headers['User-Agent']
    )

    if not w:
        logger.error("获取w参数失败，跳过本次测试")
        continue
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
