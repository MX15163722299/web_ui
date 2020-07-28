'''

编写人：
    梁超
编写日期：
    2020年7月17日

实现功能：
    读取框架的配置

    方法：



'''
import configparser
import os
from Common.Public import Public

class ReadConfig(object):
    def __init__(self):
        #属性（读取文件的参数）
        self.conf = configparser.ConfigParser()
        #获取配置文件的路径
        self.file_path = Public().get_basedir() +"\\"+'config.ini'
        # print(self.file_path)
        self.data = self.conf.read(self.file_path,encoding="utf-8-sig")
        # print(self.data,'-------')

    def get_email(self,option='all'):
        """
        获取email中的email的全部或某个option，
        如果不传参默认获取全部，
        如果传参默认获取某一个option

        :return: 结果样式：
                all：[('host', '127.0.0.1')]
                单个：127.0.0.1
        """
        if option == 'all':
            return self.conf.items('EMAIL')
        else:
            return self.conf.get('EMAIL',option)

    def get_driver(self,option='all'):
        """
        获取email中的email的全部或某个option，
        如果不传参默认获取全部，
        如果传参默认获取某一个option

        :return: 结果样式：
                all：[('host', '127.0.0.1')]
                单个：127.0.0.1
        """
        if option == 'all':
            return self.conf.items('DRIVER')
        else:
            return self.conf.get('DRIVER',option)


if __name__ == '__main__':
    rc = ReadConfig()
    print(rc.get_email('host'))