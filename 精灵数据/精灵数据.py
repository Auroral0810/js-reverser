import requests
import json
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import unpad
import pandas as pd

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.jinglingshuju.com',
    'pragma': 'no-cache',
    'priority': 'u=1js 混淆_源码乱码赛, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

data = {
    'page': '1js 混淆_源码乱码赛',
    'num': '20',
    'scope': '',
    'sub_scope': '',
    'round': '',
    'money': '',
    'born_date': '',
    'invest_time': '',
    'area': '',
    'country': '',
    'sort': '',
    'uid': '7abfac865f173069cd4a5973e8423285',
}

response = requests.post('https://vapi.jinglingshuju.com/Data/getItemList', headers=headers, data=data)
content = json.loads(response.text)
encrypted_data = content['data']

def decrypt_data(encrypted_data):
    """
    解密数据函数，实现与JavaScript相同的解密逻辑
    
    Args:
        encrypted_data: 加密的数据
        
    Returns:
        解密后的数据对象
    """
    # 如果数据已经是对象形式，说明已经解密过
    if isinstance(encrypted_data, dict):
        return encrypted_data
    
    # IV字符串和密钥
    j = "DXZWdxUZ5jgsUFPF"
    key = j.encode('utf-8')  # 对应 z = CryptoJS.enc.Utf8.parse(j)
    iv = j[:16].encode('utf-8')  # 取前16个字符作为IV
    
    # Base64解码加密数据
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    # 使用AES-ECB模式解密
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 解密并移除填充
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    
    # 转换为UTF-8字符串并解析JSON
    decrypted_str = decrypted_bytes.decode('utf-8')
    return json.loads(decrypted_str)

def save_to_excel(decrypted_data, output_file='精灵数据.xlsx'):
    """
    将解密后的数据保存到Excel表格
    
    Args:
        decrypted_data: 解密后的数据
        output_file: 输出的Excel文件名
    """
    # 获取公司列表数据
    companies = decrypted_data['list']
    
    # 准备存储主要数据的列表
    data_list = []
    
    # 遍历每个公司信息
    for company in companies:
        # 提取投资方信息
        investors = []
        if 'investor_arr' in company and company['investor_arr']:
            investors = [inv.get('investor', '') for inv in company['investor_arr']]
        
        # 创建公司数据字典
        company_data = {
            '产品名称': company.get('product', ''),
            '业务描述': company.get('business', ''),
            '行业领域': company.get('scope', ''),
            '细分领域': company.get('sub_scope', ''),
            '成立日期': company.get('born_date', ''),
            '地区': company.get('region', ''),
            '城市': company.get('city', ''),
            '投资时间': company.get('invest_time', ''),
            '融资轮次': company.get('round', ''),
            '融资金额': company.get('money', ''),
            '投资方': '、'.join(investors)
        }
        
        # 添加到列表
        data_list.append(company_data)
    
    # 创建DataFrame
    df = pd.DataFrame(data_list)
    
    # 保存到Excel
    df.to_excel(output_file, index=False)
    print(f"数据已保存到 {output_file}")

# 解密数据
decrypted_data = decrypt_data(encrypted_data)

# 保存到Excel
save_to_excel(decrypted_data)

# 打印解密后的数据
print("数据解密成功，共有{}条记录".format(decrypted_data['count']))

