from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
CHROMEDRIVER = "/Users/leomeng/tools/chromedriver/143/chromedriver"
CHROME_BIN = "/Applications/Chrome-Auto.app/Contents/MacOS/Google Chrome for Testing"
PROFILE = "/Users/leomeng/chrome-profile-auto-143"

options = Options()
options.binary_location = CHROME_BIN
options.add_argument(f"--user-data-dir={PROFILE}")
options.add_argument("--no-first-run")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER,   # 🔴 Selenium 3 只认这个
    options=options
)

driver.get("https://www.baidu.com")
print(driver.title)
time.sleep(5)
driver.quit()




