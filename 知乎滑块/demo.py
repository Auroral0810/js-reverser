import sys

import ddddocr
import requests
import json
import re
import os
import time
import requests
import execjs
import cv2
import numpy as np
import random
import math
import base64
import subprocess
with open('demo.js', 'r') as f:
    js = f.read()
    ctx = execjs.compile(js)
dt = '4uHxa+ZbG/JFVkBFVFKDJ+3jNwtWVo5h'
id = 'ffccaa537da544269b4c9c1dc84dcb73'
cb = ctx.call('getCB')
cookies = {
    'NTES_P_UTID': 'vdw2AldMLX7G1OaMM0r0NecnctFFlope|1736655377',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zhihu.com/signin?next=%2F',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'NTES_P_UTID=vdw2AldMLX7G1OaMM0r0NecnctFFlope|1736655377',
}

def get_captcha_data():
    params = {
        'referer': 'https://www.zhihu.com/signin',
        'zoneId': 'CN31',
        'dt': dt,
        'acToken': '9ca17ae2e6ffcda170e2e6eeadd654f5b087d5cc7ca2eb8eb2c84f938b9fb1d25c93aea7d7f242acb1bfaece2af0feaec3b92a8df09eb3d87ab4bfe1b2f65b879f9fb3c15ea699afa2b666edb1a29ab369f3b2ee9e',
        'id': id,
        'fp': 'j15zE+KHzCM7pyn\\U/0+dBSN6C5ftY3z4JEvbGOws2tI/acMNGHahglhuhtf2dQW53V4UabKejqY9Gd98TAbV2vUk7kYPtbtN249GuMXPS0Ge\\MnJZ/5Ha7bAUXg+te1\\16mI\\1SneRWyYRQntjtRqVKmuXi+PEgPMxqu90q/AMIMY4m:1744797368557',
        'https': 'true',
        'type': '',
        'version': '2.28.5',
        'dpr': '2',
        'dev': '1',
        'cb': cb,
        'ipv6': 'false',
        'runEnv': '10',
        'group': '',
        'scene': '',
        'lang': 'zh-CN',
        'sdkVersion': '',
        'loadVersion': '2.5.3',
        'iv': '4',
        'user': '',
        'width': '320',
        'audio': 'false',
        'sizeType': '10',
        'smsVersion': 'v3',
        'token': '',
        'callback': '__JSONP_ywrlnkn_0',
    }
    response = requests.get('https://c.dun.163.com/api/v3/get', params=params, cookies=cookies, headers=headers)
    # 解析JSONP响应
    jsonp_data = response.text
    # 使用更通用的正则表达式，匹配任意JSONP回调函数名称
    json_str = re.search(r'__JSONP_[^(]+\((.*)\)', jsonp_data)
    if json_str:
        data = json.loads(json_str.group(1))
    else:
        print("无法解析JSONP响应，请检查回调函数名称")
        sys.exit(1)

    # 提取需要的信息
    bg_url = data['data']['bg'][0]  # 背景图片URL
    front_url = data['data']['front'][0]  # 前景图片URL
    token = data['data']['token']
    type_value = data['data']['type']
    zone_id = data['data']['zoneId']

    return bg_url, front_url, token, type_value, zone_id


def get_track_raw(x_end):
    """生成原始的，未经加工的滑块轨迹"""
    x = 0
    y = 0
    t = random.randint(70, 100)
    count = 0
    track = []
    while x <= x_end:
        track_item = [x, y, t]
        track.append(track_item)
        x += 1
        t += random.randint(5, 10)
        if count % 6 == 0:
            y -= 1
        count += 1
    return track


