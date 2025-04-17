import logging
import time
import random
import execjs
import requests
import uuid
import json
import re
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

cookies = {
    'captcha_v4_user': '2007ca91c1754966b5dd806c26ab3d2c',
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22http%3A%2F%2Fwww.geetest.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2MzJlNmMwMzFkYi0wNjUyNTAzNGQwYmJhOWMtMWE1MjU2MzYtMjAyNTAwMC0xOTYzMmU2YzAzMjFiYjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%7D',
    'Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744610769',
    'HMACCOUNT': '764A7B05229BE584',
    'language': 'zh',
    '_uetsid': '9029729018f611f08786198897e8bf66',
    '_uetvid': '90299a9018f611f0943c3f2848b3a4f7',
    'Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4': '1744610807',
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
    # 'Cookie': 'captcha_v4_user=2007ca91c1754966b5dd806c26ab3d2c; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22http%3A%2F%2Fwww.geetest.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2MzJlNmMwMzFkYi0wNjUyNTAzNGQwYmJhOWMtMWE1MjU2MzYtMjAyNTAwMC0xOTYzMmU2YzAzMjFiYjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219632e6c031db-06525034d0bba9c-1a525636-2025000-19632e6c0321bb9%22%7D; Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744610769; HMACCOUNT=764A7B05229BE584; language=zh; _uetsid=9029729018f611f08786198897e8bf66; _uetvid=90299a9018f611f0943c3f2848b3a4f7; Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4=1744610807',
}

callback = 'geetest_'+str(int(time.time())*1000)
# 生成唯一标识
uuid_str = str(uuid.uuid4())
captcha_id = '54088bb07d2df3c46b79f80300b0abbe'
params = {
    'callback': callback,
    'captcha_id': captcha_id,
    'challenge': uuid_str,
    'client_type': 'web',
    'risk_type': 'slide',
    'lang': 'zh',
}

response = requests.get('https://gcaptcha4.geetest.com/load', params=params, cookies=cookies, headers=headers)

# 解析返回的结果
result_text = response.text
# 使用正则表达式提取JSON部分
pattern = r'geetest_\d+\((.*)\)'
match = re.search(pattern, result_text)

if match:
    json_str = match.group(1)
    result_data = json.loads(json_str)
    process_token = result_data['data']['process_token']
    payload = result_data['data']['payload']
    bg = result_data['data']['bg']
    slice = result_data['data']['slice']
    slice_url = 'https://static.geetest.com/'+slice
    bg_url = 'https://static.geetest.com/'+bg
    lot_number = result_data['data']['lot_number']
else:
    print("无法解析返回结果")

# 下载背景图和滑块图
def download_images(bg_url, slice_url):
    bg_response = requests.get(bg_url)
    slice_response = requests.get(slice_url)
    
    bg_img = Image.open(BytesIO(bg_response.content))
    slice_img = Image.open(BytesIO(slice_response.content))
    
    # 保存图片以便查看
    bg_img.save('bg.png')
    slice_img.save('slice.png')
    
    return 'bg.png', 'slice.png'

