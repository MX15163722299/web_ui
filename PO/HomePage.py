'''

编写人：
    梁超
编写日期：
    2020年7月3日

实现功能：首页页面对象类

    1.封装属性：
        1.1 oa首页页面的元素属性

    2.封装方法：
        2.1 左侧导航栏点击
        2.2 输入用户名
        2.3 输入密码
        2.4 点击登录


'''

from selenium.webdriver.common.by import By
from PO.BasePage import BasePage
from Common.BaseDriver import BaseDriver
from Common.Log import logger
from PO.LoginPage import LoginPage


class HomePage(BasePage):

    """页面属性"""
    _my_notice = (By.LINK_TEXT,'我的通告')
    _logout = (By.LINK_TEXT, '退出')

    _personal_office = (By.LINK_TEXT, '个人办公')
    #个人办公下的子菜单
    _to_do = (By.LINK_TEXT, '待办任务')
    _my_done = (By.LINK_TEXT, '已办任务')
    _inite_process = (By.LINK_TEXT, '发起流程')
    _my_application = (By.LINK_TEXT, '我的申请')
    _process_query = (By.LINK_TEXT, '流程查询')
    _my_temporary = (By.LINK_TEXT, '我的暂存')


    _system_settings = (By.LINK_TEXT, '系统设置')
    #系统设置下的子菜单
    _user_management = (By.LINK_TEXT,'用户管理')

    #用户角色
    _user_role = (By.XPATH,"//*[@class='lang-selected']/span")

    #一般用户
    _user_general = (By.XPATH,"//*[@class='lang-select']/span[contains(text(),'一般用户')]")




    def __init__(self,driver):
        self.driver = driver
        logger.info("进入oa主页")


    """页面元素的操作方法"""

    def expand_menu(self,*menu):
        """展开菜单"""
        self.by_find_element(*menu).click()

    def click_personal_work(self):
        """点击个人办公"""
        self.expand_menu(*self._personal_office)

    def click_my_to_do(self):
        """点击我的待办"""
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._to_do).click()

    def click_my_done(self):
        """点击我的已办"""
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._my_done).click()

    def click_initiate_process(self):
        """点击发起流程"""
        logger.info("点击发起流程")
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._inite_process).click()

    def click_my_application(self):
        """点击我的申请"""
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._my_application).click()

    def click_process_query(self):
        """点击流程查询"""
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._process_query).click()

    def click_my_temporary(self):
        """点击我的暂存"""
        self.driver.refresh()
        self.click_personal_work()
        self.by_find_element(*self._my_temporary).click()

    def click_system_setting(self):
        """点击系统设置"""
        self.driver.refresh()
        self.expand_menu(*self._system_settings)
        self.by_find_element(*self._system_settings).click()

    def click_user_management(self):
        """点击用户管理"""
        self.driver.refresh()
        self.expand_menu(*self._system_settings)
        self.by_find_element(*self._user_management).click()

    def auto_audit(self,lp,mp,up,mtp,pp,title,type):
        """
        实现自动审核，根据提供的流程标题和流程类型去查询目标流程的最终审核信息，
        如果发现未结束，则继续审核，否则自动结束审核
        传参说明：
        :param lp: 登录页面的driver对象
        :param mp: 我的待办页面的driver对象
        :param up: 用户管理页面的driver对象
        :param mtp: 我的申请页面的driver对象
        :param pp: 流程中心页面的driver对象
        :param process_title: 流程标题
        :param process_type: 流程类型
        :return: 返回最终的审核状态
        """

        while True:
            # 2拿着标题去获取流程编号,审核信息
            self.click_my_application()
            process_num = mp.get_process_num(title, type)
            mp.click_process_title()
            leader_name,status = mp.get_audit_person()
            logger.info('获取审核结果返回的leader和status：%s %s' %(leader_name,status))
            if status == '流程已结束':
                logger.info('流程已结束，用例通过')
                break

            # 3拿着审核信息，去用户管理查登录id
            # hp.click_system_setting()
            self.click_user_management()
            login_id = up.get_login_id(leader_name)

            # 4拿着loginid去登录，然后查询我的待办
            lp.logout()
            lp.login(login_id)
            self.switch_general_user()
            self.click_my_to_do()
            mtp.input_process_num(process_num)
            mtp.click_search_btn()
            mtp.click_table_first()

            # 进入流程中心页面输入审核意见
            pp.input_audit_msg('同意')
            pp.click_submit_btn()
            lp.logout()
            # 5进入我的申请，查看下一位审核人
            lp.login()

        return status



    def switch_general_user(self):
        """
        判断当前用户角色，如何不为一般用户则修改为一般用户
        :return:
        """
        role = self.by_find_element(*self._user_role).text

        flag = str(role).find('一般用户')
        if flag == -1:
            self.by_find_element(*self._user_role).click()
            self.by_find_element(*self._user_general).click()



if __name__ == '__main__':
    driver = BaseDriver()
    a = LoginPage(driver)
    a.login('DT1914982')
    h = HomePage(driver)
    h.switch_general_user()
