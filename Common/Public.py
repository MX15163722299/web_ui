
'''

编写人：
    梁超
编写日期：
    2020年7月2日

实现功能：

    封装公共的常用方法
    1-获取工程目录
    2-获取文件名称
    3-生成unittest报告
    4-




'''

import os,math
import time
from HTMLTestRunner_old import HTMLTestRunner
from Common.Log import logger

class Public(object):


    def get_basedir(self):
        """获取项目的根目录"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logger.info('获取的目标目录为%s' % base_dir)
        return base_dir

    def get_file_name(self,file):
        """
        获取文件名称
        """
        filename = os.path.split(os.path.abspath(file))[1].strip('.py')
        logger.info(filename)
        return filename


    def gen_unittest_report(self,suite,file):
        """
        生成单元测试报告
        :param suite:用来接收要运行的测试套件
        :param name:接收要执行的文件名
        :return:
        """
        # 报告
        name = self.get_file_name(file)
        report_dir = self.get_basedir() + "\\" + "TestReport\\"
        report = report_dir + str(name) + "_Report.html"
        file = open(report, 'wb')
        runner = HTMLTestRunner(stream=file, description='UI自动化测试报告', title=name+'.html')
        runner.run(suite)
        file.close()

    def time_format(self,micro_second):
        """
        将时间戳差值转化为：时分秒
        :param micro_second:
        :return:
        """
        # micro_second = float(micro_second)
        #  总秒数
        second = float(micro_second)
        # // 天数
        day = math.floor(second / 3600 / 24)
        # // 小时
        hour = math.floor(second / 3600 % 24)
        # // 分钟
        min = math.floor(second / 60 % 60)
        # // 秒/
        sec = math.floor(second % 60)

        print(day,hour,min,sec)
        return day,hour,min,sec






if __name__ == '__main__':
    Public().time_format(60)