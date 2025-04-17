import pandas as pd
import requests
import random
import hashlib
import time
import json
from bs4 import BeautifulSoup
cookies = {
    'SCF': 'AjSvyFrp6UcxodvGEySqe-NuaZzFPPgw_PsUczI5pG31auahlPdRuUPBFX3wPYvCuwE6Mr-pkQS-HMhjV-f2js4.',
    'UOR': 'www.google.com,tousu.sina.com.cn,',
    'SINAGLOBAL': '112.2.255.96_1744603429.434425',
    'Apache': '112.2.255.96_1744603429.434426',
    'SUB': '_2A25K-Pl2DeRhGeFG7VAR8SjJzj2IHXVmdHS-rDV_PUNbm9ANLW7jkW9NeT7LKxzRtVKCiLrmNtWLmZdVybVJzYcL',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFmVDW8co5l-iVWn.WBYQhv5NHD95QN1hqEeh2cSK-pWs4Dqcj_i--RiKn7iKnpi--fi-2fi-zci--fi-2fi-zci--NiKnEiK.Ei--RiKnEi-2p',
    'ALF': '1747195430',
    'ULV': '1744603431071:2:2:2:112.2.255.96_1744603429.434426:1744603429147',
    'U_TRS1': '00000060.e4fb2d4b.67fc8928.e5aa2bd1',
    'U_TRS2': '00000060.e5062d4b.67fc8928.40f00f66',
    'HM-AMT': '%7B%22amt%22%3A25216430%2C%22amt24h%22%3A19962%2C%22v%22%3A%222.3.172%22%2C%22vPcJs%22%3A%221.6.83%22%2C%22vPcCss%22%3A%221.2.395%22%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tousu.sina.com.cn/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'SCF=AjSvyFrp6UcxodvGEySqe-NuaZzFPPgw_PsUczI5pG31auahlPdRuUPBFX3wPYvCuwE6Mr-pkQS-HMhjV-f2js4.; UOR=www.google.com,tousu.sina.com.cn,; SINAGLOBAL=112.2.255.96_1744603429.434425; Apache=112.2.255.96_1744603429.434426; SUB=_2A25K-Pl2DeRhGeFG7VAR8SjJzj2IHXVmdHS-rDV_PUNbm9ANLW7jkW9NeT7LKxzRtVKCiLrmNtWLmZdVybVJzYcL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFmVDW8co5l-iVWn.WBYQhv5NHD95QN1hqEeh2cSK-pWs4Dqcj_i--RiKn7iKnpi--fi-2fi-zci--fi-2fi-zci--NiKnEiK.Ei--RiKnEi-2p; ALF=1747195430; ULV=1744603431071:2:2:2:112.2.255.96_1744603429.434426:1744603429147; U_TRS1=00000060.e4fb2d4b.67fc8928.e5aa2bd1; U_TRS2=00000060.e5062d4b.67fc8928.40f00f66; HM-AMT=%7B%22amt%22%3A25216430%2C%22amt24h%22%3A19962%2C%22v%22%3A%222.3.172%22%2C%22vPcJs%22%3A%221.6.83%22%2C%22vPcCss%22%3A%221.2.395%22%7D',
}


 
#[l, p, b, h, c, d["type" + e]].sort().join("")
def generate_random_string(e=True, t=4, r=16):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = t if not e else random.randint(t, r)
    return ''.join(random.choice(chars) for _ in range(length))
 
def get_sha256(value):
    """
    sha256加密
    :param value: 加密字符串
    :return: 加密结果转换为16进制字符串，并大写
    """
    hsobj = hashlib.sha256()
    hsobj.update(value.encode("utf-8"))
    return hsobj.hexdigest()
 
requests.packages.urllib3.disable_warnings()
sessions=requests.session()
data=[]
number=0
for i in range(1,30):#1524
    print(i)
    url_list=[]
    if len(data)%50==0 and len(data)!=0:
        time.sleep(60)
    while True:
        ts=str(int(time.time() * 1000))#ts,时间戳
        l=ts
        rs=generate_random_string(True, 4, 16)
        p=rs#rs
        b = '$d6eb7ff91ee257475%'
        h='外卖 食品安全'#keywords
        c='10'#page_size
        d=str(i)#d["type" + e]=page
        signature=''.join(sorted([l, p, b, h, c, d]))
        signature=get_sha256(signature)
        params = {
        'ts': ts,
        'rs': rs,
        'signature': signature,
        'keywords': h,
        'page_size': c,
        'page': d,
        }
        try:
            response = sessions.get('https://tousu.sina.com.cn/api/index/s',cookies=cookies,
                                      headers=headers,params=params,verify=False,allow_redirects=False)
            response=json.loads(response.text)['result']['data']['lists']
            #print(response)
            for n in range(len(response)):
                if response[n]['main']['evaluate_u']==None:
                    number+=1
                    continue
                else:
                    url=response[n]['main']['url']
                    url_list.append(url)
                number+=1
            break
        except Exception as e:
            print(e,response.text,i)
            time.sleep(300)
            continue
    for url in url_list:
        while True:
            try:
                response = sessions.get('https:'+url,cookies=cookies,headers=headers,verify=False,allow_redirects=False)
                soup = BeautifulSoup(response.text, 'html.parser')
                u_date_elements = soup.find_all(class_='u-date')
                u_list=soup.find('ul', class_='ts-q-list')
                c_num=u_list.find_all('li')[0].text
                endtime=u_date_elements[2].text
                starttime=u_date_elements[6].text
                data.append([starttime,endtime,c_num])
                break
            except Exception as e:
                print(e,response.text,i)
                time.sleep(60)
                continue
data=pd.DataFrame(data,columns=['starttime','endtime','c_num'])
data.to_csv('黑猫投诉.csv',index=False)