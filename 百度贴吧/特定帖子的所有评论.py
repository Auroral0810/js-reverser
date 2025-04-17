import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import random
import math
import html
import os
import pickle
import ast
import signal
import sys
import requests

cookies = {
    'BAIDUID': 'D7655165AC8A160FDAADE4327E8B942E:FG=1',
    'BAIDUID_BFESS': 'D7655165AC8A160FDAADE4327E8B942E:FG=1',
    'Hm_lvt_292b2e1608b0823c1cb6beef7243ef34': '1742396943,1744816776',
    'HMACCOUNT': 'DDF927EE5DF25454',
    'BAIDU_WISE_UID': 'wapp_1744869667916_527',
    'USER_JUMP': '-1',
    'video_bubble0': '1',
    'ZFY': 'bUGIEG4sK0R6gP4ojZbPri886J0wvfhS:B6BdB1xUMmA:C',
    'st_key_id': '17',
    'arialoadData': 'false',
    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqNvjLowygVbK9xeY8tvcT1iO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
    'tb_as_data': '3b670d9989e15819550f7ed3678acdb0dc06360c51d2a06cc77fb3928a8a30577379583f90a92cbdc8078b63434a84fa2672c6dbc4ba70ae95def017b01f3c0c571a0c55e1ee2e49de3deb4b9ad357578b0abb5f5e26afe38b4581669ac5b094b951382c9ba882f41183a18d3b787b1b',
    'Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34': '1744870424',
    'XFI': '1e3a7b30-1b53-11f0-8a48-01e571e1a976',
    'BA_HECTOR': '8gak8h20250la42504ah2521808ga41k0170p24',
    'ab_sr': '1.0.1_ZjViMjYyMDVhYzVlNDdlOTYxYTY2NjM3NmE0N2FkOTIxNGMzNzM2OGYyYWQxYzc1NThjMjNlZDkzY2E3NjM5YmJmZTMzYjRhZGNjYWU0NmNmZmIyYjliNTMyZDM0ZWQxY2Y4MWNlMmNiYzQwYTAzMGVlOTYzZGI3ZmExZDQ5OGVhNDU2MDk0MjNjMzViZmNhOWI2NDgzZWM4ZWQ2MjQzMg==',
    'st_data': '1b7959726d026e47f7da96ee99c5461dcbc589b982a914604572941e17b8ead76378b920eaf5b94a7677f8d63ef7fa841730270a32190269917d39a1ac92b8019485573c25c1f1937ec295362cdb8aac205be5e8c6d2a1013712886890475bb287b8ebd799cf5c59aa02bc1c5f1800e75f4d385d7e2c3b676337462b9d4ec4d4863be2f793572d84bcfb141cbfc47304',
    'st_sign': '32000195',
    'XFCS': '0C8565CC901470E2144C5EDDDE027807F4D6F052B7C29F3CD05D4227DC11CA87',
    'XFT': 'ysvgJcsPCqlDsMItQUGz4V7yh3jlq+aZ4nDpLJjTMhs=',
    'RT': '"z=1&dm=baidu.com&si=f13b43ce-40e1-4fd7-98ea-b0ac26650c14&ss=m9k7vgwi&sl=3g&tt=53ti&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=qxein&ul=qz7pw"',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://wappass.baidu.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'BAIDUID=D7655165AC8A160FDAADE4327E8B942E:FG=1; BAIDUID_BFESS=D7655165AC8A160FDAADE4327E8B942E:FG=1; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1742396943,1744816776; HMACCOUNT=DDF927EE5DF25454; BAIDU_WISE_UID=wapp_1744869667916_527; USER_JUMP=-1; video_bubble0=1; ZFY=bUGIEG4sK0R6gP4ojZbPri886J0wvfhS:B6BdB1xUMmA:C; st_key_id=17; arialoadData=false; ppfuid=FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqNvjLowygVbK9xeY8tvcT1iO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP; tb_as_data=3b670d9989e15819550f7ed3678acdb0dc06360c51d2a06cc77fb3928a8a30577379583f90a92cbdc8078b63434a84fa2672c6dbc4ba70ae95def017b01f3c0c571a0c55e1ee2e49de3deb4b9ad357578b0abb5f5e26afe38b4581669ac5b094b951382c9ba882f41183a18d3b787b1b; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1744870424; XFI=1e3a7b30-1b53-11f0-8a48-01e571e1a976; BA_HECTOR=8gak8h20250la42504ah2521808ga41k0170p24; ab_sr=1.0.1_ZjViMjYyMDVhYzVlNDdlOTYxYTY2NjM3NmE0N2FkOTIxNGMzNzM2OGYyYWQxYzc1NThjMjNlZDkzY2E3NjM5YmJmZTMzYjRhZGNjYWU0NmNmZmIyYjliNTMyZDM0ZWQxY2Y4MWNlMmNiYzQwYTAzMGVlOTYzZGI3ZmExZDQ5OGVhNDU2MDk0MjNjMzViZmNhOWI2NDgzZWM4ZWQ2MjQzMg==; st_data=1b7959726d026e47f7da96ee99c5461dcbc589b982a914604572941e17b8ead76378b920eaf5b94a7677f8d63ef7fa841730270a32190269917d39a1ac92b8019485573c25c1f1937ec295362cdb8aac205be5e8c6d2a1013712886890475bb287b8ebd799cf5c59aa02bc1c5f1800e75f4d385d7e2c3b676337462b9d4ec4d4863be2f793572d84bcfb141cbfc47304; st_sign=32000195; XFCS=0C8565CC901470E2144C5EDDDE027807F4D6F052B7C29F3CD05D4227DC11CA87; XFT=ysvgJcsPCqlDsMItQUGz4V7yh3jlq+aZ4nDpLJjTMhs=; RT="z=1&dm=baidu.com&si=f13b43ce-40e1-4fd7-98ea-b0ac26650c14&ss=m9k7vgwi&sl=3g&tt=53ti&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=qxein&ul=qz7pw"',
}
# 全局变量用于保存当前爬取状态，方便在程序退出时保存
current_post_id = None
current_page = None
all_posts_comments = {}
completed_posts = []
excel_file = None
csv_file = "孙笑川吧_所有评论回复.csv"

