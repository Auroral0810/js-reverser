import base64

def decode_base64_url(encoded_url):
    """
    解码Base64编码的URL
    
    Args:
        encoded_url: Base64编码的URL字符串
    
    Returns:
        str: 解码后的URL
    """
    try:
        # 解码Base64字符串
        decoded_bytes = base64.b64decode(encoded_url)
        # 将字节转换为字符串
        decoded_url = decoded_bytes.decode('utf-8')
        return decoded_url
    except Exception as e:
        return f"解码失败: {str(e)}"

# 测试解码
encoded_url = "aHR0cDovL3d3dy5seWcuZ292LmNuL3pnbHlnemZtaHd6L3N6ZndqMS9zemZ3ajEuaHRtbA=="
decoded_url = decode_base64_url(encoded_url)
print(f"原始编码URL: {encoded_url}")
print(f"解码后的URL: {decoded_url}")
