import random
import re
import json
import time
import requests
import ddddocr
import numpy as np
import cv2
import base64
import execjs
cookies = {
    '__jdv': '76161171|www.google.com|-|referral|-|1744784915494',
    '__jdu': '1744784915494890501850',
    '3AB9D23F7A4B3CSS': 'jdd037JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2YAAAAMWHVEP34AAAAAAC3JATW7MWVULP4X',
    '_gia_d': '1',
    'areaId': '12',
    'ipLoc-djd': '12-904-0-0',
    'PCSYCityID': 'CN_320000_320100_0',
    'mt_xid': 'V2_52007VwMUV1heW18XSR1ZDWIKGlNZWVJTG0gpCQJmARFXDlhOWRgeHkAANQEUTlRQW1wDGUpVA2IAEQJcX1ANL0oYXwF7AhdOXV9DWhpCGlUOZQoiUm1YYl8ZSBFbBmMKEFZVaFZeHEs%3D',
    'joyytokem': 'babel_3YX2dkYUKf6rBivJ1SxHQLtiYgVSMDFrYlRPbzk5MQ==.WlVge1hTVm1+Vl9UYTFeIFBmNV4GAwcjEVpOYmNeR1MqfRFaHCox.efda990c',
    'shshshfpa': '3e087c73-87d8-1af1-9724-4f9fece50141-1744784919',
    'shshshfpx': '3e087c73-87d8-1af1-9724-4f9fece50141-1744784919',
    'joyya': '0.1744784922.19.06enlrs',
    'sdtoken': 'AAbEsBpEIOVjqTAKCQtvQu17mpMMxgYIiATNT1zpxYjzEBjYkHO4pTJp4ORhVUCtCAvLQMu9rlRwhneJdAUdPoZABHzu2V_tIVZclwGZNl174bI2xsk4ORp2wfwc2dvYnRLmiRSmBDLwtlLhTb2oPn8JTg',
    'shshshfpb': 'BApXSHrJBPvNA_tJjdZ_0RSXtJuhXI7CbBgY5TjZo9xJ1MqF14oG2',
    '__jda': '95931165.1744784915494890501850.1744784915.1744784915.1744784915.1',
    '__jdb': '95931165.3.1744784915494890501850|1.1744784915',
    '__jdc': '95931165',
    'wlfstk_smdl': '95z7jqlmvrm42ngzd1p9ayhtsnoj1nwb',
    '3AB9D23F7A4B3C9B': '7JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2Y',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://passport.jd.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': '__jdv=76161171|www.google.com|-|referral|-|1744784915494; __jdu=1744784915494890501850; areaId=12; ipLoc-djd=12-904-0-0; PCSYCityID=CN_320000_320100_0; mt_xid=V2_52007VwMUV1heW18XSR1ZDWIKGlNZWVJTG0gpCQJmARFXDlhOWRgeHkAANQEUTlRQW1wDGUpVA2IAEQJcX1ANL0oYXwF7AhdOXV9DWhpCGlUOZQoiUm1YYl8ZSBFbBmMKEFZVaFZeHEs%3D; shshshfpa=3e087c73-87d8-1af1-9724-4f9fece50141-1744784919; shshshfpx=3e087c73-87d8-1af1-9724-4f9fece50141-1744784919; joyya=0.1744784922.19.06enlrs; shshshfpb=BApXSHrJBPvNA_tJjdZ_0RSXtJuhXI7CbBgY5TjZo9xJ1MqF14oG2; __jdc=95931165; wlfstk_smdl=g1jnvk6rqmbqhltrvx4y9bo45gu08wzo; 3AB9D23F7A4B3CSS=jdd037JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2YAAAAMWHWPBKMAAAAAADGAT4JO5X3GHKQX; __jda=95931165.1744784915494890501850.1744784915.1744784915.1744790493.2; 3AB9D23F7A4B3C9B=7JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2Y',
}

