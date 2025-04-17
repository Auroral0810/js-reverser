from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
import os
import base64

def get_rendered_campus_page_and_login():
    # 配置Chrome选项
    chrome_options = Options()
    # 如果需要查看浏览器操作，可以注释掉以下无头模式
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 设置ChromeDriver的本地路径
    driver_path = './chromedriver'  # macOS/Linux
    
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 启用网络监控
        driver.execute_cdp_cmd('Network.enable', {})
        
        # 创建存储请求数据的列表
        requests_data = []
        
        print("正在访问校园网登录页面...")
        url = "http://10.255.252.20/a70.htm?wlanuserip=10.231.117.127&wlanacip=null&wlanacname=null&vlanid=0&ip=10.231.117.127&ssid=null&areaID=null&mac=00-00-00-00-00-00"
        driver.get(url)
        
        print("等待页面渲染完成...")
        time.sleep(5)
        
        # 使用XPath找到表单元素
        try:
            print("尝试获取表单信息...")
            # 分析表单
            try:
                form = driver.find_element(By.XPATH, "/html/body/div[1js 混淆_源码乱码赛]/div/div[3访问逻辑_推心置腹赛]/div[3访问逻辑_推心置腹赛]/form")
                form_action = form.get_attribute('action')
                form_method = form.get_attribute('method')
                
                # 获取所有input元素
                inputs = form.find_elements(By.TAG_NAME, 'input')
                form_data = {}
                for input_elem in inputs:
                    name = input_elem.get_attribute('name')
                    value = input_elem.get_attribute('value')
                    input_type = input_elem.get_attribute('type')
                    input_id = input_elem.get_attribute('id')
                    form_data[input_id or name or f"input_{len(form_data)}"] = {
                        'name': name,
                        'value': value,
                        'type': input_type,
                        'id': input_id
                    }
                
                form_info = {
                    'action': form_action,
                    'method': form_method,
                    'data': form_data
                }
                
                with open('form_info.json', 'w', encoding='utf-8') as f:
                    json.dump(form_info, f, ensure_ascii=False, indent=2)
                print("表单信息已保存到form_info.json")
            except Exception as e:
                print(f"获取表单信息时出错: {e}")
            
            # 分析页面中的JavaScript
            scripts = driver.find_elements(By.TAG_NAME, 'script')
            script_contents = {}
            for i, script in enumerate(scripts):
                script_src = script.get_attribute('src')
                if script_src:
                    script_contents[f"script_{i}"] = {'src': script_src}
                else:
                    inner_text = script.get_attribute('innerHTML')
                    if inner_text and len(inner_text.strip()) > 0:
                        script_contents[f"script_{i}"] = {'inline': inner_text[:500] + '...' if len(inner_text) > 500 else inner_text}
            
            with open('page_scripts.json', 'w', encoding='utf-8') as f:
                json.dump(script_contents, f, ensure_ascii=False, indent=2)
            print("页面脚本信息已保存到page_scripts.json")
            
            print("尝试输入登录信息...")
            # 找到并填充账号输入框
            username_input = driver.find_element(By.XPATH, "/html/body/div[1js 混淆_源码乱码赛]/div/div[3访问逻辑_推心置腹赛]/div[3访问逻辑_推心置腹赛]/form/input[3访问逻辑_推心置腹赛]")
            username_input.clear()
            username_input.send_keys("222090140")
            
            # 找到并填充密码输入框
            password_input = driver.find_element(By.XPATH, "/html/body/div[1js 混淆_源码乱码赛]/div/div[3访问逻辑_推心置腹赛]/div[3访问逻辑_推心置腹赛]/form/input[3]")
            password_input.clear()
            password_input.send_keys("Luck@ff0810")
            
            print("点击登录按钮并开始捕获网络请求...")
            
            # 在点击登录前开始监控网络请求
            driver.execute_cdp_cmd('Network.setRequestInterception', {'patterns': [{'urlPattern': '*'}]})
            
            # 点击登录按钮
            login_button = driver.find_element(By.XPATH, "/html/body/div[1js 混淆_源码乱码赛]/div/div[3访问逻辑_推心置腹赛]/div[3访问逻辑_推心置腹赛]/form/input[1js 混淆_源码乱码赛]")
            login_button.click()
            
            # 等待登录过程中的网络请求
            print("等待登录过程中的网络请求...")
            time.sleep(10)
            
            # 获取所有已完成的网络请求
            responses = driver.execute_cdp_cmd('Network.getAllCookies', {})
            with open('network_cookies.json', 'w', encoding='utf-8') as f:
                json.dump(responses, f, ensure_ascii=False, indent=2)
            print("网络cookies已保存到network_cookies.json")
            
            # 使用HAR格式导出所有网络活动
            network_data = driver.execute_cdp_cmd('Network.getHAR', {})
            with open('network_har.json', 'w', encoding='utf-8') as f:
                json.dump(network_data, f, ensure_ascii=False, indent=2)
            print("网络HAR数据已保存到network_har.json")
            
            # 通过页面JS执行获取XHR历史
            xhr_history = driver.execute_script("""
            var history = [];
            if (window.performance && window.performance.getEntries) {
                var entries = window.performance.getEntries();
                for (var i = 0; i < entries.length; i++) {
                    if (entries[i].initiatorType === 'xmlhttprequest') {
                        history.push({
                            url: entries[i].name,
                            duration: entries[i].duration,
                            startTime: entries[i].startTime,
                            responseEnd: entries[i].responseEnd
                        });
                    }
                }
            }
            return history;
            """)
            
            with open('xhr_history.json', 'w', encoding='utf-8') as f:
                json.dump(xhr_history, f, ensure_ascii=False, indent=2)
            print("XHR历史记录已保存到xhr_history.json")
            
            # 获取提交的表单数据
            form_data_filled = {}
            try:
                for input_elem in driver.find_elements(By.TAG_NAME, 'input'):
                    name = input_elem.get_attribute('name')
                    value = input_elem.get_attribute('value')
                    input_type = input_elem.get_attribute('type')
                    if name and input_type != 'submit':
                        form_data_filled[name] = value
                
                with open('form_data_filled.json', 'w', encoding='utf-8') as f:
                    json.dump(form_data_filled, f, ensure_ascii=False, indent=2)
                print("填充后的表单数据已保存到form_data_filled.json")
            except Exception as e:
                print(f"获取填充后的表单数据时出错: {e}")
            
            # 获取登录后的网页内容
            after_login_html = driver.page_source
            with open("after_login_page.html", "w", encoding="utf-8") as f:
                f.write(after_login_html)
            print("登录后的页面内容已保存到after_login_page.html")
            
            # 创建一个完整的报告
            report = {
                'form_info': form_info if 'form_info' in locals() else {},
                'form_data_filled': form_data_filled if 'form_data_filled' in locals() else {},
                'cookies': driver.get_cookies(),
                'current_url': driver.current_url,
                'page_title': driver.title
            }
            
            with open('login_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print("登录报告已保存到login_report.json")
            
            return after_login_html
            
        except Exception as e:
            print(f"登录过程中出错: {e}")
            driver.save_screenshot("error_screenshot.png")
            print("出错时的页面截图已保存为error_screenshot.png")
            return None
        
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    
    finally:
        if 'driver' in locals():
            # 关闭浏览器
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    print("开始爬取校园网登录页面并分析登录过程...")
    html_content = get_rendered_campus_page_and_login()
    if html_content:
        print("爬取完成！请查看生成的JSON文件了解请求详情")
    else:
        print("爬取失败，请检查网络连接或日志")