import requests
import requests

cookies = {
    'RT': '"z=1&dm=baidu.com&si=f09b8af6-80d3-4024-9500-f364f0b582b1&ss=mc9uy86o&sl=1&tt=gj&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
    'ab_sr': '1.0.1_MjZkOGI5MDJjOGU1YTNhMGIyZDJkN2IxZmIxMDNiOTBlY2I4MzE2YTUyOWYyYmQ0MGQ3NTY2NzE5OTQ0MGYyNTI0NDUxNzczNzc1MWFlOGZjM2M4YzNlZjFkMTRjYjU1NDE4NTY1YzhmMjg3ZTc2OGI3MzRiNjM0YTU0YTA0NjU5YTRmN2ViZTViMjRkYzBjMDU0MWQzYzEwZWVkMzhiYQ==',
    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750729185',
    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687576,1750692669,1750729180',
    'CPID_212': '69553869',
    'CPTK_212': '1238208573',
    '__cas__id__212': '69553869',
    '__cas__rn__': '500741628',
    '__cas__st__212': '8def06ffa2bddc0d92e44e4a2d6432027c526d10f22e7f5e1a409f08bb0a3d40ed0260fe2a3607ba76de2611',
    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007416288%2FVOdE0WuKMDSUHbkoM9Vi%2BG21exSDnf2gqvBbyqu4zULk1r%2FLA8r93c9z8ksVNFYzY8ZKDL%2Bp3KiAZNEFsq6fDC5WmkUad%2B4axqegAytwXWhduK0WRfJbcgqMYg0yOXFuNI7lX7c0axUTlwxsVivthXQv50SdO%2FCrAuC5fU3CyPWBjMjThYpa4UP4u9Smwwi%2FYWriMS6DfZZL%2BVVTYAdQ%2B%2BcFatdizgkglDb5OQRUW7hK1ajSgrRTZ6D9jMRIRFQHUKpI4Bmev2SkGPIv%2BKvhg%3D%3D65351128282676620109533381010129',
    'HMACCOUNT': '496483824474D6A5',
    'bdindexid': 'ooku2h48k8cbm395f0mf45mfk6',
    'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
    'BA_HECTOR': '0kagaha1840l2k24a480ag8l8g8h0n1k5inqk24',
    'H_PS_PSSID': '60279_61684_62325_63144_63324_63568_63563_63584_63617_63639_63645_63646_63657_63675_63693_63728_63715',
    'H_WISE_SIDS': '60279_61684_62325_62967_63144_63194_63210_63241_63268_63324_63352_63386_63394_63390_63440',
    'ZFY': 'eZolgqFOY0Y0f1Qg:AhsGZTGexoRJ:Ah9e:AUlH93hdW8c:C',
    'BIDUPSID': '2FEBFD961790CF3B5CB7C06D0DCA03F8',
    'PSTM': '1745642057',
    'BAIDUID': '5E9B2757D9152FB85FDD6D4AEB4026ED:FG=1',
    'BDUSS': 'lNbUpGWFZ0RzVPUzVFN0pyaFV6QmlQUEo4ZUVqaGZySFE1RXA3Q3IteFBxZXBuSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE8cw2dPHMNnVG',
    'MAWEBCUID': 'web_oHAxQIUvPYLZZQqNfndpkAqAJlTBpabDPBBNaCvdMXrswtkRXG',
    'MCITY': '-%3A',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'same-origin',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
    'Referer': 'https://index.baidu.com/v2/main/index.html',
    'Connection': 'keep-alive',
    # 'Cookie': 'RT="z=1&dm=baidu.com&si=f09b8af6-80d3-4024-9500-f364f0b582b1&ss=mc9uy86o&sl=1&tt=gj&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; ab_sr=1.0.1_MjZkOGI5MDJjOGU1YTNhMGIyZDJkN2IxZmIxMDNiOTBlY2I4MzE2YTUyOWYyYmQ0MGQ3NTY2NzE5OTQ0MGYyNTI0NDUxNzczNzc1MWFlOGZjM2M4YzNlZjFkMTRjYjU1NDE4NTY1YzhmMjg3ZTc2OGI3MzRiNjM0YTU0YTA0NjU5YTRmN2ViZTViMjRkYzBjMDU0MWQzYzEwZWVkMzhiYQ==; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1750729185; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1750687576,1750692669,1750729180; CPID_212=69553869; CPTK_212=1238208573; __cas__id__212=69553869; __cas__rn__=500741628; __cas__st__212=8def06ffa2bddc0d92e44e4a2d6432027c526d10f22e7f5e1a409f08bb0a3d40ed0260fe2a3607ba76de2611; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a05007416288%2FVOdE0WuKMDSUHbkoM9Vi%2BG21exSDnf2gqvBbyqu4zULk1r%2FLA8r93c9z8ksVNFYzY8ZKDL%2Bp3KiAZNEFsq6fDC5WmkUad%2B4axqegAytwXWhduK0WRfJbcgqMYg0yOXFuNI7lX7c0axUTlwxsVivthXQv50SdO%2FCrAuC5fU3CyPWBjMjThYpa4UP4u9Smwwi%2FYWriMS6DfZZL%2BVVTYAdQ%2B%2BcFatdizgkglDb5OQRUW7hK1ajSgrRTZ6D9jMRIRFQHUKpI4Bmev2SkGPIv%2BKvhg%3D%3D65351128282676620109533381010129; HMACCOUNT=496483824474D6A5; bdindexid=ooku2h48k8cbm395f0mf45mfk6; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=0kagaha1840l2k24a480ag8l8g8h0n1k5inqk24; H_PS_PSSID=60279_61684_62325_63144_63324_63568_63563_63584_63617_63639_63645_63646_63657_63675_63693_63728_63715; H_WISE_SIDS=60279_61684_62325_62967_63144_63194_63210_63241_63268_63324_63352_63386_63394_63390_63440; ZFY=eZolgqFOY0Y0f1Qg:AhsGZTGexoRJ:Ah9e:AUlH93hdW8c:C; BIDUPSID=2FEBFD961790CF3B5CB7C06D0DCA03F8; PSTM=1745642057; BAIDUID=5E9B2757D9152FB85FDD6D4AEB4026ED:FG=1; BDUSS=lNbUpGWFZ0RzVPUzVFN0pyaFV6QmlQUEo4ZUVqaGZySFE1RXA3Q3IteFBxZXBuSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE8cw2dPHMNnVG; MAWEBCUID=web_oHAxQIUvPYLZZQqNfndpkAqAJlTBpabDPBBNaCvdMXrswtkRXG; MCITY=-%3A',
    'Sec-Fetch-Dest': 'empty',
    'Cipher-Text': '1750651558786_1750729187022_i6Hv4MM2kerA2l5Sy08xTqv0rfatP5iWJFg0g7Mayw+r008yDmVt5+LMbqKPNK64DD1+kF6MbzjGJlZRqXpUNBzzHylAMDMJPX9HJGyB74hHD0CKwYBuZj+8gIYI+7Tc9G95IoYLfS/LO0qhEmPU61lyUXQrhifC8Fg74uJDmwX+5eHjJGnFaPsUf1QQkSiaCLMwdYzcS0jjkHj/TMhSwHiDtA8u7sO/byj+TsAuklmcqNL5CSG8HNifOyCYyX4Iss1zEAjX5loaESD68EDvIug0SiMRJjbnZN7JN1Q+RFaoghksEzAe2mpcpO7UFWAUxpsMgIHafj/zvGZLbpY/uvRsqwgNZBtHFTZORYtHyVQD5Mq/4+AxrJmECP+/+ke2JdN3E6MmwgjYdfvjwsCYL5ZQjeSsYX9pYW8BW67JJ+aCdgjyp0y52JDH4SF06w1K',
    'Priority': 'u=3, i',
}

