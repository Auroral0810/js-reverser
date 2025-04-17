import requests
import os
import time
import json
from requests.utils import requote_uri

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://bz.zzzmh.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://bz.zzzmh.cn/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

json_data = {
    'size': 24,
    'current': 5,
    'sort': 0,
    'category': 0,
    'resolution': 0,
    'color': 0,
    'categoryId': 0,
    'ratio': 0,
}

# 创建保存图片的文件夹
save_dir = "wallpapers"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

response = requests.post('https://api.zzzmh.cn/v2/bz/v3/getData', headers=headers, json=json_data).json()
res = response['data']['list']
print(f"获取到 {len(res)} 张壁纸")
for index, item in enumerate(res):
    href = item['i']
    t = item['t']
    if t == 1:
        url = 'https://api.zzzmh.cn/v2/bz/v3/getUrl/'+href + '19'
    else:
        url = 'https://api.zzzmh.cn/v2/bz/v3/getUrl/'+href + '29'
    print(f"获取链接: {url}")
    
    # 发送请求获取重定向URL
    try:
        # 使用session跟踪重定向
        session = requests.Session()
        response = session.get(url, headers=headers, allow_redirects=False)
        
        # 检查是否有重定向
        if response.status_code in [301, 302, 303, 307, 308]:
            redirect_url = response.headers.get('Location')
            print(f"重定向到: {redirect_url}")
            
            # 如果需要获取最终URL（可能有多次重定向）
            final_response = requests.get(url, headers=headers, allow_redirects=True)
            print(f"最终URL: {final_response.url}")
            
            # 下载图片
            try:
                # 从URL中提取文件名
                import urllib.parse
                img_url = final_response.url
                # 移除URL参数
                clean_url = img_url.split('?')[0]
                # 获取文件名
                filename = os.path.basename(clean_url)
                
                # 保存图片
                img_path = os.path.join(save_dir, filename)
                # 下载图片内容
                img_response = requests.get(img_url, headers=headers, stream=True)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"图片已保存: {img_path}")
                else:
                    print(f"下载图片失败，状态码: {img_response.status_code}")
            except Exception as e:
                print(f"下载图片时出错: {e}")
        else:
            print("没有重定向")
        
        # 请求间隔，避免请求过快
        time.sleep(1)
    except Exception as e:
        print(f"获取重定向URL时出错: {e}")
    