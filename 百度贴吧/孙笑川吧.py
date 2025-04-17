import requests
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import time
import json
import html
import requests

cookies = {
    'XFI': '2a92e9b0-1afb-11f0-b196-d745e06b6291',
    'XFCS': '0C6B285A602C5CCE02525772AD598858FCDA404969B0EF4FAE569ACF7F8DDE25',
    'XFT': 'GrvIDj0wYKHp0+XimmdGxCMFrdsJDY7FFrvb611tLVE=',
    'PSTM': '1731552480',
    'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
    'MAWEBCUID': 'web_tLOJyPtvAKoNvfswvwjvwtbamyQjfWNzPnCuIEzQLaJxrnyKwQ',
    'MCITY': '-222%3A',
    'BAIDUID_BFESS': '49990CEA0201CA78E55DCE22CB98235B:FG=1',
    'H_PS_PSSID': '61027_62325_62338_62636_62330_62825_62843_62869_62878_62892_62893_62899_62918_62928_62921',
    'ariaDefaultTheme': 'undefined',
    '__bid_n': '18c42450fcc02886ca93f5',
    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqNvjLowygVbK9xeY8tvcT1iO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
    'BDUSS': 'hEfmV-dy1PNXdsMUtoS0xhd1ZVRnlyek9uS0NUdHBTVi1lOEhOeGtPUkhVeWRvSUFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEfG~2dHxv9nY0',
    'BDUSS_BFESS': 'hEfmV-dy1PNXdsMUtoS0xhd1ZVRnlyek9uS0NUdHBTVi1lOEhOeGtPUkhVeWRvSUFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEfG~2dHxv9nY0',
    'STOKEN': '14b1541d1332940e5a3f55fde33a9d01c652147f5d0eebe2f9b24e9243893611',
    'Hm_lvt_292b2e1608b0823c1cb6beef7243ef34': '1742396943,1744816776',
    'HMACCOUNT': '764A7B05229BE584',
    'BAIDU_WISE_UID': 'wapp_1744816775723_609',
    'USER_JUMP': '-1',
    'BAIDU_SSP_lcr': 'https://www.google.com/',
    'st_key_id': '17',
    'arialoadData': 'false',
    'wise_device': '0',
    '6011451794_FRSVideoUploadTip': '1',
    'video_bubble6011451794': '1',
    'ariatheme': '0',
    'ariafontScale': '1',
    'ariaoldFixedStatus': 'false',
    'ariaStatus': 'false',
    'ZFY': '1dE:Aaql44yYmGtN5mv:AVhLf3KMtY35hOD:BvmznMmSI8:C',
    'XFI': '71f3b020-1af9-11f0-b6b1-b3b3c15f261c',
    'XFCS': '6A406F45288B38BC0D42D43EF44EC5DEA11F25F1CBF56AF1F41815AD7515587E',
    'XFT': 'A2PjKUU25Q6rK4HnsssDRdlJw7mrTZS3OTmfyRElghU=',
    'Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34': '1744832650',
    'BA_HECTOR': '2g8k858gahahag2k8l808121208k061k0024a24',
    'ab_sr': '1.0.1_MDE4Y2FkOTE1NGM2MTJmM2NjZGIwYjVhNWY2ZDFhNGE2Y2RkODI0NjZiYzNkNzUwNjNjNWM4MTc4YzdhMmY2NTRmNmZiNjMyMTg5YWQ0MzU0MDY0MmRmMjVjNGQxMTc2YzBkMGE5N2QyOTczZmVjYjgxNjZhMzkwMDFjMDVhYmM3ZGIyOTM2NzY4ZGYzZTEwOGMzMTQ0ZGM2OGRjYmNlZDFiM2IyMzQ1OTI5YWJjZTllN2FhODE0MzI5ZmYyMGI4',
    'st_data': '1b7959726d026e47f7da96ee99c5461dcbc589b982a914604572941e17b8ead76378b920eaf5b94a7677f8d63ef7fa841730270a32190269917d39a1ac92b8019485573c25c1f1937ec295362cdb8aac205be5e8c6d2a1013712886890475bb2b0d8d4a621f223f19d8842ddd6cfd54667e3c4d533c3ad25e18c1748a3469f374f521c3bc004cb07592dfcb72773001c',
    'st_sign': 'f1d68c3e',
    'tb_as_data': 'abefea374a4c57ed7139403295669c597985bfee49a1802824b6ca63393ab142df1a0152cd05810bb7aaeeb93054af7148e2ef40e32a642b93f64f6349532c3be0b32bc6a3cae7ef63ecac14f9e8c98444083fcc845a72cf9e03c9edf233aa59',
    'RT': '"z=1&dm=baidu.com&si=f13b43ce-40e1-4fd7-98ea-b0ac26650c14&ss=m9k7vgwi&sl=2d&tt=36vq&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4jkwf&ul=4tjqv&hd=4tjyk"',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'XFI=2a92e9b0-1afb-11f0-b196-d745e06b6291; XFCS=0C6B285A602C5CCE02525772AD598858FCDA404969B0EF4FAE569ACF7F8DDE25; XFT=GrvIDj0wYKHp0+XimmdGxCMFrdsJDY7FFrvb611tLVE=; PSTM=1731552480; BIDUPSID=950D047CF79B4A0F8F86462CD08D849F; MAWEBCUID=web_tLOJyPtvAKoNvfswvwjvwtbamyQjfWNzPnCuIEzQLaJxrnyKwQ; MCITY=-222%3A; BAIDUID_BFESS=49990CEA0201CA78E55DCE22CB98235B:FG=1; H_PS_PSSID=61027_62325_62338_62636_62330_62825_62843_62869_62878_62892_62893_62899_62918_62928_62921; ariaDefaultTheme=undefined; __bid_n=18c42450fcc02886ca93f5; ppfuid=FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqNvjLowygVbK9xeY8tvcT1iO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP; BDUSS=hEfmV-dy1PNXdsMUtoS0xhd1ZVRnlyek9uS0NUdHBTVi1lOEhOeGtPUkhVeWRvSUFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEfG~2dHxv9nY0; BDUSS_BFESS=hEfmV-dy1PNXdsMUtoS0xhd1ZVRnlyek9uS0NUdHBTVi1lOEhOeGtPUkhVeWRvSUFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEfG~2dHxv9nY0; STOKEN=14b1541d1332940e5a3f55fde33a9d01c652147f5d0eebe2f9b24e9243893611; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1742396943,1744816776; HMACCOUNT=764A7B05229BE584; BAIDU_WISE_UID=wapp_1744816775723_609; USER_JUMP=-1; BAIDU_SSP_lcr=https://www.google.com/; st_key_id=17; arialoadData=false; wise_device=0; 6011451794_FRSVideoUploadTip=1; video_bubble6011451794=1; ariatheme=0; ariafontScale=1; ariaoldFixedStatus=false; ariaStatus=false; ZFY=1dE:Aaql44yYmGtN5mv:AVhLf3KMtY35hOD:BvmznMmSI8:C; XFI=71f3b020-1af9-11f0-b6b1-b3b3c15f261c; XFCS=6A406F45288B38BC0D42D43EF44EC5DEA11F25F1CBF56AF1F41815AD7515587E; XFT=A2PjKUU25Q6rK4HnsssDRdlJw7mrTZS3OTmfyRElghU=; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1744832650; BA_HECTOR=2g8k858gahahag2k8l808121208k061k0024a24; ab_sr=1.0.1_MDE4Y2FkOTE1NGM2MTJmM2NjZGIwYjVhNWY2ZDFhNGE2Y2RkODI0NjZiYzNkNzUwNjNjNWM4MTc4YzdhMmY2NTRmNmZiNjMyMTg5YWQ0MzU0MDY0MmRmMjVjNGQxMTc2YzBkMGE5N2QyOTczZmVjYjgxNjZhMzkwMDFjMDVhYmM3ZGIyOTM2NzY4ZGYzZTEwOGMzMTQ0ZGM2OGRjYmNlZDFiM2IyMzQ1OTI5YWJjZTllN2FhODE0MzI5ZmYyMGI4; st_data=1b7959726d026e47f7da96ee99c5461dcbc589b982a914604572941e17b8ead76378b920eaf5b94a7677f8d63ef7fa841730270a32190269917d39a1ac92b8019485573c25c1f1937ec295362cdb8aac205be5e8c6d2a1013712886890475bb2b0d8d4a621f223f19d8842ddd6cfd54667e3c4d533c3ad25e18c1748a3469f374f521c3bc004cb07592dfcb72773001c; st_sign=f1d68c3e; tb_as_data=abefea374a4c57ed7139403295669c597985bfee49a1802824b6ca63393ab142df1a0152cd05810bb7aaeeb93054af7148e2ef40e32a642b93f64f6349532c3be0b32bc6a3cae7ef63ecac14f9e8c98444083fcc845a72cf9e03c9edf233aa59; RT="z=1&dm=baidu.com&si=f13b43ce-40e1-4fd7-98ea-b0ac26650c14&ss=m9k7vgwi&sl=2d&tt=36vq&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=4jkwf&ul=4tjqv&hd=4tjyk"',
}

