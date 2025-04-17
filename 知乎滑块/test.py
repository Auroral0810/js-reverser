

# 破解知乎登陆

import requests    #请求解析库

import base64							  #base64解密加密库
from PIL import Image	  			      #图片处理库
import hmac								  #加密库
from hashlib import sha1				  #加密库
import time
from urllib.parse import urlencode		  #url编码库
import execjs							  #python调用node.js
from http import cookiejar as cookielib
class Spider():
    def __init__(self):
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar()    #使cookie可以调用save和load方法
        self.login_page_url = 'https://www.zhihu.com/signin?next=%2F'
        self.login_api = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.captcha_api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
        }

        self.captcha =''         #存验证码
        self.signature = ''	   #存签名

    # 首次请求获取cookie
    def get_base_cookie(self):
        self.session.get(url=self.login_page_url, headers=self.headers)

    def deal_captcha(self):
        r = self.session.get(url=self.captcha_api, headers=self.headers)
        r = r.json()
        if r.get('show_captcha'):
            while True:
                r = self.session.put(url=self.captcha_api, headers=self.headers)
                img_base64 = r.json().get('img_base64')
                with open('captcha.png', 'wb') as f:
                    f.write(base64.b64decode(img_base64))
                captcha_img = Image.open('captcha.png')
                captcha_img.show()
                self.captcha = input('输入验证码:')
                r = self.session.post(url=self.captcha_api, data={'input_text': self.captcha},
                                      headers=self.headers)
                if r.json().get('success'):
                    break

    def get_signature(self):
        # 生成加密签名
        a = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=sha1)
        a.update(b'password')
        a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
        a.update(b'com.zhihu.web')
        a.update(str(int(time.time() * 1000)).encode('utf-8'))
        self.signature = a.hexdigest()

    def post_login_data(self):
        data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp': str(int(time.time() * 1000)),
            'source': 'com.zhihu.web',
            'signature': self.signature,
            'username': '+8618953675221',
            'password': '',
            'captcha': self.captcha,
            'lang': 'en',
            'utm_source': '',
            'ref_source': 'other_https://www.zhihu.com/signin?next=%2SGMF',
        }

        headers = {
            'x-zse-83': '3_2.0',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
        }

        data = urlencode(data)
        with open('zhih.js', 'rt', encoding='utf-8') as f:
            js = execjs.compile(f.read(), cwd='node_modules')
        data = js.call('b', data)

        r = self.session.post(url=self.login_api, headers=headers, data=data)
        print(r.text)
        if r.status_code == 201:
            self.session.cookies.save('mycookie')
            print('登录成功')
        else:
            print('登录失败')

    def login(self):
        self.get_base_cookie()
        self.deal_captcha()
        self.get_signature()
        self.post_login_data()
if __name__ == '__main__':
    zhihu_spider = Spider()
    zhihu_spider.login()
