import requests
import re
import csv

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
f = open('data.csv', 'w')
csvWriter = csv.writer(f)

for i in range(0, 251, 25):
    url = f"https://movie.douban.com/top250?start={i}&filter="

    resp = requests.get(url, headers=headers)
    # resp = requests.get(url)
    # print(resp.text)
    # <span class="title">霸王别姬</span>
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?'
                     r'<p class="">.*?<br>(?P<year>.*?)&nbsp;/&nbsp;.*?<div class="star">.*?<span class='
                     r'"rating_num" property="v:average">(?P<stars>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>',
                     re.S)
    ret = obj.finditer(resp.text)
    for item in ret:
        dit = item.groupdict()
        dit['year'] = dit['year'].strip()
        # print(f'{item.group("name").strip()},{item.group("year").strip()},{item.group("stars").strip()},{item.group("num").strip()}')
        csvWriter.writerow(dit.values())


f.close()
resp.close()