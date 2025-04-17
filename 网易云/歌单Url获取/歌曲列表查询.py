import json
import requests
import pandas as pd
import execjs
import time

csrf_token = '9cd8b49e79fc2eb8f3197e0052ee6c24'
cookies = {
    '_ntes_nnid': '20e442659d79d6c0a6d8c7aa82074f90,1713420636872',
    '_ntes_nuid': '20e442659d79d6c0a6d8c7aa82074f90',
    '_ga': 'GA1.1.1492695192.1720416908',
    '_clck': '1b0kmll%7C2%7Cfna%7C0%7C1650',
    '_ga_PTGVM6PCHS': 'GS1.1.1720416907.1.1.1720416967.0.0.0',
    'NMTID': '00OwXvszvaHOwafPkKrrViMZHRN75wAAAGUTzapVQ',
    '_iuqxldmzr_': '32',
    'WEVNSM': '1.0.0',
    'WNMCID': 'dehirs.1736495770956.01.0',
    'sDeviceId': 'YD-iCVIUS%2FKN7FFQwAURVaEvOm79jRIU%2BDe',
    '__snaker__id': 'AK8s3TXWYoxBcwJl',
    'NTES_P_UTID': 'vdw2AldMLX7G1OaMM0r0NecnctFFlope|1736655377',
    'WM_TID': 'uxmJeToLndBBAFBUERPXM7ymw7jNHf0M',
    'WM_NI': 'AizfDob%2BjjFKgW6B5nbH8v9hxDtYBMx1k0a9oskwvgxVTrALSOl2Klk6OeHi4dV%2BWUTYqiLOZ84EBafIgV7%2FnbEG6q6YaDB7Oc%2BXqzDukF1rkJ45r6RHJQSvlTLOfZEuS0c%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee83d07bb79ba584ef44a3a88fb6c55b928f9facd76f86eda389cc338abc878bc92af0fea7c3b92a83b7b687c765a2f5a68bc541a589faa3b866a298f897bc64bc9cbcbac147bcefa5d1e433adada598f56dbc8a9c93c4489191a4d3ca68a9ea8186cb63f8bc9accd65f9887bf8acf459ae8fca6c16ba697a9b7b625aebe8ba8b57bf687afa5c13d8dbde5b9f47288aba5a7b47aa996fcd6f13e929886b2d27eb08c84b0e55287ab9dd1e237e2a3',
    'ntes_utid': 'tid._.owZ6VcKgvXtARlEBVVeXeRznlZ8xfp59._.0',
    'csrfToken': 'TCHm6FCms6LeucjmhW9mLkLG',
    'ntes_kaola_ad': '1',
    'playerid': '13971697',
    'JSESSIONID-WYYY': 'KiON9ZO4tUYROGCTsDFPtxUIGyUKnPlSv4aseRno%2BiImq1WJI%5CfQ31AP46RXVSIilZregoI4jeoXmIrZ7v8lnsfElc2TIAlrow5J%5C%2Ft7JbeyJZmI2ffO5Sj0QOA%2F2sYcFjedlrf2R15ISm6g%2BnFRfKxWucTU7dn%2Fe74Z4pakGbgo4JOe%3A1744536055109',
    'gdxidpyhxdE': 'uyevgMI39qQ8IYUIQlwMGHKQxB2mWgmtZEXqa5Mhn2ngPjizCpwZ5DTphnN0OXrt4EmqJWCjXmexOsdnV%2FS9Y7%2BipGMnI882tKd84cA70q4E%2BCbWUy2a%2B63wuxG%5CpxuzQjN7lgoL5wvokRlVu6RjHi4Lt6Wy%2FAzNmT%2F5X9rcb6JkhluR%3A1744535250203',
    'NETS_utid': 'tYyV5RHcWFmPsS2F9SvDz5XA2OlTwsA3',
    'MUSIC_U': '0020900F0A5512C0846D4A0E57F73420C186EDF7E8B125B8B9AD879579904A51B250C5130954C2D0DE8B12077E2E5ED170E122AE6B6E7C02F469FEE52873AA9A0BFD2BA4FF72D0D48FFE8C89BED535D2FB816798F44516C3BDD623D8A6E5E98C9CA8ECD50A6C73D1F9348973D67EAAC3387157611D7AA6F7FB38C3727DEE6509B2BB3E991080C67AABFAB5FDFD0A8B74B3BDE64E3F186A8403AFE96B8909DC20106BA9CA51574DE43A69721F30FDDB8E4580ED95E23403D41F428416A0CE9D0E2C7B0384890449329CC02849FEF81680CE00E17BAA435E4A88CB0B7E4CB7C8E21FBD41B9A4FEC78FD826825619AA40047CC173D0B093FD0E31CE6752DB2365C8763DEC6BE2E57CDACACEDCFA63AC91F638365B8BFE0A6D19E7F952B240713EAA952053A01612AF187D64BA3F5BE97475554409A55BAC7731387DC45BCD0CF0C01AE176E4BF6D400087DDA791C9456DE78A0628DEB02FF6E744093255E5CB1AEBB4',
    '__remember_me': 'true',
    '__csrf': '9cd8b49e79fc2eb8f3197e0052ee6c24',
    'NTES_YD_SESS': 'jQGFYv.DrRpzVv4pSn7q4Q09_Qp4sO1aqDtzTchCxxBvrOhUrIJ5LfL0x_ACR5xrTJNy0d9hQaXuMfvqB45zfOTEHdSBk6_nnb.4zBVyOj8shnjA8S35UQQKOrD4SWIhRjJUWgblxLWAmUTbZ_.Fr85O4JJrjwsQj72qTFD6Xt.EKz0HGa_.x4T8ViSmcL.aviuVX6tWh6NrGu1KiubTim1.WFNUpSylEkmlg82PUPqiQ',
    'S_INFO': '1744534562|0|0&60##|18114461685',
    'P_INFO': '18114461685|1744534562|1|music|00&99|null&null&null#jis&320100#10#0|&0||18114461685',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://music.163.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://music.163.com/search/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_ntes_nnid=20e442659d79d6c0a6d8c7aa82074f90,1713420636872; _ntes_nuid=20e442659d79d6c0a6d8c7aa82074f90; _ga=GA1.1.1492695192.1720416908; _clck=1b0kmll%7C2%7Cfna%7C0%7C1650; _ga_PTGVM6PCHS=GS1.1.1720416907.1.1.1720416967.0.0.0; NMTID=00OwXvszvaHOwafPkKrrViMZHRN75wAAAGUTzapVQ; _iuqxldmzr_=32; WEVNSM=1.0.0; WNMCID=dehirs.1736495770956.01.0; sDeviceId=YD-iCVIUS%2FKN7FFQwAURVaEvOm79jRIU%2BDe; __snaker__id=AK8s3TXWYoxBcwJl; NTES_P_UTID=vdw2AldMLX7G1OaMM0r0NecnctFFlope|1736655377; WM_TID=uxmJeToLndBBAFBUERPXM7ymw7jNHf0M; WM_NI=AizfDob%2BjjFKgW6B5nbH8v9hxDtYBMx1k0a9oskwvgxVTrALSOl2Klk6OeHi4dV%2BWUTYqiLOZ84EBafIgV7%2FnbEG6q6YaDB7Oc%2BXqzDukF1rkJ45r6RHJQSvlTLOfZEuS0c%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83d07bb79ba584ef44a3a88fb6c55b928f9facd76f86eda389cc338abc878bc92af0fea7c3b92a83b7b687c765a2f5a68bc541a589faa3b866a298f897bc64bc9cbcbac147bcefa5d1e433adada598f56dbc8a9c93c4489191a4d3ca68a9ea8186cb63f8bc9accd65f9887bf8acf459ae8fca6c16ba697a9b7b625aebe8ba8b57bf687afa5c13d8dbde5b9f47288aba5a7b47aa996fcd6f13e929886b2d27eb08c84b0e55287ab9dd1e237e2a3; ntes_utid=tid._.owZ6VcKgvXtARlEBVVeXeRznlZ8xfp59._.0; csrfToken=TCHm6FCms6LeucjmhW9mLkLG; ntes_kaola_ad=1; playerid=13971697; JSESSIONID-WYYY=KiON9ZO4tUYROGCTsDFPtxUIGyUKnPlSv4aseRno%2BiImq1WJI%5CfQ31AP46RXVSIilZregoI4jeoXmIrZ7v8lnsfElc2TIAlrow5J%5C%2Ft7JbeyJZmI2ffO5Sj0QOA%2F2sYcFjedlrf2R15ISm6g%2BnFRfKxWucTU7dn%2Fe74Z4pakGbgo4JOe%3A1744536055109; gdxidpyhxdE=uyevgMI39qQ8IYUIQlwMGHKQxB2mWgmtZEXqa5Mhn2ngPjizCpwZ5DTphnN0OXrt4EmqJWCjXmexOsdnV%2FS9Y7%2BipGMnI882tKd84cA70q4E%2BCbWUy2a%2B63wuxG%5CpxuzQjN7lgoL5wvokRlVu6RjHi4Lt6Wy%2FAzNmT%2F5X9rcb6JkhluR%3A1744535250203; NETS_utid=tYyV5RHcWFmPsS2F9SvDz5XA2OlTwsA3; MUSIC_U=0020900F0A5512C0846D4A0E57F73420C186EDF7E8B125B8B9AD879579904A51B250C5130954C2D0DE8B12077E2E5ED170E122AE6B6E7C02F469FEE52873AA9A0BFD2BA4FF72D0D48FFE8C89BED535D2FB816798F44516C3BDD623D8A6E5E98C9CA8ECD50A6C73D1F9348973D67EAAC3387157611D7AA6F7FB38C3727DEE6509B2BB3E991080C67AABFAB5FDFD0A8B74B3BDE64E3F186A8403AFE96B8909DC20106BA9CA51574DE43A69721F30FDDB8E4580ED95E23403D41F428416A0CE9D0E2C7B0384890449329CC02849FEF81680CE00E17BAA435E4A88CB0B7E4CB7C8E21FBD41B9A4FEC78FD826825619AA40047CC173D0B093FD0E31CE6752DB2365C8763DEC6BE2E57CDACACEDCFA63AC91F638365B8BFE0A6D19E7F952B240713EAA952053A01612AF187D64BA3F5BE97475554409A55BAC7731387DC45BCD0CF0C01AE176E4BF6D400087DDA791C9456DE78A0628DEB02FF6E744093255E5CB1AEBB4; __remember_me=true; __csrf=9cd8b49e79fc2eb8f3197e0052ee6c24; NTES_YD_SESS=jQGFYv.DrRpzVv4pSn7q4Q09_Qp4sO1aqDtzTchCxxBvrOhUrIJ5LfL0x_ACR5xrTJNy0d9hQaXuMfvqB45zfOTEHdSBk6_nnb.4zBVyOj8shnjA8S35UQQKOrD4SWIhRjJUWgblxLWAmUTbZ_.Fr85O4JJrjwsQj72qTFD6Xt.EKz0HGa_.x4T8ViSmcL.aviuVX6tWh6NrGu1KiubTim1.WFNUpSylEkmlg82PUPqiQ; S_INFO=1744534562|0|0&60##|18114461685; P_INFO=18114461685|1744534562|1|music|00&99|null&null&null#jis&320100#10#0|&0||18114461685',
}
params = {
    'csrf_token': csrf_token,
}

