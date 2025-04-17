from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree

driver = webdriver.Chrome()
driver.get("http://www.4399.com/")

# 使用 By.XPATH 查找元素
element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login_tologin"]')))
element.click()

name = '3515067303'
pwd = 'Luck_ff0810'

driver.switch_to.frame('popup_login_frame')
# page_source = driver.page_source
# content = etree.HTML(page_source)
# url_down = content.xpath('//*[@id="popup_login_frame"]')[0].get("src")
# login_url = 'https:'+ url_down
#
# driver1 = webdriver.Chrome()
# driver1.get(login_url)

username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="username"]')))
# username.click()
username.send_keys('3515067303')
password = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="j-password"]')))
password.send_keys('Luck_ff0810')
button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@type="submit"]')))
button.click()
# driver.find_element(By.XPATH, '//*[@id="login_tologin"]').click()
