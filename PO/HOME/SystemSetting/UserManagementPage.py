'''


实现功能：用户管理页面对象类封装

    1.封装属性：
        1.1 页面元素属性

    2.封装方法：
        具体见方法下的注释说明


'''


from selenium.webdriver.common.by import By
from PO.BasePage import BasePage
from Common.BaseDriver import BaseDriver
from Common.Log import logger
from selenium.webdriver.support.ui import Select
import time,datetime,re
# from wqrfnium.wqrfnium_api import *
import re


class UserManagementPage(BasePage):

    '''页面元素属性'''

    _name = (By.ID,"name")

    _search_btn = (By.XPATH,"//*[text()=' 查询']")


    #表格记录
    _table_all = (By.XPATH,'//table[@id="contentTable"]/tbody/*')


    #框架
    _iframe_first = "iframe85"

    _iframe_second = "officeContent"



    """元素操作方法"""


    def input_name(self,name):
        """
        输入姓名
        :param name: 接收
        :return:
        """
        logger.info('输入姓名：%s' % name)

        self.by_find_element(*self._name).send_keys(name)

    def click_search_btn(self):
        """
        点击查询按钮
        :return:
        """
        logger.info('点击查询按钮')
        self.by_find_element(*self._search_btn).click()


    def get_login_id(self,name):
        """
        根据提供的姓名，获取该用户的登录id
        :param name: 接收查询用户名
        :return:loginid: 返回该用户的登录id
        """
        self.driver.switch_to.frame(self._iframe_first)

        self.driver.switch_to.frame(self._iframe_second)
        self.input_name(name)
        self.click_search_btn()

        records = self.driver.find_elements(*self._table_all)

        #遍历获取到的所有记录，防止查出名字具有重合的记录比如：小明/小明明
        for i in records:
            html = i.get_attribute('innerHTML')
            pattern = re.compile('<td>(.*?)</td>')
            result = re.findall(pattern,html)
            logger.info('获取到的人名是:%s' % result[2])
            if name == result[2]:
                logger.info('判断通过 %s' % result[1])

                login_id = result[1].split(')">')[1].strip('</a>')
                logger.info('获取到的登录id为：%s' % login_id )
                # 退出进入的2层框架frame
                self.driver.switch_to.default_content()
                self.driver.switch_to.default_content()
                return login_id