params = {
    'appId': '1604ebb2287',
    'scene': 'login',
    'product': 'click-bind-suspend',
    'e': '7JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2Y',
    'j': 'jdd037JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2YAAAAMWHVEP34AAAAAAC3JATW7MWVULP4X',
    'lang': 'zh_CN',
    'callback': 'jsonp_08829152317179566',
}


# 基础滑动轨迹
base_slide = [
            [
                "944",
                "341",
                1637921521380
            ],
            [
                "967",
                "369",
                1637921521380
            ],
            [
                "967",
                "369",
                1637921521382
            ],
            [
                "968",
                "369",
                1637921521481
            ],
            [
                "968",
                "369",
                1637921521497
            ],
            [
                "969",
                "369",
                1637921521505
            ],
            [
                "970",
                "369",
                1637921521521
            ],
            [
                "971",
                "369",
                1637921521537
            ],
            [
                "972",
                "369",
                1637921521545
            ],
            [
                "973",
                "369",
                1637921521561
            ],
            [
                "974",
                "369",
                1637921521569
            ],
            [
                "976",
                "369",
                1637921521577
            ],
            [
                "976",
                "369",
                1637921521585
            ],
            [
                "978",
                "369",
                1637921521593
            ],
            [
                "979",
                "369",
                1637921521601
            ],
            [
                "980",
                "369",
                1637921521609
            ],
            [
                "981",
                "369",
                1637921521617
            ],
            [
                "982",
                "369",
                1637921521625
            ],
            [
                "984",
                "369",
                1637921521633
            ],
            [
                "985",
                "369",
                1637921521641
            ],
            [
                "987",
                "369",
                1637921521657
            ],
            [
                "988",
                "369",
                1637921521665
            ],
            [
                "990",
                "369",
                1637921521673
            ],
            [
                "991",
                "369",
                1637921521681
            ],
            [
                "992",
                "369",
                1637921521689
            ],
            [
                "993",
                "369",
                1637921521697
            ],
            [
                "995",
                "369",
                1637921521705
            ],
            [
                "996",
                "369",
                1637921521713
            ],
            [
                "999",
                "369",
                1637921521721
            ],
            [
                "1002",
                "369",
                1637921521729
            ],
            [
                "1004",
                "369",
                1637921521737
            ],
            [
                "1006",
                "369",
                1637921521745
            ],
            [
                "1008",
                "369",
                1637921521753
            ],
            [
                "1009",
                "369",
                1637921521761
            ],
            [
                "1012",
                "369",
                1637921521769
            ],
            [
                "1013",
                "369",
                1637921521777
            ],
            [
                "1015",
                "369",
                1637921521785
            ],
            [
                "1016",
                "369",
                1637921521793
            ],
            [
                "1018",
                "369",
                1637921521801
            ],
            [
                "1020",
                "369",
                1637921521809
            ],
            [
                "1022",
                "369",
                1637921521817
            ],
            [
                "1023",
                "369",
                1637921521825
            ],
            [
                "1026",
                "369",
                1637921521833
            ],
            [
                "1028",
                "369",
                1637921521841
            ],
            [
                "1030",
                "369",
                1637921521849
            ],
            [
                "1032",
                "369",
                1637921521857
            ],
            [
                "1036",
                "369",
                1637921521865
            ],
            [
                "1036",
                "369",
                1637921521873
            ],
            [
                "1040",
                "369",
                1637921521881
            ],
            [
                "1041",
                "369",
                1637921521890
            ],
            [
                "1044",
                "369",
                1637921521897
            ],
            [
                "1046",
                "369",
                1637921521905
            ],
            [
                "1048",
                "369",
                1637921521914
            ],
            [
                "1051",
                "369",
                1637921521921
            ],
            [
                "1052",
                "369",
                1637921521930
            ],
            [
                "1054",
                "369",
                1637921521937
            ],
            [
                "1055",
                "369",
                1637921521945
            ],
            [
                "1057",
                "369",
                1637921521953
            ],
            [
                "1059",
                "369",
                1637921521961
            ],
            [
                "1060",
                "369",
                1637921521969
            ],
            [
                "1064",
                "369",
                1637921521978
            ],
            [
                "1065",
                "369",
                1637921521985
            ],
            [
                "1067",
                "369",
                1637921521993
            ],
            [
                "1069",
                "369",
                1637921522001
            ],
            [
                "1072",
                "369",
                1637921522009
            ],
            [
                "1072",
                "369",
                1637921522017
            ],
            [
                "1076",
                "369",
                1637921522025
            ],
            [
                "1078",
                "369",
                1637921522033
            ],
            [
                "1079",
                "369",
                1637921522041
            ],
            [
                "1082",
                "369",
                1637921522049
            ],
            [
                "1084",
                "369",
                1637921522057
            ],
            [
                "1087",
                "369",
                1637921522065
            ],
            [
                "1089",
                "369",
                1637921522073
            ],
            [
                "1092",
                "369",
                1637921522081
            ],
            [
                "1095",
                "369",
                1637921522089
            ],
            [
                "1097",
                "369",
                1637921522097
            ],
            [
                "1100",
                "369",
                1637921522105
            ],
            [
                "1104",
                "369",
                1637921522113
            ],
            [
                "1104",
                "369",
                1637921522121
            ],
            [
                "1108",
                "369",
                1637921522129
            ],
            [
                "1109",
                "369",
                1637921522137
            ],
            [
                "1111",
                "369",
                1637921522145
            ],
            [
                "1114",
                "369",
                1637921522153
            ],
            [
                "1115",
                "369",
                1637921522161
            ],
            [
                "1116",
                "369",
                1637921522169
            ],
            [
                "1117",
                "369",
                1637921522178
            ],
            [
                "1119",
                "369",
                1637921522185
            ],
            [
                "1120",
                "369",
                1637921522193
            ],
            [
                "1121",
                "369",
                1637921522201
            ],
            [
                "1122",
                "369",
                1637921522209
            ],
            [
                "1124",
                "369",
                1637921522217
            ],
            [
                "1125",
                "369",
                1637921522225
            ],
            [
                "1126",
                "369",
                1637921522233
            ],
            [
                "1128",
                "369",
                1637921522241
            ],
            [
                "1128",
                "369",
                1637921522249
            ],
            [
                "1130",
                "369",
                1637921522257
            ],
            [
                "1131",
                "369",
                1637921522265
            ],
            [
                "1132",
                "369",
                1637921522281
            ],
            [
                "1134",
                "369",
                1637921522289
            ],
            [
                "1136",
                "369",
                1637921522305
            ],
            [
                "1138",
                "369",
                1637921522321
            ],
            [
                "1140",
                "369",
                1637921522329
            ],
            [
                "1141",
                "369",
                1637921522337
            ],
            [
                "1143",
                "369",
                1637921522345
            ],
            [
                "1144",
                "369",
                1637921522353
            ],
            [
                "1144",
                "369",
                1637921522361
            ],
            [
                "1146",
                "369",
                1637921522369
            ],
            [
                "1146",
                "369",
                1637921522381
            ],
            [
                "1147",
                "369",
                1637921522385
            ],
            [
                "1148",
                "369",
                1637921522395
            ],
            [
                "1148",
                "369",
                1637921522401
            ],
            [
                "1149",
                "369",
                1637921522409
            ],
            [
                "1150",
                "369",
                1637921522417
            ],
            [
                "1151",
                "369",
                1637921522425
            ],
            [
                "1152",
                "369",
                1637921522433
            ],
            [
                "1153",
                "369",
                1637921522449
            ],
            [
                "1155",
                "369",
                1637921522457
            ],
            [
                "1156",
                "369",
                1637921522481
            ],
            [
                "1156",
                "369",
                1637921522513
            ],
            [
                "1157",
                "369",
                1637921522529
            ],
            [
                "1158",
                "369",
                1637921522537
            ],
            [
                "1159",
                "369",
                1637921522545
            ],
            [
                "1160",
                "369",
                1637921522561
            ],
            [
                "1162",
                "369",
                1637921522569
            ],
            [
                "1164",
                "369",
                1637921522609
            ],
            [
                "1164",
                "369",
                1637921522617
            ],
            [
                "1165",
                "369",
                1637921522633
            ],
            [
                "1166",
                "369",
                1637921522641
            ],
            [
                "1167",
                "369",
                1637921522649
            ],
            [
                "1168",
                "369",
                1637921522657
            ],
            [
                "1170",
                "369",
                1637921522665
            ],
            [
                "1171",
                "369",
                1637921522673
            ],
            [
                "1172",
                "369",
                1637921522681
            ],
            [
                "1173",
                "369",
                1637921522689
            ],
            [
                "1174",
                "369",
                1637921522697
            ],
            [
                "1175",
                "369",
                1637921522705
            ],
            [
                "1176",
                "369",
                1637921522753
            ],
            [
                "1176",
                "369",
                1637921522769
            ],
            [
                "1177",
                "369",
                1637921522777
            ],
            [
                "1179",
                "369",
                1637921522793
            ],
            [
                "1180",
                "369",
                1637921522809
            ],
            [
                "1180",
                "369",
                1637921522817
            ],
            [
                "1181",
                "369",
                1637921522825
            ],
            [
                "1182",
                "369",
                1637921522849
            ],
            [
                "1183",
                "369",
                1637921522873
            ],
            [
                "1183",
                "369",
                1637921522880
            ],
            [
                "1184",
                "369",
                1637921522897
            ],
            [
                "1184",
                "369",
                1637921522921
            ],
            [
                "1185",
                "369",
                1637921522945
            ],
            [
                "1186",
                "369",
                1637921522961
            ],
            [
                "1188",
                "369",
                1637921522985
            ],
            [
                "1190",
                "369",
                1637921522993
            ],
            [
                "1192",
                "369",
                1637921523001
            ],
            [
                "1193",
                "369",
                1637921523010
            ],
            [
                "1196",
                "369",
                1637921523017
            ],
            [
                "1197",
                "369",
                1637921523033
            ],
            [
                "1199",
                "369",
                1637921523049
            ],
            [
                "1200",
                "369",
                1637921523057
            ],
            [
                "1200",
                "369",
                1637921523065
            ],
            [
                "1201",
                "369",
                1637921523073
            ],
            [
                "1202",
                "369",
                1637921523081
            ],
            [
                "1204",
                "369",
                1637921523089
            ],
            [
                "1204",
                "369",
                1637921523097
            ],
            [
                "1205",
                "369",
                1637921523105
            ],
            [
                "1207",
                "369",
                1637921523113
            ],
            [
                "1208",
                "369",
                1637921523121
            ],
            [
                "1208",
                "369",
                1637921523145
            ],
            [
                "1210",
                "368",
                1637921523201
            ],
            [
                "1211",
                "368",
                1637921523249
            ],
            [
                "1211",
                "368",
                1637921523380
            ],
            [
                "1211",
                "368",
                1637921523481
            ]
        ]
