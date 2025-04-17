import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置 Chrome
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

# 打开目标页面
driver.get("https://www.baidu.com")

# 清理所有现有 cookies
driver.delete_all_cookies()

# 添加 cookies
cookies = [
    {"name": "BAIDUID", "value": "49990CEA0201CA78E55DCE22CB98235B"},
    {"name": "BDUSS", "value": "2RLVHJoSlJ5b05FaU94bWg2NmhXQjNndDdYaWxya21yLTdPZktIaUVlcC1OSEZuSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6nSWd"},
    {"name": "BAIDUID_BFESS", "value": "49990CEA0201CA78E55DCE22CB98235B"},
    {"name": "BA_HECTOR", "value": "24840l0la0848k8h2k210h8l9bkgu61jo41uh1u"},
    {"name": "BDUSS_BFESS", "value": "2RLVHJoSlJ5b05FaU94bWg2NmhXQjNndDdYaWxya21yLTdPZktIaUVlcC1OSEZuSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6nSWd"},
]

for cookie in cookies:
    driver.add_cookie(cookie)

# 刷新页面以加载 cookies
driver.refresh()

# 等待加载
time.sleep(5)
driver.get("https://www.baidu.com")
# 检查是否成功登录
print("当前 URL:", driver.current_url)
