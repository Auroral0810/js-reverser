import requests
import json
import hashlib
import base64
import pandas as pd  # 添加pandas库用于Excel处理
from datetime import datetime
from loguru import logger
import execjs

# 模拟JavaScript的JSON.stringify
def json_stringify(obj):
    """
    模拟JavaScript的JSON.stringify行为
    特别处理布尔值为小写(true/false)
    """
    return json.dumps(obj, separators=(',', ':')) \
             .replace('True', 'true') \
             .replace('False', 'false') \
             .replace('Null', 'null')

def extract_company_data(company_list):
    """从公司列表中提取主要数据，并整理为可导出格式"""
    data_rows = []
    
    for company in company_list:
        # 处理标签列表，转为字符串
        tags = ", ".join(company.get("tagNameList", []))
        
        # 处理融资信息
        funding = company.get("funding", {})
        funding_money = "未披露"
        funding_round = funding.get("roundName", "未披露")
        funding_date = funding.get("fundingDate", 0)
        
        # 从funding_desc中提取投资金额
        if funding.get("fundingDesc"):
            try:
                funding_desc = json.loads(funding.get("fundingDesc", "{}"))
                funding_money = funding_desc.get("money", "未披露")
            except:
                pass
        
        # 提取投资方
        investors = []
        if funding.get("fundingDesc"):
            try:
                funding_desc = json.loads(funding.get("fundingDesc", "{}"))
                investor_list = funding_desc.get("investorList", [])
                investors = [investor.get("name", "") for investor in investor_list]
            except:
                pass
        
        investors_str = ", ".join(investors)
        
        # 处理日期 (毫秒时间戳转为YYYY-MM-DD格式)
        establish_date = ""
        if company.get("establishDate", 0) > 0:
            establish_date = datetime.fromtimestamp(company.get("establishDate", 0)/1000).strftime('%Y-%m-%d')
        
        funding_date_str = ""
        if funding_date > 0:
            funding_date_str = datetime.fromtimestamp(funding_date/1000).strftime('%Y-%m-%d')
        
        # 构建行数据
        row = {
            "公司ID": company.get("id", ""),
            "公司代码": company.get("code", ""),
            "公司名称": company.get("name", ""),
            "公司简介": company.get("brief", ""),
            "公司标签": tags,
            "公司logo": company.get("logo", ""),
            "融资轮次": funding_round,
            "融资金额": funding_money,
            "融资日期": funding_date_str,
            "投资方": investors_str,
            "成立日期": establish_date,
            "公司状态": company.get("companyStatus", ""),
            "地区": company.get("regionName", ""),
            "省份": company.get("provinceName", ""),
            "城市": company.get("cityName", ""),
            "区县": company.get("districtName", ""),
        }
        data_rows.append(row)
    
    return data_rows

