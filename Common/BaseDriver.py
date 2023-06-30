'''

编写人：
    梁超
编写日期：
    2020年7月2日

实现功能：封装用例依赖的driver

    1.方法：BaseDriver
        1.1 准备浏览器，设置driver的参数（无界面/取消自动化提示）
        1.2 根据config.ini配置文件读取driver配置是否需要有界面运行
        1.3 返回diver对象，提供给测试用例调用



'''



from selenium import webdriver
from Common.Log import logger
import time
from selenium.webdriver.chrome.options import Options
from Common.ReadConfig import ReadConfig

def BaseDriver():
    """准备对外依赖的driver"""
    opt = Options()
    rc = ReadConfig()
    gui = rc.get_driver('gui')
    #判断config配置是否需要有界面运行
    if gui == 'yes' or gui == 'YES':
        logger.info('chrome 有界面运行')
        # 添加浏览器启动参数
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument('--start-maximized')
        # 启动浏览器
        driver = webdriver.Chrome(options=opt)
    else:
        #无界面参数
        opt.add_argument('--headless')
        #v78版本以上的自动化提示消除
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        #初始最大化参数
        opt.add_argument('--start-maximized')
        # 启动浏览器
        driver = webdriver.Chrome(options=opt)

    url = rc.get_driver('url')
    driver.get(url)
    return driver



if __name__ == '__main__':
    BaseDriver()