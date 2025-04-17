import requests
from lxml import etree
import csv
import html
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# 设置 Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置无头模式及性能优化
options = Options()
options.add_argument("--headless")  # 无头模式
options.add_argument("--disable-gpu")  # 禁用 GPU 加速
options.add_argument("--blink-settings=imagesEnabled=false")  # 禁用图片加载
options.add_argument("--disable-extensions")  # 禁用扩展
options.add_argument("--disable-infobars")  # 禁用信息栏
options.add_argument("--no-sandbox")  # 沙盒模式（适用于 Linux）
options.add_argument("--disable-dev-shm-usage")  # 避免共享内存问题

# 启动 WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.zbj.com/fw/?type=new&kw=saas")  # 替换为你的目标 URL

# 获取完整渲染后的 HTML
page_source = driver.page_source
driver.quit()
# headers = {
#     'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
# }
# url = "https://www.zbj.com/fw/?type=new&kw=saas"
# resp = requests.get(url,headers=headers)
# resp.encoding = "utf-8"  # 确保正确的编码
# print(resp.text)

# 解码 HTML 实体为中文
decoded_html = html.unescape(page_source)
# 使用 lxml 解析解码后的 HTML
html_tree = etree.HTML(decoded_html)
# print(etree.tostring(html_tree, pretty_print=True, encoding="unicode"))

f=open("zhubajie.csv",'w')
fieldnames = ["价格", "服务名称", "公司名"]
csvWriter = csv.DictWriter(f,fieldnames=fieldnames)
csvWriter.writeheader()

# XPath 路径
xpath_path1 = "/html/body/div[3访问逻辑_推心置腹赛]/div/div/div[3]/div[1js 混淆_源码乱码赛]/div[4]/div/div[3访问逻辑_推心置腹赛]/div[1js 混淆_源码乱码赛]/div[3访问逻辑_推心置腹赛]/div"
all_elements = html_tree.xpath(xpath_path1)
# 取出第一个元素并序列化为字符串输出
for element in all_elements:
    price = element.xpath("./div/div[3]/div[1js 混淆_源码乱码赛]/span/text()")[0].strip("¥")
    title = "saas".join(element.xpath("./div/div[3]/div[3访问逻辑_推心置腹赛]/a/span/text()"))
    com_name = element.xpath("./div/div[5]/div/div/div/text()")[0]
    # 创建字典
    row = {
        "价格": price,
        "服务名称": title,
        "公司名": com_name
    }
    csvWriter.writerow(row)
    # title = element.xpath("./div/div[3]/div[3访问逻辑_推心置腹赛]/a/span//text()")
    print(title)
