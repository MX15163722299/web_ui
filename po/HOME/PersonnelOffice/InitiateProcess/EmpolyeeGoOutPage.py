'''

实现功能：员工外出申请页面

    1.封装属性：
        1.1 外出申请的页面元素定位

    2.封装方法：
        元素的操作方法

'''


from selenium.webdriver.common.by import By
from po.BasePage import BasePage
from common.base_driver import BaseDriver
from common.log import logger
from selenium.webdriver.support.ui import Select
import time,datetime
# from wqrfnium.wqrfnium_api import *


class EmployeeGoOutPage(BasePage):

    '''页面元素属性'''



    _process_title = (By.ID,"lcbt")

    _emergency_situations = (By.ID,"jjqk")
    # _emergency_situations = (By.XPATH, "//*[@id='jjqk']")
    _employee_level = (By.ID, "ygjb")
    _leave_time = (By.XPATH, "//*[@id='KSRQ']")
    _return_time = (By.XPATH, "//*[@id='JSRQ']")

    _matter = (By.XPATH, "//*[@id='sx']")
    _address = (By.XPATH, "//*[@id='dz']")
    _remark = (By.XPATH, "//*[@id='bz']")

    _btn_search = (By.XPATH,"//*[text()=' 查询']")
    _btn_return = (By.XPATH,'//*[@id="btnCancel"]')
    _btn_tmp_save = (By.XPATH, '//*[@id="btnSaveDraft"]')
    _btn_submit = (By.XPATH, '//*[@id="btnSubmit"]')

    #流程编号表头
    _table_info = (By.XPATH,'//*[@id="contentTable"]/tbody/tr[1]/td[3]')

    #流程表格第一条记录
    _table_one = (By.XPATH,'//*[@id="contentTable"]/tbody/*')
    # _table_one = (By.XPATH, '//*[@id="contentTable"]/tbody/tr')

    #内嵌框架属性
    _iframe_name = "iframe6"

    #时间控制
    today = datetime.date.today()
    # 此处默认输入后天的时间
    tomorrow = today + datetime.timedelta(days=1)
    day_after = today + datetime.timedelta(days=2)
    leave_time = datetime.date.strftime(tomorrow, '%Y-%m-%d %H:%M')
    return_time = datetime.date.strftime(day_after, '%Y-%m-%d %H:%M')


    """操作方法封装"""

    def __init__(self,driver):
        '''初始化方法'''
        super(EmployeeGoOutPage, self).__init__(driver)
        logger.info('进入员工外出申请填写页面')


    def get_process_title(self):
        """获取流程标题"""
        self.driver.switch_to.frame(self._iframe_name)
        title = self.by_find_element(*self._process_title).get_attribute("value")
        logger.info('获取的流程标题是：%s' % title)
        self.driver.switch_to.default_content()
        return title

    def input_emergency_situations(self,option):
        """
        输入：紧急情况
        :param option:
        :return:
        """
        self.driver.switch_to.frame(self._iframe_name)

        logger.info('输入：紧急情况%s' % option)
        # self.by_find_element(*self._emergency_situations).click()
        s = self.by_find_element(*self._emergency_situations)
        Select(s).select_by_visible_text(option)

        self.driver.switch_to.default_content()

    def input_employee_level(self,level):
        """
        输入：员工级别
        :param option:
        :return:
        """
        try:
            self.driver.switch_to.frame(self._iframe_name)

            logger.info('输入：员工级别%s' % level)
            item = self.by_find_element(*self._employee_level)
            Select(item).select_by_visible_text(level)

            self.driver.switch_to.default_content()
        except Exception as msg:
            logger.error(msg)

    def input_leave_time(self,item=1):
        """
        输入：外出时间，默认是1明天，2是后天以此类推
        :param item: 默认today后间隔两天
        :return:
        """
        try:
            self.driver.switch_to.frame(self._iframe_name)
            goal_time = self.today + datetime.timedelta(days=item)
            leave_time = datetime.date.strftime(goal_time, '%Y-%m-%d %H:%M')
            logger.info('输入的外出时间为：%s' % goal_time)
            self.by_find_element(*self._leave_time).send_keys(leave_time)

            self.driver.switch_to.default_content()
        except Exception as msg:
            logger.error(msg)

    def input_return_time(self,item=2):
        """
        输入：归来时间，item代表今天后的第几天，1代表明天，2代表后天，以此类推
        :param item: 默认today后间隔1天
        :return:
        """
        try:
            self.driver.switch_to.frame(self._iframe_name)

            goal_time = self.today + datetime.timedelta(days=item)
            logger.info('输入的归来时间为：%s' % goal_time)
            return_time = datetime.date.strftime(goal_time, '%Y-%m-%d %H:%M')
            self.by_find_element(*self._return_time).send_keys(return_time)
            self.driver.switch_to.default_content()
        except Exception as msg:
            logger.error(msg)

    def input_matter(self,text='事项'):
        """
        输入：事项
        :param text:
        :return:
        """

        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._matter).send_keys(text)

        self.driver.switch_to.default_content()

    def input_address(self,text='地址'):
        """
        输入：地址
        :param text:
        :return:
        """
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._address).send_keys(text)

        self.driver.switch_to.default_content()

    def input_remark(self,text='备注'):
        """
        输入：备注
        :param text:
        :return:
        """
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._remark).send_keys(text)

        self.driver.switch_to.default_content()


    def click_submit_button(self):
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._btn_submit).click()

        #该定位用来判断提交是否结束，如果定位到页面上的查询按钮则说明已经提交成功，且刷新完页面
        result = self.by_find_element(*self._btn_search)
        logger.info('定位的结果是：%s' % result)
        if result:
            logger.info('定位成功')

        self.driver.switch_to.default_content()

    def click_return_button(self):
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._btn_return).click()

        self.driver.switch_to.default_content()

    def click_tmpSave_button(self):
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._btn_tmp_save).click()

        self.driver.switch_to.default_content()

    def get_process_num(self):
        """
        功能：此处有两种方法实现获取流程编号的方法
            1.通过父元素定位，获取每个元素的innerHTML，然后拿到<td>为1的对应的流程编号
            2.通过目标元素的固定xpath路径获取流程编号
        :return:
        """
        self.driver.switch_to.frame(self._iframe_name)
        """第一种方案：
        # list = self.driver.find_elements(*self._table_one)
        # for i in list:
        #     print('list的元素为outer',i.get_attribute('outerHTML'))
        #     print('list的元素为inner', i.get_attribute('innerHTML'))
        # logger.info('innerhtml %s' % list)
        """
        """第二种方案："""

        process_num = self.by_find_element(*self._table_info).get_attribute('innerHTML')
        logger.info('innerhtml %s' % str(process_num))

        self.driver.switch_to.default_content()









