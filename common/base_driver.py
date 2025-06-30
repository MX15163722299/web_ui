'''


实现功能：封装用例依赖的driver

    1.方法：BaseDriver
        1.1 准备浏览器，设置driver的参数（无界面/取消自动化提示）
        1.2 根据config.ini配置文件读取driver配置是否需要有界面运行
        1.3 返回diver对象，提供给测试用例调用

'''

# 导入所需的模块
from selenium import webdriver  # Selenium WebDriver 用于浏览器自动化
from common.log import logger    # 自定义日志模块
import time                     # 时间模块（虽然未使用，但可以保留）
from selenium.webdriver.chrome.options import Options  # 配置 Chrome 浏览器选项
# from common.ReadConfig import ReadConfig  # 读取配置文件的自定义类
from common.read_config import ReadConfig  # 读取配置文件的自定义类
import os                       # 操作系统接口模块，用于路径和文件操作


def BaseDriver():
    """准备对外依赖的driver"""

    # 初始化 Chrome 浏览器选项
    opt = Options()

    # 创建 ReadConfig 实例，用于读取配置文件中的参数
    rc = ReadConfig()

    # 从配置文件中读取是否启用 GUI（有界面）模式
    gui = rc.get_config('driver','gui')

    # macOS 上配置 Chrome 可执行文件路径
    # 如果 chrome_path_mac 存在，则设置 binary_location
    chrome_path_mac = "/Applications/chrome-mac-119/chrome-mac-119.app/Contents/MacOS/Google Chrome for Testing"
    if os.path.exists(chrome_path_mac):
        opt.binary_location = chrome_path_mac

    # 根据配置决定是有界面还是无头运行
    if gui.lower() == 'yes':
        logger.info('chrome 有界面运行')
        # 添加实验性选项：禁用自动化扩展提示
        opt.add_experimental_option('useAutomationExtension', False)
        # 排除自动化相关的开关提示
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        # 启动时最大化窗口
        opt.add_argument('--start-maximized')
    else:
        logger.info('chrome 无头运行')
        # 启用无头模式（不显示浏览器界面）
        opt.add_argument('--headless')
        # 禁用沙箱模式（适用于某些环境如 Docker 或 CI）
        opt.add_argument('--no-sandbox')
        # 禁用 /dev/shm 的使用（避免共享内存不足问题）
        opt.add_argument('--disable-dev-shm-usage')
        # 启动时最大化窗口
        opt.add_argument('--start-maximized')
        # 禁用自动化扩展提示
        opt.add_experimental_option('useAutomationExtension', False)
        # 排除自动化相关的开关提示
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])

    # 在 Mac 上需要显式指定 chromedriver 路径
    from selenium.webdriver.chrome.service import Service
    service = Service("/usr/local/bin/chromedriver")

    # 创建 Chrome WebDriver 实例
    driver = webdriver.Chrome(service=service, options=opt)

    # 从配置文件中获取测试起始 URL
    url = rc.get_config('driver','url')

    # 打开指定的 URL
    driver.get(url)

    # 返回 driver 实例，供测试用例使用
    return driver


if __name__ == '__main__':
    # 如果作为主程序运行，则直接调用 BaseDriver 函数创建浏览器实例
    b = BaseDriver()
    # url = rc.get_driver('url')
    # driver.get(url)
    # return driver