# 加载JS加密函数
with open('netease.js','r',encoding='utf-8') as f:
    js = f.read()
ctx = execjs.compile(js)

# 创建一个空列表来存储所有歌曲信息
all_song_data = []

# 搜索关键词
search_keyword = "邓紫棋"
# 标准每页数量
limit = 30
# 起始偏移量
offset = 0
# 总歌曲数量
total_song_count = None

# 第一次请求，获取总歌曲数量
i5n = {
    "hlpretag": "<span class=\"s-fc7\">",
    "hlposttag": "</span>",
    "id": "7763",
    "s": search_keyword,
    "type": "1",
    "offset": "0",
    "total": "false",
    "limit": str(limit),
    "csrf_token": csrf_token
}
i5n_params = json.dumps(i5n)

# 加密参数
result = ctx.call('d', i5n_params,
        '010001',
    '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7',
    '0CoJUm6Qyw8W8jud')
data_params = result['encText']
data_encSecKey = result['encSecKey']

data = {
    'params': data_params,
    'encSecKey': data_encSecKey
}

# 发送请求
response = requests.post(
    'https://music.163.com/weapi/cloudsearch/get/web',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
).json()

# 获取总歌曲数量
total_song_count = response['result'].get('songCount', 0)
print(f"搜索结果共有 {total_song_count} 首歌曲")

