# -*- coding: utf-8 -*-
from sockshandler import SocksiPyHandler
from pymongo import MongoClient
from get_ss import getss, mythread
import threading
import subprocess
import urllib2
import socks
import json
import time
def latency(url):
    """测试三个外网的get的平均延时"""
    t_start = time.time()
    try:
        opener = urllib2.build_opener(
            SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1080))
        time.sleep(1)
        s = opener.open(url, timeout=2)
    except:
        pass
    t_end = time.time()
    return t_end - t_start
def average_latency():
    """测试抓取的每个shadowsocks账号的平均延时"""
    sum_time = 0
    url_test = ["https://www.twitter.com",
                "https://www.youtube.com", "https://www.google.hk"]
    for url in url_test:
        sum_time += latency(url)
    aver_time = sum_time // len(url_test)
    print("the average time of lantency:", aver_time)
    return aver_time
def test(account):
    """测试抓取的每个shadowsocks账号，account为从getss类实例调用获取的生成器对象"""
    json_obj = json.dumps(account)
    # print account
    with open("shadowsocks.json", "w") as fp:
        fp.write(json_obj)
    try:
        subprocess.Popen(["/home/mathhan/.local/bin/sslocal  -c shadowsocks.json"],
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #latency = average_latency()
        # if latency < 8:
        # storess(account)
    except Exception as e:
        raise e
    finally:
        subprocess.Popen(["pkill -f shadowsocks.json"], shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#def storess(temp):
 # TODO
 #   """储存字典对象的账号的信息到数据库，我这里用的是mongodb数据库，传入的参数是python字典"""
 #  client = MongoClient('localhost:2701')
 #  db = client.proxy
 #  collections = db.fetch_proxy
 #   temp['_id'] = round(time.time(), 2)
 #   collections.insert(temp)
egg = getss()
listdic = [eval(repr(x)) for x in egg()]#测试的时候突然不能取了，很奇怪
def main():
    threads = []
    for i in range(len(listdic)):
        t = mythread(test, (listdic[i],), test.__name__)
        threads.append(t)
    for i in range(len(listdic)):
        threads[i].start()
    for i in range(len(listdic)):
        threads[i].join()
        # print threads[i].res()
        print listdic[i]
    print 'fininsh'
if __name__ == '__main__':
	main()
