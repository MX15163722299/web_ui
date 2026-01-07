from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common.log import logger
from common.read_config import ReadConfig
import os
import time


def BaseDriver():
    """准备对外依赖的 driver（Selenium 3.141.0 专用）"""

    opt = Options()
    rc = ReadConfig()

    gui = str(rc.get_config('driver', 'gui')).strip().lower()  # yes/no

    # ✅ Chrome for Testing（你已安装成功）
    CHROME_BIN = "/Applications/Chrome-Auto.app/Contents/MacOS/Google Chrome for Testing"
    if not os.path.exists(CHROME_BIN):
        raise FileNotFoundError(f"未找到 Chrome 可执行文件：{CHROME_BIN}")
    opt.binary_location = CHROME_BIN
    logger.info(f"使用 Chrome for Testing: {CHROME_BIN}")

    # ✅ chromedriver（你已安装成功）
    CHROMEDRIVER = "/Users/leomeng/tools/chromedriver/143/chromedriver"
    if not os.path.exists(CHROMEDRIVER):
        raise FileNotFoundError(f"未找到 chromedriver：{CHROMEDRIVER}")

    # ✅ 每次启动都用“独立 profile”，避免被占用/脏数据导致闪退
    # GUI 模式尤其重要，否则很容易 session not created
    profile_dir = f"/Users/leomeng/chrome-profile-auto-143-{int(time.time())}"
    os.makedirs(profile_dir, exist_ok=True)
    opt.add_argument(f"--user-data-dir={profile_dir}")

    # 通用稳定参数
    opt.add_argument("--no-first-run")
    opt.add_argument("--disable-default-apps")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disable-popup-blocking")
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    opt.add_experimental_option("useAutomationExtension", False)

    if gui == "yes":
        logger.info("chrome 有界面运行")
        opt.add_argument("--start-maximized")
    else:
        logger.info("chrome 无头运行")
        # Selenium 3 更稳的 headless 写法（别用 headless=new）
        opt.add_argument("--headless")
        opt.add_argument("--window-size=1920,1080")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")

    # ✅ 开启 chromedriver log（定位 session not created 的关键证据）
    driver_log = f"/Users/leomeng/chromedriver-143-{int(time.time())}.log"
    logger.info(f"chromedriver 日志输出到: {driver_log}")

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER,
        options=opt,
        service_log_path=driver_log,
    )

    url = rc.get_config('driver', 'url')
    driver.get(url)
    return driver
if __name__ == "__main__":
    print("===== BaseDriver main 调试开始 =====")

    try:
        driver = BaseDriver()
        print("✅ driver 创建成功:", driver)

        # 停 5 秒，肉眼确认浏览器真的起来了
        import time
        time.sleep(5)

        driver.quit()
        print("✅ driver 正常退出")

    except Exception as e:
        print("❌ 启动失败，请检查错误：")
        raise
