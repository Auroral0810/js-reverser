import requests
from lxml import etree
import os
import time

cookies = {
    'route': '9d169c0aea4b7c89fa0d073417b5645f',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'route=9d169c0aea4b7c89fa0d073417b5645f',
}

params = {
    'objectid': 'aa004cda69408e7f1d546474c03c9934',
    'puid': '228712261',
}

response = requests.get(
    'https://pan-yz.chaoxing.com/preview/objectshowpreview.html',
    params=params,
    cookies=cookies,
    headers=headers,
)

html = etree.HTML(response.text)

# 创建文件夹
os.makedirs('images', exist_ok=True)

# 获取所有li元素
li_elements = html.xpath('//li[starts-with(@id, "anchor")]')

# 遍历每个li元素并获取其中的img
for index, li in enumerate(li_elements):
    # 获取li的id
    li_id = li.get('id')
    
    # 获取img的src
    img_elements = li.xpath('./img')
    if img_elements:
        img_url = img_elements[0].get('src')
        print(f"第{index+1}个li(id={li_id})的图片URL: {img_url}")
        
        # 下载图片
        try:
            img_response = requests.get(img_url, headers=headers)
            if img_response.status_code == 200:
                # 保存图片
                with open(f'images/{li_id}.png', 'wb') as f:
                    f.write(img_response.content)
                print(f"图片已保存为 images/{li_id}.png")
            else:
                print(f"下载图片失败，状态码: {img_response.status_code}")
        except Exception as e:
            print(f"下载图片时出错: {str(e)}")
        
        # 添加延迟，避免请求过快
        time.sleep(0.5)
    else:
        print(f"第{index+1}个li(id={li_id})没有找到图片")