# 晃动的轨迹
push_slide = [
        [
            0,
            "160",
            1638111121463
        ],
        [
            1,
            "160",
            1638111121467
        ],
        [
            2,
            "160",
            1638111121486
        ],
        [
            3,
            "160",
            1638111121498
        ],
        [
            3,
            "159",
            1638111121499
        ],
        [
            4,
            "159",
            1638111121511
        ],
        [
            4,
            "159",
            1638111121520
        ],
        [
            5,
            "159",
            1638111121523
        ],
        [
            6,
            "159",
            1638111121532
        ],
        [
            7,
            "159",
            1638111121538
        ],
        [
            8,
            "159",
            1638111121547
        ],
        [
            8,
            "159",
            1638111121551
        ],
        [
            9,
            "159",
            1638111121555
        ],
        [
            9,
            "158",
            1638111121558
        ],
        [
            10,
            "158",
            1638111121564
        ],
        [
            11,
            "158",
            1638111121570
        ],
        [
            11,
            "157",
            1638111121572
        ],
        [
            12,
            "157",
            1638111121589
        ],
        [
            12,
            "157",
            1638111121644
        ],
        [
            13,
            "157",
            1638111121677
        ],
        [
            14,
            "157",
            1638111121714
        ],
        [
            14,
            "157",
            1638111121715
        ],
        [
            15,
            "157",
            1638111121719
        ],
        [
            16,
            "157",
            1638111121732
        ],
        [
            16,
            "156",
            1638111121735
        ],
        [
            16,
            "156",
            1638111121737
        ],
        [
            17,
            "156",
            1638111121741
        ],
        [
            17,
            "155",
            1638111121745
        ],
        [
            18,
            "155",
            1638111121758
        ],
        [
            19,
            "155",
            1638111121765
        ],
        [
            20,
            "155",
            1638111121782
        ],
        [
            19,
            "155",
            1638111121903
        ],
        [
            18,
            "155",
            1638111121916
        ],
        [
            17,
            "155",
            1638111121925
        ],
        [
            16,
            "155",
            1638111121931
        ],
        [
            16,
            "155",
            1638111121939
        ],
        [
            15,
            "155",
            1638111121947
        ],
        [
            14,
            "155",
            1638111121953
        ],
        [
            13,
            "155",
            1638111121970
        ],
        [
            12,
            "155",
            1638111121975
        ],
        [
            12,
            "155",
            1638111121983
        ],
        [
            12,
            "156",
            1638111121994
        ],
        [
            11,
            "156",
            1638111122009
        ],
        [
            10,
            "156",
            1638111122013
        ],
        [
            9,
            "157",
            1638111122039
        ],
        [
            8,
            "157",
            1638111122053
        ],
        [
            8,
            "157",
            1638111122059
        ],
        [
            7,
            "157",
            1638111122074
        ],
        [
            7,
            "157",
            1638111122078
        ],
        [
            6,
            "157",
            1638111122079
        ],
        [
            5,
            "157",
            1638111122092
        ],
        [
            4,
            "157",
            1638111122123
        ],
        [
            4,
            "158",
            1638111122128
        ],
        [
            4,
            "158",
            1638111122165
        ],
        [
            3,
            "158",
            1638111122240
        ],
        [
            2,
            "158",
            1638111122255
        ],
        [
            2,
            "159",
            1638111122298
        ],
        [
            1,
            "159",
            1638111122337
        ],
        [
            0,
            "159",
            1638111122438
        ],
        [
            0,
            "160",
            1638111122444
        ],
        [
            0,
            "160",
            1638111122489
        ],
        [
            0,
            "160",
            1638111122858
        ]
]

