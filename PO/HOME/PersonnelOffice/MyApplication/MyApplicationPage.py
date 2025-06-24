'''


实现功能：我的申请页面对象类封装

    1.封装属性：
        1.1 我的申请页面元素属性

    2.封装方法：
        2.1-输入流程编号：


'''

from selenium.webdriver.common.by import By
from PO.BasePage import BasePage
from Common.BaseDriver import BaseDriver
from Common.Log import logger
from selenium.webdriver.support.ui import Select
import time,datetime,re
from PO.LoginPage import LoginPage
from PO.HomePage import HomePage


class MyApplicationPage(BasePage):

    '''页面元素属性'''

    _process_num = (By.ID,"actFormId")
    _search_btn = (By.XPATH,'//*[@class="fa fa-search"]')

    #流程
    _process_name = (By.ID,'procDefKey')

    #内嵌框架属性
    _iframe_name = "iframe7"


    #表格内属性

    _table_all = (By.XPATH, '//*[@id="contentTable"]/tbody/*')
    #表格中的第一条记录标题
    _table_one = (By.XPATH, '//*[@id="contentTable"]/tbody/tr/td[2]/a')

    #翻页属性
    _next_page = (By.XPATH,'//li[@class="paginate_button next"]/a/i[@class="fa fa-angle-right"]')



    #审核信息
    _audit_all = (By.XPATH,'//*[@id="histoicFlowList"]/table/tbody/*')


    """操作方法封装"""

    def __init__(self,driver):
        '''初始化方法'''
        super(MyApplicationPage, self).__init__(driver)
        logger.info('进入我的申请查询页面')


    def input_process_num(self,num):
        """
        输入：流程编号
        :param option:
        :return:
        """
        logger.info('输入：流程编号%s' % num)
        self.driver.switch_to.frame(self._iframe_name)
        # self.by_find_element(*self._emergency_situations).click()
        self.by_find_element(*self._process_num).send_keys(num)

        self.driver.switch_to.default_content()

    def select_process_type(self, type):
        """
        选择流程
        :param option:
        :return:
        """
        self.driver.switch_to.frame(self._iframe_name)

        logger.info('选择流程类型：%s' % type)
        s = self.by_find_element(*self._process_name)
        Select(s).select_by_visible_text(type)

        self.driver.switch_to.default_content()



    def click_search_btn(self):
        """
        点击查询
        :param option:
        :return:
        """
        logger.info('点击查询按钮')
        self.driver.switch_to.frame(self._iframe_name)

        self.by_find_element(*self._search_btn).click()

        self.driver.switch_to.default_content()


    def get_process_num(self, title=None,type=None):
        """
        功能：传入流程标题，通过我的申请页面进行查询，得到和流程标题匹配的流程编号，
            如果第一页没有查找到，则点击下一页继续查找

        :param:title
        :return:
        """
        logger.info('根据title获取流程编号')
        self.select_process_type(type)
        self.click_search_btn()
        """第一种方案："""
        self.driver.switch_to.frame(self._iframe_name)


        #设置一个flag，表示是否查到目标流程，如果第一轮没有查到，则点击下一页，继续查询
        flag = False
        while True:
            list = self.by_find_elements(*self._table_all)
            #遍历默认第一页查询到的流程记录
            for i in list:
                mystr = i.get_attribute('outerHTML')
                # print('list的元素为outer',i.get_attribute('outerHTML'))
                pattern = 'actFormId=(\d*?)">(自动化测试.*?)</a>'
                result = re.search(pattern,mystr)
                list_process_num = result.group(1)
                list_process_title = result.group(2)
                logger.info('正则匹配的结果%s-%s-%s' % (result,result.group(1),result.group(2)))
                #判断传入的流程标题和查到的流程标题是否一致
                if title == list_process_title:
                    flag = True
                    logger.info('查找到目标流程编号:%s' % list_process_num)
                    self.driver.switch_to.default_content()
                    break
            #如果在第一页记录中未查找到流程编号，则点击下一页继续查找，直到查找到
            # else:
            if flag == False:
                logger.info('未查找到目标流程编号，点击下一页继续查找')
                self.scroll_to_view(*self._next_page)
                self.by_find_element(*self._next_page).click()
            else:
                break
        return list_process_num





    def click_process_title(self):
        """
        默认点击第一条记录流程标题
        :return:
        """
        logger.info('点击第一条记录标题')
        self.driver.switch_to.frame(self._iframe_name)
        self.by_find_element(*self._table_one).click()
        self.driver.switch_to.default_content()



    def get_audit_person(self):
        """
        功能：获取审核信息中最后一条，返回下一位审批人，如果流程结束，则返回空
        :return:
        """
        try:
            logger.info('获取审核信息')
            self.driver.switch_to.frame(self._iframe_name)
            self.scroll_to_view(*self._audit_all)
            tag_list  = self.driver.find_elements(*self._audit_all)

            tag = tag_list[-1].get_attribute('innerHTML')
            logger.info('获取的最后一条审核信息为：%s',str(tag))
            pattern1 = re.compile('relative;">(.*?)</td>')
            result1 = re.search(pattern1,tag)
            leader = result1.group(1).split(',')[0]
            flag = tag.find('结束')

            logger.info('获取到的流程信息为：%s，查找结果：%s' % (leader,flag))

            if leader != '':
                self.driver.switch_to.default_content()
                logger.info("审核还未结束，继续下次审核")
                return leader,'流程未结束'
            elif flag != -1:
                logger.info("流程已结束")
                return leader,'流程已结束'

        except Exception as msg:
            logger.info('获取审核信息异常，请核查！')
            raise




if __name__ == '__main__':
    driver = BaseDriver()
    lp = LoginPage(driver)
    lp.login()
    hp = HomePage(driver)
    hp.click_my_application()
    mp = MyApplicationPage(driver)
    mp.input_process_num(29440)
    mp.click_search_btn()
    mp.click_process_title()
    print(mp.get_audit_person())