city =  {
        1: "济南",
        2: "贵阳",
        3: "黔南",
        4: "六盘水",
        5: "南昌",
        6: "九江",
        7: "鹰潭",
        8: "抚州",
        9: "上饶",
        10: "赣州",
        11: "重庆",
        13: "包头",
        14: "鄂尔多斯",
        15: "巴彦淖尔",
        16: "乌海",
        17: "阿拉善盟",
        19: "锡林郭勒盟",
        20: "呼和浩特",
        21: "赤峰",
        22: "通辽",
        25: "呼伦贝尔",
        28: "武汉",
        29: "大连",
        30: "黄石",
        31: "荆州",
        32: "襄阳",
        33: "黄冈",
        34: "荆门",
        35: "宜昌",
        36: "十堰",
        37: "随州",
        38: "恩施",
        39: "鄂州",
        40: "咸宁",
        41: "孝感",
        42: "仙桃",
        43: "长沙",
        44: "岳阳",
        45: "衡阳",
        46: "株洲",
        47: "湘潭",
        48: "益阳",
        49: "郴州",
        50: "福州",
        51: "莆田",
        52: "三明",
        53: "龙岩",
        54: "厦门",
        55: "泉州",
        56: "漳州",
        57: "上海",
        59: "遵义",
        61: "黔东南",
        65: "湘西",
        66: "娄底",
        67: "怀化",
        68: "常德",
        73: "天门",
        74: "潜江",
        76: "滨州",
        77: "青岛",
        78: "烟台",
        79: "临沂",
        80: "潍坊",
        81: "淄博",
        82: "东营",
        83: "聊城",
        84: "菏泽",
        85: "枣庄",
        86: "德州",
        87: "宁德",
        88: "威海",
        89: "柳州",
        90: "南宁",
        91: "桂林",
        92: "贺州",
        93: "贵港",
        94: "深圳",
        95: "广州",
        96: "宜宾",
        97: "成都",
        98: "绵阳",
        99: "广元",
        100: "遂宁",
        101: "巴中",
        102: "内江",
        103: "泸州",
        104: "南充",
        106: "德阳",
        107: "乐山",
        108: "广安",
        109: "资阳",
        111: "自贡",
        112: "攀枝花",
        113: "达州",
        114: "雅安",
        115: "吉安",
        117: "昆明",
        118: "玉林",
        119: "河池",
        123: "玉溪",
        124: "楚雄",
        125: "南京",
        126: "苏州",
        127: "无锡",
        128: "北海",
        129: "钦州",
        130: "防城港",
        131: "百色",
        132: "梧州",
        133: "东莞",
        134: "丽水",
        135: "金华",
        136: "萍乡",
        137: "景德镇",
        138: "杭州",
        139: "西宁",
        140: "银川",
        141: "石家庄",
        143: "衡水",
        144: "张家口",
        145: "承德",
        146: "秦皇岛",
        147: "廊坊",
        148: "沧州",
        149: "温州",
        150: "沈阳",
        151: "盘锦",
        152: "哈尔滨",
        153: "大庆",
        154: "长春",
        155: "四平",
        156: "连云港",
        157: "淮安",
        158: "扬州",
        159: "泰州",
        160: "盐城",
        161: "徐州",
        162: "常州",
        163: "南通",
        164: "天津",
        165: "西安",
        166: "兰州",
        168: "郑州",
        169: "镇江",
        172: "宿迁",
        173: "铜陵",
        174: "黄山",
        175: "池州",
        176: "宣城",
        177: "巢湖",
        178: "淮南",
        179: "宿州",
        181: "六安",
        182: "滁州",
        183: "淮北",
        184: "阜阳",
        185: "马鞍山",
        186: "安庆",
        187: "蚌埠",
        188: "芜湖",
        189: "合肥",
        191: "辽源",
        194: "松原",
        195: "云浮",
        196: "佛山",
        197: "湛江",
        198: "江门",
        199: "惠州",
        200: "珠海",
        201: "韶关",
        202: "阳江",
        203: "茂名",
        204: "潮州",
        205: "揭阳",
        207: "中山",
        208: "清远",
        209: "肇庆",
        210: "河源",
        211: "梅州",
        212: "汕头",
        213: "汕尾",
        215: "鞍山",
        216: "朝阳",
        217: "锦州",
        218: "铁岭",
        219: "丹东",
        220: "本溪",
        221: "营口",
        222: "抚顺",
        223: "阜新",
        224: "辽阳",
        225: "葫芦岛",
        226: "张家界",
        227: "大同",
        228: "长治",
        229: "忻州",
        230: "晋中",
        231: "太原",
        232: "临汾",
        233: "运城",
        234: "晋城",
        235: "朔州",
        236: "阳泉",
        237: "吕梁",
        239: "海口",
        241: "万宁",
        242: "琼海",
        243: "三亚",
        244: "儋州",
        246: "新余",
        253: "南平",
        256: "宜春",
        259: "保定",
        261: "唐山",
        262: "南阳",
        263: "新乡",
        264: "开封",
        265: "焦作",
        266: "平顶山",
        268: "许昌",
        269: "永州",
        270: "吉林",
        271: "铜川",
        272: "安康",
        273: "宝鸡",
        274: "商洛",
        275: "渭南",
        276: "汉中",
        277: "咸阳",
        278: "榆林",
        280: "石河子",
        281: "庆阳",
        282: "定西",
        283: "武威",
        284: "酒泉",
        285: "张掖",
        286: "嘉峪关",
        287: "台州",
        288: "衢州",
        289: "宁波",
        291: "眉山",
        292: "邯郸",
        293: "邢台",
        295: "伊春",
        297: "大兴安岭",
        300: "黑河",
        301: "鹤岗",
        302: "七台河",
        303: "绍兴",
        304: "嘉兴",
        305: "湖州",
        306: "舟山",
        307: "平凉",
        308: "天水",
        309: "白银",
        310: "吐鲁番",
        311: "昌吉",
        312: "哈密",
        315: "阿克苏",
        317: "克拉玛依",
        318: "博尔塔拉",
        319: "齐齐哈尔",
        320: "佳木斯",
        322: "牡丹江",
        323: "鸡西",
        324: "绥化",
        331: "乌兰察布",
        333: "兴安盟",
        334: "大理",
        335: "昭通",
        337: "红河",
        339: "曲靖",
        342: "丽江",
        343: "金昌",
        344: "陇南",
        346: "临夏",
        350: "临沧",
        352: "济宁",
        353: "泰安",
        356: "莱芜",
        359: "双鸭山",
        366: "日照",
        370: "安阳",
        371: "驻马店",
        373: "信阳",
        374: "鹤壁",
        375: "周口",
        376: "商丘",
        378: "洛阳",
        379: "漯河",
        380: "濮阳",
        381: "三门峡",
        383: "阿勒泰",
        384: "喀什",
        386: "和田",
        391: "亳州",
        395: "吴忠",
        396: "固原",
        401: "延安",
        405: "邵阳",
        407: "通化",
        408: "白山",
        410: "白城",
        417: "甘孜",
        422: "铜仁",
        424: "安顺",
        426: "毕节",
        437: "文山",
        438: "保山",
        456: "东方",
        457: "阿坝",
        466: "拉萨",
        467: "乌鲁木齐",
        472: "石嘴山",
        479: "凉山",
        480: "中卫",
        499: "巴音郭楞",
        506: "来宾",
        514: "北京",
        516: "日喀则",
        520: "伊犁",
        525: "延边",
        563: "塔城",
        582: "五指山",
        588: "黔西南",
        608: "海西",
        652: "海东",
        653: "克孜勒苏柯尔克孜",
        654: "天门仙桃",
        655: "那曲",
        656: "林芝",
        657: "None",
        658: "防城",
        659: "玉树",
        660: "伊犁哈萨克",
        661: "五家渠",
        662: "思茅",
        663: "香港",
        664: "澳门",
        665: "崇左",
        666: "普洱",
        667: "济源",
        668: "西双版纳",
        669: "德宏",
        670: "文昌",
        671: "怒江",
        672: "迪庆",
        673: "甘南",
        674: "陵水黎族自治县",
        675: "澄迈县",
        676: "海南",
        677: "山南",
        678: "昌都",
        679: "乐东黎族自治县",
        680: "临高县",
        681: "定安县",
        682: "海北",
        683: "昌江黎族自治县",
        684: "屯昌县",
        685: "黄南",
        686: "保亭黎族苗族自治县",
        687: "神农架",
        688: "果洛",
        689: "白沙黎族自治县",
        690: "琼中黎族苗族自治县",
        691: "阿里",
        692: "阿拉尔",
        693: "图木舒克"
    }

