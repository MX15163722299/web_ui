'''


实现功能：我的待办页面对象类封装

    1.封装属性：
        1.1 页面元素属性

    2.封装方法：
        2.1


'''


from selenium.webdriver.common.by import By
from PO.BasePage import BasePage
from Common.BaseDriver import BaseDriver
from Common.Log import logger
from selenium.webdriver.support.ui import Select
import time,datetime,re
# from wqrfnium.wqrfnium_api import *
import re


class MyToDoPage(BasePage):

    '''页面元素属性'''

    _process_num = (By.ID,"actFormId")

    _search_btn = (By.XPATH,"//*[text()=' 查询']")

    #表格记录
    _table_all = (By.XPATH,'//table[@id="contentTable"]/tbody/*')

    _table_first = (By.XPATH, '//table[@id="contentTable"]/tbody/tr/td[2]/a')

    #框架
    _iframe_first = "iframe4"






    """元素操作方法"""


    def input_process_num(self,num):
        """
        输入流程编号
        :param num:
        :return:
        """
        logger.info('输入姓名：%s' % num)
        self.driver.switch_to.frame(self._iframe_first)
        self.by_find_element(*self._process_num).send_keys(num)
        self.driver.switch_to.default_content()


    def click_search_btn(self):
        """点击查询按钮"""
        logger.info('点击查询按钮')
        self.driver.switch_to.frame(self._iframe_first)
        self.by_find_element(*self._search_btn).click()
        self.driver.switch_to.default_content()


    def click_table_first(self):
        """
        点击表格中的第一条记录
        :param name:
        :return:
        """
        logger.info("点击表格记录中的第一条")
        self.driver.switch_to.frame(self._iframe_first)
        self.by_find_element(*self._table_first).click()
        #退出进入的框架frame
        self.driver.switch_to.default_content()





