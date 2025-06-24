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


class ProcessCenterPage(BasePage):

    '''页面元素属性'''

    _audit_msg = (By.ID,"act.comment")

    _search_btn = (By.XPATH,"//*[text()=' 查询']")
    _end_btn = (By.ID,'btnEnd')
    _submit_btn = (By.ID,"btnSubmit")

    #框架
    # _iframe_first = "iframeundefined"
    _iframe_first = (By.XPATH,'//*[@name="iframeundefined"]')

    _to_do = (By.LINK_TEXT,"待办任务")

    """元素操作方法"""


    def input_audit_msg(self,msg):
        """
        输入审核意见
        :param num:
        :return:
        """
        logger.info('输入审核意见：%s' % msg)

        iframe = self.by_find_element(*self._iframe_first)
        self.driver.switch_to.frame(iframe)
        self.scroll_to_bottom()
        self.by_find_element(*self._audit_msg).send_keys(msg)

        self.driver.switch_to.default_content()


    def click_submit_btn(self):
        """
        点击提交
        :return:
        """
        logger.info('点击同意按钮')

        iframe = self.by_find_element(*self._iframe_first)
        self.driver.switch_to.frame(iframe)
        self.scroll_to_view(*self._submit_btn)
        self.scroll_to_bottom()
        self.by_find_element(*self._submit_btn).click()

        #该定位用来判断提交是否结束，如果定位到页面上的查询按钮则说明已经提交成功，且刷新完页面
        result = self.by_find_element(*self._search_btn)
        logger.info('定位的结果是：%s' % result)
        if result:
            logger.info('定位成功')

        self.driver.switch_to.default_content()

    def click_end_btn(self):
        """
        点击终止
        :return:
        """
        logger.info('点击提交按钮')
        iframe = self.by_find_element(*self._iframe_first)
        self.driver.switch_to.frame(iframe)

        self.by_find_element(*self._end_btn).click()
        self.driver.switch_to.default_content()