# 修改全局变量声明部分，添加可以动态更新的凭证
global_cookies = cookies.copy()  # 创建全局可更新的cookies
global_headers = headers.copy()  # 创建全局可更新的headers

# 信号处理函数，处理Ctrl+C等中断信号
def signal_handler(sig, frame):
    print("\n捕获到中断信号，正在保存已爬取的数据...")
    
    # 保存当前进度
    if current_post_id and current_page:
        save_progress(completed_posts, current_post_id, current_page, excel_file)
    
    # 保存已爬取的数据
    if all_posts_comments:
        save_comments_to_csv_all(all_posts_comments, csv_file)
        print(f"已保存所有爬取的数据到: {csv_file}")
    
    print("程序已安全退出")
    sys.exit(0)

# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)  # 处理Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # 处理终止信号

def update_credentials():
    """让用户输入新的cookie和header"""
    global global_cookies, global_headers  # 声明使用全局变量
    
    print("\n" + "="*50)
    print("请选择输入方式:")
    print("1. 直接输入")
    print("2. 从文件读取")
    print("3. 使用默认值")
    print("="*50 + "\n")
    
    while True:  # 循环直到成功获取有效凭证
        input_method = input("请选择输入方式 (1/2/3): ").strip()
        
        if input_method == "2":
            # 从文件读取
            cookie_file = input("请输入Cookie文件路径 (cookie.txt): ") or "cookie.txt"
            header_file = input("请输入Header文件路径 (headers.txt): ") or "headers.txt"
            
            # 尝试读取Cookie文件
            cookie_success = False
            try:
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookies_str = f.read().strip()
                    # 处理带有变量赋值的文件格式
                    if cookies_str.startswith('cookies = '):
                        # 提取字典部分
                        dict_part = cookies_str[cookies_str.find('{'):].strip()
                        # 确保字典完整闭合
                        if dict_part.count('{') == dict_part.count('}'):
                            try:
                                # 尝试解析字典部分
                                new_cookies = ast.literal_eval(dict_part)
                                if isinstance(new_cookies, dict):
                                    print("已成功从文件读取Cookie")
                                    # 打印部分Cookie内容以便确认
                                    cookie_keys = list(new_cookies.keys())[:3]  # 获取前3个键
                                    print(f"Cookie包含键: {cookie_keys}...")
                                    cookie_success = True
                                    # 更新全局cookie
                                    global_cookies = new_cookies
                                else:
                                    print("Cookie文件内容不是有效的字典格式")
                            except Exception as e:
                                print(f"解析Cookie字典出错: {str(e)}")
                        else:
                            print("Cookie文件中的字典格式不完整")
                    else:
                        # 尝试直接解析整个文件内容
                        try:
                            new_cookies = ast.literal_eval(cookies_str)
                            if not isinstance(new_cookies, dict):
                                print("Cookie文件格式错误")
                            else:
                                print("已成功从文件读取Cookie")
                                # 打印部分Cookie内容以便确认
                                cookie_keys = list(new_cookies.keys())[:3]  # 获取前3个键
                                print(f"Cookie包含键: {cookie_keys}...")
                                cookie_success = True
                                # 更新全局cookie
                                global_cookies = new_cookies
                        except Exception as e:
                            print(f"解析Cookie文件出错: {str(e)}")
            except Exception as e:
                print(f"读取Cookie文件出错: {str(e)}")
                
            # 如果Cookie读取失败，提示用户重新选择
            if not cookie_success:
                print("Cookie文件读取失败，请重新选择输入方式")
                continue
                
            # 尝试读取Header文件
            header_success = False
            try:
                with open(header_file, 'r', encoding='utf-8') as f:
                    headers_str = f.read().strip()
                    # 处理带有变量赋值的文件格式
                    if headers_str.startswith('headers = '):
                        # 提取字典部分
                        dict_start = headers_str.find('{')
                        if dict_start != -1:
                            dict_part = headers_str[dict_start:].strip()
                            # 找到最后一个右花括号
                            dict_end = dict_part.rfind('}')
                            if dict_end != -1:
                                dict_part = dict_part[:dict_end+1]
                                try:
                                    # 尝试解析字典部分
                                    new_headers = ast.literal_eval(dict_part)
                                    if isinstance(new_headers, dict):
                                        print("已成功从文件读取Header")
                                        # 打印部分Header内容以便确认
                                        header_keys = list(new_headers.keys())[:3]  # 获取前3个键
                                        print(f"Header包含键: {header_keys}...")
                                        header_success = True
                                        # 更新全局header
                                        global_headers = new_headers
                                    else:
                                        print("Header文件内容不是有效的字典格式")
                                except Exception as e:
                                    print(f"解析Header字典出错: {str(e)}")
                            else:
                                print("Header文件中的字典格式不完整")
                        else:
                            print("Header文件中找不到字典开始符号")
                    else:
                        # 尝试直接解析整个文件内容
                        try:
                            new_headers = ast.literal_eval(headers_str)
                            if not isinstance(new_headers, dict):
                                print("Header文件格式错误")
                            else:
                                print("已成功从文件读取Header")
                                # 打印部分Header内容以便确认
                                header_keys = list(new_headers.keys())[:3]  # 获取前3个键
                                print(f"Header包含键: {header_keys}...")
                                header_success = True
                                # 更新全局header
                                global_headers = new_headers
                        except Exception as e:
                            print(f"解析Header文件出错: {str(e)}")
            except Exception as e:
                print(f"读取Header文件出错: {str(e)}")
                
            # 如果Header读取失败，提示用户重新选择
            if not header_success:
                print("Header文件读取失败，请重新选择输入方式")
                continue
            
            # 两个文件都读取成功，返回结果
            if cookie_success and header_success:
                # 进行简单测试
                print("正在测试新凭证是否有效...")
                test_url = "https://tieba.baidu.com/f?kw=孙笑川"
                try:
                    # 打印请求细节
                    print(f"测试请求使用的Cookie内容示例: {str(global_cookies)[:100]}...")
                    test_response = requests.get(test_url, cookies=global_cookies, headers=global_headers, timeout=5)
                    if test_response.status_code == 200:
                        print(f"凭证测试成功! 状态码: {test_response.status_code}")
                        
                        # 额外测试：检查是否包含需要登录的提示
                        if "请先登录" in test_response.text or "登录百度帐号" in test_response.text:
                            print("警告: 虽然状态码为200，但可能未正确登录，检测到登录提示")
                        else:
                            print("登录状态验证通过，未检测到登录提示")
                    else:
                        print(f"凭证测试返回非成功状态码: {test_response.status_code}")
                except Exception as e:
                    print(f"测试凭证时出错: {str(e)}")
                
                # 返回全局更新后的凭证
                return global_cookies, global_headers
                
        elif input_method == "3":
            # 使用默认值
            print("使用默认Cookie和Header值")
            global_cookies = cookies.copy()
            global_headers = headers.copy()
            return global_cookies, global_headers
            
        elif input_method == "1":
            # 直接输入
            try:
                cookies_input = input("请输入新的Cookie字典 (或直接按Enter使用默认值): ")
                if cookies_input.strip():
                    # 使用ast.literal_eval安全地解析字符串为Python对象
                    new_cookies = ast.literal_eval(cookies_input)
                    if not isinstance(new_cookies, dict):
                        print("输入格式错误，请输入有效的字典格式")
                        continue
                    else:
                        global_cookies = new_cookies
                        print("已成功设置新的Cookie")
                else:
                    print("使用默认Cookie值")
                    global_cookies = cookies.copy()
                
                headers_input = input("请输入新的Header字典 (或直接按Enter使用默认值): ")
                if headers_input.strip():
                    # 使用ast.literal_eval安全地解析字符串为Python对象
                    new_headers = ast.literal_eval(headers_input)
                    if not isinstance(new_headers, dict):
                        print("输入格式错误，请输入有效的字典格式")
                        continue
                    else:
                        global_headers = new_headers
                        print("已成功设置新的Header")
                else:
                    print("使用默认Header值")
                    global_headers = headers.copy()
                
                return global_cookies, global_headers
            except Exception as e:
                print(f"解析输入时出错: {str(e)}，请重新输入")
        else:
            print("无效的选择，请重新输入")