def get_tieba_posts(url):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有帖子的li标签
    posts = soup.find_all('li', class_='j_thread_list')
    
    result = []
    for post in posts:
        # 获取帖子ID
        post_id = post.get('data-tid')
        
        # 获取帖子标题和链接
        title_element = post.find('a', class_='j_th_tit')
        title = title_element.get('title') if title_element else ''
        link = 'https://tieba.baidu.com' + title_element.get('href') if title_element else ''
        
        # 获取作者
        author_element = post.find('span', class_='tb_icon_author')
        author = author_element.get('title').replace('主题作者: ', '') if author_element else ''
        
        # 获取回复数
        reply_element = post.find('span', class_='threadlist_rep_num')
        reply_num = int(reply_element.text.strip()) if reply_element else 0
        
        post_info = {
            'id': post_id,
            'title': title,
            'link': link,
            'author': author,
            'reply_num': reply_num
        }
        result.append(post_info)
    
    return result
def get_tieba_posts_page(page_num):
    """获取指定页码的贴吧帖子"""
    # 计算pn值：(页数-1)*50
    pn = (page_num - 1) * 50
    
    params = {
        'kw': '孙笑川',
        'ie': 'utf-8',
        'pn': str(pn),
    }
    
    try:
        response = requests.get('https://tieba.baidu.com/f', params=params, cookies=cookies, headers=headers)
        html_content = response.text
        
        # 使用正则表达式提取帖子信息
        # 1. 提取帖子标题和链接
        title_pattern = r'<a rel="noopener" href="([^"]+)" title="([^"]+)" target="_blank" class="j_th_tit'
        titles = re.findall(title_pattern, html_content)
        
        # 2. 提取帖子作者
        author_pattern = r'title="主题作者: ([^"]+)"'
        authors = re.findall(author_pattern, html_content)
        
        # 3. 提取发帖时间
        time_pattern = r'<span class="pull-right is_show_create_time" title="创建时间">([^<]+)</span>'
        times = re.findall(time_pattern, html_content)
        
        # 4. 提取帖子内容摘要
        content_pattern = r'<div class="threadlist_abs threadlist_abs_onlyline ">\s*([^<]+)\s*</div>'
        contents = re.findall(content_pattern, html_content)
        
        # 5. 提取回复信息
        reply_pattern = r'<span class="tb_icon_author_rely j_replyer " title="最后回复人: ([^"]+)">'
        repliers = re.findall(reply_pattern, html_content)
        
        reply_time_pattern = r'<span class="threadlist_reply_date pull_right j_reply_data" title="最后回复时间">\s*([^<]+)\s*</span>'
        reply_times = re.findall(reply_time_pattern, html_content)
        
        # 6. 提取回复数量 - 修正正则表达式
        reply_num_pattern = r'<span class="threadlist_rep_num center_text"\s*title="回复">(\d+)</span>'
        reply_nums = re.findall(reply_num_pattern, html_content)
        # print(reply_nums)
        
        # 7. 提取帖子ID
        post_id_pattern = r'<li class="[^"]*j_thread_list[^"]*" data-field=\'[^\']*"id":(\d+)[^\']*\''
        post_ids = re.findall(post_id_pattern, html_content)
        
        # 8. 提取是否精品和置顶
        is_good_pattern = r'"is_good":([^,]+),'
        is_goods = re.findall(is_good_pattern, html_content)
        
        is_top_pattern = r'"is_top":([^,]+),'
        is_tops = re.findall(is_top_pattern, html_content)
        
        # 整合结果
        posts = []
        for i in range(min(len(titles), len(authors), len(times))):
            # 确保内容摘要存在
            content_summary = contents[i].strip() if i < len(contents) else ""
            
            # 从链接中提取帖子ID
            link = "https://tieba.baidu.com" + titles[i][0]
            post_id_from_link = link.split('/')[-1]
            
            # 获取回复数
            reply_num = int(reply_nums[i]) if i < len(reply_nums) else 0
            # 获取是否精品和置顶
            is_good = is_goods[i].lower() == 'true' if i < len(is_goods) else False
            is_top = is_tops[i].lower() == 'true' if i < len(is_tops) else False
            
            post = {
                "标题": titles[i][1],
                "链接": link,
                "作者": authors[i],
                "发布时间": times[i].strip(),
                "内容摘要": content_summary,
                "页码": page_num,
                "帖子ID": post_id_from_link,
                "回复数量": reply_num,
                "是否精品": is_good,
                "是否置顶": is_top
            }
            
            # 如果有回复信息，也添加进去
            if i < len(repliers):
                post["最后回复人"] = repliers[i]
            if i < len(reply_times):
                post["最后回复时间"] = reply_times[i].strip()
                
            posts.append(post)
        
        return posts
    except Exception as e:
        print(f"获取第{page_num}页时出错: {e}")
        return []