def find_slider_offset(background_image_path, slider_image_path):
    # 加载背景图像和滑块图像
    background = cv2.imread(background_image_path)
    slider = cv2.imread(slider_image_path)

    # 将图像转换为灰度图
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    slider_gray = cv2.cvtColor(slider, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配方法查找滑块在背景图像中的位置
    result = cv2.matchTemplate(background_gray, slider_gray, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # 计算滑块的偏移距离
    slider_width = slider.shape[1]
    offset = max_loc[0] + slider_width / 2

    return offset

# 调用函数
bg_path, slice_path = download_images(bg_url, slice_url)
# 计算滑动距离
slide_distance = find_slider_offset(bg_path, slice_path)
print(f"滑动距离: {slide_distance}像素")

callback = 'geetest_'+str(int(time.time())*1000)
with open('demo.js','r',encoding='utf-8') as f:
    fs_code = f.read()
ctx = execjs.compile(fs_code)

# 调用极验接口
w = ctx.call('getW', slide_distance, lot_number,captcha_id)
params = {
    'callback': callback,
    'captcha_id': captcha_id,
    'client_type': 'web',
    'lot_number': lot_number,
    'risk_type': 'slide',
    "payload": payload,
    "process_token": process_token,
    'payload_protocol': '1',
    'pt': '1',
    'w': w
}
response = requests.get('https://gcaptcha4.geetest.com/verify', params=params, cookies=cookies, headers=headers)

# 解析返回结果
result_text = response.text
pattern = r'geetest_\d+\((.*)\)'
match = re.search(pattern, result_text)

if match:
    json_str = match.group(1)
    result_data = json.loads(json_str)
    
    # 创建日志函数
    def log_info(message):
        print(f"[INFO] {message}")
    
    def log_success(message):
        print(f"[SUCCESS] {message}")
    
    # 解析验证结果
    status = result_data.get("status")
    log_info(f"状态: {status}")
    
    if "data" in result_data:
        data = result_data["data"]
        result = data.get("result")
        lot_number = data.get("lot_number")
        fail_count = data.get("fail_count")
        
        log_info(f"批次号: {lot_number}")
        log_info(f"失败次数: {fail_count}")
        
        if result == "success":
            log_success("验证通过")
        else:
            log_info(f"验证结果: {result}")
        
        if "seccode" in data:
            seccode = data["seccode"]
            log_info(f"验证码ID: {seccode.get('captcha_id')}")
            log_info(f"通过令牌: {seccode.get('pass_token')}")
            log_info(f"生成时间: {seccode.get('gen_time')}")
        
        log_info(f"分数: {data.get('score')}")
else:
    print("无法解析返回结果")

# 循环执行20次
print("\n开始循环执行20次验证...")
success_count = 0
for i in range(20):
    print(f"\n第 {i+1} 次验证:")
    
    # 重新获取challenge
    callback = 'geetest_'+str(int(time.time())*1000)
    uuid_str = str(uuid.uuid4())
    params_load = {
        'callback': callback,
        'captcha_id': captcha_id,
        'challenge': uuid_str,
        'client_type': 'web',
        'risk_type': 'slide',
        'lang': 'zh',
    }
    
    response = requests.get('https://gcaptcha4.geetest.com/load', params=params_load, cookies=cookies, headers=headers)
    
    # 解析返回的结果
    result_text = response.text
    match = re.search(pattern, result_text)
    
    if match:
        json_str = match.group(1)
        result_data = json.loads(json_str)
        process_token = result_data['data']['process_token']
        payload = result_data['data']['payload']
        bg = result_data['data']['bg']
        slice = result_data['data']['slice']
        slice_url = 'https://static.geetest.com/'+slice
        bg_url = 'https://static.geetest.com/'+bg
        lot_number = result_data['data']['lot_number']
        
        # 下载图片并计算滑动距离
        bg_path, slice_path = download_images(bg_url, slice_url)
        slide_distance = find_slider_offset(bg_path, slice_path)
        log_info(f"滑动距离: {slide_distance}像素")
        
        # 生成w参数
        callback = 'geetest_'+str(int(time.time())*1000)
        w = ctx.call('getW', slide_distance, lot_number, captcha_id)
        
        # 验证
        params_verify = {
            'callback': callback,
            'captcha_id': captcha_id,
            'client_type': 'web',
            'lot_number': lot_number,
            'risk_type': 'slide',
            "payload": payload,
            "process_token": process_token,
            'payload_protocol': '1',
            'pt': '1',
            'w': w
        }
        
        response = requests.get('https://gcaptcha4.geetest.com/verify', params=params_verify, cookies=cookies, headers=headers)
        
        # 解析验证结果
        result_text = response.text
        match = re.search(pattern, result_text)
        
        if match:
            json_str = match.group(1)
            result_data = json.loads(json_str)
            
            if "data" in result_data and result_data["data"].get("result") == "success":
                log_success("验证通过")
                success_count += 1
            else:
                log_info(f"验证结果: {result_data.get('data', {}).get('result', '失败')}")
        else:
            log_info("无法解析返回结果")
    else:
        log_info("无法获取验证参数")
    
    # 等待一段时间再进行下一次验证
    time.sleep(2)

log_info(f"\n总计执行20次，成功{success_count}次，成功率: {success_count/20*100}%")
