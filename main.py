"""


功能描述：框架的入口文件，主要实现框架的功能集成，报告的输出，邮件的发送或通知等，后续根据需求进行持续优化

实现功能：


"""


import threading
import time

from common.public import Public
from common.Log import logger
import os,subprocess
from common.merge_report import MergeReport



cur_dir = Public().get_basedir()
case_dir = cur_dir + "\\" + 'testcase\\'


def get_test_list():
    """
    获取框架内要运行的所有用例文件名称
    :return: 返回用例组成的列表
    """
    t_list = os.listdir(case_dir)
    return t_list


def run_test(filename):
    """
    多线程调用的目标函数
    :param name: 用来接收传入的i---用例文件名称
    :return:
    """
    #通过控制信号量，来控制同时启动的线程最大数量，with是上下文管理器，可以引用主线程里面的变量
    with pool_sema:
        print('run py start')
        logger.info("python %s%s " % (case_dir,filename))
        # 命令行执行python执行xxpy文件的命令(os.system())
        subprocess.run("python %s%s" % (case_dir,filename))
        print('run py end')


if __name__ == '__main__':
    # 获取当前时间为开始时间
    start_time = time.time()
    # 定义一个存放线程对象的列表
    tlist = []
    # 获取testcase目录下的所有用例文件名称组成的列表
    test_list = get_test_list()
    # 设置启动线程的最大数量，因为电脑不能支持过多的线程执行
    maxconnections = 4
    # 设置信号量，以在run_test方法中使用with来引用控制多线程执行的最大线程数量
    pool_sema = threading.BoundedSemaphore(value=maxconnections)

    logger.info('运行的测试列表：%s' % str(tlist))
    # 遍历用例文件列表
    for i in test_list:
        # 创建线程，传递被执行方法run_test，和参数i---每个用例文件名称
        t = threading.Thread(target=run_test, args=(i,), name='Thread' + str(test_list.index(i)))
        # 设置守护线程
        # t.setDaemon(True)
        # 追加进线程对象列表
        tlist.append(t)

    # 遍历线程列表启动线程
    for i in tlist:
        i.start()

    # 遍历线程列表阻塞线程，让每个执行用例文件的线程全部执行完毕后再执行后面的代码
    for i in tlist:
        i.join()
    time.sleep(5)
    # 获取当前时间作为结束时间，因为当代码执行到此步时说明所有的多线程均已执行完毕
    end_time = time.time()
    # 获取整个项目执行时间（结束-开始）
    elpase_time = end_time - start_time
    logger.info(int(elpase_time))
    # 转换时间戳为时分秒
    d, h, m, s = Public().time_format(int(elpase_time))
    # 实例化合并报告模块
    mr = MergeReport()
    start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(start_time))
    elpase = ' %s 时 %s 分 %s 秒' % ( h, m, s)
    # 合并报告
    mr.merge(start,elpase)
    print('主线程结束，程序运行时长 %s天 %s小时 %s分钟 %s秒' % (d, h, m, s))