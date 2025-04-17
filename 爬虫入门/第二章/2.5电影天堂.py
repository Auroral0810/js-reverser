import requests
import re
import csv


domain = "https://www.dy2018.com/"

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

f = open('result.csv','w')
csvWriter = csv.writer(f)
child_href_list = []

resq = requests.get(domain, headers=headers)
resq.encoding='gb2312'
# print(resq.text)

obj1 = re.compile(r"2025必看热片.*?<ul>(?P<ul>.*?)</ul>",re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'",re.S)
obj3 = re.compile(r'◎片　　名　(?P<name>.*?)<br />.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<address>.*?)">', re.S)

result1 = obj1.finditer(resq.text)
ul = next(result1).group('ul')
result2 = obj2.finditer(ul)

# print(ul)
for e in result2:
    # print(e.group('href'))
    new_url = domain+e.group('href').strip("/")
    child_href_list.append(new_url)#保存子页面链接
# print(child_href_list)

#提取子页面内容
for href in child_href_list:
    new_resq = requests.get(href, headers=headers)
    new_resq.encoding='gb2312'
    result3 = obj3.search(new_resq.text)
    # print(result3.group('name'))
    # print(result3.group('address'))
    dict = result3.groupdict()
    csvWriter.writerow(dict.values())
    # print(new_resq.text)
    # break
    new_resq.close()

f.close()
resq.close()