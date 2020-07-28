"""

编写人：
    梁超
编写日期：
    2020年7月15日


功能描述：框架的入口文件，主要实现框架的功能集成，报告的输出，邮件的发送或通知等，后续根据需求进行持续优化

实现功能：


"""


import threading
import time

from Common.Public import Public
from Common.Log import logger
import os,subprocess
from Common.MergeReport import MergeReport



cur_dir = Public().get_basedir()
case_dir = cur_dir + "\\" + 'TestCase\\'


def get_test_list():
    """
    获取框架内要运行的所有用例文件名称
    :return: 返回用例组成的列表
    """
    t_list = os.listdir(case_dir)
    return t_list


def run_test(name):
    """
    多线程调用的目标函数
    :param name:
    :return:
    """
    #通过控制信号量，来控制同时启动的线程最大数量
    with pool_sema:
        print('run py start')
        logger.info("python %s%s " % (case_dir,name))
        subprocess.run("python %s%s " % (case_dir,name))
        print('run py end')


if __name__ == '__main__':
    start_time = time.time()
    tlist = []
    test_list = get_test_list()
    # 设置启动线程的最大数量
    maxconnections = 4
    pool_sema = threading.BoundedSemaphore(value=maxconnections)

    logger.info('运行的测试列表：%s' % str(tlist))
    for i in test_list:
        t = threading.Thread(target=run_test, args=(i,), name='Thread' + str(test_list.index(i)))
        t.setDaemon(True)
        tlist.append(t)

    for i in tlist:
        i.start()

    for i in tlist:
        i.join()
    time.sleep(5)
    end_time = time.time()
    elpase_time = end_time - start_time
    logger.info(int(elpase_time))
    d, h, m, s = Public().time_format(int(elpase_time))
    mr = MergeReport()
    start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(start_time))
    elpase = ' %s 时 %s 分 %s 秒' % ( h, m, s)
    mr.merge(start,elpase)
    print('主线程结束，程序运行时长 %s天 %s小时 %s分钟 %s秒' % (d, h, m, s))