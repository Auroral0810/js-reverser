import requests
import execjs
import json
import time
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import base64
import binascii

def decrypt_data(encrypted_data):
    """
    解密服务器返回的加密数据
    
    Args:
        encrypted_data: 加密的数据字符串
    
    Returns:
        解密后的数据(字符串或JSON对象)
    """
    try:
        # 密钥和IV - 需与加密时相同
        key = "xxxxxxxxoooooooo".encode('utf-8')
        iv = "0123456789ABCDEF".encode('utf-8')
        
        # 将十六进制字符串转换为字节
        encrypted_bytes = binascii.unhexlify(encrypted_data)
        
        # 创建AES解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 解密数据
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        
        # 去除填充
        unpadded_bytes = unpad(decrypted_bytes, AES.block_size)
        
        # 转换为字符串
        result = unpadded_bytes.decode('utf-8')
        
        # 尝试解析为JSON
        try:
            return json.loads(result)
        except:
            return result
            
    except Exception as e:
        print(f"解密失败: {e}")
        return encrypted_data  # 解密失败返回原始数据

cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1744098732',
    'HMACCOUNT': '764A7B05229BE584',
    'sessionid': '94q4ek0xqrop8nhln9ndop819vwea79m',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744211285',
}

with open('demo.js', 'r') as f:
    js = f.read()

ctx = execjs.compile(js)
sum = 0
for i in range(1,21):
    current_time = str(int(time.time()*1000))
    x = ctx.call('getX', current_time)
    headers = ctx.call('getHeaders', current_time)
    params = {
        'page': i,
        'x': x,
    }
    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/7/data/', 
                          params=params, cookies=cookies, headers=headers)
    
    # 获取加密的响应数据
    encrypted_data = response.json()['r']
    print(response.headers)
    # 解密数据
    decrypted_data = decrypt_data(encrypted_data)
    res = decrypted_data['current_array']
    for item in res:
        sum += item
print(sum)
