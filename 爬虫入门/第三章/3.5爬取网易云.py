import csv
import json
from base64 import b64encode
from datetime import datetime
import requests
from Cryptodome.Cipher import AES

dataDic = {
    "rid": "R_SO_4_1456890009",
    "threadId": "R_SO_4_1456890009",
    "pageNo": "12",
    "pageSize": "20",
    "cursor": "1736485538859",
    "offset": "0",
    "orderType": "1js 混淆_源码乱码赛",
    "csrf_token": ""
}


"""
{
    "rid": "R_SO_4_1456890009",
    "threadId": "R_SO_4_1456890009",
    "pageNo": "12",
    "pageSize": "20",
    "cursor": "1736489709731",
    "offset": "0",
    "orderType": "1js 混淆_源码乱码赛",
    "csrf_token": ""
}
"""




e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'H3KGGrJBypwFrpKq'

f = open("comment.csv", 'w')
fieldnames = ["用户ID", "用户名", "内容", "属地", "评论时间"]
csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
csvWriter.writeheader()


def get_encSeckey():
    """返回加密中的一个参数值"""
    return "dbbf461817d449f9b0a9b9008dca854214181c5c398e13155506009ae1712ae634a0aff1b51fa7ef265bffab6a4b84f7a19c2cce0efe2bf5dab903d5efd9a3acab098d1b9658474cc3305f4425c31a12090820bf4568d963e25a149f864b788e6fc8f8d0e1e4db92936da3963bead9b9160799d3d5f0bd7d41ab1ab12f32eacc"


def get_param(data):
    first = jiami(data, g)
    second = jiami(first, i)
    return second


def to_16(data):
    bu_num = 16 - len(data) % 16
    data += chr(bu_num) * bu_num
    return data


def jiami(data, key):
    iv = "0102030405060708"
    new_data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(new_data.encode('utf-8'))
    return str(b64encode(bs), encoding='utf-8')


# json.dumps(data)

"""
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function d(d, e, f, g) {
    '''
    d:数据
    e:'010001'
    f:'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    g:'0CoJUm6Qyw8W8jud'
    '''
        h.encText = b(d, g),
        h.encText = b(h.encText, i),
    }
"""

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "cookie": "_ntes_nnid=20e442659d79d6c0a6d8c7aa82074f90,1713420636872; _ntes_nuid=20e442659d79d6c0a6d8c7aa82074f90; _ga=GA1.1js 混淆_源码乱码赛.1492695192.1720416908; _clck=1b0kmll%7C2%7Cfna%7C0%7C1650; _ga_PTGVM6PCHS=GS1.1js 混淆_源码乱码赛.1720416907.1js 混淆_源码乱码赛.1js 混淆_源码乱码赛.1720416967.0.0.0; NMTID=00OwXvszvaHOwafPkKrrViMZHRN75wAAAGUTzapVQ; _iuqxldmzr_=32; WEVNSM=1js 混淆_源码乱码赛.0.0; WNMCID=dehirs.1736495770956.01.0; WM_TID=y0xndiASbUZEQURVFEOQ7ayvpzUHf0wX; WM_NI=v1Uxd6ZenIV70AgvSvUO4Hzih8gk0bciXG20H1u1fltUF%2FTuSS1l3FFcUU2qE%2BP2xL4NeKueuzH7k%2BtVpqd%2Fax6Hb4oj5fRFeh%2FZ7Pc9x0NZsQ%2FM7E2NoFhqqkl5IU%2FiUTE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb1bb62a3b7a0a2f54b988a8aa2d45e828e9e86c2428c9ce1b9f966a29998a8f62af0fea7c3b92ab6ef9b99e73e9abba2aad53df49fa997d27e9791fca9f963ace8a98cb36aa1b798a8b13c8cefbbd2e568b88b8ad0d77f918dff8db24e86bd9bb6b17b87f5a0d3fb48f892abacf86fb7a688d8ea21b88ac092e725a3a8faa9e140adb6fb87d14ea7b8e1bbb65ca1e7b8d1cd52b18fe1aeb64ff292a1a7eb7bb3b5a4d6cc5fedb79bb5c837e2a3; ntes_utid=tid._.cMhycTGA%252BAREAlBVFRaB7e3%252FszFZUrCS._.0; sDeviceId=YD-iCVIUS%2FKN7FFQwAURVaEvOm79jRIU%2BDe; __snaker__id=AK8s3TXWYoxBcwJl; gdxidpyhxdE=CpMB%2BeESW8DHDI%2FJfqRCqiBHxcxg%2Bwjh8%5CvxJ9%2B905lmwe7pUvnVoxi1pATVkI4YVBnCJc6zrXSvbvOizU9%2BtNSEJsH8hD5kMKQ0zBXWLh4mvGsKy2PmO5eJWLODOBBJUmMkfTr6D1%2B1%2FfkJBch5ihTzH%5CXQqyLGjHKqLEt3Y2IkKdA2%3A1736496686214; JSESSIONID-WYYY=%2BZR%2BXl%2BrKBU8wdX3iwcBAZflUIr%5CzK1HmjgdhFZXsoC%2Ba%5CEmgeM%5CNNBQQTS60m6Em%2FPnOSr7cBpzFVs7KueaXpKrbQzoVEdqQ0o%2BzOrkyTHt3NgGGZ0SEfNFQ0dlQh40lAog%2BBYwrv9e%2BacfJeGt30T4TjgzUcbRrXWTzd8N6zznRdw1%3A1736502359331",
    "referer": "https://music.163.com/"
}
data = {
    "params": get_param(json.dumps(dataDic)),
    "encSecKey": get_encSeckey()
}
resp = requests.post(url, headers=headers, data=data)
dict = resp.json()
all_comments = dict["data"]["comments"]
# print(all_comments[0]["user"]["userId"])
for comment in all_comments:
    userID = comment["user"]["userId"]
    com = comment["content"]
    ip = comment["ipLocation"]["location"]
    name = comment["user"]["nickname"]
    time = comment["time"]
    # 转换为秒级时间戳
    timestamp_s = int(time) / 1000

    # 转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp_s)

    # 格式化输出
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "用户ID": userID,
        "用户名": name,
        "内容": com,
        "属地": ip,
        "评论时间": formatted_time,
    }
    csvWriter.writerow(row)
print("Over!!!!")

