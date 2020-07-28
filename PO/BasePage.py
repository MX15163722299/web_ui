"""

编写人：
    梁超
编写日期：
    2020年7月2日

功能描述：所有page页面的基类，提供统一的方法

方法说明：

    1-构造方法：init
        1.1 接收test用例传入的driver
    2-定位方法：find_element
        2.1 二次封装find_element方法，加入超时判断
    3-打开方法：get
        3.1 二次封装get方法，一次性判断，进入的页面是否成功


"""
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from Common.Log import logger

class BasePage(object):


    def __init__(self,driver):
        #接收test传入的driver对象
        self.driver = driver


    def by_find_element(self,*item):
        # print('***element',item)
        try:

            logger.info('定位的目标元素：%s' % str(item))
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。

            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(item))

            return self.driver.find_element(*item)

        except Exception as msg:
            logger.info('系统提示%s异常' % msg)
            logger.info(u"页面中未能找到 %s 元素" % str(item))

    def by_find_elements(self,*item):
        # print('***element',item)
        try:
            logger.info('定位的目标元素：%s' % str(item))
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。

            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(item))

            return self.driver.find_elements(*item)

        except Exception as msg:
            logger.info('系统提示:' % str(msg))
            logger.info(u"页面中未能找到 %s 元素" % str(item))


    def focus(self,*item):
        try:

            logger.info("聚焦元素")
            target = self.driver.by_find_element(*item)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)

        except Exception as msg:
            logger.info("系统聚焦失败，提示%s" % msg)


    def get(self,url):
        try:

            self.driver.get(url)
            self.driver.maiximize_window()

        except Exception as msg:
            print(u'%s页面打开失败'% url)
            logger.info('')


    def scroll_to_mid(self):
        logger.info('设置滚动条到中间')
        height = 'document.body.scrollHeight'
        page_height = self.driver.execute_script(height)
        logger.info('页面的高度为:%s' % page_height)
        js = 'var action=document.documentElement.scrollTop={}'.format(page_height/2)
        # 设置滚动条距离顶部的位置，设置为 10000， 超过10000就是最底部
        self.driver.execute_script(js)  # 执行脚本


    def scroll_to_top(self):
        logger.info('设置滚动条到顶部')
        js = 'window.scrollTo(0,0)'
        # 设置滚动条距离顶部的位置，设置为 10000， 超过10000就是最底部
        self.driver.execute_script(js)  # 执行脚本


    def scroll_to_bottom(self):
        logger.info('设置滚动条到底部')
        time.sleep(1)
        js = 'window.scrollTo(0,document.body.scrollHeight);'
        js = 'window.scrollTo(0,10000);'
        # 设置滚动条距离顶部的位置，设置为 10000， 超过10000就是最底部
        self.driver.execute_script(js)  # 执行脚本

    def scroll_to_view(self,*loc):
        """
        让滚动条滚动到目标元素可见的位置
        :param loc: 目标元素定位信息
        :return:
        """
        logger.info('滚动到目标元素存在的位置')
        next = self.by_find_element(*loc)
        self.driver.execute_script("arguments[0].scrollIntoView();",next)
        logger.info('滚动成功')

