import hashlib
import hmac
import json
import random
import re
import sys
import time
from urllib.parse import urlencode

import cv2
import ddddocr
import execjs
import numpy as np
import requests

with open('demo.js', 'r') as f:
    js = f.read()
    ctx = execjs.compile(js)
dt = '4uHxa+ZbG/JFVkBFVFKDJ+3jNwtWVo5h'
id = 'ffccaa537da544269b4c9c1dc84dcb73'
cb = ctx.call('getCB')
cookies = {
    '_zap': '5e67ae2e-d486-4eaa-810f-a4ac00866d10',
    '_xsrf': 'be651da9-a7ef-4103-bd79-08acedea7994',
    'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1744799065',
    'HMACCOUNT': '3A28917D0CBE0214',
    'd_c0': 'RMTTiOSbTxqPTpFacVtO2d5W_QOtnO7wB50=|1744799065',
    '__snaker__id': 'VivvvEQLYmAR7QZO',
    'SESSIONID': 'JH2qh9PgnScChinozKEWUxIRatBKxOka7ROPqkHSncV',
    'JOID': 'VFESBEsDv6x9mET8NINGPqZ73rovRvmeC_ZyolNr48E-9yudVfovVBuRRfIzz1l0OYly5Bru-uRuWGKOoq0eFSY=',
    'osd': 'U1EdAUIEv6N4kUP8O4ZPOaZ027MoRvabAvFyrVZi5MEx8iKaVfUqXRyRSvc6yFl7PIB15BXr8-NuV2eHpa0REC8=',
    'captcha_ticket_v2': '2|1:0|10:1744808115|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfVWliRGJBeVhXKipxRjJiNG5fZFlyejhHQUtsTlRnWHM1Umo2UjZibUVIUDlMZHFQaGpTOGsqM0N4Z3Y4dkVOKiphNUNTRWRDZXNndV9hVTg0aGEyc2lua0E5MS5LT3JqNXF4YzZ3VE9qazRzWU5WQlhTZ0dUcnE1ZW9fTDRXZTBmQTNCdkVjOUFXMTJyWVp2KjJfbEUzUHVNRExDNGVXb0N0WnVaX18zV2htaEkuX0tmR01rZ19qMUswTUQxOVlBTTBNZHdGZ2Y2b3VjUDM1NkU0VTRFUE5IWEJFakc0Y1JsNVhBZ1ZjR04yTGswV01ldmVVcV9TVEtONThhckhEdVBFMENVQXJ6SkpkZGo4OTNIajhmdkVZMkpTcnpSMEU0MHlwM214U0VneGg5Z2lpek54SC5RNUY4bEpGaEtGNmFTOE11XzAxWjVjTUx4ZUxNclZPUlMzd0NZMzJKXzlkRUF3RkFfUm9uVioqWllJdjNjR3Vxa2dDS2UzWFlaSkJEdGlkM1ZtbjF1VE5UT3ZtQlhxMFhoaFRzMkxtdC4uM1M0NXpDbWRFYkJkMUZHOFNtX2NoWlczbm15KmhFU2pza1BLdDRSUzBjVFNJRElaKk1vRUExS3Z5ZHVIdTVNT2JNZWRKV0hBZHZqMFh3YU01SkN4ZHVzOW9peW1nTHVmMEtSLlVVLk03N192X2lfMSJ9|77c5671fdca5eeb50b9898ffddd96e415a288814caf3cadf82291ef60900945b',
    'gdxidpyhxdE': 'YMhN%5C04DhPwSq0Buy79mNinijQYu0zOvELf7Sbg35KTYmZT6X8j8YM%2BBmaCEE%5Co5k9g7hMNu%5C6LlGpGx%2FJ4jzNGp80eRR3YIkoaR%2FRSewew8ca3xR6jyBMBniHdHVgyIprzk8AApwQ41zqAHMGQN4QXNdy1sl41ziczP%5CnygYUTfiabV%3A1744810839860',
    'BEC': '46faae78ffea44ab7c29d705bdab5c18',
    'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1744809950',
    'captcha_session_v2': '2|1:0|10:1744809952|18:captcha_session_v2|88:NWdTYUtoMFp0eFNxNGM1N1QyeTRSMGlkcUZqQjYvRU9MTWc1OVlkL1VNYWZQVE9mc3FOaEp3cUppL3VJWXlDeg==|2c8f65b4c6da690fb00cf9bd69f3a5ae62423b3c0e475e828ad1663d500bb543',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://www.zhihu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.zhihu.com/signin?next=%2F',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'fetch',
    'x-xsrftoken': 'be651da9-a7ef-4103-bd79-08acedea7994',
    'x-zse-93': '101_3_3.0',
    'x-zse-96': '2.0_0QsIgNyfNA=+7uHLMhRKGT/uPytUVz9A64Tu=4TJuPeN5eOB6B3RCkg=ukGqnNjT',
    'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZs0Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTF0xKTwV_jgCqzCLBoXSMpC2Xc9ty2CYLaJgGtgo8kqg8vCpmfhVynveVS9cTV72_wUp0Uu38ghFCsbLZ67wOPC2xPgXLGQN9brr8SqwKbhwOmCgBOJefDUFLwcLqtDgCkqg9SwXfUB3LwceqkiUOUvHK192YfRCCWbUYS8omhCC_yCL0Cg_zwqXmBwHqwDeYJh31OCOGSD3LMiVqhCOKfrxLQeeVdqOM6vVGouCsFgV1Y_2G2brMIBHOs9xLEBOZsgVGQMYxb_3qjhHf-GxK8ut96RVMBqeGCUOCoBws',
    # 'cookie': '_zap=5e67ae2e-d486-4eaa-810f-a4ac00866d10; _xsrf=be651da9-a7ef-4103-bd79-08acedea7994; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1744799065; HMACCOUNT=3A28917D0CBE0214; d_c0=RMTTiOSbTxqPTpFacVtO2d5W_QOtnO7wB50=|1744799065; __snaker__id=VivvvEQLYmAR7QZO; SESSIONID=JH2qh9PgnScChinozKEWUxIRatBKxOka7ROPqkHSncV; JOID=VFESBEsDv6x9mET8NINGPqZ73rovRvmeC_ZyolNr48E-9yudVfovVBuRRfIzz1l0OYly5Bru-uRuWGKOoq0eFSY=; osd=U1EdAUIEv6N4kUP8O4ZPOaZ027MoRvabAvFyrVZi5MEx8iKaVfUqXRyRSvc6yFl7PIB15BXr8-NuV2eHpa0REC8=; captcha_ticket_v2=2|1:0|10:1744808115|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfVWliRGJBeVhXKipxRjJiNG5fZFlyejhHQUtsTlRnWHM1Umo2UjZibUVIUDlMZHFQaGpTOGsqM0N4Z3Y4dkVOKiphNUNTRWRDZXNndV9hVTg0aGEyc2lua0E5MS5LT3JqNXF4YzZ3VE9qazRzWU5WQlhTZ0dUcnE1ZW9fTDRXZTBmQTNCdkVjOUFXMTJyWVp2KjJfbEUzUHVNRExDNGVXb0N0WnVaX18zV2htaEkuX0tmR01rZ19qMUswTUQxOVlBTTBNZHdGZ2Y2b3VjUDM1NkU0VTRFUE5IWEJFakc0Y1JsNVhBZ1ZjR04yTGswV01ldmVVcV9TVEtONThhckhEdVBFMENVQXJ6SkpkZGo4OTNIajhmdkVZMkpTcnpSMEU0MHlwM214U0VneGg5Z2lpek54SC5RNUY4bEpGaEtGNmFTOE11XzAxWjVjTUx4ZUxNclZPUlMzd0NZMzJKXzlkRUF3RkFfUm9uVioqWllJdjNjR3Vxa2dDS2UzWFlaSkJEdGlkM1ZtbjF1VE5UT3ZtQlhxMFhoaFRzMkxtdC4uM1M0NXpDbWRFYkJkMUZHOFNtX2NoWlczbm15KmhFU2pza1BLdDRSUzBjVFNJRElaKk1vRUExS3Z5ZHVIdTVNT2JNZWRKV0hBZHZqMFh3YU01SkN4ZHVzOW9peW1nTHVmMEtSLlVVLk03N192X2lfMSJ9|77c5671fdca5eeb50b9898ffddd96e415a288814caf3cadf82291ef60900945b; gdxidpyhxdE=YMhN%5C04DhPwSq0Buy79mNinijQYu0zOvELf7Sbg35KTYmZT6X8j8YM%2BBmaCEE%5Co5k9g7hMNu%5C6LlGpGx%2FJ4jzNGp80eRR3YIkoaR%2FRSewew8ca3xR6jyBMBniHdHVgyIprzk8AApwQ41zqAHMGQN4QXNdy1sl41ziczP%5CnygYUTfiabV%3A1744810839860; BEC=46faae78ffea44ab7c29d705bdab5c18; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1744809950; captcha_session_v2=2|1:0|10:1744809952|18:captcha_session_v2|88:NWdTYUtoMFp0eFNxNGM1N1QyeTRSMGlkcUZqQjYvRU9MTWc1OVlkL1VNYWZQVE9mc3FOaEp3cUppL3VJWXlDeg==|2c8f65b4c6da690fb00cf9bd69f3a5ae62423b3c0e475e828ad1663d500bb543',
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


def signature(self):
    self.e["timestamp"] = str(self.timestamp())
    ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
    grant_type = self.e['grant_type']
    client_id = self.e['client_id']
    source = self.e['source']
    timestamp = self.e["timestamp"]
    ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
    self.e["signature"] = ha.hexdigest()


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


result = verify_captcha()

if result and 'data' in result and result['data'].get('result') == True:
    # 如果需要，可以保存validate值
    validate = result['data'].get('validate', '')
    print(f"验证值: {validate}")
else:
    print(f"验证失败，等待后重试...")

# data = 'ticket=%7B%22validate%22%3A%22CN31_PyUUeynJh8.OtGcgdCRE9fJPhZcqJskBFAVQ1EFvs1EUgv0hKgpgppcjl5MZA1ECzzoASV*o3sa*eRSho6ixL62EEDdIOxrwN*NEDrmgjnasGUKjIqF3KRUVQWUdPTD53_Dqv8DGqOvig14U8IcZgFP5r0F4.lR4nHErvtHWOlHRGZCoE3bmh.wY3PrCil21afTbDLgWv*X1_cQpFzdcatSM6HHFs5IfuJoqU1OdrA1Xj42kypPDomcDs9JlDH_LCswh4l00nThy5aRpI3n1vJnktErGUIYUfXiNoqQnCuuSy5l01KdjDhVn*LH8xqkRRMuCrWjSE4AbeDBGq_U*kGGhEY3mSeM1v*k_rj1x_Jaqw0qU6Sj_38DUsCpvwJNUWIQs_yRzvlD_XmFA10UjhMXLBE6ngIqDaODhOcdsm2gVFdPcguyioUzutVnqMQEG_zMdlkrr.F5VIuR_58Si3ddlJZUa_FJfR_9L9ypQHC9LXeivwY0RTnnH*XmdZ_v6ljNiWX77_v_i_1%22%7D'
with open('demo.js', 'r') as f:
    js = f.read()
    ctx = execjs.compile(js)

data = ctx.call('getData', validate)

time.sleep(5)
response = requests.put(
    'https://www.zhihu.com/api/v3/oauth/captcha/v2?ticket=%7B%22validate%22%3A%22CN31_PyUUeynJh8.OtGcgdCRE9fJPhZcqJskBFAVQ1EFvs1EUgv0hKgpgppcjl5MZA1ECzzoASV*o3sa*eRSho6ixL62EEDdIOxrwN*NEDrmgjnasGUKjIqF3KRUVQWUdPTD53_Dqv8DGqOvig14U8IcZgFP5r0F4.lR4nHErvtHWOlHRGZCoE3bmh.wY3PrCil21afTbDLgWv*X1_cQpFzdcatSM6HHFs5IfuJoqU1OdrA1Xj42kypPDomcDs9JlDH_LCswh4l00nThy5aRpI3n1vJnktErGUIYUfXiNoqQnCuuSy5l01KdjDhVn*LH8xqkRRMuCrWjSE4AbeDBGq_U*kGGhEY3mSeM1v*k_rj1x_Jaqw0qU6Sj_38DUsCpvwJNUWIQs_yRzvlD_XmFA10UjhMXLBE6ngIqDaODhOcdsm2gVFdPcguyioUzutVnqMQEG_zMdlkrr.F5VIuR_58Si3ddlJZUa_FJfR_9L9ypQHC9LXeivwY0RTnnH*XmdZ_v6ljNiWX77_v_i_1%22%7D',
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.json())
# 从响应中提取验证票据信息
# 根据响应标头中的内容获取，其中的内容为：
# set-cookie:
# captcha_ticket_v2=2|1:0|10:1744806828|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfOFFZUEVGTGQ0enNhSkEuc3dXVHhSY1VETmVYUkZGY1IzQU9VZjhSVSp0eldPeFlabUg4eTJhdG1mZXJHcHBneXp3c0NuTUMwRUZhcE1ZRS5CVkFZYzNzbERxVFVaWVBlR0JDaWcqWVlPbmd3VFJJQ2p6cHROVG4zRWMqeVpsNVlOKnFTSDVCc3JPb3EuYUY2d3BsSWtQSGdnbE1NbXYzaXZqUkhJcndOaEhNdWNkNW4qWlRwandab01hTzBPNkRBOWhmMFBzZ242aUVFQm5EaEUzMnlrcUloOFd1Sm5JWUdKTTlFQWpzYWpYdS4zTlJ2bW9oeUpYVjJKcm9oRDRzbWh5YkNLdmUzR2hydTNmR1BEcno5NE5pY3IyR1AuY19xaEkuS240clkwZVh0MVIxUWVLYVFyeTVYcTMzM2dlWFNjc2JmbER4d3p2MipyWk1rRm0zMWgzb0YuNlVSSGZsTUk4RjRVZUhlT28wZ04qRENqSGlxZCozblJ6T0xFLkFlaUp0ODhOMGJOa2h1YjNRWGNFUkN3YnNCZ1ZRTjNwTHBua1J0Y2s2blN1bjZFYTYwVEE2b0pBNkQ2VUw0TkcxZHNvWW9fdE1VSy5uZCpHd2R6QjZQUmpYWWRFdE9tZ1BCamUqc2xVNWw5NGRCbSo1bW1ETkJDdUxmTlhrQSprU1BaWnRyck03N192X2lfMSJ9|44659f47c595babebcdcc28ced8282c67bd7c55e717358d0fae5ed0b2f6a4fce; Path=/; Domain=zhihu.com; Expires=Fri, 16 May 2025 12:33:48 GMT; HttpOnly

# 从响应中获取验证会话和票据
captcha_session_v2 = response.cookies.get('captcha_session_v2')
captcha_ticket_v2 = response.cookies.get('captcha_ticket_v2')

# 更新cookies字典
cookies = {
    '_zap': '5e67ae2e-d486-4eaa-810f-a4ac00866d10',
    '_xsrf': 'be651da9-a7ef-4103-bd79-08acedea7994',
    'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1744799065',
    'HMACCOUNT': '3A28917D0CBE0214',
    'd_c0': 'RMTTiOSbTxqPTpFacVtO2d5W_QOtnO7wB50=|1744799065',
    '__snaker__id': 'VivvvEQLYmAR7QZO',
    'SESSIONID': 'JH2qh9PgnScChinozKEWUxIRatBKxOka7ROPqkHSncV',
    'JOID': 'VFESBEsDv6x9mET8NINGPqZ73rovRvmeC_ZyolNr48E-9yudVfovVBuRRfIzz1l0OYly5Bru-uRuWGKOoq0eFSY=',
    'osd': 'U1EdAUIEv6N4kUP8O4ZPOaZ027MoRvabAvFyrVZi5MEx8iKaVfUqXRyRSvc6yFl7PIB15BXr8-NuV2eHpa0REC8=',
    'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1744806045',
    'BEC': 'd6322fc1daba6406210e61eaa4ec5a7a',
    'gdxidpyhxdE': 'Q9Uz0NWy%2BMxon444QNcCwS9UDw%5C1oy9BGv5%5Cvm1RiC7aRZ4ekdDRZVNPtdqK%2BeP6kt%2Fym5vAHX4vSa%5CD9LazscKnKOGa9X5fk76sEn5qEzQfNdt0jGzSt9eD9miaUg0vecza8JL%2FL1ST4p%5C%2BUyPD7CnCVyN4qOWyICyg1Ki7znXJNALp%3A1744807444809',
    'captcha_session_v2': captcha_session_v2,
    'captcha_ticket_v2': captcha_ticket_v2
}
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://www.zhihu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.zhihu.com/signin?next=%2F',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'fetch',
    'x-xsrftoken': 'be651da9-a7ef-4103-bd79-08acedea7994',
    'x-zse-83': '3_3.0',
    'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZs0Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTF0xKTwV_jgCqzCLBoXSMpC2Xc9ty2CYLaJgGtgo8kqg8vCpmfhVynveVS9cTV72_wUp0Uu38ghFCsbLZ67wOPC2xPgXLGQN9brr8SqwKbhwOmCgBOJefDUFLwcLqtDgCkqg9SwXfUB3LwceqkiUOUvHK192YfRCCWbUYS8omhCC_yCL0Cg_zwqXmBwHqwDeYJh31OCOGSD3LMiVqhCOKfrxLQeeVdqOM6vVGouCsFgV1Y_2G2brMIBHOs9xLEBOZsgVGQMYxb_3qjhHf-GxK8ut96RVMBqeGCUOCoBws',
    # 'cookie': '_zap=5e67ae2e-d486-4eaa-810f-a4ac00866d10; _xsrf=be651da9-a7ef-4103-bd79-08acedea7994; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1744799065; HMACCOUNT=3A28917D0CBE0214; d_c0=RMTTiOSbTxqPTpFacVtO2d5W_QOtnO7wB50=|1744799065; __snaker__id=VivvvEQLYmAR7QZO; SESSIONID=JH2qh9PgnScChinozKEWUxIRatBKxOka7ROPqkHSncV; JOID=VFESBEsDv6x9mET8NINGPqZ73rovRvmeC_ZyolNr48E-9yudVfovVBuRRfIzz1l0OYly5Bru-uRuWGKOoq0eFSY=; osd=U1EdAUIEv6N4kUP8O4ZPOaZ027MoRvabAvFyrVZi5MEx8iKaVfUqXRyRSvc6yFl7PIB15BXr8-NuV2eHpa0REC8=; gdxidpyhxdE=YMhN%5C04DhPwSq0Buy79mNinijQYu0zOvELf7Sbg35KTYmZT6X8j8YM%2BBmaCEE%5Co5k9g7hMNu%5C6LlGpGx%2FJ4jzNGp80eRR3YIkoaR%2FRSewew8ca3xR6jyBMBniHdHVgyIprzk8AApwQ41zqAHMGQN4QXNdy1sl41ziczP%5CnygYUTfiabV%3A1744810839860; BEC=46faae78ffea44ab7c29d705bdab5c18; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1744809950; captcha_session_v2=2|1:0|10:1744809952|18:captcha_session_v2|88:NWdTYUtoMFp0eFNxNGM1N1QyeTRSMGlkcUZqQjYvRU9MTWc1OVlkL1VNYWZQVE9mc3FOaEp3cUppL3VJWXlDeg==|2c8f65b4c6da690fb00cf9bd69f3a5ae62423b3c0e475e828ad1663d500bb543; captcha_ticket_v2=2|1:0|10:1744809960|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfMDZLRkd6S0w1amVvVTlBS28xV0ZnQ0JYWjJxZmhYWW02akNSYzA5LldOaVlGVGZ1c3RVOUJpTnJOTDJfKnV1U291bTVrMEtUbjRTVUs4eUpudFN6ZkpJNHJJNnptZTNlc1lXOF9BRFVPV0VhOFRRMmVaR2pSQ0xmV3JmSUVyUDJzSXVvb1hHVXNsTEZxTDFnQio0NWF4cTlxMGpod3pHdERlNTFtUk1NYVJTVVMyc25tdE1vbFpsamRYZjBGNGtEZTJFSmtXLndrQnE4WDVCZVFuSkhBdkROOEJ3Sl9iWXRsTGhaSng0QVNhRGg1RzRaY2ZxZ1Y5eEt3ZnppeHo2VCowZEhSOUlIUSpta1BCMmVWVU9JVzE0UWU4RkYzczRheFZQS0VOOCpFYllUdHBkRHI1ZlcxYkVWbUNyaVJ5cFhkdTZUOERzQ3E1OVBRY0h6bjhqXy5aNEZwTnhpNUZEd2NoNmhBWlpBeUJjQ2xiTTM4WTlKSmRQTS5oZ0JVKlNoUjJxVkpwbWZKOFcqV2tUZk9RRGRiSVQwQmttcm9vcS4xUGczenNkWFhjZXFnRldrbFRRbE02LkNDaHI5THpaWVpEKkd5ejhmQ1dJS3liMWY4VUtnV3ZPank0SGEub3dpUUZnU2F1SjAxdmdCV2VxcndEUjBlMHZqbVZ5d3JWZnN4cnBib1k3N192X2lfMSJ9|923e3eaf137a8ff94995c66b85f9f3bdcf722ef983b73d4d785ad896c48c563c',
}
def get_signature():
    # 生成加密签名
    timestamp = int(time.time() * 1000)
    a = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
    a.update(b'password')
    a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
    a.update(b'com.zhihu.web')
    a.update(str(timestamp).encode('utf-8'))
    signature = a.hexdigest()
    return signature, timestamp