# 将保存CSV的函数分成两部分，一个用于实时追加，一个用于全量保存
def save_comments_to_csv(comments, post_id, csv_file="孙笑川吧_所有评论回复.csv"):
    """将单个帖子的评论和回复保存到CSV文件，使用追加模式"""
    all_data = []
    
    for comment in comments:
        # 添加主评论
        comment_row = {
            "帖子ID": post_id,
            "内容类型": "主评论",
            "ID": comment["评论ID"],
            "父评论ID": "",  # 主评论没有父评论
            "楼层": comment["楼层"],
            "用户名": comment["用户名"],
            "昵称": comment["昵称"],
            "内容": comment["评论内容"],
            "图片": ', '.join(comment["评论图片"]) if comment["评论图片"] else "",
            "发布时间": comment["评论时间"],
            "回复数量": comment["回复数量"]
        }
        all_data.append(comment_row)
        
        # 添加该评论下的所有回复
        for reply in comment["回复"]:
            reply_row = {
                "帖子ID": post_id,
                "内容类型": "回复",
                "ID": reply.get("回复ID", ""),
                "父评论ID": comment["评论ID"],
                "楼层": f"{comment['楼层']}的回复",
                "用户名": reply.get("用户名", ""),
                "昵称": reply["页面显示名"],
                "内容": reply["回复内容"],
                "图片": ', '.join(reply["回复图片"]) if reply["回复图片"] else "",
                "发布时间": reply["回复时间"],
                "回复数量": ""  # 回复没有下级回复数量
            }
            all_data.append(reply_row)
    
    # 转换为DataFrame
    df = pd.DataFrame(all_data)
    
    # 检查文件是否存在，决定是否需要写入表头
    file_exists = os.path.isfile(csv_file)
    
    # 以追加模式写入CSV文件
    if file_exists:
        df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
        print(f"数据已追加到 {csv_file}")
    else:
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"创建新文件 {csv_file} 并写入数据")
    
    return len(all_data)

