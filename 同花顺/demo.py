import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

cookies = {
    'log': '',
    'Hm_lvt_722143063e4892925903024537075d0d': '1744813460',
    'Hm_lpvt_722143063e4892925903024537075d0d': '1744813460',
    'HMACCOUNT': '764A7B05229BE584',
    'Hm_lvt_929f8b362150b1f77b477230541dbbc2': '1744813460',
    'Hm_lpvt_929f8b362150b1f77b477230541dbbc2': '1744813460',
    'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1744813460',
    'Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca': '1744813485',
    'Hm_lvt_f79b64788a4e377c608617fba4c736e2': '1744813485',
    'Hm_lpvt_f79b64788a4e377c608617fba4c736e2': '1744813506',
    'Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca': '1744813506',
    'Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1': '1744813506',
    'v': 'A4KxFJ1EUaLS4E1-QeO7P-Ap1YPhU4coOFV6rcybrwKj1iw9tOPWfQjnyqWf',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://data.10jqka.com.cn/financial/yjyg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'hexin-v': 'A4KxFJ1EUaLS4E1-QeO7P-Ap1YPhU4coOFV6rcybrwKj1iw9tOPWfQjnyqWf',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# 创建一个列表来存储所有页面的数据
all_data = []
table_headers = []

# 先获取第一页，从中提取总页数
url_template = 'https://data.10jqka.com.cn/ajax/yjyg/date/2025-03-31/board/ALL/field/enddate/order/desc/page/{}/ajax/1/free/1/'
first_page_url = url_template.format(1)

response = requests.get(first_page_url, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 解析总页数
total_pages = 1
page_info = soup.find('span', class_='page_info')
if page_info:
    page_match = re.search(r'(\d+)/(\d+)', page_info.text)
    if page_match:
        total_pages = int(page_match.group(2))
        print(f"检测到总页数: {total_pages}")

# 提取表头
table = soup.find('table', class_='m-table J-ajax-table J-canvas-table')
if table:
    thead = table.find('thead')
    if thead:
        header_row = thead.find('tr', class_='row2')
        if header_row:
            for th in header_row.find_all('th'):
                header_text = th.get_text(strip=True).replace('\n', ' ')
                table_headers.append(header_text)
    
    print("表头：")
    for i, header in enumerate(table_headers):
        print(f"{i+1}. {header}")

# 遍历所有页面获取数据
for page in range(1, total_pages + 1):
    print(f"\n正在爬取第 {page}/{total_pages} 页...")
    
    if page > 1:  # 第一页已经获取
        page_url = url_template.format(page)
        response = requests.get(page_url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='m-table J-ajax-table J-canvas-table')
    
    if table:
        # 提取数据行
        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = []
                for td in row.find_all('td'):
                    cell_text = td.get_text(strip=True)
                    row_data.append(cell_text)
                all_data.append(row_data)
            
            print(f"第{page}页爬取完成，当前共有{len(all_data)}条数据")
    else:
        print(f"第{page}页未找到表格")

# 创建DataFrame并保存为CSV
if table_headers and all_data:
    df = pd.DataFrame(all_data, columns=table_headers)
    df.to_csv('同花顺业绩预告_全部.csv', index=False, encoding='utf-8-sig')
    print(f"\n所有数据已保存到'同花顺业绩预告_全部.csv'，共{len(all_data)}条记录")
else:
    print("没有获取到数据或表头")