city_name = "济南"
word = "智能手机"
startDate = "2016-01-01"
endDate = "2016-12-31"


# 解密算法
def decrypt(t, e):
    if not t:
        return ""
    i = list(t)
    n = list(e)
    a = {}
    r = []
    
    # 构建映射字典
    for A in range(len(i) // 2):
        a[i[A]] = i[len(i) // 2 + A]
    
    # 根据映射解密数据
    for o in range(len(n)):
        r.append(a[n[o]])
    
    return ''.join(r)



# 根据城市名称获取对应的城市代码
area = None
for code, name in city.items():
    if name == city_name:
        area = code
        break



response = requests.get(
    f'https://index.baidu.com/api/SearchApi/index?area={area}&word=[[{{"name":"{word}","wordType":1}}]]&startDate={startDate}&endDate={endDate}',
    cookies=cookies,
    headers=headers,
)

data = response.json()
# 打印响应内容，查看实际数据结构
print("响应数据:", data)

# 检查数据结构并安全获取数据
if isinstance(data, dict) and 'data' in data and isinstance(data['data'], dict):
    # 获取用户指数数据
    if 'userIndexes' in data['data'] and isinstance(data['data']['userIndexes'], list) and len(data['data']['userIndexes']) > 0:
        userIndexes = data['data']['userIndexes'][0]
        userIndexes_all = userIndexes.get('all', {}).get('data', '')
        userIndexes_wish = userIndexes.get('wise', {}).get('data', '')
        userIndexes_pc = userIndexes.get('pc', {}).get('data', '')
    else:
        print("无法获取userIndexes数据")
        userIndexes_all = userIndexes_wish = userIndexes_pc = ''
    
    # 获取比率数据
    if 'generalRatio' in data['data'] and isinstance(data['data']['generalRatio'], list) and len(data['data']['generalRatio']) > 0:
        generalRatio = data['data']['generalRatio'][0]
        # 整体数据
        generalRatio_all_avg = generalRatio.get('all', {}).get('avg', 0)  # 整体日均值
        generalRatio_all_yoy = generalRatio.get('all', {}).get('yoy', 0)  # 整体同比
        generalRatio_all_qoq = generalRatio.get('all', {}).get('qoq', 0)  # 整体环比
        # 移动数据
        generalRatio_wise_avg = generalRatio.get('wise', {}).get('avg', 0)  # 移动日均值
        generalRatio_wise_yoy = generalRatio.get('wise', {}).get('yoy', 0)  # 移动同比
        generalRatio_wise_qoq = generalRatio.get('wise', {}).get('qoq', 0)  # 移动环比
        # PC数据
        generalRatio_pc_avg = generalRatio.get('pc', {}).get('avg', 0)  # PC日均值
        generalRatio_pc_yoy = generalRatio.get('pc', {}).get('yoy', 0)  # PC同比
        generalRatio_pc_qoq = generalRatio.get('pc', {}).get('qoq', 0)  # PC环比
    else:
        print("无法获取generalRatio数据")
        generalRatio_all_avg = generalRatio_all_yoy = generalRatio_all_qoq = 0
        generalRatio_wise_avg = generalRatio_wise_yoy = generalRatio_wise_qoq = 0
        generalRatio_pc_avg = generalRatio_pc_yoy = generalRatio_pc_qoq = 0
else:
    print("响应数据格式不正确")
    userIndexes_all = userIndexes_wish = userIndexes_pc = ''
    generalRatio_all_avg = generalRatio_all_yoy = generalRatio_all_qoq = 0
    generalRatio_wise_avg = generalRatio_wise_yoy = generalRatio_wise_qoq = 0
    generalRatio_pc_avg = generalRatio_pc_yoy = generalRatio_pc_qoq = 0

uniqid = data['data']['uniqid']

params = {
    'uniqid': uniqid,
}

response = requests.get('https://index.baidu.com/Interface/ptbk', params=params, cookies=cookies, headers=headers)

key = response.json()['data']

# 解密趋势数据
decrypted_data = decrypt(key, userIndexes_all)
print(decrypted_data)

