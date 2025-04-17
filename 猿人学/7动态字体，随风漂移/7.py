import requests
import base64
from fontTools.ttLib import TTFont

cookies = {
    'sessionid': 'a0san8v13c61zw435r31r0zpq62xafx5',
    'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1744004527',
    'HMACCOUNT': '764A7B05229BE584',
    'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1744004548',
    'Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3': '1744004548',
    'HMACCOUNT': '764A7B05229BE584',
    'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1744004555',
    'no-alert3': 'true',
    'tk': '-6834914907875830726',
    'yuanrenxue_cookie': '1744041254|Ner3meWTenBw8QgzAc9RirHc6wchy9E0GqnkH3Onu85nbN49ZmfnoNlp7QxScahQbhzXHbaayOEmlwxI0wYAlFwYI6vFTGJH36CYvovfuIJ4U9F5LHBfMmUd0uf1UVaMfNaQmk1OFw8kQdym0eZS2zdTWQElNlrQi0dCdiMAXdILz0Cmc',
    'm': 'a39cf1a67b614599915b6528290e86ab',
    'RM4hZBv0dDon443M': 'WE5gncA7M7Z3lGdzbmrwP3QE4ncG/6YtdA0Qk5Uw3mRdPI4A9yQ5aebuFC1tnR6ZgwksMHFkoBuh1xSsFeVjkoaC8a7EDxOIlQvP+Nb7/rt2qai5mf4fUZIB7oK8N01QlAxPv7bv0DdyhJCMJn+orFwC31+SU/SOOqCmK4nN18msSoF7tXdCPOKTJEjHanzNiLYH99RxTeuzHuDOGtZ5cfc55A4NKCYYdrl1wbVUOew=',
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1744181307',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1744181980',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/7',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=a0san8v13c61zw435r31r0zpq62xafx5; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1744004527; HMACCOUNT=764A7B05229BE584; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3=1744004548; HMACCOUNT=764A7B05229BE584; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1744004555; no-alert3=true; tk=-6834914907875830726; yuanrenxue_cookie=1744041254|Ner3meWTenBw8QgzAc9RirHc6wchy9E0GqnkH3Onu85nbN49ZmfnoNlp7QxScahQbhzXHbaayOEmlwxI0wYAlFwYI6vFTGJH36CYvovfuIJ4U9F5LHBfMmUd0uf1UVaMfNaQmk1OFw8kQdym0eZS2zdTWQElNlrQi0dCdiMAXdILz0Cmc; m=a39cf1a67b614599915b6528290e86ab; RM4hZBv0dDon443M=WE5gncA7M7Z3lGdzbmrwP3QE4ncG/6YtdA0Qk5Uw3mRdPI4A9yQ5aebuFC1tnR6ZgwksMHFkoBuh1xSsFeVjkoaC8a7EDxOIlQvP+Nb7/rt2qai5mf4fUZIB7oK8N01QlAxPv7bv0DdyhJCMJn+orFwC31+SU/SOOqCmK4nN18msSoF7tXdCPOKTJEjHanzNiLYH99RxTeuzHuDOGtZ5cfc55A4NKCYYdrl1wbVUOew=; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1744181307; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1744181980',
}

def decode_base64_to_woff(base64_content, filename):
    """将base64编码的内容解码并写入woff文件"""
    woff_data = base64.b64decode(base64_content)
    with open(f'./{filename}.woff', 'wb') as file:
        file.write(woff_data)
    print(f"已将woff数据写入到{filename}.woff文件")

def woff_to_xml(woff_file, xml_file):
    """
    将woff文件转换为xml格式
    :param woff_file: woff文件路径
    :param xml_file: 输出的xml文件路径
    """
    try:
        # 打开woff字体文件
        font = TTFont(woff_file)
        # 将字体保存为XML格式
        font.saveXML(xml_file)
        print(f"成功将 {woff_file} 转换为 {xml_file}")
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")

for i in range(1,2):
    response = requests.get('https://match.yuanrenxue.cn/api/match/7', cookies=cookies, headers=headers).json()
    woff = response['woff']
    data = response['data']
    decode_base64_to_woff(woff, 'woff_data')
    woff_file = "woff_data.woff"  # 你的woff文件路径
    xml_file = "font_data.xml"    # 要保存的xml文件路径
    woff_to_xml(woff_file, xml_file)