import json
import pandas as pd

# 假设JSON数据已经从API获取，这里我们使用提供的数据
data_json = '''
{
    "code": 200,
    "data": {
        "class": [],
        "list": [
            {
                "alias_name": "",
                "cover_url": "https://study-cdn-img.jobpi.cn/upload/2024-03-08/1709883583859.jpeg",
                "id": 1736,
                "is_redirect": "0",
                "logo": "550640",
                "logo_url": "https://study-cdn-img.jobpi.cn/upload/2025-03-13/17418492381115.png",
                "major": [
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 5400,
                        "is_redirect": "0",
                        "name": "审计学（资源环境审计方向）",
                        "open_video_url": "",
                        "organ_id": 1736,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    },
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 5401,
                        "is_redirect": "0",
                        "name": "审计学（政府审计方向）",
                        "open_video_url": "",
                        "organ_id": 1736,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    },
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 5402,
                        "is_redirect": "0",
                        "name": "审计学",
                        "open_video_url": "",
                        "organ_id": 1736,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    }
                ],
                "name": "政府审计学院",
                "open_video_url": "",
                "redirect_url": ""
            },
            {
                "alias_name": "",
                "cover_url": "https://study-cdn-img.jobpi.cn/upload/2023-11-13/16998702050972.png",
                "id": 1737,
                "is_redirect": "0",
                "logo": "550642",
                "logo_url": "https://study-cdn-img.jobpi.cn/upload/2025-03-13/17418492467777.png",
                "major": [
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 5403,
                        "is_redirect": "0",
                        "name": "审计学（国际内部审计IAEP方向）",
                        "open_video_url": "",
                        "organ_id": 1737,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    },
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 5404,
                        "is_redirect": "0",
                        "name": "审计学（数智内部审计方向）",
                        "open_video_url": "",
                        "organ_id": 1737,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    },
                    {
                        "alias_name": "",
                        "class_id": 0,
                        "class_str": "",
                        "cover_url": "",
                        "degree": "",
                        "des_url": "",
                        "id": 19150,
                        "is_redirect": "0",
                        "name": "内部审计（内部审计方向）",
                        "open_video_url": "",
                        "organ_id": 1737,
                        "organ_name": "",
                        "pdf_id_url": "",
                        "pdf_name": "",
                        "redirect_url": "",
                        "type": "",
                        "video_cover_url": "",
                        "xl": 0,
                        "xz": ""
                    }
                ],
                "name": "内部审计学院",
                "open_video_url": "",
                "redirect_url": ""
            }
        ]
    }
}
'''

# 将JSON字符串解析为Python对象
parsed_data = json.loads(data_json)

# 提取学院信息
colleges = []
majors = []

for college in parsed_data["data"]["list"]:
    # 提取学院信息
    college_info = {
        "id": college["id"],
        "name": college["name"],
        "cover_url": college["cover_url"],
        "logo_url": college["logo_url"],
        "is_redirect": college["is_redirect"]
    }
    colleges.append(college_info)

    # 提取每个学院的专业信息
    for major in college["major"]:
        major_info = {
            "id": major["id"],
            "name": major["name"],
            "organ_id": major["organ_id"],
            "college_name": college["name"],  # 添加学院名称便于关联
            "is_redirect": major["is_redirect"],
            "degree": major["degree"],
            "xl": major["xl"],
            "xz": major["xz"]
        }
        majors.append(major_info)

# 创建DataFrame用于展示
colleges_df = pd.DataFrame(colleges)
majors_df = pd.DataFrame(majors)

# 显示学院信息
print("学院信息:")
print(colleges_df)
print("\n专业信息:")
print(majors_df)

# 保存到CSV文件
colleges_df.to_csv('colleges.csv', index=False, encoding='utf-8-sig')
majors_df.to_csv('majors.csv', index=False, encoding='utf-8-sig')

print("\n数据已保存到colleges.csv和majors.csv")


# 修改你的原始代码，将提取的数据结合到网络请求中
def fetch_and_process_data():
    import requests

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://zs.nau.edu.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    params = {
        'sch_school_id': '19024',
        'page': '1',
        'page_size': '999',
        'version': '1',
    }

    try:
        response = requests.get('https://job-web-api.jobpi.cn/organ', params=params, headers=headers)
        data = response.json()

        # 提取学院和专业信息
        colleges = []
        majors = []

        for college in data["data"]["list"]:
            # 提取学院信息
            college_info = {
                "id": college["id"],
                "name": college["name"],
                "cover_url": college["cover_url"],
                "logo_url": college["logo_url"],
                "is_redirect": college["is_redirect"]
            }
            colleges.append(college_info)

            # 提取每个学院的专业信息
            for major in college["major"]:
                major_info = {
                    "id": major["id"],
                    "name": major["name"],
                    "organ_id": major["organ_id"],
                    "college_name": college["name"],
                    "is_redirect": major["is_redirect"],
                    "degree": major["degree"],
                    "xl": major["xl"],
                    "xz": major["xz"]
                }
                majors.append(major_info)

        # 创建DataFrame
        colleges_df = pd.DataFrame(colleges)
        majors_df = pd.DataFrame(majors)

        # 保存到CSV
        colleges_df.to_csv('colleges_live.csv', index=False, encoding='utf-8-sig')
        majors_df.to_csv('majors_live.csv', index=False, encoding='utf-8-sig')

        print("实时数据已保存到colleges_live.csv和majors_live.csv")

    except Exception as e:
        print(f"获取数据时出错: {e}")

# 如果需要从API获取实时数据，可以取消下面这行的注释
fetch_and_process_data()