signature, timestamp = get_signature()

# 构建请求参数字符串
data = f"client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={timestamp}&source=com.zhihu.web&signature={signature}&username=15968588744%40163.com&password=Luck_ff0810&captcha=&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin"
# data = urlencode(data)
with open('answer.js', 'rt', encoding='utf-8') as f:
    js = execjs.compile(f.read(), cwd='node_modules')
data = "x/BMA4K912CXTvQ/D+393zLjlq0d6M0sXpU17ON62+HAIQvDR+vWQaRXsVdrss7oBPVnRVqKZ4z/9RnfHY7SIyalv6XTnHNmdtQ3c3OeA0vRjuAnhCpnemmxFhzDk4=FyUSyYmyTKmv068yP4nTzgPRxu/=Yt0/e6N1ativvjUZwj5bfs0c=Kb2qcv9mJXspnDPAPBTCFXMTu7BHawS/suOX20BOj3tXts0cD0=Xp5JjyLGp9tMWu/LT1M31SZGHzHzt4=u=TbW6HxjwcmBIcplhUJoJXm59J4NilXduveAjA2GUo2rPb60xWyFYPlt=NfP00B9fJmA8F2eTW4ZUIIfhJZh/9BveerB4WWUGnbXa=2SUUWxS=a+2xah6/GjC7y2gBlI3UeiMyij+iCbkswLrxT2VupIJNTApzpgNlP9/gCaZiBYvZVZmALtLMXAa"

# with open('answer.js', 'r', encoding='utf-8') as f:
#     answer_js = f.read()
#     ctx = execjs.compile(answer_js)
# data_params = ctx.call('getData', data)
# print(data)
response = requests.post('https://www.zhihu.com/api/v3/oauth/sign_in', cookies=cookies, headers=headers, data=data)
print(response.json())
