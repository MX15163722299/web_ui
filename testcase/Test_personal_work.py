'''



功能描述：
        个人办公页面的测试用例

实现功能：






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
from po.HOME.PersonnelOffice.MyApplication.MyApplicationPage import MyApplicationPage
from po.HOME.SystemSetting.UserManagementPage import UserManagementPage
from po.HOME.PersonnelOffice.MyToDoPage import MyToDoPage
from po.HOME.PersonnelOffice.ProcessCenterPage import ProcessCenterPage


class TestPersonalWork(unittest.TestCase):

    def test_employee_go_out_normal(self):
        self.driver = BaseDriver()
        lp = LoginPage(self.driver)
        hp = HomePage(self.driver)
        ip = InitiatePage(self.driver)
        ep = EmployeeGoOutPage(self.driver)
        mp = MyApplicationPage(self.driver)
        up = UserManagementPage(self.driver)
        mtp = MyToDoPage(self.driver)
        pp = ProcessCenterPage(self.driver)

        #登录进首页
        lp.login('xxxxx','xxxxx')
        hp.click_initiate_process()
        process_type = ip.click_personnel_process()
        #1发起员工外出申请，记录下审核标题
        ip.click_employee_go_out()
        process_title = ep.get_process_title()
        ep.input_emergency_situations('一般')
        ep.input_employee_level('普通员工')
        ep.input_leave_time()
        ep.input_return_time()
        ep.input_matter()
        ep.input_address()
        ep.click_submit_button()
        #调用自动审核，完成一系列后续操作
        status = hp.auto_audit(lp,mp,up,mtp,pp,process_title,process_type)

        assert '流程已结束' == status,'用例未通过，请核查原因'
        self.driver.quit()


if __name__ == '__main__':
    # 使用defaultTestLoader调用加载测试套件的方法将当前测试用例类的所有用例加载进suite
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPersonalWork)
    # 获取当前文件的绝对路径
    file = os.path.abspath(__file__)
    # 生成当前用例文件的测试报告
    Public().gen_unittest_report(suite, file)
