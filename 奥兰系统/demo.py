import random
import requests
from bs4 import BeautifulSoup
import execjs
import ddddocr
import os
import time
from PIL import Image, ImageEnhance
import pandas as pd


def enhance_image(image_path):
    """预处理图片以提高识别率"""
    img = Image.open(image_path)
    # 增加对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # 增加锐度
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    # 保存增强后的图片
    enhanced_path = f"enhanced_{os.path.basename(image_path)}"
    img.save(enhanced_path)
    return enhanced_path


def recognize_with_ddddocr(image_path, enhance=True):
    """使用ddddocr识别验证码"""
    if enhance:
        image_path = enhance_image(image_path)

    # 创建识别器
    ocr = ddddocr.DdddOcr(show_ad=False)

    # 读取图片内容
    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    # 识别验证码
    result = ocr.classification(img_bytes)

    # 清理临时文件
    if enhance and os.path.exists(image_path) and image_path.startswith("enhanced_"):
        os.remove(image_path)

    # 对结果进行处理，确保只返回数字
    result = ''.join(filter(str.isdigit, result))

    return result


with open('demo.js', 'r', encoding='utf-8') as f:
    js = f.read()

ctx = execjs.compile(js)



cookies = {
    'SESSION': 'c03b8096-43fc-4aaf-900b-5d819a8b5851',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'Cookie': 'SESSION=c03b8096-43fc-4aaf-900b-5d819a8b5851',
}

# 创建会话对象，用于管理整个登录流程中的cookies
session = requests.Session()
session.verify = False  # 关闭SSL验证，与您之前的代码一致

# 获取登录页面
response = session.get(
    'http://sso.nau.edu.cn/sso/login?service=http://ngx.nau.edu.cn/wengine-auth/login?cas_login=true',
    headers=headers
)
soup = BeautifulSoup(response.text, 'html.parser')

# 2.获取验证码图片
captcha_img = soup.select_one('#fm1 > div.codeCon.fill_form.code > img')
if captcha_img:
    captcha_suffix = captcha_img.get('src')  # 获取 /sso/captcha.jpg
    captcha_url = f"http://sso.nau.edu.cn{captcha_suffix}?tt={random.random()}"
    # print(f"验证码图片URL: {captcha_url}")
    
    # 下载验证码图片 - 使用session
    captcha_response = session.get(captcha_url, headers=headers)
    
    # 保存验证码图片到本地
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha_response.content)
    
    # print("验证码图片已保存为captcha.jpg")
else:
    print("未找到验证码图片元素")
captcha_path = "captcha.jpg"
result = recognize_with_ddddocr(captcha_path)
# print("验证码识别结果:", result)