def get_image_url(api_server, image_data):
    """获取图片URL，类似JS中的getImageUrl函数
    
    如果是图片路径，返回完整URL；如果是base64数据，直接返回data URI
    """
    if (image_data.endswith('.png') or
        image_data.endswith('.jpg') or
        image_data.endswith('.webp')):
        return api_server + image_data
    else:
        return 'data:image/png;base64,' + image_data

def slide_match(slice_url, bg_url):
    """根据URL获取图片内容并计算滑动距离"""
    # 处理base64图片数据
    if slice_url.startswith('data:image/png;base64,'):
        import base64
        slice_data = slice_url.split(',')[1]
        slice_bytes = base64.b64decode(slice_data)
    else:
        # 下载图片内容
        slice_bytes = requests.get(slice_url).content
        
    if bg_url.startswith('data:image/png;base64,'):
        import base64
        bg_data = bg_url.split(',')[1]
        bg_bytes = base64.b64decode(bg_data)
    else:
        bg_bytes = requests.get(bg_url).content
    
    # 保存图片用于调试
    with open("front.png", mode='wb') as f:
        f.write(slice_bytes)
    with open("bg.png", mode='wb') as f:
        f.write(bg_bytes)
    
    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slice_bytes, bg_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    # print(x1, y1, x2, y2)  # 114 45 194 125
    distance = int(x1 * 278 / 360 + 25)
    return distance
