'''


实现功能：登录页面对象类

    1.封装属性：
        1.1 登录页面的元素属性

    2.封装方法：
        2.1 页面元素属性对应的操作方法
        2.2 输入用户名
        2.3 输入密码
        2.4 点击登录


'''
from selenium.webdriver.common.by import By
from po.BasePage import BasePage
from common.base_driver import BaseDriver
from common.log import logger


class LoginPage(BasePage):

    """页面属性"""
    _username = (By.ID,'username')
    _password = (By.ID,'password')
    _login_button = (By.NAME,"submit")
    #退出
    _logout = (By.LINK_TEXT,'退出')

    def __init__(self,driver):
        super().__init__(driver)
        logger.info("进入登录页面")

    def input_username(self,username):
        """元素的操作方法"""
        self.by_find_element(*self._username).send_keys(username)

    def input_password(self,pwd='111111'):
        """元素的操作方法"""
        self.by_find_element(*self._password).send_keys(pwd)

    def click_login(self):
        """点击登录"""
        self.by_find_element(*self._login_button).click()

    def login(self,username='DT2016809',pwd='111111'):

        self.input_username(username)
        self.input_password(pwd)
        self.click_login()


    def logout(self):
        """退出系统"""
        self.by_find_element(*self._logout).click()



if __name__ == '__main__':
    driver = BaseDriver()
    driver.get('http://172.16.6.86:8080/oa')
    a = LoginPage(driver)
    a.login()