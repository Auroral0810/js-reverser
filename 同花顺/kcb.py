from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

# 设置Chrome选项
chrome_options = Options()
# 以下两行取消注释可以实现无头模式（不显示浏览器窗口）
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化特征
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# 指定当前目录下的chromedriver
service = Service('./chromedriver')

# 初始化浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    '''
})

# 设置页面加载超时时间
driver.set_page_load_timeout(30)

# 存储所有数据
all_data = []
table_headers = []

try:
    # 首先访问主页
    print("访问主页...")
    driver.get('https://data.10jqka.com.cn/kcb/index/')
    time.sleep(random.uniform(2, 4))
    
    # 获取总页数
    total_pages = 1
    try:
        page_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "page_info"))
        )
        page_text = page_info.text
        if '/' in page_text:
            total_pages = int(page_text.split('/')[1])
        print(f"检测到总页数: {total_pages}")
    except Exception as e:
        print(f"获取总页数失败: {str(e)}")
        print("默认设置为1页")
    
    # 提取表头
    print("提取表头...")
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        thead = table.find_element(By.TAG_NAME, "thead")
        headers = thead.find_elements(By.TAG_NAME, "th")
        
        for header in headers:
            header_text = header.text.strip().replace('\n', ' ')
            table_headers.append(header_text)
        
        print("表头：")
        for i, header in enumerate(table_headers):
            print(f"{i+1}. {header}")
    except Exception as e:
        print(f"提取表头失败: {str(e)}")
    
    # 处理第一页数据
    current_page = 1
    if table_headers:
        print(f"提取第{current_page}页数据...")
        
        # 直接在表格中查找所有的tr元素，而不是先查找tbody
        try:
            # 方法1：直接在表格中查找所有行（除了表头行）
            rows = table.find_elements(By.TAG_NAME, "tr")
            # 排除第一行（表头行）
            data_rows = rows[1:] if len(rows) > 1 else []
            
            if not data_rows:
                # 方法2：尝试查找表格内的所有行(不经过tbody)
                print("尝试替代方法查找数据行...")
                data_rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(:first-child)")
            
            for row in data_rows:
                row_data = []
                cells = row.find_elements(By.TAG_NAME, "td")
                
                for cell in cells:
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                
                if row_data and len(row_data) > 1:  # 确保行有数据且不是空行
                    all_data.append(row_data)
            
            print(f"第{current_page}页爬取完成，找到{len(data_rows)}行数据")
        except Exception as e:
            print(f"提取第{current_page}页数据时出错: {str(e)}")
    
    # 处理剩余页面，使用页面上的分页按钮
    while current_page < total_pages:
        current_page += 1
        print(f"\n正在爬取第 {current_page}/{total_pages} 页...")
        
        # 随机延时
        delay = random.uniform(3, 7)
        print(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)
        
        try:
            # 点击下一页按钮
            try:
                # 尝试方法1：直接使用CSS选择器查找下一页按钮
                next_page_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#J-ajax-main > div.m-page.J-ajax-page > a.next"))
                )
            except:
                try:
                    # 尝试方法2：查找文本包含"下一页"的链接
                    next_page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '下一页')]"))
                    )
                except:
                    # 尝试方法3：使用用户提供的选择器
                    next_page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#J-ajax-main > div.m-page.J-ajax-page > a:nth-child(8)"))
                    )
            
            # 在点击前检查当前页码，用于后面验证是否真的切换了页面
            old_page_info = driver.find_element(By.CLASS_NAME, "page_info").text
            
            # 点击下一页按钮
            driver.execute_script("arguments[0].click();", next_page_btn)
            print("已点击下一页按钮")
            
            # 等待页面刷新 - 确保页码真的变了
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.CLASS_NAME, "page_info").text != old_page_info
            )
            
            # 等待表格重新加载
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # 同样使用直接获取行的方式
            rows = table.find_elements(By.TAG_NAME, "tr")
            # 排除表头行
            data_rows = rows[1:] if len(rows) > 1 else []
            
            if not data_rows:
                print("尝试替代方法查找数据行...")
                data_rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(:first-child)")
            
            # 打印当前页码，验证确实切换到了新页面
            current_page_info = driver.find_element(By.CLASS_NAME, "page_info").text
            print(f"当前页面信息: {current_page_info}")
            
            rows_found = 0
            for row in data_rows:
                row_data = []
                cells = row.find_elements(By.TAG_NAME, "td")
                
                for cell in cells:
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                
                if row_data and len(row_data) > 1:
                    all_data.append(row_data)
                    rows_found += 1
            
            print(f"第{current_page}页爬取完成，找到{rows_found}行数据，当前共有{len(all_data)}条数据")
            
            # 每爬取5页保存一次数据，避免中途失败
            if current_page % 5 == 0 and table_headers and all_data:
                temp_df = pd.DataFrame(all_data, columns=table_headers)
                temp_df.to_csv(f'同花顺科创板数据_临时保存_至第{current_page}页.csv', index=False, encoding='utf-8-sig')
                print(f"已将当前数据临时保存至'同花顺科创板数据_临时保存_至第{current_page}页.csv'")
        
        except Exception as e:
            print(f"处理第{current_page}页时发生错误: {str(e)}")
            # 尝试刷新页面重新获取
            try:
                driver.refresh()
                time.sleep(5)
                # 重新尝试？
            except:
                pass

except Exception as e:
    print(f"发生错误: {str(e)}")

finally:
    # 创建DataFrame并保存为CSV
    if table_headers and all_data:
        # 确保数据行的长度与表头一致
        valid_data = []
        for row in all_data:
            if len(row) == len(table_headers):
                valid_data.append(row)
            else:
                print(f"跳过长度不匹配的行: {row}，长度: {len(row)}，应为: {len(table_headers)}")
        
        df = pd.DataFrame(valid_data, columns=table_headers)
        df.to_csv('同花顺科创板数据_全部.csv', index=False, encoding='utf-8-sig')
        print(f"\n所有数据已保存到'同花顺科创板数据_全部.csv'，共{len(valid_data)}条记录")
    else:
        print("没有获取到数据或表头")
    
    # 关闭浏览器
    driver.quit()