import json

with open('crawler_progress.json', 'r') as f:
    data = json.load(f)

print(len(data))

# data = dict(list(data.items())[:12964])

# # 将截取后的数据写回文件
# with open('crawler_progress.json', 'w') as f:
#     json.dump(data, f, indent=2, ensure_ascii=False)

# print(f"保留了数据，当前数据量：{len(data)}")