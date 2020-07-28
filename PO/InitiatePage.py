'''

编写人：
    梁超
编写日期：
    2020年7月6日

实现功能：发起流程页面的对象类封装

    1.封装属性：
        1.1 个人办公--发球流程页面属性

    2.封装方法：
        2.1

'''
import datetime

from selenium.webdriver.common.by import By
from PO.BasePage import BasePage
from Common.BaseDriver import BaseDriver
from Common.Log import logger
import time
# from wqrfnium.wqrfnium_api import *


class InitiatePage(BasePage):

    """页面属性"""
    #流程类

    _peronnel_process = (By.ID,'i_1')
    # _employee_go_out = (By.LINK_TEXT,u'员工外出申请')
    _employee_leave = (By.LINK_TEXT, '员工请假申请')
    _employee_go_out = (By.XPATH, '//*[text()="员工外出申请流程"]')
    _iframe_name = "iframe6"


    #时间配置
    today = datetime.date.today()
    # 此处默认输入明天的时间
    tomorrow = today + datetime.timedelta(days=1)
    goal_time = datetime.date.strftime(tomorrow, '%Y-%m-%d %H:%M')
    after_tomorrow = today + datetime.timedelta(days=2)



    def __init__(self,driver):
        super().__init__(driver)
        logger.info("进入发起流程选择页面")

    """元素操作方法"""
    def click_employee_go_out(self):
        """进入流程类中的子流程选项"""
        #进去iframe框架
        self.driver.switch_to.frame(self._iframe_name)

        self.scroll_to_view(*self._employee_go_out)

        logger.info('点击员工外出申请流程')

        self.by_find_element(*self._employee_go_out).click()
        logger.info("进入%s页面" % (self._employee_go_out[1].split('=')[1]))

        self.driver.switch_to.default_content()

    def click_personnel_process(self):
        """点击人事流程类"""
        # 进去iframe框架
        self.driver.switch_to.frame(self._iframe_name)
        self.by_find_element(*self._peronnel_process).click()
        self.driver.switch_to.default_content()
        process_type = self._employee_go_out[1].split('=')[1].strip(']').strip('"')
        return process_type



        # ip.click_employee_go_out()
        # process_title = ep.get_process_title()
        # ep.input_emergency_situations('一般')
        # ep.input_employee_level('普通员工')
        # ep.input_leave_time()
        # ep.input_return_time()
        # ep.input_matter()
        # ep.input_address()
        # ep.click_submit_button()

    def initate_process(self,
                        ep,
                        siuation='一般',
                        level='普通员工',
                        leave_time=goal_time,
                        return_time=after_tomorrow,
                        matter='事项',
                        address='地址'):
        """
        发起
        :param ep:
        :param siuation:
        :param level:
        :param leave_time: %Y-%m-%d %H:%M
        :param return_time: %Y-%m-%d %H:%M
        :param matter:
        :param address:
        :return: process_title
        """
        process_title = ep.get_process_title()
        ep.input_emergency_situations(siuation)
        ep.input_employee_level(level)
        ep.input_leave_time(leave_time)
        ep.input_return_time(return_time)
        ep.input_matter(matter)
        ep.input_address(address)
        ep.click_submit_button()
        return process_title


if __name__ == '__main__':
    driver = BaseDriver()
    driver.get('http://172.16.6.86:8080/oa')
    # a = LoginPage(driver)
    a.login()