def main():
    js_code = open("rhino_data.js", "r", encoding="utf-8").read()

    # 使用 PyExecJS 执行 JavaScript 代码
    ctx = execjs.compile(js_code)
    
    # 存储所有公司数据
    all_company_data = []
    
    # 分页参数
    start = 0
    
    total_companies = None
    
    while True:
        search_params = {
            "industry_ids": 1250,
            "domestic": True,
            "corporate_locationIds": [],
            "tag_names": [],
            "corporate_rounds": [],
            "sort": 76006,
            "order": -1,
            "start": start,
            "limit": 10
        }
        
        print(f"正在获取第 {start//10 + 1} 页数据 (start={start}, limit={10})...")
        
        # 对payload字符串进行e1和e2加密
        encrypted_payload = ctx.call("e1",ctx.call("e2",json_stringify(search_params)))

        # 对加密后的payload生成签名
        signature = ctx.call("sig",encrypted_payload)

        # 构建最终的请求参数
        request_params = {
            "payload": encrypted_payload,
            "sig": signature,
            "v": 1
        }

  
        cookies = {
            'btoken': 'DOIXWHDS1S4VVHO3GAK9LPJHFTAJ9E69',
            'Hm_lvt_42317524c1662a500d12d3784dbea0f8': '1743967648',
            'HMACCOUNT': 'A4704EBE74B38B2E',
            'hy_data_2020_id': '1960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42',
            'hy_data_2020_js_sdk': '%7B%22distinct_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%7D',
            'sajssdk_2020_cross_new_user': '1js 混淆_源码乱码赛',
            'utoken': 'L081Z46N9KHK07EY0YE8A4KETO8K931E',
            'username': 'Auroral',
            'Hm_lpvt_42317524c1662a500d12d3784dbea0f8': '1743967672',
        }

        headers = {
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.xiniudata.com',
            'pragma': 'no-cache',
            'priority': 'u=1js 混淆_源码乱码赛, i',
            'referer': 'https://www.xiniudata.com/industry/170cc0d4dc2e41dbbed69d0ca13f1f6d/overview',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            # 'cookie': 'btoken=DOIXWHDS1S4VVHO3GAK9LPJHFTAJ9E69; Hm_lvt_42317524c1662a500d12d3784dbea0f8=1743967648; HMACCOUNT=A4704EBE74B38B2E; hy_data_2020_id=1960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%7D; sajssdk_2020_cross_new_user=1js 混淆_源码乱码赛; utoken=L081Z46N9KHK07EY0YE8A4KETO8K931E; username=Auroral; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1743967672',
        }
        
        # 发送请求
        response = requests.post(
            'https://www.xiniudata.com/api/search3/company/search_company_for_lib',
            cookies=cookies,
            headers=headers,
            json=request_params,
        )

        # 获取加密的响应数据
        response_dict = json.loads(response.text)
        encrypted_data = response_dict.get('d')
        
        try:
            if encrypted_data:
                # 解密响应数据
                stage1_data = ctx.call("d1", encrypted_data)
                decrypted_data = ctx.call("d2", stage1_data)
                
                # 解析为Python字典
                search_result = json.loads(decrypted_data)
                
                # 获取总数量
                if total_companies is None:
                    total_companies = search_result.get("total", 0)
                    print(f"总共有 {total_companies} 家公司")
                
                # 提取公司代码列表
                companies_data = search_result.get("data", [])
                
                if not companies_data:
                    print("没有更多数据，爬取完成")
                    break
                
                companies = []
                for company in companies_data:
                    companies.append(company.get("company_code"))
                
                print(f"本页获取到 {len(companies)} 家公司")
                
                # 构造符合要求的格式
                payload = {
                    "codes": companies
                }
                
                # 对payload字符串进行e1和e2加密
                encrypted_payload = ctx.call("e1", ctx.call("e2", json_stringify(payload)))
                
                # 对加密后的payload生成签名
                signature = ctx.call("sig", encrypted_payload)
                
                # 构建最终的请求参数
                request_params1 = {
                    "payload": encrypted_payload,
                    "sig": signature,
                    "v": 1
                }
                cookies1 = {
                    'btoken': 'DOIXWHDS1S4VVHO3GAK9LPJHFTAJ9E69',
                    'Hm_lvt_42317524c1662a500d12d3784dbea0f8': '1743967648',
                    'HMACCOUNT': 'A4704EBE74B38B2E',
                    'hy_data_2020_id': '1960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42',
                    'hy_data_2020_js_sdk': '%7B%22distinct_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%7D',
                    'sajssdk_2020_cross_new_user': '1js 混淆_源码乱码赛',
                    'utoken': 'L081Z46N9KHK07EY0YE8A4KETO8K931E',
                    'username': 'Auroral',
                    'Hm_lpvt_42317524c1662a500d12d3784dbea0f8': '1743967672',
                }

                headers1 = {
                    'accept': 'application/json',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/json',
                    'origin': 'https://www.xiniudata.com',
                    'pragma': 'no-cache',
                    'priority': 'u=1js 混淆_源码乱码赛, i',
                    'referer': 'https://www.xiniudata.com/industry/170cc0d4dc2e41dbbed69d0ca13f1f6d/overview',
                    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                    # 'cookie': 'btoken=DOIXWHDS1S4VVHO3GAK9LPJHFTAJ9E69; Hm_lvt_42317524c1662a500d12d3784dbea0f8=1743967648; HMACCOUNT=A4704EBE74B38B2E; hy_data_2020_id=1960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221960c9277d516a2-04ed90a89be777-1b525636-2025000-1960c9277d61d42%22%7D; sajssdk_2020_cross_new_user=1js 混淆_源码乱码赛; utoken=L081Z46N9KHK07EY0YE8A4KETO8K931E; username=Auroral; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1743967672',
                }
                
                # 发送请求
                response1 = requests.post(
                    'https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes',
                    cookies=cookies1,
                    headers=headers1,
                    json=request_params1,
                )

                # 获取加密的响应数据
                response_dict1 = json.loads(response1.text)
                encrypted_data1 = response_dict1.get('d')

                # 解密响应数据
                stage1_data1 = ctx.call("d1", encrypted_data1)
                decrypted_data1 = ctx.call("d2", stage1_data1)

                # 解析为Python字典
                search_result1 = json.loads(decrypted_data1)
                
                # 从结果中提取公司列表
                company_list = search_result1.get("list", [])
                
                if company_list:
                    print(f"成功获取到 {len(company_list)} 家公司的详细信息")
                    
                    # 使用extract_company_data函数提取公司数据
                    extracted_data = extract_company_data(company_list)
                    
                    # 将提取的数据添加到总数据列表中
                    all_company_data.extend(extracted_data)
                else:
                    print("未获取到公司数据列表，请检查API响应或搜索条件")
                
                # 更新分页参数
                start += 10
                
                # 如果已经获取了所有数据，则退出循环
                if start >= total_companies:
                    print("已获取所有数据，爬取完成")
                    break
                
                # 添加延时，避免请求过于频繁
                time.sleep(1)
            else:
                print("未获取到加密数据，请检查API响应")
                break
                
        except Exception as e:
            print(f"处理响应时出错: {e}")
            print(f"原始响应: {response.text}")
            break
    
    # 所有数据爬取完成后，创建DataFrame并导出到Excel
    if all_company_data:
        df = pd.DataFrame(all_company_data)
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"xiniu_companies_all_{timestamp}.xlsx"
        
        # 保存到Excel文件
        df.to_excel(excel_filename, index=False)
        print(f"所有数据已成功导出到 {excel_filename}，共 {len(all_company_data)} 条记录")
    else:
        print("未获取到任何公司数据，无法导出Excel")

if __name__ == "__main__":
    import time
    main()