def get_all_tieba_posts():
    """获取前100页的贴吧帖子"""
    all_posts = []
    max_pages = 10000  # 设置爬取前100页
    
    print("开始爬取前100页的帖子...")
    
    for page_num in range(1, max_pages + 1):
        print(f"正在爬取第 {page_num} 页...")
        posts = get_tieba_posts_page(page_num)
        
        if not posts:
            print(f"第 {page_num} 页没有数据")
        else:
            all_posts.extend(posts)
            print(f"第 {page_num} 页成功获取 {len(posts)} 个帖子")
        
        # 添加延时，避免请求过于频繁
        time.sleep(2)
    
    print(f"爬取完成，共获取 {len(all_posts)} 个帖子")
    return all_posts

def save_to_excel(posts, filename=None):
    """将帖子数据保存到Excel文件"""
    # 如果没有指定文件名，使用当前日期时间作为文件名
    if filename is None:
        now = datetime.now()
        filename = f"孙笑川吧_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # 创建DataFrame
    df = pd.DataFrame(posts)
    
    # 保存到Excel
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='贴吧帖子', index=False)
    
    # 获取xlsxwriter对象
    workbook = writer.book
    worksheet = writer.sheets['贴吧帖子']
    
    # 设置列宽
    worksheet.set_column('A:A', 30)  # 标题列宽
    worksheet.set_column('B:B', 40)  # 链接列宽
    worksheet.set_column('C:C', 15)  # 作者列宽
    worksheet.set_column('D:D', 10)  # 发布时间列宽
    worksheet.set_column('E:E', 50)  # 内容摘要列宽
    worksheet.set_column('F:F', 8)   # 页码列宽
    worksheet.set_column('G:G', 15)  # 帖子ID列宽
    worksheet.set_column('H:H', 10)  # 回复数量列宽
    worksheet.set_column('I:I', 10)  # 是否精品列宽
    worksheet.set_column('J:J', 10)  # 是否置顶列宽
    worksheet.set_column('K:K', 15)  # 最后回复人列宽
    worksheet.set_column('L:L', 15)  # 最后回复时间列宽
    
    # 保存文件
    writer.close()
    
    print(f"数据已成功保存到 {filename}")
    return filename

# 主程序
if __name__ == "__main__":
    # 获取前100页的帖子
    all_posts = get_all_tieba_posts()
    print(f"共找到 {len(all_posts)} 个帖子")

    
    # 保存到Excel
    excel_file = save_to_excel(all_posts)
    print(f"所有帖子数据已保存到：{excel_file}")