# 3.获取execution
execution = soup.select_one('input[name="execution"]').get('value')
# print(f"获取到的execution值: {execution}")
# e1de8cd8-41d6-400d-9e93-45bea05190af_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuUTNWd1pFb3ZkWHBPT1M5a1dHcEJhVXR6UVRWb1YwOTFaRVZHZG5sbFJuUkJPRWhIVmtoWFNTdHVlalJRTm1zeVRqRklURlJFVDFWaGRXWXZjakkxWmxZMU5XNWFXbEpZTjJSSlYyVkJRbkpUWlUxMU0wVm9UbFZUYUZoU2RYSXhORVV5U1hObmRVZFFTMDlaUTBSM1VWRlhaakF4T0haSFdVbDVZbVEwWm5seU0yZ3lRVGd2TkZSWlNHUk5XbWhqV201SWJUZzFRWFJYY0dSUldYZFpkM2QzZVVad1VWcHNUbEpUZHk4eWExbHpUa3NyZUROMVFqVkhkRk54TUhSeGFFeHhiMnB1V1VKQlVGbGpPVk5YV2xkaU1DOTJkVU5OVjNoUWVERmlURUZrTTNkTkt6Tm5lSGQwTW1aNVZEaGxkVWxOUTBORU5FSm9XblpRVms5UWRtbENaRGxqWW5kQkwyRjZSRGRHYTNFMVVIRkJVa3hKY0hOVVUzVkxZVlF3VHl0TWFVMHZOVTh5YURGalRFWmlkREZhVW5KemRIbFVWbkZ2UVU5RVFscFVTMGhDYWsxemVTOHhSa3d5YlhwMmRXUk5aWEpSY3pSaGRIWmxjV3R4Um0xVmFFZHVheXRHWldkbmJYbzNXVnBUY1VZeFFUY3ZaakZ3WjNGb2EzcEZUVll6VERka1dFcDRNV1pUU2xwbEx6bG9TaTlhWlRoc016ZHdOV1pEZEVReVpGWXpkWGxPY0ZKR1VGZ3JaVVZyWmxGUlNETlNPRGRqUmxoWFRGcDZWMDF6YlVad1dqUkRUVzh3ZGpCRFpWbFJTMFpLVjBGMk5HWmlaSE5yVm1GWE1YbE9hV2R3WVdOeWVsaDZSWGRMYkRoVVVqbGpiM1I0UkRoaGMyaFNRVE5PTWxoWFNFRndXRU5HYW01cmRHeHBlRFUzVVdWREwycFdjMWx6TWpWTE0zbEhiaTk2VlhKWGRVeHdNVlE0YmtoTWRrMDFURE5tWWxVMVVuUnJjRXQ1ZWpOeVNuWlBNR0VyY25OcUsxZzRNRzVoVlhWaU9FMXRWelpPTjJjNFRGbGtVVzR3VlU1VU4wOTZhSFIyTmxJd04yVkNlbkpZUW5BeVRrcFlTVXRoTkRFM1IxVXJOM1YwZFdadVJIbGpPRWhJYkdweGQzVllXbFl3ZWpkek1VaEJSazF0UVdkeE1qbHJiMHRSYURabFpWSkJibFUwVjNaUlQyMVdORmN2UmxwUGVHNVNVbU5IVFZoMGFtbFNNV1phUmxadGRHSmhkMVExWmpWaU1XbFdSR1ZqV0VSVGNuSjJkemRzYUVJeWRYazJWMDlWTURSUVVFTmlOSEZWZHpoR1VsWlRhbGx6TkhGdVprNUdPVzFGZW1NNVZuaFZiM2wyVnpKbFJsZ3dTVkZ0WmpCcFFrcHFjbkJSYjJsNE9YaFNRVUZXZG5wUlZteGFkSGsxVEdSRVNrVnhlbkptVjNFcmRtb3hZbXBZU0ZsWVpuVnFlSHB5Wml0SFp6TXhZMlZNZEVSUVkzQmhPVTVDVjNOUEwyZFpSRnBsTlU4M2QzQk5abXRSWm14Qk9FcFdOR3R2Y205RmJrMVhNa05qUVhKQ2QwTmFUbFpTZVNzeVducHhkMkl3WW5KQlV6bHFjMFIwY2tkVU1WZEhVR2RPVTNKblFXdEdUVXhFVjNCbGRUZEpabTVDVUVNMldtWXlNSGh5VW01dFZGZEJVVE42Y25NcldrcFZObGMwTkhsV1ZWQnBSR2czT0dNMWMwMW5UVFpPVFhsa2Qyd3lOM0ZKU1ZKVFlVMHhXbEUwZWtSVFVsRlJRVlpPUnpGdGFXcExaQ3RXVlhBeE1uUlJXbGRTV2tONlFuUkRXU3RpVWpCTFJtUTFXbkowVVZFdlpUUmxURzh2YUdrNVpIQmFaVTVvY0d0RlJsZGxXbWhZWTBadGFHWnhRa3hMVldSM0wxZEhTa1JHY0ZCdVlWUlFMMDEwUm1GbVdURlNkM2NyUm1SUVVYb3lXWE5oU0VwNk9XRXJZVmREWTNsb1NFaGxURXRGWkZaRWFFZGthblpwYjBobFZIaEJWRkppYkdKclJuQnFkVlZUWW1Sa2FWY3diak5SUzB4d2NsRnNOazlwU1cxdmJXUkRLMnNyU0hVMWVUTlVjblptWWtsQmJHRTRWMEZqTUhCeWQxaExiVkprU1hoR2VHZ3dPVFo2Y0dwb2RXMVdXbk5CTDFwdllrVkxSbGcyT1N0dFpGVkxOV3h4VVVaU1ZGZENjRnAyZDA1Qk1EaDZXRTVJWWpWTVdFSlBaV1J0Y0cxNlpHazRWbFo0ZUhCV01uQnhNamR3TVdaQk4xaEpNMDgwU2xWbmExRmpibkZXVW0xdGNESlpNbTFPVjNGMmNpOTFWRWt4T1ZOd1dtSkdSSFJhTm01V1dqbGlVbUp4YUZKalNTdE5iV0pFUkhGWk5GVnhhRGhQV25JMU5VWnVTV0ZFV2xkbWNGcDBkVEp0V201WFVtcDFTalZyWjJwVFFWVkRla3R0WWtKWE4wdzBTRFpNVld4TmEzQjJlQzlVUkUwMlYyMHpiRGsyVVhSMmRXOXZXU3RTYUZVMk9EYzFVR0pDZHl0SWFEWlJUV2t3ZDFSNWJsVktZM05oVmtkalUzSkpkM1JvWWs5Sk4xbEVOWFI2YWtObVlrWlBaakZQTUdrM1ozaEhjbTlqUmtVeVYzcFFSSEJYUlRBdmFHNWxaV2xWZUVKQ016QXdVU3M1YVZwblZHNUZVM1phUW5OVU0wZ3JlVGRXWXpVMFpHTkNZaTgyVkVkNGVVWlJSVmRWSzBZeFIxVlhWVXRzUVdOblFqY3dRa2RTYjFKTVRubDFiM1IxUVhSTmFWSklkSEZDTTNsV1puSnNUV0l4VG5sWWIzbG5WMG94TmxoUmF6bHpiWHBOZERSc1NESTJlV1ZLTWtSWlpGaDBRMUpzTkdvMFZrOXlOQ3RwYTFwc1VqSm1lR1l4V2xocWEwNXNlVWxKVDBaR2JsZFJORzVzZURnMlNEUXJSbTF3VlV4aFNua3ZNMXBhVkVWbVRpOW1ZbUpNUlhOSVZWbHZWbEJRZGtaeVZrVnhRM0ZXVEc0MlpEbFpSa1Z4TDNWUlNYTTNZV2swUzBwVmNtOUZlWHB6WlVwTmVsRjRUVGR0T1RRMWRXcFRORFpUTXprcmIyOUxSelpVZW1GeFduSTVWRlpQVnpoRE1WVlBXVXR2YkdsdE1rWnlkeTlSU1VWeVlsVXhSVWN3TVdoRWNIQlZlRTVWVTJoWVdXSkhjbmhQWnpNclVWWm1USHAwZG0xWWRESklWbXhPY201clp6RXZiVlpRWjBwemFIaFpWMFZUTmpCVGNqbERTR1I2VGtSVFJEZEhPV1Z0VjIxek5XNDRNWE15TjFoemRFbEVOVlJpV1VrM1ZHdDZhbTFSY0dOS0syOWlkMjhyUWpsWGFGbEJNMVZTVVM5alFXdFhURUZRYzNWb1JXOXRjbG8yZDBsVVFVWm5TMHBaU0dveGIzRlJOVWg0UVhSdVRrMDVVMFV6UmxRek1HUkZkRkpGYlhsalEwOVhVVE5JUzFSTmJITkxlQ3RIU25NMFV6aHNjakJaZVVkcWNUZ3lXVkpNUWtSaFJWZFZSamhQV2k5cVNVd3dXbVZaVjJWd01YUnlWMDFJZFVoSE5USkNSVlZtWVhKdFYxbEZUMlpMUzJVeWIzSklOSHBMVEV4dVUwMXFUMGc1YTBwVGJIUXdjeXMwTm5sUVJYQmxhRmhIWm1sMFVEZEdjRkJuUkRsTlRXZFlZMkV5V1hSdGFuUkZhVzFRZUZjeFZTdG9VMDFFUjJVM1NXa3JTMDlCYlRWQlJFbFhiRVl4TlN0elR5OHphWFo2TlVFM1FtNHlTRkZGZEc5S2JXaFFWblkzVlRaamN6aEhNMGd2TWxsVGVFaFpZMDFtTkZadlduQlpWMlkzVDBOUlV6Z3lVVWRzY0RCVGIzQm5OM0V2T0daRVFVMDNlVmhSTmsxeFR6Wk5UVU41YkhsM1IzRkdOWEJVUlhWV1VGTlVVRlZrY1VWaVpYaEVZbE4zUlZjd1R6Rk5WVGhyWkRWbk1FbGpWWFZFZUVaVmFWUTBkVkJ0Uldod2JtVjFUbkozVDJWWGJuZERiRWhEVmpaMlNHc3hTaTk0SzBkV01ESjNVMFZqZGxwRWIybzVVVEJUWm5kWmJVNTJValp0YlVNelNUUkZNbUpKYnpWUGEyRjZUWEF4TjBVdlNubHRiMVJFZDJWSWVuWjRSV1k1VWpBNFVFNDBMMUZJVEhNM1YwUXhNbVF4SzNsUE9HazVURk5VTkZVMlZYSmhhMmh3TjI1cEwzUjZObXdyWWs4eFEwNDBZMUZSV2xaWE5YUkhTalZDZFhGS05sSkZjVXg1WkdkNlREbDFNREJ6U1RaV1NHcFVOVUpMY1RkdVNUQlZURXBqVFVSMGRVNWhPQzlrWmpKNE5WTTJVR1IwTm1GUU5qZFNWVEEzTVdoUlpEZEZObGRRWm5NeFJXbGhVMHM0V1ZOV2VWSXZlR2x3Um10MFNuTjZjbG8xTVU5TFp6Rk9OVGhRTURjNGNtb3ZVSGRwZEUxeVZUQnZOWGc0V0dKWmVtNW9ORnA0VEZCUVVXSm5hRGcwY0hGMVJTdE1VMlZGWjJoaGFVWmhhMHN3Ymt0TVVFNUJURGhuVGpsdll6WTRaa05yTWpoSmFuSkhaVWRQUkVWM2VreGxNMGd3UzB0TlZFSkdZMFEySzI1T01sZ3JURWh2UzJWeU9XRkNVelZtVXpReGVVMTNZWHBsVDNKVWMwWnBLek4xVWpaaFMzWXdTUzl3Y0dKMFZsZFZkRmhCUVhNMWNUTkxUWGxQWlVwMGQyaFRkakYyZEhaUVdtcGtlbVJvUTFKcmFWWjNSMk5RWkUwcmRXdENXa1pNVVRBck5sb3diM1J2VDJWcGIwb3hTMFZDY21wWk1qUkxNVVZwYjFOS2MxUnBOa3BNVTBNNFJIQlhNRk42YlZGMmFVTnZTbHBhUTJaSVQyUkhhRkZUT0ZZek9WUjNjVnBFWWpWblJHNVBTazExV2twRWNXRjJaVTFPUzB3eWRYbFBVbEExVEdGNWFreFVRa3BwUVc4d2RERm5ZbTh4TUUxSGVscE9hV3RXZW1sbWNsSkRRek13V1RoVUwxUXlXbGdyYkV0MlFUbFNOV2xXU3cubHpKNjlhR0xWN2lGSFZIZFo5Z05nNmxpUllSSmh2eWpfd0k5a2tWNEVId05DaGFnUmpacHdVZmZrd29pYmlxcUdUbjRLNHpaVGc5UVRmYVMyZThobEE=
#
username = 'username'
password = 'password'