def save_comments_to_csv_all(all_posts_comments, csv_file="孙笑川吧_所有评论回复.csv"):
    """将所有帖子的评论和回复保存到一个CSV文件中（覆盖模式）"""
    all_data = []
    
    for post_id, comments in all_posts_comments.items():
        for comment in comments:
            # 添加主评论
            comment_row = {
                "帖子ID": post_id,
                "内容类型": "主评论",
                "ID": comment["评论ID"],
                "父评论ID": "",  # 主评论没有父评论
                "楼层": comment["楼层"],
                "用户名": comment["用户名"],
                "昵称": comment["昵称"],
                "内容": comment["评论内容"],
                "图片": ', '.join(comment["评论图片"]) if comment["评论图片"] else "",
                "发布时间": comment["评论时间"],
                "回复数量": comment["回复数量"]
            }
            all_data.append(comment_row)
            
            # 添加该评论下的所有回复
            for reply in comment["回复"]:
                reply_row = {
                    "帖子ID": post_id,
                    "内容类型": "回复",
                    "ID": reply.get("回复ID", ""),
                    "父评论ID": comment["评论ID"],
                    "楼层": f"{comment['楼层']}的回复",
                    "用户名": reply.get("用户名", ""),
                    "昵称": reply["页面显示名"],
                    "内容": reply["回复内容"],
                    "图片": ', '.join(reply["回复图片"]) if reply["回复图片"] else "",
                    "发布时间": reply["回复时间"],
                    "回复数量": ""  # 回复没有下级回复数量
                }
                all_data.append(reply_row)
    
    # 如果数据为空，返回
    if not all_data:
        print("没有数据需要保存")
        return 0
        
    # 转换为DataFrame
    df = pd.DataFrame(all_data)
    
    # 保存到CSV文件
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"所有数据已保存到 {csv_file}")
    
    return len(all_data)

def get_comment_replies(thread_id, post_id, total_reply_count, cookies, headers):
    """通过评论URL获取回复数据，支持分页爬取所有回复"""
    global global_cookies, global_headers  # 使用全局最新凭证
    
    print(f"开始获取评论 {post_id} 的回复数据...")
    all_replies = []
    
    # 使用传入的cookie和header，这些应该是update_credentials更新后的值
    current_cookies = cookies
    current_headers = headers
    
    # 计算总页数（每页10条回复）
    total_pages = math.ceil(total_reply_count / 10)
    print(f"评论回复总数: {total_reply_count}, 总页数: {total_pages}")
    
    # 遍历每一页获取回复
    consecutive_failures = 0  # 连续失败计数
    
    for page in range(1, total_pages + 1):
        # 构建评论URL，加入页码参数
        comment_url = f"https://tieba.baidu.com/p/comment?tid={thread_id}&pid={post_id}&pn={page}"
        
        try:
            response = requests.get(comment_url, headers=current_headers, cookies=current_cookies)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"请求第 {page} 页失败，状态码: {response.status_code}")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print(f"连续 {consecutive_failures} 次请求失败，可能需要更新Cookie或Header")
                    return all_replies, True  # 返回中断标志
                continue
                
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有回复项
            reply_items = soup.select('li.lzl_single_post')
            if not reply_items:
                print(f"第 {page} 页没有找到回复")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print(f"连续 {consecutive_failures} 次请求无数据，可能需要更新Cookie或Header")
                    return all_replies, True  # 返回中断标志
                continue
            
            # 成功找到数据，重置失败计数
            consecutive_failures = 0
                
            print(f"第 {page} 页找到 {len(reply_items)} 个回复")
            
            # 提取当前页的回复
            for reply_item in reply_items:
                reply_info = extract_reply_info(reply_item, post_id)
                if reply_info:
                    all_replies.append(reply_info)
            
            # 添加短暂延迟避免请求过快
            if page < total_pages:
                time.sleep(0.5 + random.random())  # 随机延迟0.5-1.5秒
            
        except Exception as e:
            print(f"获取第 {page} 页回复时出错: {str(e)}")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print(f"连续 {consecutive_failures} 次请求失败，可能需要更新Cookie或Header")
                return all_replies, True  # 返回中断标志
    
    print(f"评论 {post_id} 共获取到 {len(all_replies)} 个回复")
    return all_replies, False  # 返回正常完成标志

