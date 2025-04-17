import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import jieba
from pandas import read_csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_text(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding='utf-8'
    # print(response.status_code)
    time.sleep(2)
    return response.text

f = open('movies.csv','w')
csvWriter = csv.writer(f)

def find_and_save(page_content_bs):
    contents = page_content_bs.find_all('div', class_='short-content')
    # 遍历内容，处理和打印
    for content in contents:
        # 找到并移除可能的提示内容 <p class="spoiler-tip">
        spoiler_tip = content.find('p', class_='spoiler-tip')
        if spoiler_tip:
            spoiler_tip.decompose()  # 移除提示内容
        spoiler_unfold = content.find('a', class_='unfold',href='javascript:;')
        if spoiler_unfold:
            spoiler_unfold.decompose()
        # 提取文本内容
        text = content.get_text(strip=True)
        # 移除 `()` 内容
        cleaned_text = text.replace("()", "").strip()
        # 打印清理后的文本
        # print(cleaned_text)
        csvWriter.writerow(cleaned_text.split())

def create_wordcloud(text, stopwords):
    # 使用 jieba 分词
    words = jieba.lcut(text)
    # 过滤掉停用词
    words = [word for word in words if word not in stopwords and len(word) > 1]
    # 拼接成词云输入的文本
    processed_text = " ".join(words)

    # 创建词云对象
    wordcloud = WordCloud(
        font_path="simhei.ttf",  # 设置中文字体路径，确保字体文件已安装
        background_color="white",
        width=800,
        height=400,
        max_words=200
    ).generate(processed_text)

    # 绘制词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    #爬取数据
    for num in range(0,601,20):
        url = f'https://movie.douban.com/subject/3878007/reviews?start={num}'
        page_content = get_text(url)
        page_content_bs = BeautifulSoup(page_content, 'html.parser')
        find_and_save(page_content_bs)
    # 制作词云图
    text_list = read_csv('movies.csv')
    # 合并所有影评为一个大文本
    full_text = " ".join(text_list)

    # 停用词列表
    stopwords = {"我", "你", "他", "的", "是", "了", "在", "和", "就", "有", "人", "都", "看", "说", "这"}

    # 创建词云图
    create_wordcloud(full_text, stopwords)