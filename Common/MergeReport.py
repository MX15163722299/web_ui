'''

编写人：
    梁超
编写日期：
    2020年7月22日

实现功能：将多线程生成的报告抽取合并
    1-抽取关键信息
        1.1-测试执行时间
        1.2-每份报告中的汇总记录
        1.3-每份报告的名称
    2-写入新报告模板
        2.1-替换报告头部概要信息，
            2.1.1将提取出来的信息，替换到tr1中
        2.2-插入每份报告中提取的报告名称和汇总记录
            2.2.1-将提取的每个报告的概要信息替换到tr2中
            2.2.2-逐个写入到报告模板中
        2.3-插入汇总计算后的统计信息
        2.4-插入最后的html末尾

'''

import re, os
from Common.Public import Public
from Common.Log import logger

# 定义报告模板头部信息
head = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>UI自动化</title>
    <meta name="generator" content="HTMLTestRunner 0.8.2.1" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>

    <style type="text/css" media="screen">
        body {
            font-family: Microsoft YaHei, Tahoma, arial, helvetica, sans-serif;
            padding: 20px;
            font-size: 100%;
        }

        table {
            font-size: 100%;
        }

        /* -- heading ---------------------------------------------------------------------- */
        .heading {
            margin-top: 0ex;
            margin-bottom: 1ex;
            font-size: 20px;
        }

        .heading .description {
            margin-top: 4ex;
            margin-bottom: 6ex;
        }

        /* -- report ------------------------------------------------------------------------ */
        #total_row {
            font-weight: bold;
        }

        .passCase {
            color: #5cb85c;
        }

        .failCase {
            color: #d9534f;
            font-weight: bold;
        }

        .errorCase {
            color: #f0ad4e;
            font-weight: bold;
        }

        .hiddenRow {
            display: none;
        }

        .testcase {
            margin-left: 2em;
        }
    </style>

</head>

<body>

"""

# html写入的第1部分
div = """
    <div class='heading'>
        <h1 style="font-family: Microsoft YaHei">UI自动化测试报告</h1>
        <p class='attribute'><strong>测试人员 : </strong> hujingyi</p>
        <p class='attribute'><strong>开始时间 : </strong> {}</p>
        <p class='attribute'><strong>合计耗时 : </strong> {}</p>
        <p class='attribute'><strong>测试结果 : </strong> 共 {}，通过 {}，通过率= {} </p>
        <p class='description'>UI自动化测试报告</p>
    </div>
    """

# html写入的第2部分
p = """
    <p id='show_detail_line'>
        <a class="btn btn-primary" href='javascript:showCase(4)'>概要{}</a>
        <a class="btn btn-warning" href='javascript:showCase(2)'>错误{}</a>
        <a class="btn btn-danger" href='javascript:showCase(1)'>失败{}</a>
        <a class="btn btn-success" href='javascript:showCase(0)'>通过{}</a>
        <a class="btn btn-info" href='javascript:showCase(3)'>所有{}</a>
    </p>
    """
print(p.format('{ 1 }', '2', '3', '4', '5'))
# html写入的第3部分
table = """
    <table id='result_table' class="table table-condensed table-bordered table-hover">
        <tr id='header_row' class="text-center active" style="font-weight: bold;font-size: 14px;">
            <td>用例集/测试用例</td>
            <td>总计</td>
            <td>通过</td>
            <td>失败</td>
            <td>错误</td>
            <td>通过率</td>
            <td>详细</td>
        </tr>
"""
# html写入的第4部分
tr1 = """
            <tr class='passClass'>
                <td>{}</td>
                <td class="text-center">{}</td>
                <td class="text-center">{}</td>
                <td class="text-center">{}</td>
                <td class="text-center">{}</td>
                <td class="text-center">{}</td>
                <td class="text-center"><a href="./{}" class="detail"
                        id='c1'>详细</a>
                </td>

            </tr>

        """
# html写入的第5部分
tr2 = """
            <tr id='total_row' class="text-center info">
            <td>总计</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>通过率：{}</td>
            <td> <a href="" target="_blank"></a></td>
        </tr>
"""
# html写入的第四部分
tail = """
    </table>
