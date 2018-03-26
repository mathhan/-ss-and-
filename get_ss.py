# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import threading
import time


# class mythread(threading.Thread):
#     def __init__(self, function, args, name=''):
#         self.function = function
#         self.args = args
#         self.name = name

#     def res(self):
#         return apply(self.function, self.args)

#     def run(self):
#         apply(self.function, self.args)


class getss():
    """TODO:产生含有shadow账号的生成器"""

    def __init__(self, url="https://github.com/Biulink/ShadowsocksTutorials"):
        self.url = url        # self.domins = domins

    def __call__(self):
        return self.get_account_generator()  # 对类的instance的调用可以返回生成器

    def get_link(self):
        """ 获取网页上的当天含有shadowsocks的页面URL"""
        s = time.strftime("%Y-%m-%d", time.localtime())
        response_url = requests.get(self.url, timeout=5)
        bsobj = BeautifulSoup(response_url.text, "lxml")
        info_need = bsobj.find_all('a')
        temp = [x["href"] for x in info_need if s in x['href']][0]
        return temp

    def get_account_generator(self):
        """产生一个含有shadowsocks账号的生成器"""
        j = 0
        dic = {}
        temp = []
        url = requests.get(self.get_link())
        info = BeautifulSoup(url.text, "lxml")
        info_need = info.find_all('p')
        for i in info_need:
            f = re.findall('：([\S]+)', i.text.encode('utf-8'))
            if f:
                temp.append(f[0])
        te = len(temp) // 6
        while j < te:
            for i in ["server", "server_port", "password", "method", "size", "date"]:
                if i == "server_port":
                    dic[i] = int(temp.pop(0))
                else:
                    dic[i] = temp.pop(0)
            j = j + 1
            dic.pop("size")
            dic.pop("date")
            dic["local_port"] = 1080
            yield dic
