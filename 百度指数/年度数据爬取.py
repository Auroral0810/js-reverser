import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from fake_useragent import UserAgent
import execjs


ua = UserAgent()
useragent=ua.chrome#随机生成谷歌浏览器的useragent，想要各种浏览器的改chrome为randome


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
# 请求接口获取数据
def get_data(city_number, word, startDate, endDate):
    # 构建请求URL
    url = f'https://index.baidu.com/api/SearchApi/index?area={city_number}&word=[[{{"name":"{word}","wordType":1}}]]&startDate={startDate}&endDate={endDate}'
    word1 = f'{word},手机'
    url_cipyter = f'https://index.baidu.com/v2/main/index.html#/trend/{word}?words={word1}'
    
    # BAIDUID=0847F44F05CED62B7984A1F61457C322:FG=1; BA_HECTOR=802k052l8h2k8lag8124g00l8lqtev1k0j6c922; BDORZ=AE84CDB3A529C0F8A2B9DCDD1D18B695; bd_af=1; SE_LAUNCH=5%3A29090993_0%3A29090993; fuid=FOCoIC3q5fKa8fgJnwzbE3sZaS3poGTofPItBD67MTHOloTQtOTfZukshuG%2BjikL0BLZATIysMZjIWM25YkzcOzx42AgVwH%2BQiRkYeSdQRX7pD6IAtw%2FB1vAZBFSZg6KPVooT%2F7PbHY2R%2F%2BpdmY%2BloQCXA%2FjWsVU99N5aeUCl4BoVg9vfhdYe%2FeDrTJH07dCJvcEdb68gHdA2UsMYRAo09TqDPKZgfjFmOPY2vLt%2Bg3HFyRaugxWDX%2FKOkX6bggSw5tr3KUJUzjo%2Br5dGtAgbWBgQBPOtnE8BQ7BIltSXGS3lmrP4M1iwuxRGegVZNCeowaXPHngVQMRm6PtZO2pdLl69fslWV7RhqHxc8QZna8S7h9hTwtHueurzSUO31NYkICx44IlIgvBq7Ab5JQWQ9ckH3PfLajwqrF6nlcEKy6A05bkLvd7%2BDniS5jg8ohLtIfEwLYPDMJ%2F1KfrzX109PrDoJ4LyeuAIWWfI6C6KGFFO9ZDRdnbL6n8KLyBHKCEuerHm37EZLal5KwM6tCLmMheeciRI7bZS61mzwLJvT54XIWkktu4TY6WXC6fyKrok1ZcoSdyVwupM9EDeOngYM963nQ6KHi7INdTJoQ%2B430GlkeTLZiPZ8AuCF%2BPgL8Rbni4tAhmgyEPkLb4lD4V%2BiBe%2Bw8usmWA7PWIi4qEuSHCaQeG2ysZGa%2FGX7VWAylrasHjUj1CSrUe7jPtRI3cnwET2bral0E%2FJK6%2FilWpD1KUBSPLSwZYy3pvDmxbzbLCu8DswBB2N%2FRkMW%2FthSpNgujQ08vd%2BHpXRB%2FzhfSUcIaHPhEvjg4XLL%2Br9axZtHmhrOK6OPZXIGGPLkewVepfhPPF%2F%2F07OJKnyfGTZ2nKT6txq%2FVVBT01vdKk6zo6c08eh1M6RLDSrNAOF6HajDa6MPmMLGC9%2F3W1TAj7Jir%2FzxIMkRVl1yvsSYgu4PZBQGX7EOWfx0oHud59wS6fx2Wqhmzi406j6mSnJyTBY%2FhVtaWgL3a9RS1naVWoqIay8kq8uBpQD2w%2BfEsel1%2Fheiao8nPBpgxFG%2BfK82%2Bm1ib8f1MnzYS2uBw%2F%2BeqDXtP%2BEes4VbZvKn%2Bi7GkjiUXx1C06iO5tvXxI56x2WnpCBxHUSkZmxkkJ644Fymto2YVGh4UQwuo%2Fu5GI9LEKglalBZoWi5CJfNSGrHvwtel1Tyjo%2FVw%3D; logTraceID=6467aeb1f0e9428cc998ccca36cbeee88205fd251fdf6d6b82; LASTLOGINTYPE=0; BAIDU_WISE_UID=wpass_1745459778784_873; rsv_i=67f7gB0iuqDMuoKX4gZf91pfRsv4k4yy0F0jiC6kP5W7Si+e2uIk82gbjcGsOnJFeHZZe/LHEPBdbFbVQazEMp9qGElYZpU; H_WISE_SIDS=110085_621489_626068_628198_632161_633612_637557_632292_632299_641765_642950_643584_641767_644665_644641_645101_645227_644369_645169_645434_645925_646541_646274_646561_647080_646774_646741_645030_646084_647709_647689_647904_644402_647925_648254_648404_648428_648453_648452_648467_648465_648470_648479_648476_648449_648500_648474_648498_648504_648503_648506_648473_648460_648355_648448_648438_648595_648727_648852_648995_649074_649061_649038_649034_649159_648093_649235_649325_649361_649344_641262_649532_649592_649658_649652_649233_649715_649818_649775_649869_649848_649777_649910_649960_649935_649919_646202_650035_650047_650071_650057_650041_639680_649893_644053_650213_650203_650209_650220_650084_650256_650262_650287_650329_650324_650322_650328_650418_650452_650521_650302; BDUSS=dzZzNGSUhQU2JBb2ZxQXpqWWNSNlRuOH5MWnpWbnVITFFsfmwtN203LXRKekZvRUFBQUFBJCQAAAAAAQAAAAEAAAAhEzOXQzIwQWIxODEyMjAzNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK2aCWitmgloWD; STOKEN=5c3b70fe4bafddc80cb589ffcbd1b8283eceecf949818e6fa6c88c2c5f21bffd; PTOKEN=7c2a60f32225e9be6d5b42fd9e253795; UBI=fi_PncwhpxZ%7ETaJc9Kk3IgEPU3f3FHRWh4Y; SEARCH_MARKET_URL=http%3A//wk.baidu.com/ndWapLaunch/browse/view/e257afcaf11dc281e53a580216fc700aba685278%3Ffr%3Dlaunch_ad%26utm_source%3Dbdss-WD%26utm_medium%3Dcpc%26keyword%3D%25E7%2599%25BE%25E5%25BA%25A6%25E6%2596%2587%25E5%25BA%2593%25E4%25BC%259A%25E5%2591%2598%25E5%2593%25AA%25E9%2587%258C%25E5%258F%2596%25E6%25B6%2588%25E8%2587%25AA%25E5%258A%25A8%25E7%25BB%25AD%25E8%25B4%25B9%26utm_account%3DSS-bdtg883%26e_creative%3D108585211755%26e_keywordid%3D950416350347%26query_reqid%3DuHIWm17WmHRsnjKBnj03n-tk%26bd_vid%3D8764586727771552885%26_wkts_%3D1745322131306%26needWelcomeRecommand%3D1; __bid_n=196657fe3c192962d04961

    # cookies = {
    #     'BAIDU_WISE_UID': 'wapp_1744869667916_527',
    #     'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    #     'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    #     'PSTM': '1744882843',
    #     'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
    #     'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
    #     '__bid_n': '18c42450fcc02886ca93f5',
    #     'BDUSS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    #     'H_PS_PSSID': '62325_63140_63324_63401_63584_63638_63643_63647_63659_63724_63712_63749_63756',
    #     'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271,1750768658,1751079964,1751181661',
    #     'HMACCOUNT': 'DDF927EE5DF25454',
    #     'bdindexid': 'f66itdoq39iiem694ho44h70n3',
    #     'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05011941100edWg33s3DV8OV0CJlsjP0DBLlBTc0b5Jwg9dqdt5vVlB%2BsFyuefaEWS81mVoiy2BAKuTdFm%2BOcxSI7kjW9mmyi0kuPQ8NUMh1HwJd0wGsV4Y1Pnz1WD0PhkojzJXZI19rQUTGBrXRzP6705tEO3cTiVxdviICWVMnKOcZw6DUJmUo9FxgqK%2FqsZ%2BBQeHOClvb0hgJS%2FOgwGbDbDLlWxsm77HPeusF4P%2FydHB4KOn27CmvJMA2LuRZv2ZIR9G7rIYsJoOf5mRnIZzUZUg2mSf1PpfmVE4oMC%2B25%2F4GwPWi9gKLEvNu3hI466jMrNuwAkvezVMVZLDHPaabaauoUgBLQ%3D%3D01766774846724411156782136199821',
    #     '__cas__rn__': '501194110',
    #     '__cas__st__212': 'a7f09d59c3bc1a452c603a087d576a16f04a4b672d409f08bb0a3d40204c45fa5e4522bea1de0d302a1a38af',
    #     '__cas__id__212': '69563296',
    #     'CPTK_212': '552996471',
    #     'CPID_212': '69563296',
    #     'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mchccgwg&sl=g&tt=mzh&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
    #     'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1751182559',
    #     'ab_sr': '1.0.1_NzNhOWYxMmI5MDFkMDBiMTVkYmRjMzVmNzI2OGRiZTRmOGUyMjFkZTRmZTc4NDY4N2NkZDA0ZTk2OGM3YTUyMzI0OGYxNzIwNDlkYWI0N2JmZTY4ZTZlZDY1NWNlMjEyMTY2ZGE3MmM0MTY0NTM3OTk3YzMyZjkxODRiY2RmZDBmZGRlOWU4MDY1YTA1MTk0MjVkYzc4MzJmN2QwNWYwOQ==',
    #     'BDUSS_BFESS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    #
    # }
    cookies = {
    'BAIDU_WISE_UID': 'wapp_1744869667916_527',
    'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    'PSTM': '1744882843',
    'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
    'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
    '__bid_n': '18c42450fcc02886ca93f5',
    'BDUSS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    'H_PS_PSSID': '62325_63140_63324_63401_63584_63638_63643_63647_63659_63724_63712_63749_63756',
    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1751181661,1751210338,1751213710,1751243261',
    'HMACCOUNT': 'DDF927EE5DF25454',
    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a0501255709984FEi9UEKliGHWSHXZ6oYd17WpvF4UpTpi0S%2FMkYmfiNAqK1M0jX%2FRqCmmXdrDEKGvA1CsZHHN0J6ilBmnFop%2F8%2B6kq5c6KzFnXz9L69g0uZoezgZ760lQ3%2FUb20RzzXNbk81Z8UtRs%2FPC06mHQdR82YpdoLC1zwfBABKuYj%2BJSlme6%2FJz8fJh4BK9HFN2Wz3RmPvMQj1MCnGMm79Lwvycr04s7oj8%2FcIHSQ4uxrGwiuKRkD%2BW0QDFVw%2FJv4smgVX%2BEyECGZwW%2BO0NxOEr65Tck9T8YE1aDXFoucNxhXryU4iEwfAomNvsLSlXKVdvtppWhAXzpyghmbU5%2BSA%2BJUIw%3D%3D34813889920872661871379264310074',
    '__cas__rn__': '501255709',
    '__cas__st__212': '8667dbced52a16d95b022f15621d78910c7bb72005387e9d4326869b031a70d6907b3470b90ff2b24eeeb20d',
    '__cas__id__212': '69563296',
    'CPTK_212': '1532251641',
    'CPID_212': '69563296',
    'bdindexid': '42r0a9do4patuegrcfi2pcmkl7',
    'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mcis9mum&sl=7&tt=5lm&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1751270136',
    'ab_sr': '1.0.1_YmM1MGE2MDViMmQ0OGU2MmFmZWJkYmE4Zjc2MWU2MzNkNTZlYzMxMDllNjg5NDhhNjJkNzY1Yjk3YzFiYzVlMjI1NjJiZjRkYTdjYjBmNGM3YmMyNjQzNDQ4MzhlMTJjMDVmNmZiY2Y0ZjFlNWM5NDQ2NTQ4YTViNmMxYTdlMTAwMTk2MjlhY2Y0ZDUyMThmYjU4YzFkN2NjODZmZDA4Yg==',
        'BDUSS_BFESS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    }# cookies = {
    # 'BAIDU_WISE_UID': 'wapp_1744869667916_527',
    # 'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    # 'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
    # 'PSTM': '1744882843',
    # 'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
    # 'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
    # 'H_PS_PSSID': '61027_62325_62485_62967_63042_63044_63140_63074_63189_63194_63210_63226_63242_63244_63249_63253',
    # '__bid_n': '18c42450fcc02886ca93f5',
    # 'BDUSS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    # 'bdindexid': 'lbjajepvj48ik2npi9efsppm32',
    # 'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271,1750768658',
    # 'HMACCOUNT': 'DDF927EE5DF25454',
    # 'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007811055iHW74BOJZpR8fIXeOGeBx5M6y7phE8fVUA6A5%2FT9V%2FlsHxmc8X4j0VNC%2F9LwP2zmQdfNMKxnxGOsso9i6z5EBqAppSnxsfJ24BKZ2HbQq2iyXFknWsLKsmgGjJw1B4gnKBPQaKQ17uqsRk7kRjIMxMQ9I09xx2H5mLprCONYZIbGfHaYp1BTvGG6rrGQtybXmNaMwxxsWVpk5FXOZ9eQ4K3Wkdor%2FZuxF6vZoZZboMBLW7wT1x8%2FnAf2M49uCYlG7sR%2B%2F2vpsj8pGF1p7tZvY9RSVz9Zuo7VoVT643%2FkQeIjx7VwkUgLo5BwXQ4wGzR60WWFDjO93A1KqcAW0Cufkg%3D%3D19042442273391681046897992923981',
    # '__cas__st__212': 'bbc20157a0eb310bf75a06fe47852349e3fdc208669fbd29ee3ef0f2081a8a25ae8d802c8eff57ed1747ef5a',
    # '__cas__id__212': '69563296',
    # '__cas__rn__': '500781105',
    # 'CPTK_212': '1747583717',
    # 'CPID_212': '69563296',
    # 'RT': 'z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mcbaf2i5&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf',
    # 'BDUSS_BFESS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    # 'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750816072',
    # 'ab_sr': '1.0.1_ZmY5M2E1ZjhkMDE3NzEyODI3ZjhiZjhhMzJkNTg1NDUyODI4Y2M3OTA0ZjFkNTRjM2JjOWEwOGViZWFiNDRkNDFiMjRlMjZjNTU4ZDYyMjc0YjkyNjcyYzBhM2Q4M2E1Yjk5NWYxNjJiM2UwZjNkNjRmZGQ3ODZmNjEyMzZmNDcyZDg5MmY1NmRlYTlmODJiZDJjMmZmODEzMWRjOWNlNQ==',
    # }

    with open('Cipher-Text.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cipyer_text=ctx.call('ascToken',url_cipyter)
    print(cipyer_text)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Cipher-Text': cipyer_text,
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': useragent,
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        # 'Cookie': 'BAIDU_WISE_UID=wapp_1744869667916_527; BAIDUID=FF85DF65CC7463F3726D5301B69C0672:FG=1; BAIDUID_BFESS=FF85DF65CC7463F3726D5301B69C0672:FG=1; PSTM=1744882843; BIDUPSID=950D047CF79B4A0F8F86462CD08D849F; ZFY=:AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C; __bid_n=18c42450fcc02886ca93f5; BDUSS=3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa; H_PS_PSSID=62325_63140_63324_63401_63584_63638_63643_63647_63659_63724_63712_63749_63756; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1751181661,1751210338,1751213710,1751243261; HMACCOUNT=DDF927EE5DF25454; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a0501255709984FEi9UEKliGHWSHXZ6oYd17WpvF4UpTpi0S%2FMkYmfiNAqK1M0jX%2FRqCmmXdrDEKGvA1CsZHHN0J6ilBmnFop%2F8%2B6kq5c6KzFnXz9L69g0uZoezgZ760lQ3%2FUb20RzzXNbk81Z8UtRs%2FPC06mHQdR82YpdoLC1zwfBABKuYj%2BJSlme6%2FJz8fJh4BK9HFN2Wz3RmPvMQj1MCnGMm79Lwvycr04s7oj8%2FcIHSQ4uxrGwiuKRkD%2BW0QDFVw%2FJv4smgVX%2BEyECGZwW%2BO0NxOEr65Tck9T8YE1aDXFoucNxhXryU4iEwfAomNvsLSlXKVdvtppWhAXzpyghmbU5%2BSA%2BJUIw%3D%3D34813889920872661871379264310074; __cas__rn__=501255709; __cas__st__212=8667dbced52a16d95b022f15621d78910c7bb72005387e9d4326869b031a70d6907b3470b90ff2b24eeeb20d; __cas__id__212=69563296; CPTK_212=1532251641; CPID_212=69563296; bdindexid=42r0a9do4patuegrcfi2pcmkl7; RT="z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mcis9mum&sl=7&tt=5lm&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1751270136; ab_sr=1.0.1_MGEzOGQ3MjY3MjNkYmE3OTk0ZGEzNDJkNjhmZGU1MTZjZjc1OWMzNzBkODA0NDhkNWUxNGM2MTQzNDhhNzVhNjgzYjQ4ODQxOGY5MmY4NDYxYTY1YjJjYjNlNDZkYjkyMTJmMTNlN2U0NjIzZGJlMWI1MDI4OWEyMjExODIwNzAxYTQ2MzAxODhjMzBhOTA0ZTE3NGM4ZTNjY2UyNjVkMQ==; BDUSS_BFESS=3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
    }

    # 发送请求获取数据
    response = requests.get(url, cookies=cookies,headers=headers)
    time.sleep(1)
    return response.json()

# 分析数据
def analyze_data(data, city_number, city_name, word, year):
    try:
        # 获取统计数据
        generalRatio_all_avg = data['data']['generalRatio'][0]['all']['avg'] # 整体日均值
        generalRatio_wise_avg = data['data']['generalRatio'][0]['wise']['avg'] # 移动日均值
        generalRatio_pc_avg = data['data']['generalRatio'][0]['pc']['avg'] # PC日均值

        # 计算年份的天数
        def get_days_in_year(year):
            if year == 2025:  # 2025年只统计到6月23日
                return (datetime(2025, 6, 23) - datetime(2025, 1, 1)).days + 1
            elif (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # 闰年
                return 366
            else:  # 平年
                return 365
        
        # 获取当前年份的天数
        days_in_year = get_days_in_year(year)
        
        # 创建数据框
        df = pd.DataFrame({
            '搜索关键词': [word],
            '城市': [city_name],
            '年份': [year],
            '整体日均值': [generalRatio_all_avg],
            '移动日均值': [generalRatio_wise_avg],
            'PC日均值': [generalRatio_pc_avg],
            '整体年总值': [generalRatio_all_avg * days_in_year],
            '移动年总值': [generalRatio_wise_avg * days_in_year],
            'PC年总值': [generalRatio_pc_avg * days_in_year]
        })
        
        return df
    except (TypeError, KeyError) as e:
        print(f"数据解析错误: {e}")
        print(f"原始数据: {data}")
        # 返回空数据框
        return pd.DataFrame()


if __name__ == "__main__":
    # 读取关键词列表
    try:
        word_list = pd.read_excel('数字设备和服务关键词.xlsx')
        keywords = word_list['关键词'].tolist()
        print(f"成功读取到 {len(keywords)} 个关键词")
    except Exception as e:
        print(f"读取关键词文件失败: {str(e)}")
        print("使用默认关键词'数字政务APP'继续")
        keywords = ["数字政务APP"]
    
    years = range(2016, 2026)  # 2016年到2025年
    
    # 用于合并所有数据的DataFrame
    all_data = []
    
    # 循环遍历所有关键词
    for word in keywords:
        print(f"\n开始爬取关键词: {word}")
        
        # 循环遍历所有年份
        for year in years:
            startDate = f"{year}-01-01"
            endDate = f"{year}-12-31"
            
            # 如果是2025年，结束日期为2025-06-23
            if year == 2025:
                endDate = "2025-06-23"
                
            # 循环遍历所有城市
            for city_number, city_name in city.items():
                print(f"正在获取 {word} 在 {city_name}({city_number}) 的 {year}年 数据...")
                try:
                    data = get_data(city_number, word, startDate, endDate)
                    df = analyze_data(data, city_number, city_name, word, year)
                    
                    if not df.empty:
                        # 将当前数据添加到总数据中
                        all_data.append(df)
                    
                    print(f"{word} 在 {city_name} {year}年 数据获取成功")
                except Exception as e:
                    print(f"{word} 在 {city_name} {year}年 数据获取失败: {str(e)}") 
                break
            break
        break
    
    # 合并所有数据
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 保存到Excel文件
        excel_path = "百度指数_全部关键词.xlsx"
        combined_df.to_excel(excel_path, index=False)
        
        print(f"所有数据已保存到 {excel_path}")
    else:
        print("没有获取到任何有效数据")
