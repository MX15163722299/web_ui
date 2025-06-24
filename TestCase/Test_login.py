'''

实现功能：
    登录界面的测试用例




'''

import os
from Common.Log import logger
from Common.Public import Public
from Common.BaseDriver import BaseDriver
from PO.LoginPage import LoginPage
import unittest

class TestLogin(unittest.TestCase):


    def test_login_normal1(self):
        """测试普通员工的外出申请流程"""
        self.driver = BaseDriver()
        self.url = 'https://www.baidu.com'
        self.driver.get(self.url)
        login_page = LoginPage(self.driver)
        login_page.login()
        logger.info('登录测试完毕')
        assert '办公系统' == self.driver.title
        self.driver.quit()

    def test_login_normal2(self):
        """测试部门负责人含以上的"""
        self.driver = BaseDriver()
        self.url = 'xxxxx'
        self.driver.get(self.url)
        login_page = LoginPage(self.driver)
        login_page.login()
        logger.info('登录测试完毕')
        assert '办公系' == self.driver.title
        self.driver.quit()

if __name__ == '__main__':
    # 使用defaultTestLoader调用加载测试套件的方法将当前测试用例类的所有用例加载进suite
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLogin)
    # 获取当前文件的绝对路径
    file = os.path.abspath(__file__)
    # 生成当前用例文件的测试报告
    Public().gen_unittest_report(suite, file)