def get_left_param(bg_img_path, front_img_path):
    """
    根据背景图和滑块图，计算滑块需要移动的距离，并返回格式化的left参数

    参数:
        bg_img_path: 背景图路径
        front_img_path: 滑块图路径
    返回:
        格式化的left参数，如 "129.5px"
    """
    # 读取图片
    bg_img = cv2.imread(bg_img_path)
    front_img = cv2.imread(front_img_path, cv2.IMREAD_UNCHANGED)  # 保留Alpha通道

    # 滑块图片预处理 - 处理透明图片
    if front_img.shape[2] == 4:  # 带有Alpha通道
        # 创建一个蒙版
        mask = front_img[:, :, 3]
        # 将前景图转为3通道
        front_img = front_img[:, :, :3]
        # 二值化蒙版
        _, mask = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
    else:
        # 如果没有透明通道，可以使用边缘检测等方法创建蒙版
        gray = cv2.cvtColor(front_img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # 使用模板匹配寻找缺口位置
    result = cv2.matchTemplate(bg_img, front_img, cv2.TM_CCOEFF_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 根据模板匹配结果，获取最佳匹配位置的横坐标
    x = max_loc[0]

    # 可能需要根据实际情况调整偏移量（比如滑块的中心点）
    offset = front_img.shape[1] // 3  # 这个值需要根据实际测试调整
    distance = x + offset

    # 添加一些随机扰动，让值更自然
    distance += np.random.uniform(-0.5, 0.5)
    distance = (2 * distance) / 3  # 因为图片是480*240，但是实际是320*160，所以需要除以3再乘以2
    # 格式化为"px"单位
    left_param = f"{distance:.1f}px"

    return left_param, distance


def slide_match(front_url, bg_url):
    slice_bytes = requests.get(front_url).content
    with open("front.png", mode='wb') as f:
        f.write(slice_bytes)
    bg_bytes = requests.get(bg_url).content
    with open("bg.png", mode='wb') as f:
        f.write(bg_bytes)

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slice_bytes, bg_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    # print(x1, y1, x2, y2)  # 114 45 194 125
    return int(x1 / 1.5)


def get_track(distance):
    """生成轨迹"""
    # 73.5px   22.8125   300 x 160  6.5
    base_track = [
        [4, 0, 94], [6, 0, 102], [9, 0, 111], [13, 0, 118], [18, 0, 126], [22, 0, 134], [28, 0, 140], [32, 0, 148],
        [35, 0, 156], [40, 0, 164], [42, 1, 172], [45, 2, 180], [46, 2, 189], [47, 3, 196], [49, 4, 204],
        [50, 4, 212], [51, 4, 220], [52, 4, 237], [53, 4, 244], [54, 4, 252], [55, 4, 260], [57, 4, 268],
        [58, 4, 276], [60, 4, 294], [62, 4, 373], [62, 4, 380], [63, 4, 388], [65, 4, 396], [66, 4, 405],
        [67, 4, 412], [68, 4, 421], [70, 4, 428], [73, 5, 437], [74, 5, 444], [75, 6, 452], [78, 6, 460],
        [80, 7, 468], [82, 8, 477], [84, 8, 485], [86, 8, 492], [90, 8, 501], [94, 8, 509], [95, 8, 518],
        [98, 8, 525], [102, 9, 533], [105, 10, 541], [106, 10, 588], [107, 10, 604], [109, 10, 612], [110, 10, 620],
        [110, 10, 628], [113, 11, 636], [115, 11, 644], [116, 11, 653], [118, 11, 660], [118, 11, 668],
        [120, 11, 676], [122, 11, 684], [122, 11, 692], [123, 11, 700], [124, 12, 764], [125, 12, 772],
        [126, 12, 788], [128, 12, 804], [129, 12, 812], [130, 12, 1190], [130, 12, 1252], [131, 12, 1268],
        [132, 12, 1340], [134, 12, 1710]
    ]
    random_y = random.randint(-3, 5)
    radio = distance / (base_track[-1][0] - base_track[0][0])
    new_track = []
    for x, y, t in base_track:
        y = y + random_y if y else 0
        point = [round(x * radio), y, round(t * radio)]
        new_track.append(point)
    return new_track


def verify_captcha():
    # 获取验证码数据
    bg_url, front_url, token, type_value, zone_id = get_captcha_data()
    print(f"获取到新的token: {token}")

    # 计算滑动距离
    x_distance = slide_match(front_url, bg_url)
    print(f"计算的滑动距离: {x_distance}")
    # 生成轨迹数据
    atmTraceData = get_track(x_distance + 7)  # 现在就是这两个轨迹生成有问题。
    with open('dun163.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        ctx = execjs.compile(js_code)
    traceData = ctx.call('gettraceData', atmTraceData, token)
    with open('demo.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        ctx = execjs.compile(js_code)
    # 生成验证参数
    d = str(ctx.call('getD', traceData))
    m = ""
    p = str(ctx.call('getP', token, x_distance))
    f = str(ctx.call('getF', token, atmTraceData))
    ext = str(ctx.call('getExt', token, traceData))
    # 构建验证请求
    data = {
        'd': d,
        'm': "",
        'p': p,
        'f': f,
        'ext': ext,
    }

    # 转换为JSON字符串
    json_string = json.dumps(data)

    # 验证请求参数
    params = {
        'referer': 'https://dun.163.com/trial/jigsaw',
        'zoneId': 'CN31',
        'dt': dt,
        'id': id,
        'token': token,
        'data': json_string,
        'width': '320',
        'type': '2',
        'version': '2.28.5',
        'cb': ctx.call('getCB'),
        'user': '',
        'extraData': '',
        'bf': '0',
        'runEnv': '10',
        'sdkVersion': '',
        'loadVersion': '2.5.3',
        'iv': '4',
        'callback': f'__JSONP_az66x53_{random.randint(1, 100)}',
    }

    # 发送验证请求
    response = requests.get('https://c.dun.163.com/api/v3/check', params=params, cookies=cookies, headers=headers)

    # 解析响应
    jsonp_data = response.text
    json_str = re.search(r'__JSONP_[^(]+\((.*)\)', jsonp_data)
    if json_str:
        result_data = json.loads(json_str.group(1))
        print(f"验证结果: {result_data}")
        return result_data
    else:
        print("无法解析验证响应")
        return None


# 主循环，一直尝试直到验证成功
max_attempts = 200  # 设置最大尝试次数，避免无限循环
attempt = 0

while attempt < max_attempts:
    attempt += 1
    print(f"\n尝试第 {attempt} 次验证...")

    result = verify_captcha()

    if result and 'data' in result and result['data'].get('result') == True:
        print(f"验证成功! 结果: {result}")
        # 如果需要，可以保存validate值
        validate = result['data'].get('validate', '')
        print(f"验证值: {validate}")
        break
    else:
        print(f"验证失败，等待后重试...")
        # 随机等待一段时间，避免请求过于频繁
        time.sleep(random.uniform(1.5, 3.0))

if attempt >= max_attempts:
    print(f"达到最大尝试次数 {max_attempts}，验证失败")
