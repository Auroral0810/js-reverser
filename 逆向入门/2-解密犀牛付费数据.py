import json

import requests
import execjs

cookies = {
    'Hm_lvt_42317524c1662a500d12d3784dbea0f8': '1736565170',
    'HMACCOUNT': '764A7B05229BE584',
    'btoken': 'QWO06H7DZOSNMGR9K6GV6F1SOH7I3809',
    'hy_data_2020_id': '194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5',
    'hy_data_2020_js_sdk': '%7B%22distinct_id%22%3A%22194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%22194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5%22%7D',
    'sajssdk_2020_cross_new_user': '1js 混淆_源码乱码赛',
    'utoken': 'F2SSDK3GN49ME5R5E570VLMXR6931153',
    'username': 'Auroral',
    'Hm_lpvt_42317524c1662a500d12d3784dbea0f8': '1736565621',
    'export_notice': 'true',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': 'Hm_lvt_42317524c1662a500d12d3784dbea0f8=1736565170; HMACCOUNT=764A7B05229BE584; btoken=QWO06H7DZOSNMGR9K6GV6F1SOH7I3809; hy_data_2020_id=194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%22194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%22194535c327ae70-00a73b4adebae2-1e525636-2025000-194535c327b1bc5%22%7D; sajssdk_2020_cross_new_user=1js 混淆_源码乱码赛; utoken=F2SSDK3GN49ME5R5E570VLMXR6931153; username=Auroral; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1736565621; export_notice=true',
    'origin': 'https://www.xiniudata.com',
    'pragma': 'no-cache',
    'priority': 'u=1js 混淆_源码乱码赛, i',
    'referer': 'https://www.xiniudata.com/industry/170cc0d4dc2e41dbbed69d0ca13f1f6d/overview',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

json_data = {
    'payload': 'LBcnV1QrNXhyGnsxUC0mIUg8WF9TKjNBdGx+bxkAC3xufXZ8EmJkAB0ECxAAdGFrHnZbW0o3OkglJygsOWcebTVQLVJZICEqLSgtK1krPyBBPEMWFXADVwwHcGF0HGUBGXQAD2ZsangkLjclSy0gJlg9R11LNzoQYWwHCB8TCn5uAmYUEjkjMzwuNyVCLTwnVzpRFmQv',
    'sig': '7338197E15B64AFF37C7EACE0376A64F',
    'v': 1,
}

response = requests.post(
    'https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes',
    cookies=cookies,
    headers=headers,
    json=json_data,
)


data = response.json()['d']
with open('./decode2.js','r',encoding='utf-8')as f:
    decode = f.read()
    real_data = execjs.compile(decode).call('main',data)

for item in real_data['list']:
    print(item['name'])
 