</body>
</html>
"""


class MergeReport(object):
    """
    准备模板文件
    准备要提取的目标报告
    """

    _template = Public().get_basedir() + '\\' + 'TestReport\\' + 'template.html'
    _report_dir = Public().get_basedir() + '\\' + 'TestReport\\'
    _report_list = []

    """方法"""
    """


    1-抽取关键信息
        1.1-测试执行时间
        1.2-每份报告中的汇总记录
        1.3-每份报告的名称
    2-写入新报告模板
        2.1-替换报告头部概要信息
        2.2-插入每份报告中提取的报告名称和汇总记录
        2.3-插入汇总计算后的统计信息
    3-拿到报告下的所有独立报告

    """

    def __init__(self):
        with open(self._template, 'w', encoding="utf-8") as file:
            file.write(head)

    def get_report_list(self):
        """"""
        rep_list = []
        report_list = os.listdir(self._report_dir)
        report_list.remove('template.html')
        logger.info('' % report_list)

        for i in report_list:
            rep_list.append(self._report_dir + i)
        return rep_list

    def get_all_report_list(self):
        """
        提取每个报告的汇总信息和名称"
        :param:file 接收要提取信息的报告文件
        :return: 返回每个报告抽取出来的概要信息汇总成的list

        """""

        # hujingyi修改---字段顺序错误导致的报告成功数量不正确。错误的顺序是：name_list = ['file','summary','error','failure','pass','total']
        name_list = ['file', 'summary', 'pass', 'failure', 'error', 'total']
        total_sum = []
        report_list = self.get_report_list()
        logger.info('获取到的list%s' % report_list)
        # 先获取报告列表，再遍历每个报告，提取公共概要信息
        for i in report_list:
            sum_list = []
            with open(i, 'r', encoding='utf-8') as f:
                while True:
                    result = f.readline()
                    # logger.info('result %s' % result)
                    if len(str(result)) == 0:
                        break
                    elif result.find('javascript:showCase(') != -1:

                        pattern = re.compile("(showCase\(\d\)'>.*\{\s)(.*?)(\s\}</a>)")
                        re_list = re.search(pattern, result)
                        sum_list.append(re_list.group(2))

                # 将报告的名称插入第一位
                filename = os.path.split(i)[1]
                sum_list.insert(0, filename)
                # 将提取出来的概要信息拼成dict
            sum_dict = {x: y for x, y in zip(name_list, sum_list)}
            logger.info('组织的概要信息%s', str(sum_dict))

            # 将获取到的每个报告的概要信息添加到一个list，方便后期写入和计算
            total_sum.append(sum_dict)
        logger.info('最终的统计列表%s' % total_sum)
        return total_sum

    def get_summary(self, start=None, elapse=None):
        """
        根据汇总的报告列表，统计报告的摘要信息

        :param start: 传入开始时间
        :param end: 传入结束时间
        :param elapse: 传入运行时长
        :return: start_time 框架运行时间
        :return: duration 合计时长
        :return: passing_rate 全部的通过率
        :return: sum 全部用例总数
        :return: pas 全部通过的用例总数
        :return: passing_rate 全部的通过率
        :return: err 全部错误的用例总数
        :return: fail 全部失败的用例总数
        """
        start_time = start
        duration = elapse

        s_list = self.get_all_report_list()
        # sum用来保存total总数，pas用来保存pass的总数
        sum, pas, err, fail = 0, 0, 0, 0
        # 概要=通过的总数/总计的总数
        # 先获取通过的总数，在获取总计的总数
        for i in s_list:
            logger.info('遍历的信息：%s' % str(i))
            sum += int(i.get('total'))
            pas += int(i.get('pass'))
            err += int(i.get('error'))
            fail += int(i.get('failure'))
        logger.info('sum: %s, pas: %s' % (sum, pas))
        passing_rate = '{:.0f}%'.format(pas / sum * 100)

        # 读取所有报告，汇总所有用例数量，通过，失败，错误
        return start_time, duration, sum, pas, passing_rate, err, fail

    def write_html_summary(self, start, elapse):
        """
        提取报告汇总信息，替换模板内容，写入表头
        :return:
        """
        start_time, duration, sum, pas, passing_rate, err, fail = self.get_summary(start, elapse)
        content1 = div.format(start_time, duration, sum, pas, passing_rate)
        logger.info(content1)
        # 写入头部
        with open(self._template, 'a', encoding='utf-8') as file:
            file.write(content1)

        passing_rate = '{ ' + passing_rate + ' }'
        err = '{ ' + str(err) + ' }'
        fail = '{ ' + str(fail) + ' }'
        pas = '{ ' + str(pas) + ' }'
        sum = '{ ' + str(sum) + ' }'
        content2 = p.format(passing_rate, err, fail, pas, sum)
        logger.info(content2)

        # 写入概要信息和表格头部
        with open(self._template, 'a', encoding='utf-8') as file:
            file.write(content2)
            file.write(table)

    def write_html_record(self):
        """
        获取所有报告的记录列表，遍历写入tr

        :return:
        """
        rep_list = self.get_all_report_list()
        with open(self._template, 'a', encoding='utf-8') as file:
            # 遍历报告的概要信息列表，提取每个元素的字段信息，迭代写入报告模板
            for i in rep_list:
                # 提取字段
                record = tr1.format(i.get('file'), i.get('total'), i.get('pass'), i.get('failure'), i.get('error'),
                                    i.get('summary'), i.get('file'))
                # 替换字段
                file.write(record)
                # 写入字段

            # 将报告最终的统计和尾部写入
            start_time, duration, sum, pas, passing_rate, err, fail = self.get_summary()
            content = tr2.format(sum, pas, fail, err, passing_rate)
            file.write(content)
            file.write(tail)

    def merge(self, start, elapse):
        self.write_html_summary(start, elapse)
        self.write_html_record()


if __name__ == '__main__':
    m = MergeReport()
    m.write_html_summary()
    m.write_html_record()


