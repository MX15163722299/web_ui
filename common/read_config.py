"""
创建一个类
1.定义初始化方法：
    1.1 获取配置文件路径
    1.2 实例化configparser类
    1.3 读取路径下的配置文件
2.定义一个对外的方法，获取某个section下所有option的值
    获取section下所有option的值


"""

import os
from configparser import ConfigParser

#
# 创建一个类
class ReadConfig:
    # 1.定义初始化方法：
    def __init__(self):
        #     1.1 获取配置文件路径
        self.path = os.path.dirname(os.path.dirname(__file__)) + r"/config.ini"
        #     1.2 实例化configparser类
        self.conf = ConfigParser()
        #     1.3 读取路径下的配置文件
        self.conf.read(self.path, encoding="utf-8")
        print(f"所有sesion值：{self.conf.sections()}")
    # 2.定义一个对外的方法，获取某个section下所有option的值
    def get_options(self,section):

        #     获取section下所有option的值
        return self.conf.items(section)
    #2.定义一个对外获取某个section下的option的值
    def get_option(self,section,option):
        return self.conf.get(section,option)

    def get_config(self,*args):
        print(args)
        print(args[0])
        print(args[1])

        if len(args) == 1:
            return self.conf.items(args[0])
        elif args[1].lower() == 'all':
            return self.conf.items(args[0])
        else:
            return self.conf.get(args[0],args[1])


if __name__ == '__main__':
    re = ReadConfig()
    # print(re.get_options("mysql"))
    print(re.get_option("driver","gui"))
    # print(re.get_config("driver","gui",'url'))
    print(re.get_config("driver","all"))
    # print(re.get_config("email","sender"))