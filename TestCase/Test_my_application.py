'''

编写人：
    梁超
编写日期：
    2020年7月9日

实现功能：
    个人办公--我的申请--测试用例




'''
import time

import os,unittest
from Common.Log import logger
from Common.Public import Public
from Common.BaseDriver import BaseDriver
from PO.LoginPage import LoginPage
from PO.HomePage import HomePage
from PO.InitiatePage import InitiatePage
from PO.HOME.PersonnelOffice.MyApplication.MyApplicationPage import MyApplicationPage


class TestMyApplication(unittest.TestCase):


    def test_my_application_normal(self):
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        mp = MyApplicationPage(self.driver)
        lp.login('xxxx','xxxxx')
        hp.click_my_application()
        mp.select_process_type()
        mp.click_search_btn()
        assert 1==2,'用例失败'
        # time.sleep(10)
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMyApplication)
    file = os.path.abspath(__file__)
    Public().gen_unittest_report(suite,file)