# 计算总页数
total_pages = (total_song_count + limit - 1) // limit

# 处理第一页数据
songs = response['result']['songs']
for song in songs:
    # 提取歌手信息
    artists = ', '.join([artist['name'] for artist in song.get('ar', [])])

    # 提取专辑信息
    album = song.get('al', {})
    album_name = album.get('name', '')
    album_pic = album.get('picUrl', '')

    # 提取歌曲基本信息
    song_info = {
        '歌曲名': song.get('name', ''),
        '歌曲ID': song.get('id', ''),
        '歌手': artists,
        '专辑': album_name,
        '专辑封面': album_pic,
        '时长(ms)': song.get('dt', 0),
        '热度': song.get('pop', 0),
        '发行时间': song.get('publishTime', ''),
        'MV ID': song.get('mv', 0)
    }

    # 添加到列表
    all_song_data.append(song_info)

print(f"已获取第1页数据，共{len(songs)}首歌曲")
offset += len(songs)

# 获取剩余页数据
for page in range(2, total_pages + 1):
    # 对于最后一页，调整limit为剩余的歌曲数量
    if page == total_pages:
        current_limit = total_song_count - offset
    else:
        current_limit = limit
    
    print(f"正在获取第{page}页数据，偏移量：{offset}，本页数量：{current_limit}")
    
    # 构建请求参数
    i5n = {
        "hlpretag": "<span class=\"s-fc7\">",
        "hlposttag": "</span>",
        "id": "7763",
        "s": search_keyword,
        "type": "1",
        "offset": str(offset),
        "total": "false",
        "limit": str(current_limit),
        "csrf_token": csrf_token
    }
    i5n_params = json.dumps(i5n)
    
    # 加密参数
    result = ctx.call('d', i5n_params,
            '010001',
        '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7',
        '0CoJUm6Qyw8W8jud')
    data_params = result['encText']
    data_encSecKey = result['encSecKey']
    
    data = {
        'params': data_params,
        'encSecKey': data_encSecKey
    }

    # 发送请求
    response = requests.post(
        'https://music.163.com/weapi/cloudsearch/get/web',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    ).json()
    
    # 获取歌曲列表
    songs = response['result']['songs']
    
    # 处理本页歌曲数据
    for song in songs:
        # 提取歌手信息
        artists = ', '.join([artist['name'] for artist in song.get('ar', [])])

        # 提取专辑信息
        album = song.get('al', {})
        album_name = album.get('name', '')
        album_pic = album.get('picUrl', '')

        # 提取歌曲基本信息
        song_info = {
            '歌曲名': song.get('name', ''),
            '歌曲ID': song.get('id', ''),
            '歌手': artists,
            '专辑': album_name,
            '专辑封面': album_pic,
            '时长(ms)': song.get('dt', 0),
            '热度': song.get('pop', 0),
            '发行时间': song.get('publishTime', ''),
            'MV ID': song.get('mv', 0)
        }

        # 添加到列表
        all_song_data.append(song_info)
    
    print(f"已获取第{page}页数据，共{len(songs)}首歌曲，当前总计：{len(all_song_data)}首")
    
    # 更新偏移量
    offset += len(songs)
    
    # 防止请求过快，添加延时
    time.sleep(1)

print(f"已成功获取全部 {len(all_song_data)} 首歌曲")

# 创建DataFrame并保存为Excel
df = pd.DataFrame(all_song_data)
excel_file = f'网易云音乐_{search_keyword}_歌曲列表.xlsx'
df.to_excel(excel_file, index=False)
print(f"已成功将{len(all_song_data)}首歌曲信息保存到 {excel_file}")