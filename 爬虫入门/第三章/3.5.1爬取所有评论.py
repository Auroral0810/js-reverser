import csv
import json
from base64 import b64encode
from datetime import datetime
import requests
from Cryptodome.Cipher import AES
import time
import logging
import random
import string

# ========== 配置日志记录 ==========
logging.basicConfig(
    filename='crawler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ========== 加密相关函数 ==========
def get_pub_key():
    return '010001'

def get_modulus():
    return '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'

def rsa_encrypt(text, pub_key, modulus):
    text = text[::-1]  # Reverse the text
    text = text.encode('utf-8').hex()
    text_int = int(text, 16)
    pub_key_int = int(pub_key, 16)
    modulus_int = int(modulus, 16)
    encSecKey = pow(text_int, pub_key_int, modulus_int)
    encSecKey = format(encSecKey, 'x').zfill(256)
    return encSecKey

def get_encSecKey(key2):
    pub_key = get_pub_key()
    modulus = get_modulus()
    return rsa_encrypt(key2, pub_key, modulus)

def generate_random_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

def to_16(data):
    bu_num = 16 - len(data) % 16
    data += chr(bu_num) * bu_num
    return data

def jiami(data, key):
    iv = "0102030405060708"
    new_data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(new_data.encode('utf-8'))
    return b64encode(bs).decode('utf-8')

def get_params(data, key1='0CoJUm6Qyw8W8jud'):
    """生成params和encSecKey"""
    key2 = generate_random_key()
    enc_data = jiami(data, key1)
    enc_data = jiami(enc_data, key2)
    encSecKey = get_encSecKey(key2)
    return enc_data, encSecKey

# ========== CSV 文件准备 ==========
with open("comment.csv", 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["用户ID", "用户名", "内容", "属地", "评论时间"]
    csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
    csvWriter.writeheader()

    # ========== 请求配置 ==========
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36",
        "Referer": "https://music.163.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "cookie": "_ntes_nnid=20e442659d79d6c0a6d8c7aa82074f90,1713420636872; _ntes_nuid=20e442659d79d6c0a6d8c7aa82074f90; _ga=GA1.1js 混淆_源码乱码赛.1492695192.1720416908; _clck=1b0kmll%7C2%7Cfna%7C0%7C1650; _ga_PTGVM6PCHS=GS1.1js 混淆_源码乱码赛.1720416907.1js 混淆_源码乱码赛.1js 混淆_源码乱码赛.1720416967.0.0.0; NMTID=00OwXvszvaHOwafPkKrrViMZHRN75wAAAGUTzapVQ; _iuqxldmzr_=32; WEVNSM=1js 混淆_源码乱码赛.0.0; WNMCID=dehirs.1736495770956.01.0; WM_TID=y0xndiASbUZEQURVFEOQ7ayvpzUHf0wX; WM_NI=v1Uxd6ZenIV70AgvSvUO4Hzih8gk0bciXG20H1u1fltUF%2FTuSS1l3FFcUU2qE%2BP2xL4NeKueuzH7k%2BtVpqd%2Fax6Hb4oj5fRFeh%2FZ7Pc9x0NZsQ%2FM7E2NoFhqqkl5IU%2FiUTE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb1bb62a3b7a0a2f54b988a8aa2d45e828e9e86c2428c9ce1b9f966a29998a8f62af0fea7c3b92ab6ef9b99e73e9abba2aad53df49fa997d27e9791fca9f963ace8a98cb36aa1b798a8b13c8cefbbd2e568b88b8ad0d77f918dff8db24e86bd9bb6b17b87f5a0d3fb48f892abacf86fb7a688d8ea21b88ac092e725a3a8faa9e140adb6fb87d14ea7b8e1bbb65ca1e7b8d1cd52b18fe1aeb64ff292a1a7eb7bb3b5a4d6cc5fedb79bb5c837e2a3; ntes_utid=tid._.cMhycTGA%252BAREAlBVFRaB7e3%252FszFZUrCS._.0; sDeviceId=YD-iCVIUS%2FKN7FFQwAURVaEvOm79jRIU%2BDe; __snaker__id=AK8s3TXWYoxBcwJl; gdxidpyhxdE=CpMB%2BeESW8DHDI%2FJfqRCqiBHxcxg%2Bwjh8%5CvxJ9%2B905lmwe7pUvnVoxi1pATVkI4YVBnCJc6zrXSvbvOizU9%2BtNSEJsH8hD5kMKQ0zBXWLh4mvGsKy2PmO5eJWLODOBBJUmMkfTr6D1%2B1%2FfkJBch5ihTzH%5CXQqyLGjHKqLEt3Y2IkKdA2%3A1736496686214; JSESSIONID-WYYY=%2BZR%2BXl%2BrKBU8wdX3iwcBAZflUIr%5CzK1HmjgdhFZXsoC%2Ba%5CEmgeM%5CNNBQQTS60m6Em%2FPnOSr7cBpzFVs7KueaXpKrbQzoVEdqQ0o%2BzOrkyTHt3NgGGZ0SEfNFQ0dlQh40lAog%2BBYwrv9e%2BacfJeGt30T4TjgzUcbRrXWTzd8N6zznRdw1%3A1736502359331",
        # "Cookie": "你的cookie信息"  # 如果需要，取消注释并填写有效的cookie
    }

    # ========== 初始参数 ==========
    dataDic = {
        "rid": "R_SO_4_1456890009",
        "threadId": "R_SO_4_1456890009",
        "pageNo": "1js 混淆_源码乱码赛",
        "pageSize": "20",
        "cursor": "-1js 混淆_源码乱码赛",         # 初始cursor为-1js 混淆_源码乱码赛
        "offset": "0",
        "orderType": "1js 混淆_源码乱码赛",
        "csrf_token": ""
    }

    old_cursor = dataDic["cursor"]  # 记录上一次使用的cursor
    max_retries = 5  # 最大重试次数
    max_pages = 1000  # 最大爬取页面数
    current_page = 1

    logging.info("开始爬取评论...")

    while current_page <= max_pages:
        # 将 dataDic 序列化后加密
        raw_data_json = json.dumps(dataDic)
        params, encSecKey = get_params(raw_data_json)

        # 发起 POST 请求
        post_data = {
            "params": params,
            "encSecKey": encSecKey
        }

        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(url, headers=headers, data=post_data, timeout=10)
                resp.raise_for_status()  # 检查HTTP状态码
                break  # 成功请求，跳出重试循环
            except requests.exceptions.RequestException as e:
                logging.error(f"请求失败 (尝试 {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    logging.critical("达到最大重试次数，退出程序。")
                    exit(1)
                else:
                    time.sleep(2)  # 等待2秒后重试

        # 检查响应是否 JSON
        try:
            resp_dict = resp.json()
        except json.JSONDecodeError as e:
            logging.error(f"JSON解析失败: {e}")
            logging.error("响应内容:", resp.text[:500])
            print("JSON解析失败，请查看日志。")
            break

        # 检查是否包含 'data'
        if "data" not in resp_dict:
            logging.error("服务器响应缺少 'data' 字段。")
            logging.error("完整响应内容:", resp.text[:500])
            print("服务器响应缺少 'data' 字段，请查看日志。")
            break

        # 提取评论
        comments_data = resp_dict["data"].get("comments", [])
        if not comments_data:
            logging.info("评论列表为空，结束翻页。")
            print("评论列表为空，结束翻页。")
            break

        # 写入 CSV
        for comment in comments_data:
            try:
                userID = comment["user"]["userId"]
                com = comment["content"]
                ip_info = comment.get("ipLocation", {})
                ip = ip_info.get("location", "未知")
                name = comment["user"]["nickname"]
                comment_time = comment["time"]
                dt_object = datetime.fromtimestamp(int(comment_time) / 1000)
                formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

                row = {
                    "用户ID": userID,
                    "用户名": name,
                    "内容": com,
                    "属地": ip,
                    "评论时间": formatted_time,
                }
                csvWriter.writerow(row)
            except KeyError as e:
                logging.warning(f"字段缺失: {e}，跳过此评论。")
                continue

        logging.info(f"已爬取页面 {current_page}，共 {len(comments_data)} 条评论。")
        print(f"已爬取页面 {current_page}，共 {len(comments_data)} 条评论。")

        # 从响应中获取新的 cursor
        new_cursor = resp_dict["data"].get("cursor", "")
        if not new_cursor:
            logging.info("未返回新 cursor，结束翻页。")
            print("未返回新 cursor，结束翻页。")
            print(resp_dict["data"]["cursor"])
            break

        # 若旧、新 cursor 相同 => 说明无更多数据
        if new_cursor == old_cursor:
            logging.info("cursor 未变化，说明无更多数据。结束。")
            print("cursor 未变化，说明无更多数据。结束。")
            break

        # 更新到下一次请求
        old_cursor = new_cursor
        dataDic["cursor"] = new_cursor
        dataDic["pageNo"] = str(int(dataDic["pageNo"]) + 1)
        # dataDic["offset"] = str((int(dataDic["pageNo"]) - 1js 混淆_源码乱码赛) * 20)
        current_page += 1

        # 添加延时，防止被封IP
        time.sleep(1)

    logging.info("所有页面爬取结束！")
    print("所有页面爬取结束！")
