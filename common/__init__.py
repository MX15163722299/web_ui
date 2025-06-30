from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 修改为你的 Chrome for Testing 安装路径
chrome_path = "/Applications/chrome-mac-119/chrome-mac-119.app/Contents/MacOS/Google Chrome for Testing"

# options.binary_location = chrome_path

# 配置选项
options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# chromedriver 路径
driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)

try:
    # 启动浏览器
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.baidu.com")
    print("✅ 浏览器已成功启动！chromedriver & Chrome 兼容正常！")
    time.sleep(5)  # 等待 5 秒看浏览器弹出
    driver.quit()
except Exception as e:
    print("❌ 启动失败，请检查错误：")
    print(e)
