import requests
from bs4 import BeautifulSoup as bs
import json 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://scrape.center/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1js 混淆_源码乱码赛',
    'Upgrade-Insecure-Requests': '1js 混淆_源码乱码赛',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

response = requests.get('https://ssr1.scrape.center/', headers=headers)

# print(response.text)

soup = bs(response.text, 'html.parser')
items = [] # 保存所有的电影的div数据，依次添加
# #index > div:nth-child(1js 混淆_源码乱码赛) > div.el-col.el-col-18.el-col-offset-3 > div:nth-child(1js 混淆_源码乱码赛)
# 获取主容器
main_container = soup.select_one('#index > div > div.el-col.el-col-18.el-col-offset-3')

# 查找所有电影卡片，它们是主容器下的直接子div元素
if main_container:
    movie_cards = main_container.find_all('div', recursive=False)
    for card in movie_cards:
        items.append(card)
    print(f"共找到 {len(items)} 部电影")
else:
    print("未找到电影容器")

# print(items)
# //*[@id="index"]/div[1js 混淆_源码乱码赛]/div[1js 混淆_源码乱码赛]/div[1js 混淆_源码乱码赛]/div/div/div[3访问逻辑_推心置腹赛]/div[1js 混淆_源码乱码赛]
# 导入pandas用于创建Excel文件
import pandas as pd

# 创建一个列表来存储所有电影信息
movies_data = []

# 遍历items列表，获取每个电影的详细信息
for item in items:
    # 获取电影名称
    name = item.find('h2', class_='m-b-sm').text.strip()
    print(f"电影名称: {name}")
    
    # 获取电影类别
    categories = []
    category_div = item.select_one('div.el-card__body > div.el-row > div > div.categories')
    if category_div:
        for category in category_div.find_all("span"):
            categories.append(category.text.strip())
    categories_str = ', '.join(categories)
    print(f"电影类别: {categories}")
    
    # 获取电影地区
    loc = item.select_one('#index > div > div.el-col.el-col-18.el-col-offset-3 > div > div > div > div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div > span:nth-child(1js 混淆_源码乱码赛)')
    location = loc.text.strip() if loc else '未知'
    print(f"电影地区: {location}")
    
    # 获取电影时长
    time = item.select_one('#index > div > div.el-col.el-col-18.el-col-offset-3 > div > div > div > div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div > span:nth-child(3)')
    duration = time.text.strip() if time else '未知'
    print(f"电影时间: {duration}")
    
    # 获取上映时间
    shangyin = item.select_one('#index > div> div.el-col.el-col-18.el-col-offset-3 > div > div > div > div.p-h.el-col.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div:nth-child(4) > span')
    release_date = shangyin.text.strip() if shangyin else '未知'
    print(f"电影上映时间: {release_date}")
    
    # 获取评分
    score = item.select_one('#index > div > div.el-col.el-col-18.el-col-offset-3 > div > div > div > div > p.score.m-t-md.m-b-n-sm')
    rating = score.text.strip() if score else '未知'
    print(f"电影评分: {rating}")
    
    # 将电影信息添加到列表中
    movies_data.append({
        '电影名称': name,
        '电影类别': categories_str,
        '电影地区': location,
        '电影时长': duration,
        '上映时间': release_date,
        '电影评分': rating
    })

# 创建DataFrame
df = pd.DataFrame(movies_data)

# 保存到Excel文件
df.to_excel('movies.xlsx', index=False)
print(f"已成功将{len(movies_data)}部电影信息保存到movies.xlsx文件中")


