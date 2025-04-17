from urllib.request import urlopen

url = "http://www.baidu.com"
resq = urlopen(url) #得到响应

# print(resq.read().decode("utf-8"))

with open("mybaidu.html","w",encoding="utf-8") as f:
    f.write(resq.read().decode("utf-8")) #读取到网页的页面源代码
print("over")
