'''


实现功能：
    系统设置-用户管理的测试用例




'''
import time

import os,unittest
from common.log import logger
from common.public import Public
from common.base_driver import BaseDriver
from po.LoginPage import LoginPage
from po.HomePage import HomePage
from po.InitiatePage import InitiatePage
from po.HOME.PersonnelOffice.InitiateProcess.EmpolyeeGoOutPage import EmployeeGoOutPage
from po.HOME.SystemSetting.UserManagementPage import UserManagementPage

class TestUserManagement(unittest.TestCase):


    def test_user_management_normal(self):
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        lp.login()
        hp = HomePage(self.driver)
        hp.click_system_setting()
        hp.click_user_management()
        up = UserManagementPage(self.driver)
        up.get_login_id('xxx')



if __name__ == '__main__':
    # 使用defaultTestLoader调用加载测试套件的方法将当前测试用例类的所有用例加载进suite
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUserManagement)
    # 获取当前文件的绝对路径
    file = os.path.abspath(__file__)
    # 生成当前用例文件的测试报告
    Public().gen_unittest_report(suite, file)