def continue_crawling(post_ids, start_page, completed_posts, excel_file, current_cookies, current_headers, csv_file="孙笑川吧_所有评论回复.csv"):
    """从指定位置继续爬取"""
    global current_post_id, current_page, all_posts_comments, global_cookies, global_headers
    
    # 使用函数开始时传入的最新全局凭证，确保接收到新更新的值
    current_cookies = global_cookies
    current_headers = global_headers
    
    # 顺序爬取每个帖子的评论和回复
    post_counter = 0  # 帖子计数器
    total_records = 0  # 记录总数
    global_consecutive_failures = 0  # 全局连续失败计数器
    
    # 确保从当前帖子开始，而不是跳过
    current_post_index = 0
    for i, post_id in enumerate(post_ids):
        # 如果帖子已经完成，跳过
        if post_id in completed_posts:
            continue
            
        current_post_index = i
        break  # 找到第一个未完成的帖子
    
    i = current_post_index
    while i < len(post_ids):
        post_id = post_ids[i]
        
        # 再次检查是否已完成，以防万一
        if post_id in completed_posts:
            i += 1
            continue
        
        # 更新全局状态
        current_post_id = post_id
        current_page = start_page if i == current_post_index else 1
            
        print(f"正在爬取第 {i+1}/{len(post_ids)} 个帖子 (ID: {post_id})...")
        
        while True:  # 添加一个无限循环，允许用户在失败时选择继续尝试
            try:
                # 使用最新的全局凭证
                print(f"请求使用的Cookie: {str(global_cookies)[:50]}...")
                
                # 获取该帖子的所有评论和回复，从指定页开始
                comments, interrupted, next_page = get_post_comments(post_id, current_page, global_cookies, global_headers)
                
                # 更新全局状态
                current_page = next_page
                
                # 检查是否需要立即中断（连续多个帖子失败）
                if not comments or interrupted:
                    global_consecutive_failures += 1
                    print(f"帖子 {post_id} 爬取失败，这是全局连续第 {global_consecutive_failures} 次失败")
                    
                    # 如果连续失败，则提示用户更新凭证
                    if global_consecutive_failures >= 1:  # 这里设置为1，表示任何失败都会触发更新
                        print(f"连续 {global_consecutive_failures} 个帖子都失败，需要更新Cookie和Header")
                        
                        # 保存当前爬取进度，但不将当前帖子标记为已完成
                        save_progress(completed_posts, post_id, next_page, excel_file)
                        
                        # 提示用户选择更新凭证或退出或跳过
                        print("\n请选择操作:")
                        print("1. 更新Cookie和Header并重试")
                        print("2. 保存进度并退出")
                        print("3. 跳过当前帖子")
                        choice = input("请选择 (1/2/3): ").strip()
                        
                        if choice == "2":
                            # 保存已爬取的数据
                            if all_posts_comments:
                                save_comments_to_csv_all(all_posts_comments, csv_file)
                                print(f"部分爬取的数据已保存到：{csv_file}")
                            
                            print(f"总共爬取了 {len(completed_posts)} 个帖子，{total_records} 条记录")
                            return
                        elif choice == "3":
                            # 用户选择跳过当前帖子
                            print(f"跳过帖子 {post_id}")
                            # 标记为已完成（虽然是跳过的）
                            completed_posts.append(post_id)
                            # 重置失败计数
                            global_consecutive_failures = 0
                            # 跳出当前帖子的循环，处理下一个帖子
                            i += 1
                            break
                        
                        # 用户选择继续，更新凭证
                        global_cookies, global_headers = update_credentials()
                        # 更新当前使用的凭证
                        current_cookies = global_cookies
                        current_headers = global_headers
                        
                        # 重置失败计数器
                        global_consecutive_failures = 0
                        
                        # 不退出循环，继续尝试爬取当前帖子
                        continue
                
                # 如果成功获取评论或没有达到中断阈值，跳出循环继续处理下一个帖子
                break
                
            except Exception as e:
                print(f"爬取帖子 {post_id} 时出错: {str(e)}")
                # 增加全局连续失败计数
                global_consecutive_failures += 1
                # 保存当前进度，但不将当前帖子标记为已完成
                save_progress(completed_posts, post_id, current_page, excel_file)
                
                # 提示用户选择是继续尝试还是退出或跳过
                print("\n请选择操作:")
                print("1. 更新Cookie和Header并重试")
                print("2. 保存进度并退出")
                print("3. 跳过当前帖子")
                choice = input("请选择 (1/2/3): ").strip()
                
                if choice == "2":
                    # 保存已爬取的数据
                    if all_posts_comments:
                        save_comments_to_csv_all(all_posts_comments, csv_file)
                        print(f"部分爬取的数据已保存到：{csv_file}")
                    
                    print(f"总共爬取了 {len(completed_posts)} 个帖子，{total_records} 条记录")
                    return
                elif choice == "3":
                    # 用户选择跳过当前帖子
                    print(f"跳过帖子 {post_id}")
                    # 标记为已完成（虽然是跳过的）
                    completed_posts.append(post_id)
                    # 重置失败计数
                    global_consecutive_failures = 0
                    # 跳出当前帖子的循环，处理下一个帖子
                    i += 1
                    break
                
                # 用户选择继续，更新凭证
                global_cookies, global_headers = update_credentials()
                # 更新当前使用的凭证
                current_cookies = global_cookies
                current_headers = global_headers
                global_consecutive_failures = 0
                
                # 不退出循环，继续尝试爬取当前帖子
                continue
        
        # 如果是通过跳过操作进入这里，继续下一个循环
        if i >= len(post_ids):
            break
            
        # 爬取成功，保存帖子数据到CSV
        if comments:
            # 添加到全局数据存储
            all_posts_comments[post_id] = comments
            
            # 实时保存到CSV
            records_added = save_comments_to_csv(comments, post_id, csv_file)
            total_records += records_added
            
            # 只有在成功爬取完成后，才将帖子添加到已完成列表
            if post_id not in completed_posts:  # 避免重复添加
                completed_posts.append(post_id)
            
            print(f"帖子 {post_id} 共找到 {len(comments)} 个主评论")
            
            # 统计回复总数
            total_replies = sum(comment["回复数量"] for comment in comments)
            print(f"帖子 {post_id} 共找到 {total_replies} 个回复")
        else:
            print(f"帖子 {post_id} 没有评论数据")
            # 若评论列表为空但没有中断，依然把它标记为已完成
            if post_id not in completed_posts:  # 避免重复添加
                completed_posts.append(post_id)
        
        # 帖子计数器增加
        post_counter += 1
        
        # 每爬取5个帖子后或最后一个帖子，保存进度
        if post_counter % 5 == 0 or i == len(post_ids) - 1:
            # 保存进度
            save_progress(completed_posts, post_ids[min(i+1, len(post_ids)-1)], 1, excel_file)
            print(f"已保存进度，当前已爬取 {len(completed_posts)} 个帖子，{total_records} 条记录")
            
        # 普通帖子间的延迟
        if i < len(post_ids) - 1:
            delay_time = 1 + random.random()  # 1-2秒随机延迟
            print(f"等待 {delay_time:.2f} 秒后继续爬取下一个帖子...")
            time.sleep(delay_time)
            
        # 移动到下一个帖子
        i += 1
    
    print(f"所有帖子爬取完成！总共爬取了 {len(completed_posts)} 个帖子，{total_records} 条记录")
    print(f"所有数据已保存到: {csv_file}")
    
    # 爬取完成，删除进度文件
    if os.path.exists('tieba_crawler_progress.pkl'):
        os.remove('tieba_crawler_progress.pkl')
        print("爬取完成，进度文件已删除")

