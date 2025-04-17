import requests
url = " https://fanyi.baidu.com/sug"
s = input("请输入你要翻译的英文单词:\n")
dat = {
    "kw":s
}

resp = requests.post(url,data=dat)
# resp.encoding="GB2312"
print(resp.json()) #将服务器返回的内容直接处理成json() =>dict
resp.close() #关闭resp