encrypted_password = ctx.call('encrypt_password', password)
# print(encrypted_password)
data = {
    'username': username,
    'password': encrypted_password,
    'authcode': result,
    'execution': execution,
    'encrypted': 'true',
    '_eventId': 'submit',
    'loginType': '1',
    'submit': '登 录',
}

# 登录请求 - 使用session，并允许重定向
login_response = session.post(
    'http://sso.nau.edu.cn/sso/login?service=http://ngx.nau.edu.cn/wengine-auth/login?cas_login=true',
    headers=headers,
    data=data,
)

# 如果需要手动跟踪重定向的过程
if 'Location' in login_response.headers:
    next_url = login_response.headers['Location']
    print(f"重定向到: {next_url}")
    
    # 跟踪第一次重定向
    redirect_response = session.get(next_url, headers=headers)
    
    # 如果还有更多重定向，继续跟踪
    if 'Location' in redirect_response.headers:
        next_url = redirect_response.headers['Location']
        print(f"进一步重定向到: {next_url}")
        redirect_response = session.get(next_url, headers=headers)

# 无论手动还是自动重定向，最终直接访问目标页面
final_response = session.get('http://alstu.nau.edu.cn/default.aspx', headers=headers)
print("最终页面状态码:", final_response.status_code)

# 解析最终页面内容
soup = BeautifulSoup(final_response.text, 'html.parser')

# 提取校级公告数据
print("正在提取校级公告数据...")
school_notices = []
school_notice_items = soup.select('#MyDataList_zh tr td ul li a')
for item in school_notice_items:
    href = item.get('href')
    title = item.get('title')
    full_url = f"http://alstu.nau.edu.cn/{href}"
    school_notices.append({"标题": title, "链接": full_url})

# 提取学院公告数据
print("正在提取学院公告数据...")
college_notices = []
college_notice_items = soup.select('#MyDataList_gg tr td ul li a')
for item in college_notice_items:
    href = item.get('href')
    title = item.get('title')
    full_url = f"http://alstu.nau.edu.cn/{href}"
    college_notices.append({"标题": title, "链接": full_url})

# 创建校级公告DataFrame
school_df = pd.DataFrame(school_notices)
print("\n校级公告：")
print(school_df)

# 创建学院公告DataFrame
college_df = pd.DataFrame(college_notices)
print("\n学院公告：")
print(college_df)

# 可选：保存到Excel文件
school_df.to_excel("校级公告.xlsx", index=False)
college_df.to_excel("学院公告.xlsx", index=False)
print("\n数据已保存到Excel文件")
