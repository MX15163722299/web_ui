'''

编写人：
    梁超
编写日期：
    2020年7月8日

实现功能：
    员工外出流程的测试用例




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
from PO.HOME.PersonnelOffice.MyApplication.MyApplicationPage import MyApplicationPage
from PO.HOME.SystemSetting.UserManagementPage import UserManagementPage
from PO.HOME.PersonnelOffice.MyToDoPage import MyToDoPage
from PO.HOME.PersonnelOffice.ProcessCenterPage import ProcessCenterPage

class TestEmployeeGoOut(unittest.TestCase):

    @unittest.skip('n')
    def test_employee_go_out_normal(self):
        """测试一般员工的外出申请流程"""
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        ip = InitiatePage(self.driver)
        ep = EmployeeGoOutPage(self.driver)
        mp = MyApplicationPage(self.driver)
        up = UserManagementPage(self.driver)
        mtp = MyToDoPage(self.driver)
        pp = ProcessCenterPage(self.driver)

        # 登录进首页
        lp.login('xxxxx', 'xxxx')
        hp.click_initiate_process()
        process_type = ip.click_personnel_process()
        # 1发起员工外出申请，记录下审核标题
        ip.click_employee_go_out()
        process_title = ep.get_process_title()
        ep.input_emergency_situations('一般')
        ep.input_employee_level('普通员工')
        ep.input_leave_time()
        ep.input_return_time()
        ep.input_matter()
        ep.input_address()
        ep.click_submit_button()
        # 调用自动审核，完成一系列后续操作
        status = hp.auto_audit(lp, mp, up, mtp, pp, process_title, process_type)

        assert '流程已结束' == status, '用例未通过，请核查原因'
        self.driver.quit()

    @unittest.skip('n')
    def test_employee_go_out_leader(self):
        """测试部门负责人含以上的"""
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        ip = InitiatePage(self.driver)
        ep = EmployeeGoOutPage(self.driver)
        mp = MyApplicationPage(self.driver)
        up = UserManagementPage(self.driver)
        mtp = MyToDoPage(self.driver)
        pp = ProcessCenterPage(self.driver)

        # 登录进首页
        lp.login('xxxx', 'xxxx')
        hp.click_initiate_process()
        process_type = ip.click_personnel_process()
        # 1发起员工外出申请，记录下审核标题
        ip.click_employee_go_out()
        process_title = ep.get_process_title()
        ep.input_emergency_situations('一般')
        ep.input_employee_level('部门负责人')
        ep.input_leave_time()
        ep.input_return_time()
        ep.input_matter()
        ep.input_address()
        ep.click_submit_button()
        # 调用自动审核，完成一系列后续操作
        status = hp.auto_audit(lp, mp, up, mtp, pp, process_title, process_type)

        assert '流程已结束' == status, '用例未通过，请核查原因'
        self.driver.quit()


    def test_employee_go_out_greater_five_day(self):
        """测试请假外出时间大于5天"""
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        ip = InitiatePage(self.driver)
        ep = EmployeeGoOutPage(self.driver)
        mp = MyApplicationPage(self.driver)
        up = UserManagementPage(self.driver)
        mtp = MyToDoPage(self.driver)
        pp = ProcessCenterPage(self.driver)

        # 登录进首页
        lp.login('xxxx', 'xxxxx')
        hp.click_initiate_process()
        process_type = ip.click_personnel_process()
        # 1发起员工外出申请，记录下审核标题
        ip.click_employee_go_out()
        process_title = ep.get_process_title()
        ep.input_emergency_situations('一般')
        ep.input_employee_level('普通员工')
        ep.input_leave_time()
        ep.input_return_time(6)
        ep.input_matter()
        ep.input_address()
        ep.click_submit_button()
        # 调用自动审核，完成一系列后续操作
        status = hp.auto_audit(lp, mp, up, mtp, pp, process_title, process_type)

        assert '流程已结束' == status, '用例未通过，请核查原因'
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEmployeeGoOut)
    file = os.path.abspath(__file__)
    Public().gen_unittest_report(suite, file)
