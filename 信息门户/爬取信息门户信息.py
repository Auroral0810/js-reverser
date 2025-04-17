import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
import sys

# 如果是在 Windows 下，导入 winsound 用于播放提示音
if sys.platform.startswith('win'):
    import winsound


    def beep():
        # winsound.Beep(频率, 时长[毫秒])
        winsound.Beep(1000, 500)
else:
    def beep():
        # 非 Windows 环境简单用打印控制字符代替
        print('\a')

# 全局变量
cookies = {}
headers = {}
csvWriter = None
f = None


# 初始化
def Init():
    global cookies, headers, csvWriter, f

    # 日志设置：INFO 级别、同时打印时间、日志级别和具体信息
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='app.log',  # 如果想把日志写到文件，就取消注释并指定文件名
    )

    logging.info("程序初始化中...")

    f = open("信息门户.csv", 'w', encoding='utf-8', newline='')
    fieldnames = ['序号', '课程编号', '课程名称', '学分', '教学班', '平时', '期中', '期末', '总评', '课程类别',
                  '课程性质']
    csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
    csvWriter.writeheader()

    cookies = {
        'ASP.NET_SessionId': 'zxfemrys5lzysg4ezrbfzsmx',
        'wengine_new_ticket': '1144f1341c68b6e6',
        '_d_id': '09fb27caaf27a27c25f6e40b782e07',
        '.ASPXCOOKIEDEMO': '25E0CC5C0BCF3E35264C3A112D0FDDC4323A51166DC86B2D39154C8E11533600A752EF02E8FD13DC78852595E00D57BFFEF77A5B0A48D9EDE41F4DDA69E3B42A68BF637A36A8CA71614373B99D2CF6CA0A1CA63609916799DC4502AA934EF82403C4337A16B1D057802372201C1C2C35AF2D23D9F4309AA68C67986355110B3F12DC8F61A5395614535F66CCCDF2C768C1B76D7A6B40A6558491BE2A3B5D4366',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'ASP.NET_SessionId=zxfemrys5lzysg4ezrbfzsmx; wengine_new_ticket=1144f1341c68b6e6; _d_id=09fb27caaf27a27c25f6e40b782e07; .ASPXCOOKIEDEMO=25E0CC5C0BCF3E35264C3A112D0FDDC4323A51166DC86B2D39154C8E11533600A752EF02E8FD13DC78852595E00D57BFFEF77A5B0A48D9EDE41F4DDA69E3B42A68BF637A36A8CA71614373B99D2CF6CA0A1CA63609916799DC4502AA934EF82403C4337A16B1D057802372201C1C2C35AF2D23D9F4309AA68C67986355110B3F12DC8F61A5395614535F66CCCDF2C768C1B76D7A6B40A6558491BE2A3B5D4366',
        'Pragma': 'no-cache',
        'Referer': 'http://jwc.nau.edu.cn/Students/default.aspx?r=0.654511110230587&d=A5E0F1CAECD043AF66DDC70D1ADBACC5',
        'Upgrade-Insecure-Requests': '1js 混淆_源码乱码赛',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    logging.info("初始化完成")


def get_html(url):
    # 发送 GET 请求
    try:
        # 禁用 HTTPS 请求的证书警告（可选）
        requests.packages.urllib3.disable_warnings()

        response = requests.get(url, cookies=cookies, headers=headers, verify=False)
        response.encoding = 'utf-8'  # 设置响应编码
        html = BeautifulSoup(response.text, 'html.parser')
        return html
    except Exception as e:
        logging.error(f"获取页面出现异常: {e}")
        return None


def parse_html(html):
    """
    负责“页面的解析”逻辑，并将解析后的结果写入 CSV。
    每次写入时会清除文件中除了表头的内容。
    """
    global f

    if not html:
        logging.warning("HTML 内容为空，无法解析。")
        print("HTML 内容为空，无法解析。")
        return []

    logging.info("开始解析页面...")
    print("开始解析页面...")
    # 解析 HTML 文档
    rows = html.find('table').find_all('tr')[2:]  # 去掉表头
    result_list = []

    for row in rows:
        id = row.find_all('td')[0].text.strip()  # 序号
        course_id = row.find_all('td')[1].text.strip()
        course_name = row.find_all('td')[2].text.strip()
        credit = row.find_all('td')[3].text.strip()
        class_name = row.find_all('td')[4].text.strip()
        usual_grade = row.find_all('td')[5].text.strip()
        midterm_grade = row.find_all('td')[6].text.strip()
        final_grade = row.find_all('td')[7].text.strip()
        total_grade = row.find_all('td')[8].text.strip()
        course_type = row.find_all('td')[9].text.strip()
        course_nature = row.find_all('td')[10].text.strip()

        row_data = {
            '序号': id,
            '课程编号': course_id,
            '课程名称': course_name,
            '学分': credit,
            '教学班': class_name,
            '平时': usual_grade,
            '期中': midterm_grade,
            '期末': final_grade,
            '总评': total_grade,
            '课程类别': course_type,
            '课程性质': course_nature,
        }
        result_list.append(row_data)

    # 清空文件内容并写入当前数据
    logging.info("清空文件内容并重新写入当前数据...")
    with open("信息门户.csv", 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['序号', '课程编号', '课程名称', '学分', '教学班', '平时', '期中', '期末', '总评', '课程类别', '课程性质']
        csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
        csvWriter.writeheader()  # 写入表头
        csvWriter.writerows(result_list)  # 写入所有数据

    logging.info("解析页面完成")
    return result_list

def main():
    # 初始化
    Init()

    url = 'http://jwc.nau.edu.cn/Students/MyCourse.aspx'

    # 用于对比新旧数据
    previous_data = None

    while True:
        logging.info("开始执行轮询，获取页面数据...")
        print("开始执行轮询，获取页面数据...")
        # 获取 HTML
        html = get_html(url)
        # 解析 HTML 并写入 CSV，同时拿到解析数据列表
        current_data = parse_html(html)

        # 如果发现与上一次数据不同，则发声提醒
        if previous_data is not None and current_data != previous_data:
            logging.info("检测到页面数据发生更新，发出提示音...")
            print("页面数据更新了！!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            beep()
            return
        else:
            print("页面数据无变化或是首次检测。")
            logging.info("页面数据无变化或是首次检测。")

        previous_data = current_data

        # 间隔 10s 再下一轮
        logging.info("轮询结束，等待 180 秒...")
        print("轮询结束，等待 180 秒...")
        time.sleep(180)


if __name__ == "__main__":
    main()