def load_progress():
    """加载保存的爬取进度"""
    try:
        with open('tieba_crawler_progress.pkl', 'rb') as f:
            progress = pickle.load(f)
        
        print(f"找到保存的进度: 已完成 {len(progress['completed_posts'])} 个帖子")
        print(f"上次中断于: 帖子 {progress['current_post_id']} 的第 {progress['current_page']} 页")
        print(f"保存时间: {progress.get('timestamp', '未知')}")
        
        return progress
    except FileNotFoundError:
        print("没有找到保存的进度文件，将从头开始爬取")
        return None
    except Exception as e:
        print(f"加载进度文件时出错: {str(e)}，将从头开始爬取")
        return None

def save_progress(completed_posts, current_post_id, current_page, excel_file):
    """保存当前爬取进度"""
    progress = {
        'completed_posts': completed_posts,
        'current_post_id': current_post_id,
        'current_page': current_page,
        'excel_file': excel_file,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('tieba_crawler_progress.pkl', 'wb') as f:
        pickle.dump(progress, f)
    
    print(f"进度已保存: 已完成 {len(completed_posts)} 个帖子，当前正在处理帖子 {current_post_id} 的第 {current_page} 页")
    return progress

def extract_reply_info(reply_item, parent_comment_id, is_hidden=False):
    """从回复li元素中提取回复信息"""
    try:
        # 提取data-field属性数据
        data_field = reply_item.get('data-field', '{}')
        try:
            # 处理单引号JSON问题
            data_field = data_field.replace("'", '"')
            field_data = json.loads(data_field)
            pid = field_data.get('pid', '')
            spid = field_data.get('spid', '')
            user_name = field_data.get('user_name', '')
            portrait = field_data.get('portrait', '')
            showname = field_data.get('showname', '')
            user_nickname = field_data.get('user_nickname', '')
        except Exception as e:
            print(f"解析回复data-field出错: {str(e)}, 原数据: {data_field}")
            pid = parent_comment_id
            spid = ""
            user_name = portrait = showname = user_nickname = "未知"
        
        # 提取回复用户
        user_elem = reply_item.select_one('a.at.j_user_card')
        username_display = user_elem.get_text().strip() if user_elem else showname or user_nickname or user_name or "未知用户"
        
        # 提取回复内容
        content_elem = reply_item.select_one('span.lzl_content_main')
        content = content_elem.get_text().strip() if content_elem else ""
        
        # 提取回复中的图片
        images = []
        img_tags = content_elem.select('img') if content_elem else []
        for img in img_tags:
            src = img.get('src', '')
            if src and not src.startswith('http'):
                src = 'https:' + src if src.startswith('//') else src
            if src and 'BDE_Smiley' not in src:  # 排除表情图片
                images.append(src)
        
        # 提取回复时间
        time_elem = reply_item.select_one('span.lzl_time')
        reply_time = time_elem.get_text().strip() if time_elem else ""
        
        # 返回完整的回复信息
        return {
            "回复ID": spid,
            "父评论ID": pid,
            "用户名": user_name,
            "用户头像ID": portrait,
            "显示名称": showname,
            "用户昵称": user_nickname,
            "页面显示名": username_display,
            "回复内容": content,
            "回复图片": images,
            "回复时间": reply_time,
            "是否隐藏回复": is_hidden
        }
    except Exception as e:
        print(f"处理回复项时出错: {str(e)}")
        return None

def get_post_comments(post_id, page_num, cookies, headers):
    """获取帖子的指定页面的评论"""
    url = f'https://tieba.baidu.com/p/{post_id}?pn={page_num}'
    print(f"开始爬取帖子 {post_id} 的第 {page_num} 页")
    
    # 显示正在使用的凭证信息
    print(f"使用的Cookie: 包含 {len(cookies)} 个键")
    print(f"使用的Header: 包含 {len(headers)} 个键")
    print(f"Cookie内容片段: {str(cookies)[:100]}...")
    
    try:
        # 确保使用最新的全局凭证
        response = requests.get(url, cookies=cookies, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        print(f"请求状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"请求页面 {page_num} 失败，状态码: {response.status_code}")
            return [], True, page_num  # 返回中断标志和当前页码
        
        html_content = response.text
        
        # 检查返回内容是否包含特定标记，确认已经登录
        login_required = False
        if "请先登录" in html_content or "登录百度帐号" in html_content:
            print("警告: 似乎没有正确登录，检测到登录提示")
            login_required = True
        
        # 检查是否有验证码或安全检查
        if "安全验证" in html_content or "验证码" in html_content:
            print("警告: 检测到安全验证或验证码，可能需要人工处理")
            
            # 保存页面内容
            debug_filename = f"security_check_{post_id}_{page_num}.html"
            with open(debug_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"已保存安全检查页面到 {debug_filename}")
            
            return [], True, page_num
        
        # 获取总页数
        total_pages = get_total_pages(html_content)
        print(f"帖子 {post_id} 总共有 {total_pages} 页")
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 先尝试检查页面是否有可能的错误提示
        error_msg = soup.select_one('.error_text')
        if error_msg:
            error_text = error_msg.get_text().strip()
            print(f"页面显示错误: {error_text}")
            
            # 检查是否是帖子不存在
            if "帖子不存在" in error_text:
                print("帖子可能已被删除或不存在")
                return [], False, page_num  # 不需要更新凭证，只是帖子不存在
                
            return [], True, page_num
        
        # 尝试不同的选择器来查找评论区
        comment_area = None
        selectors = [
            '#pb_content', 
            '#j_p_postlist',
            '.p_postlist',
            '.l_posts',
            '.thread_list',
            '.thread-list',
            '.core_title'
        ]
        
        for selector in selectors:
            try:
                area = soup.select_one(selector)
                if area:
                    print(f"找到可能的评论区: {selector}")
                    comment_area = area
                    break
            except Exception:
                continue
        
        if not comment_area:
            print(f"页面 {page_num} 找不到评论区，请检查页面结构或选择器")
            
            # 保存页面内容以便调试
            debug_filename = f"debug_page_{post_id}_{page_num}.html"
            with open(debug_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"已保存页面内容到 {debug_filename} 以便调试")
            
            # 如果需要登录，标记为需要更新凭证
            if login_required:
                print("检测到需要登录，请更新凭证")
                return [], True, page_num
                
            # 尝试查看页面是否有其他内容
            page_title = soup.select_one('title')
            if page_title:
                print(f"页面标题: {page_title.get_text().strip()}")
            
            # 如果找不到评论区但页面正常，可能是页面结构变化
            return [], True, page_num  # 返回中断标志和当前页码
        
        # 尝试不同的选择器查找评论块
        comment_blocks = []
        block_selectors = [
            'div.l_post.l_post_bright',
            '.l_post',
            '.j_l_post',
            '.post_item',
            '.thread_item'
        ]
        
        for selector in block_selectors:
            blocks = comment_area.select(selector)
            if blocks:
                comment_blocks = blocks
                print(f"使用选择器 '{selector}' 找到 {len(blocks)} 个评论块")
                break
        
        if len(comment_blocks) == 0:
            # 没找到评论块，可能是页面结构变了或权限问题
            print("没有找到评论块，可能需要更新凭证或调整选择器")
            return [], True, page_num  # 返回中断标志和当前页码
        
        # 其余代码保持不变...
        all_comments = []
        for i, block in enumerate(comment_blocks):
            try:
                # 获取data-field属性并解析
                data_field = block.get('data-field', '{}')
                try:
                    # 处理引号问题，确保JSON格式正确
                    data_field = data_field.replace("&quot;", '"')
                    data_obj = json.loads(data_field)
                    
                    # 提取评论ID和帖子ID
                    content_data = data_obj.get('content', {})
                    comment_id = str(content_data.get('post_id', f"comment_{i}"))
                    thread_id = str(content_data.get('thread_id', post_id))
                    comment_no = content_data.get('post_no', i+1)
                    comment_num = content_data.get('comment_num', 0)  # 回复数量
                    
                    # 提取作者信息
                    author_data = data_obj.get('author', {})
                    username = author_data.get('user_name', "未知用户")
                    nickname = author_data.get('user_nickname', "")
                    
                    print(f"页面 {page_num} 的评论 {i+1} - ID: {comment_id}, 帖子ID: {thread_id}, 楼层: {comment_no}, 回复数: {comment_num}")
                    
                except json.JSONDecodeError as e:
                    print(f"解析data-field出错: {str(e)}")
                    print(f"原始data-field: {data_field[:100]}...")
                    comment_id = f"comment_{i}"
                    thread_id = post_id
                    comment_no = i+1
                    comment_num = 0
                    username = "未知用户"
                    nickname = ""
                
                # 提取评论内容
                content_div = block.select_one('div.d_post_content')
                content_text = content_div.get_text().strip() if content_div else ""
                
                # 处理图片内容
                images = []
                img_tags = content_div.select('img') if content_div else []
                for img in img_tags:
                    src = img.get('src', '')
                    if src and not src.startswith('http'):
                        src = 'https:' + src if src.startswith('//') else src
                    if src:
                        images.append(src)
                
                # 提取评论时间
                comment_time_elem = block.select_one('span.tail-info:nth-last-child(2)')
                comment_time = comment_time_elem.get_text().strip() if comment_time_elem else "未知时间"
                
                # 获取评论的所有回复（跨所有回复页）
                replies = []
                if comment_num > 0:
                    replies, interrupted = get_comment_replies(thread_id, comment_id, comment_num, cookies, headers)
                    if interrupted:
                        # 回复获取中断，需要更新凭证
                        return all_comments, True, page_num
                
                # 整合评论和回复数据
                comment_data = {
                    "评论ID": comment_id,
                    "帖子ID": thread_id,
                    "用户名": username,
                    "昵称": nickname if nickname else username,
                    "评论内容": content_text,
                    "评论图片": images,
                    "评论时间": comment_time,
                    "楼层": comment_no,
                    "回复数量": len(replies),
                    "回复": replies
                }
                
                all_comments.append(comment_data)
                
            except Exception as e:
                print(f"处理页面 {page_num} 的评论块 {i} 时出错: {str(e)}")
        
        # 检查是否还有下一页
        has_next_page = page_num < total_pages
        next_page = page_num + 1 if has_next_page else page_num
        
        return all_comments, False, next_page  # 返回正常完成标志和下一页码
    except Exception as e:
        print(f"获取帖子 {post_id} 的评论时出错: {str(e)}")
        return [], True, page_num  # 返回中断标志和当前页码

def get_total_pages(html_content):
    """从帖子HTML中获取总页数"""
    try:
        # 方法1：通过正则表达式匹配 <span class="red">数字</span>
        pattern = r'<span class="red">(\d+)</span>'
        match = re.search(pattern, html_content)
        if match:
            return int(match.group(1))
        
        # 方法2：通过BeautifulSoup查找
        soup = BeautifulSoup(html_content, 'html.parser')
        page_span = soup.select_one('#thread_theme_7 > div.l_thread_info > ul > li:nth-child(2) > span:nth-child(2)')
        if page_span:
            return int(page_span.text.strip())
        
        # 方法3：尝试找到最后一页的链接
        pagination = soup.select_one('.pagination-default')
        if pagination:
            last_page_links = pagination.select('a')
            for link in reversed(last_page_links):
                if link.text.isdigit():
                    return int(link.text)
        
        # 如果以上方法都失败，检查是否只有一页
        if '下一页' not in html_content:
            return 1
        
        # 默认返回1页
        print("无法确定总页数，默认返回1页")
        return 1
        
    except Exception as e:
        print(f"获取总页数时出错: {str(e)}")
        return 1

def read_post_ids_from_excel(excel_file):
    """从Excel文件中读取帖子ID"""
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 检查是否存在帖子ID列
        if "帖子ID" in df.columns:
            # 提取帖子ID列，并转换为字符串列表
            post_ids = df["帖子ID"].astype(str).tolist()
            # 过滤空值
            post_ids = [pid for pid in post_ids if pid and pid != 'nan']
            print(f"从Excel中读取到 {len(post_ids)} 个帖子ID")
            return post_ids
        else:
            print("Excel文件中没有找到'帖子ID'列")
            return []
    except Exception as e:
        print(f"读取Excel文件出错: {str(e)}")
        return []

def generate_credential_templates():
    """生成Cookie和Header的文件模板，方便用户填写"""
    try:
        # 创建纯字典格式的cookies文件
        with open('cookie.txt', 'w', encoding='utf-8') as f:
            f.write(str(cookies))
        
        # 创建纯字典格式的headers文件
        with open('headers.txt', 'w', encoding='utf-8') as f:
            f.write(str(headers))
        
        print("已生成凭证模板文件：cookie.txt 和 headers.txt")
        print("请编辑这些文件，填入新的凭证后保存")
    except Exception as e:
        print(f"生成模板文件时出错: {str(e)}")

def main():
    global excel_file, csv_file, global_cookies, global_headers
    
    print("="*50)
    print("百度贴吧爬虫程序")
    print("1. 开始/继续爬取")
    print("2. 生成凭证模板文件")
    print("3. 退出")
    print("="*50)
    
    choice = input("请选择操作 (1/2/3): ").strip()
    
    if choice == "2":
        generate_credential_templates()
        return
    elif choice == "3":
        print("程序已退出")
        return
    
    # 在开始前就更新凭证
    print("在开始爬取前，请输入或确认您的Cookie和Header...")
    global_cookies, global_headers = update_credentials()
    print("凭证已更新，准备开始爬取")
    
    # 检查是否有保存的进度
    progress = load_progress()
    
    # 设置CSV文件名
    csv_file = "孙笑川吧_所有评论回复.csv"
    
    if progress:
        # 询问是否继续上次的爬取
        choice = input("找到保存的进度，是否继续上次的爬取? (y/n): ").strip().lower()
        if choice == 'y':
            completed_posts = progress['completed_posts']
            current_post_id = progress['current_post_id']
            current_page = progress['current_page']
            excel_file = progress['excel_file']
            
            # 读取所有帖子ID
            all_post_ids = read_post_ids_from_excel(excel_file)
            
            # 找到当前帖子在列表中的位置
            try:
                current_index = all_post_ids.index(current_post_id)
                # 从当前帖子开始爬取，而不是跳过它
                all_post_ids = all_post_ids[current_index:]
            except ValueError:
                print(f"在帖子列表中找不到ID为 {current_post_id} 的帖子，将从头开始爬取")
                completed_posts = []
                current_page = 1
            
            # 从中断处继续爬取
            for post_id in completed_posts:
                print(f"跳过已完成的帖子 {post_id}")
            
            # 继续当前被中断的帖子
            continue_crawling(all_post_ids, current_page, completed_posts, excel_file, global_cookies, global_headers, csv_file)
            return
    
    # 从头开始爬取
    excel_file = "孙笑川吧_20250417_034219.xlsx"  # 你的Excel文件名
    
    # 检查文件是否存在
    if not os.path.exists(excel_file):
        print(f"文件 {excel_file} 不存在，请检查文件路径")
        return
    
    post_ids = read_post_ids_from_excel(excel_file)
    
    if not post_ids:
        print("没有找到有效的帖子ID，程序退出")
        return
    
    # 从头开始爬取
    continue_crawling(post_ids, 1, [], excel_file, global_cookies, global_headers, csv_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n捕获到Ctrl+C，正在保存进度和数据...")
        # 保存当前进度
        if current_post_id and current_page:
            save_progress(completed_posts, current_post_id, current_page, excel_file)
        # 保存已爬取的数据
        if all_posts_comments:
            save_comments_to_csv_all(all_posts_comments, csv_file)
        print("程序已安全退出")
    except Exception as e:
        print(f"程序出现未处理的异常: {str(e)}")
        # 保存当前进度
        if current_post_id and current_page:
            save_progress(completed_posts, current_post_id, current_page, excel_file)
        # 保存已爬取的数据
        if all_posts_comments:
            save_comments_to_csv_all(all_posts_comments, csv_file)
        print("程序异常退出，但已保存进度和数据")