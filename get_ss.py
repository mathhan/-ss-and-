# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import threading
import time
class mythread(threading.Thread):
	def __init__(self,function,args,name=''):
		self.function=function
		self.args=args
		self.name=name
	def res(self):
		return apply(self.function,self.args)
	def run(self):
		apply(self.function,self.args)
class getss():
    """TODO:产生含有shadow账号的生成器"""
    def __init__(self, domins="https://github.com", url="https://github.com/Biulink/ShadowsocksTutorials"):
        self.url = url
        self.domins = domins
    def __call__(self):
        return self.get_account_generator()  # 对类的instance的调用可以返回生成器

    def get_link(self): 
	""" 获取网页上的当天含有shadowsocks的页面URL"""
        s = time.strftime("%Y-%m-%d", time.localtime())
        response_url = requests.get(self.url, timeout=5)
        bsobj = BeautifulSoup(response_url.text, "lxml")
        info_need = bsobj.find_all(
            "span", {"class": "css-truncate css-truncate-target"})
        for span in info_need:
            if span.a:
                if s in span.a.contents[0]:
                    self.domins += span.a["href"]
        return self.domins

    def get_account_generator(self):
  	"""产生一个含有shadowsocks账号的生成器"""
        j = 0
        dic = {}
        infi = []
        url = requests.get(self.get_link())
        info = BeautifulSoup(url.text, "lxml")
        info_need = (info.find_all("article", {"itemprop": "text"}))
        for i in info_need[0].find_all("p"):
            s = repr(i).decode("unicode–escape").encode("utf-8")
            if re.findall(re.compile("地址|密码|端口|加密"), s):
                infi.append(re.findall(r'：([\S]+)<', s))
        k = len(infi) // 4
        while j < k:
            for i in ["server", "server_port", "password", "method"]:
                if i == "server_port":
                    dic[i] = int(infi.pop(0)[0])
                else:
                    dic[i] = infi.pop(0)[0]
            j += 1
            dic["local_port"] = 1080
            yield dic
if __name__ == '__main__':
    main()