def offer(distance):
    """根据距离生成轨迹"""
    index = 0
    slide = []
    indexTime = str(int(time.time()))[:9]
    
    for item in base_slide:
        index += 1
        item_copy = item.copy()
        item_copy[2] = int(indexTime + str(item[2])[-4:])
        
        if int(item[0]) >= (distance + int(base_slide[0][0])):
            slide = base_slide[:index]
            slide.append(
                [str(distance + int(base_slide[0][0])), item[1], item[2] + 700 + int(random.random() * 1000)]
            )
            break
    
    last = int(slide[-1][0].split('.')[0])
    pIndex = 0
    
    for item in push_slide:
        if pIndex == 0 or pIndex == len(push_slide) - 1:
            times = slide[-1][2]
        else:
            times = slide[-1][2] + (push_slide[pIndex + 1][2] - push_slide[pIndex][2])
        
        slide.append([str(item[0] + last), "369", times])
        pIndex += 1
    
    return slide

# 计算成功率
success_count = 0
total_attempts = 20

for attempt in range(total_attempts):
    print(f"尝试第 {attempt+1} 次验证")

    response = requests.get('https://iv.jd.com/slide/g.html', params=params, cookies=cookies, headers=headers)
    response_text = response.text
    # 解析响应数据
    json_str = re.search(r'jsonp_\d+\((.*)\)', response_text).group(1)
    data = json.loads(json_str)

    # 提取需要的字段
    patch = data.get('patch')
    bg = data.get('bg')
    challenge = data.get('challenge')
    api_server = data.get('api_server')
    static_servers = data.get('static_servers')
    y = data.get('y')
    o = data.get('o')
    # 获取图片URL
    bg_url = get_image_url(api_server, bg)
    patch_url = get_image_url(api_server, patch)

    # 计算滑动距离
    distance = slide_match(patch_url, bg_url)

    # 生成轨迹
    track_data = offer(distance)

    with open('demo.js','r',encoding='utf-8') as f:
        js = f.read()
        ctx = execjs.compile(js)
    d = ctx.call('getD', track_data)  # 传入轨迹数据
    c = challenge
    time.sleep(5)
    
    params = {
        'd': d,
        'c': c,
        'w': '278',#固定
        'appId': '1604ebb2287',#固定
        'scene': 'login',#固定
        'product': 'click-bind-suspend',#固定
        'e': '7JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2Y',#固定
        'j': 'jdd037JDGMPWYR7EN3GTXNFJ4V7WLKXNDQE24T2PF2CP5QP6U3MGCVOCN274ZMIJSUNKHKKOECUVQHV3IV7P24YL7BU2K2YAAAAMWHVEP34AAAAAAC3JATW7MWVULP4X',#固定
        's': '191933150913710945',#固定
        'o': '15968588744', #用户名
        'o1': '0',
        'u': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fd', #固定
        'lang': 'zh_CN', #固定
        'callback': f'jsonp_{random.randint(10000000000000000, 99999999999999999)}',#随机生成
    }

    response = requests.get('https://iv.jd.com/slide/s.html', params=params, cookies=cookies, headers=headers)
    print(response.text)
    
    # 判断是否成功
    if '"message":"success"' in response.text:
        success_count += 1
        print(f"验证成功!")
    else:
        print(f"验证失败!")
    
    # 每次验证之间稍微等待一下
    time.sleep(5)

# 计算成功率
success_rate = (success_count / total_attempts) * 100
print(f"\n总共尝试: {total_attempts} 次")
print(f"成功次数: {success_count} 次")
print(f"成功率: {success_rate:.2f}%")