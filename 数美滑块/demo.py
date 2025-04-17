# 分析返回结果
import json
import random
import re
import time
import logging
import colorama
from colorama import Fore, Style

import cv2
import execjs
import numpy as np
import onnxruntime
import requests

# 初始化colorama
colorama.init(autoreset=True)

# 配置日志
# 添加一个SUCCESS日志级别
SUCCESS_LEVEL = 25  # 在INFO和WARNING之间
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

# 创建logger实例
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建控制台处理器并设置格式
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 正确使用自定义日志级别的方法
def log_success(message):
    logger.log(SUCCESS_LEVEL, message)

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_warning(message):
    logger.warning(message)


def get_distance(slider: bytes, background: bytes):
    """
    slider: 滑块图
    background: 背景图
    """
    target = cv2.imdecode(np.frombuffer(slider, dtype=np.uint8), 0)
    template = cv2.imdecode(np.frombuffer(background, dtype=np.uint8), 0)
    result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
    _, distance = np.unravel_index(result.argmax(), result.shape)
    return distance

def download_image(url):
    response = requests.get(url)
    return response.content

def get_slide_track(distance):
    slide_track = [[0, -1, 1]]
    x = y = t = 0
    while x < distance:
        x += random.randint(5, 8)
        t += random.randint(100, 110)
        slide_track.append([x, y, t])

    return slide_track

def crack_captcha():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ishumei.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ishumei.com/trial/captcha.html',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    callback = 'sm_' + str(int(time.time()) * 1000)
    captcha_id = '202504151149433nPeWbSbpxwx7XPWf5'
    params = {
        'organization': 'd6tpAY1oV0Kv5jRSgxQr',
        'rversion': '1.0.4',
        'appId': 'default',
        'channel': 'DEFAULT',
        'callback': callback,
        'lang': 'zh-cn',
        'captchaUuid': captcha_id,
        'sdkver': '1.1.3',
        'data': '{}',
        'model': 'slide',
    }

    response = requests.get('https://captcha1.fengkongcloud.cn/ca/v1/register', params=params, headers=headers)

    # 提取JSON数据
    result_text = response.text
    pattern = r'sm_\d+\((.*)\)'
    match = re.search(pattern, result_text)

    if match:
        json_str = match.group(1)
        result_data = json.loads(json_str)

        # 提取所需信息
        requestId = result_data.get('requestId')
        detail = result_data.get('detail', {})
        bg = detail.get('bg')
        bg_height = detail.get('bg_height')
        bg_width = detail.get('bg_width')
        fg = detail.get('fg')
        k = detail.get('k')
        rid = detail.get('rid')

        
        url_bg = 'https://castatic.fengkongcloud.cn/' + bg
        url_fg = 'https://castatic.fengkongcloud.cn/' + fg

        bg_content = download_image(url_bg)
        fg_content = download_image(url_fg)

        # 使用模板匹配检测缺口位置
        try:
            slide_distance = get_distance(fg_content, bg_content)
        except Exception as e:
            slide_distance = 100  # 设置一个默认值

        callback = 'sm_' + str(int(time.time()) * 1000)

        with open('test.js', 'r', encoding='utf-8') as f:
            fs = f.read()

        ctx = execjs.compile(fs)

        # 计算滑动轨迹和加密参数
        adjusted_distance = slide_distance / 2  # 根据实际情况调整
        tb = ctx.call('getTB', adjusted_distance, 300)
        slide_track = get_slide_track(adjusted_distance)
        tm = ctx.call('getTM', slide_track)

        
        params = {
            'og': 'IxbGpVfruz0=',  # 固定
            'jp': 'Wq4jwGqOHYM=',  # 固定
            'captchaUuid': captcha_id,
            'callback': callback,
            'organization': 'd6tpAY1oV0Kv5jRSgxQr',  # 固定
            'dj': '7SnISxDhfjI=',  # 固定
            'rid': rid,
            'wz': 'ufdT5h7SVes=',  # 固定
            'sy': 'lN908/15DcI=',  # 固定
            'gp': '7kP9OL4ZRNU=',  # 固定
            'aj': 'Z8JptdSbQHg=',  # 固定
            'sdkver': '1.1.3',  # 固定
            'protocol': '184',  # 固定
            'act.os': 'web_pc',  # 固定
            'ostype': 'web',  # 固定
            'tb': tb,
            'rversion': '1.0.4',  # 固定
            'ly': "nOTwmf4mjpE=",  # 固定
            'tm': tm,
            'fc': '2VKLJM6OJCc=',  # 固定
            'uc': 'b8IY1XIB1iA=',  # 固定
        }

        response = requests.get('https://captcha1.fengkongcloud.cn/ca/v2/fverify', params=params, headers=headers)
        
        # 解析验证结果
        result_text = response.text
        
        pattern = r'sm_\d+\((.*)\)'
        match = re.search(pattern, result_text)
        
        if match:
            json_str = match.group(1)
            result_data = json.loads(json_str)
            
            risk_level = result_data.get('riskLevel', '')
            
            if risk_level == 'PASS':
                log_success(f"验证通过: {result_text}")
                return True
            else:
                log_error(f"验证失败: {result_text}")
                return False
        else:
            log_error("无法解析验证结果")
            return False
    else:
        log_error("无法获取验证码信息")
        return False

def batch_test(count=30):
    """批量测试验证码"""
    success_count = 0

    for i in range(count):
        log_info(f"第 {i + 1}/{count} 次验证:")
        result = crack_captcha()
        if result:
            success_count += 1

        # 间隔一段时间
        if i < count - 1:
            time.sleep(2)

    success_rate = success_count / count * 100
    log_info(f"测试完成: 总计执行{count}次，成功{success_count}次，成功率: {success_rate:.2f}%")
    
    if success_rate > 80:
        log_success(f"测试结果优秀! 成功率: {success_rate:.2f}%")
    elif success_rate > 50:
        log_info(f"测试结果良好. 成功率: {success_rate:.2f}%")
    else:
        log_warning(f"测试结果不佳. 成功率: {success_rate:.2f}%")
    
    return success_rate

if __name__ == "__main__":
    try:
        batch_test(30)
    except Exception as e:
        log_error(f"程序执行出错: {e}")
