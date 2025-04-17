import requests
import re
# findall:匹配字符串中所有的复合正则的内容
lst = re.findall(r"\d+","我的电话是：10086，我女朋友的电话是10010")
print(lst)

# finditer：匹配字符串中所有的内容【返回的是迭代器】,从迭代器中拿到内容需要：.group()
it = re.finditer(r"\d+","我的电话是:10086,我女朋友的电话是：10010")
for i in it:
    print(i.group())

# search，找到一个结果就返回，返回的结果是match对象，那数据需要.group()
s = re.search(r"\d+","我的电话是:10086,我女朋友的电话是：10010")
print(s.group())
#match是从头开始匹配
s = re.match(r"\d+","10086,我女朋友的电话是：10010")
print(s.group())

# AttributeError: 'NoneType' object has no attribute 'group'这个报错是找这一行的点前面是空

# 预加载正则表达式
obj = re.compile(r"\d+")

ret = obj.finditer("我的电话是:10086,我女朋友的电话是：10010")
print(ret)


obj = re.compile(r"\d+",re.S)# re.S 的作用是让.能匹配换行符

# (?P<分组名字>正则)可以单独从正则匹配到的内容中提取内容