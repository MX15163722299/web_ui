
import requests
from common.read_config import ReadConfig
rc = ReadConfig()

class DingTalk:
    # 1.定义初始化方法
    def __init__(self):
        self.headers = {'Content-Type': 'application/json;charset=utf-8'}
        # self.url = 'https://oapi.dingtalk.com/robot/send?access_token=ded597142fbee3889e19d9b1ecc06ad89b7b91c7bbc55fd30c38ba06f5f46818'
        self.url = rc.get_config("dingtalk","roboturl")


  #
    def send_msg(self, text):
        dic = {
            "msgtype": "text",
            "text": {"content": text},
            "at": {
                "atMobiles": ["+86-18513813721","+86-15163722299","+86-15106372158"],
                "isAtaLL": False}
        }
        requests.post(url=self.url, json=dic, headers=self.headers)

    def send_link(self,text,url):
        dic = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": "橙好登录模块测试报告,请查收",
                "messageUrl": url
            }
        }
        requests.post(url=self.url, json=dic, headers=self.headers)


if __name__ == '__main__':
    dt = DingTalk()
    dt.send_msg('test：孟旭-接口测试报告已发邮箱')
    # dt.send_link('test：谢广坤','https://mp.weixin.qq.com/s/CAi8GRJXQZwv4AoFCYe9hA')
