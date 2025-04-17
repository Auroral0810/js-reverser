# -*- coding: utf-8 -*-
# @Time    : 2019/9/29 18:37
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import os
import random
import numpy as np
import requests
import execjs
import json
import time
from PIL import Image
import cv2
from urllib.parse import urlencode


headers = {
    'Referer': 'https://id.163yun.com/login?referrer=https://dun.163.com/dashboard&h=yd&t=yd&i18nEnable=true&locale=zh_CN',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def _reload_js():
    """
    加载 js
    :return:
    """
    with open('yd_slider.js', 'rb') as f:
        slider_js = f.read().decode()
    with open('generate_fp.js', 'rb') as f:
        fp_js = f.read().decode()
    return slider_js, fp_js


def _get_cb(js):
    """
    生成 cp 参数
    :param js:
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('get_cb')[:64]


def _get_fp(js):
    """
    生成指纹 fp
    :param js:
    :return:
    """
    ctx_ = execjs.compile(js)
    return ctx_.call('generateFingerprint')


def _encrypt_data(js, token, trace):
    """
    加密轨迹
    :param token:
    :param trace:
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('encrypt', token, trace)


def _generate_trace(distance, start_time):
    """
    生成轨迹
    :param distance:
    :param start_time:
    :return:
    """
    back = random.randint(2, 6)
    distance += back
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    # 回退
    for _ in range(back):
        current -= 1
        tracks_list.append(round(current))
    tracks_list.append(round(current) - 1)
    if tracks_list[-1] != distance - back:
        tracks_list.append(distance - back)
    # 生成时间戳列表
    timestamp_list = []
    timestamp = int(time.time() * 1000)
    for i in range(len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    zy = 0
    for j in range(len(tracks_list)):
        y = random.choice([0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, -1, 0, 0])
        zy += y
        y_list.append(zy)
        j += 1
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([x, y_list[index], timestamp_list[index] - start_time])
    return trace


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_path = os.path.abspath('...') + '\\' + '{}.jpg'.format(type)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def _cut_slider(path):
    """
    滑块切割
    :return:
    """
    image = Image.open(path)
    x = []
    y = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pix = image.load()[i, j]
            if pix != 255:
                x.append(i)
                y.append(j)
    z = (np.min(x), np.min(y), np.max(x), np.max(y))
    result = image.crop(z)
    result.convert('RGB').save('targ.jpg')
    result.show()
    return result.size[0], result.size[1]


def _get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url: 滑块图片 url
    :param captcha_url: 验证码图片 url
    :return:
    """

    # 引用上面的图片下载
    slider_path = _pic_download(slider_url, 'slider')

    # time.sleep(2)

    # 引用上面的图片下载
    captcha_path = _pic_download(captcha_url, 'captcha')

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(targ, target)
    w, h = _cut_slider(slider_path)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y + 3, x + 3, y + w - 3, x + h - 3)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save("new_image.jpg")
    imagecrop.show()
    return int(y + 3)


def _init_slider(slider_js, fp):
    """
    滑块初始化
    :param slider_js:
    :param fp:
    :return:
    """
    url = 'https://c.dun.163yun.com/api/v2/get?'
    params = {
        'id': 'cff8becfc6914bf6a81d255f67a626b9',
        'fp': fp,
        'https': 'true',
        'type': 'undefined',
        'version': '2.12.0',
        'dpr': '1',
        'dev': '1',
        'cb': _get_cb(slider_js),
        'ipv6': 'false',
        'runEnv': 10,
        'width': '306',
        'token': '41dede6702394d39861c709641713297',  # 可固定
        'referer': 'https://id.163yun.com/login',
        'callback': '__JSONP_55xb89m_0'
    }

    resp = requests.get(url, params=params, headers=headers)
    result = json.loads(resp.text.replace('__JSONP_55xb89m_0(', '').replace(');', ''))
    if result['data']['type'] == 2:
        print('滑块验证初始化成功! ')
        token = result['data']['token']
        bg = result['data']['bg']
        front = result['data']['front']
        return {
            'token': token,
            'captcha_url': bg,
            'slider_url': front
        }
    elif result['data']['type'] == 3:
        print('当前验证码为点选验证, 跳过...')
        return None
    raise Exception('未知类型验证码! ')


def _slider_verify(slider_js, token, trace, fp):
    """
    验证
    :param slider_js:
    :param token:
    :param distance:
    :param fp:
    :return:
    """
    data = _encrypt_data(slider_js, token, trace)
    params = {
        'id': 'cff8becfc6914bf6a81d255f67a626b9',
        'token': token,
        'acToken': '',
        'data': data,
        'width': '306',
        'type': '2',
        'version': '2.12.0',
        'cb': _get_cb(slider_js),
        'extraData': '',
        'runEnv': 10,
        'referer': 'https://id.163yun.com/login',
        'callback': '__JSONP_bc4jy3y_1'
    }
    cookies = {
        'gdxidpyhxdE': fp
    }
    check_url = 'https://c.dun.163yun.com/api/v2/check?' + urlencode(params)
    resp = requests.get(check_url, headers=headers, cookies=cookies)
    result = json.loads(resp.text.replace('__JSONP_bc4jy3y_1(', '').replace(');', ''))
    print(result)
    if result['data']['result']:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validate': result['data']['validate']
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def crack():
    slider_js, fp_js = _reload_js()
    fp = _get_fp(fp_js)
    while True:
        init_data = _init_slider(slider_js, fp)
        if init_data:
            token = init_data['token']
            bg = init_data['captcha_url']
            fg = init_data['slider_url']
            break
        time.sleep(1)
    distance = int(_get_distance(fg[1], bg[1]) * (306 / 320))
    start_time = int(time.time() * 1000)
    time.sleep(random.uniform(0.01, 0.05))
    trace = _generate_trace(distance, start_time)
    result = _slider_verify(slider_js, token, trace, fp)
    return result


if __name__ == '__main__':
    crack()
