import requests

cookies = {
    'SCF': 'AjSvyFrp6UcxodvGEySqe-NuaZzFPPgw_PsUczI5pG31auahlPdRuUPBFX3wPYvCuwE6Mr-pkQS-HMhjV-f2js4.',
    'HM-AMT': '%7B%22amt%22%3A25216261%2C%22amt24h%22%3A20001%2C%22v%22%3A%222.3.172%22%2C%22vPcJs%22%3A%221.6.83%22%2C%22vPcCss%22%3A%221.2.395%22%7D',
    'UOR': 'www.google.com,tousu.sina.com.cn,',
    'SINAGLOBAL': '112.2.255.96_1744603429.434425',
    'Apache': '112.2.255.96_1744603429.434426',
    'SUB': '_2A25K-Pl2DeRhGeFG7VAR8SjJzj2IHXVmdHS-rDV_PUNbm9ANLW7jkW9NeT7LKxzRtVKCiLrmNtWLmZdVybVJzYcL',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFmVDW8co5l-iVWn.WBYQhv5NHD95QN1hqEeh2cSK-pWs4Dqcj_i--RiKn7iKnpi--fi-2fi-zci--fi-2fi-zci--NiKnEiK.Ei--RiKnEi-2p',
    'ALF': '1747195430',
    'ULV': '1744603431071:2:2:2:112.2.255.96_1744603429.434426:1744603429147',
    'U_TRS1': '00000060.e4fb2d4b.67fc8928.e5aa2bd1',
    'U_TRS2': '00000060.e5062d4b.67fc8928.40f00f66',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tousu.sina.com.cn/company/index',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'SCF=AjSvyFrp6UcxodvGEySqe-NuaZzFPPgw_PsUczI5pG31auahlPdRuUPBFX3wPYvCuwE6Mr-pkQS-HMhjV-f2js4.; HM-AMT=%7B%22amt%22%3A25216261%2C%22amt24h%22%3A20001%2C%22v%22%3A%222.3.172%22%2C%22vPcJs%22%3A%221.6.83%22%2C%22vPcCss%22%3A%221.2.395%22%7D; UOR=www.google.com,tousu.sina.com.cn,; SINAGLOBAL=112.2.255.96_1744603429.434425; Apache=112.2.255.96_1744603429.434426; SUB=_2A25K-Pl2DeRhGeFG7VAR8SjJzj2IHXVmdHS-rDV_PUNbm9ANLW7jkW9NeT7LKxzRtVKCiLrmNtWLmZdVybVJzYcL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFmVDW8co5l-iVWn.WBYQhv5NHD95QN1hqEeh2cSK-pWs4Dqcj_i--RiKn7iKnpi--fi-2fi-zci--fi-2fi-zci--NiKnEiK.Ei--RiKnEi-2p; ALF=1747195430; ULV=1744603431071:2:2:2:112.2.255.96_1744603429.434426:1744603429147; U_TRS1=00000060.e4fb2d4b.67fc8928.e5aa2bd1; U_TRS2=00000060.e5062d4b.67fc8928.40f00f66',
}

import pandas as pd
import time

# 创建空列表存储所有数据
all_data = []

page = 1
has_data = True

while page<=100:
# while has_data:
    params = {
        'sort_col': '4',
        'sort_ord': '2',
        'page_size': '10',
        'page': page,
    }
    
    try:
        response = requests.get('https://tousu.sina.com.cn/api/company/main_search', params=params, cookies=cookies, headers=headers).json()
        data_list = response['result']['data']['lists']
        
        # 检查是否还有数据
        if not data_list:
            has_data = False
            print(f"爬取完成，共爬取{page-1}页数据")
            break
            
        # 将当前页数据添加到总列表中
        all_data.extend(data_list)
        print(f"成功爬取第{page}页，获取{len(data_list)}条数据")
        
        # 翻页
        page += 1
        
        # 添加延时，避免请求过快
        time.sleep(1)
        
    except Exception as e:
        print(f"爬取第{page}页时出错: {str(e)}")
        has_data = False

# 将数据转换为DataFrame
df = pd.DataFrame(all_data)

# 保存到Excel文件
excel_file = "黑猫投诉排行榜.xlsx"
df.to_excel(excel_file, index=False)
print(f"数据已保存到 {excel_file}，共{len(all_data)}条记录")