import time
import requests
import os

""" 
2021.8.3测试有效
如果需要提交答案并通过需要登录
"""

def main():
    sums = 0
    headers = {"User-Agent": "yuanrenxue.project",}
    for i in range(1, 6):
        t = str(int(time.time()))+'000'
        nodejs = os.popen('node 16 '+ t)
        m = nodejs.read().replace('\n', '')
        params = {
            "page":i,
            "m":m,
            "t":t,
        }
        response = requests.get(url="http://match.yuanrenxue.com/api/match/16",params = params,headers=headers).json()
        print(response)
        for each in response["data"]:
            sums += each["value"]
    print(sums)
 
 
 
 
if __name__ == "__main__":
    main()