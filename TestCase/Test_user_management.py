'''

编写人：
    梁超
编写日期：
    2020年7月13日

实现功能：
    系统设置-用户管理的测试用例




'''
import time

import os,unittest
from Common.Log import logger
from Common.Public import Public
from Common.BaseDriver import BaseDriver
from PO.LoginPage import LoginPage
from PO.HomePage import HomePage
from PO.InitiatePage import InitiatePage
from PO.HOME.PersonnelOffice.InitiateProcess.EmpolyeeGoOutPage import EmployeeGoOutPage
from PO.HOME.SystemSetting.UserManagementPage import UserManagementPage

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
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUserManagement)
    file = os.path.abspath(__file__)
    Public().gen_unittest_report(suite,file)