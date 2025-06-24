# '''

#
# 实现功能：封装用例依赖的driver
#
#     1.方法：BaseDriver
#         1.1 准备浏览器，设置driver的参数（无界面/取消自动化提示）
#         1.2 根据config.ini配置文件读取driver配置是否需要有界面运行
#         1.3 返回diver对象，提供给测试用例调用
#
# '''
from selenium import webdriver
from Common.log import logger
import time
from selenium.webdriver.chrome.options import Options
from Common.ReadConfig import ReadConfig
import os


def BaseDriver():
    """准备对外依赖的driver"""
    opt = Options()
    rc = ReadConfig()
    gui = rc.get_driver('gui')

    # ✅ macOS 上配置 Chrome 执行路径
    # ⚠️ 建议用统一配置来区分平台
    chrome_path_mac = "/Applications/chrome-mac-119/chrome-mac-119.app/Contents/MacOS/Google Chrome for Testing"
    if os.path.exists(chrome_path_mac):
        opt.binary_location = chrome_path_mac

    # ✅ GUI 参数处理
    if gui.lower() == 'yes':
        logger.info('chrome 有界面运行')
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument('--start-maximized')
    else:
        logger.info('chrome 无头运行')
        opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])

    # ✅ Mac 需要 Service 显式指定 chromedriver 路径
    from selenium.webdriver.chrome.service import Service
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=opt)

    # ✅ 访问起始 URL
    url = rc.get_driver('url')
    driver.get(url)
    return driver

if __name__ == '__main__':
    BaseDriver()
