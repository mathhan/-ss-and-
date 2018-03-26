# -*- coding: utf-8 -*-
from sockshandler import SocksiPyHandler
from pymongo import MongoClient
from get_ss import getss
import threading
import Queue
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
        time.sleep(2)
        s = opener.open(url)
        # print s.read()
        t_end = time.time()
        return t_end - t_start
    except:
        return 9999999


def average_latency():
    """测试抓取的每个shadowsocks账号的平均延时"""
    sum_time = 0
    url_test = ["https://www.youtube.com",
                "https://www.twitter.com", "https://www.google.hk"]
    for url in url_test:
        sum_time += latency(url)
    aver_time = sum_time // len(url_test)
    print("the average time of lantency:", aver_time)
    return aver_time


def test(account):
    """测试抓取的每个shadowsocks账号，account为从getss类实例调用获取的生成器对象"""
    json_obj = json.dumps(account)
    with open("shadowsocks.json", "w") as fp:
        fp.write(json_obj)
    try:
        subprocess.Popen(["/home/mathhan/.local/bin/sslocal  -c shadowsocks.json"],
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        latency = average_latency()
        print account
        time.sleep(3)
    except Exception as e:
        raise e
    finally:
        subprocess.Popen(["pkill -f shadowsocks.json"], shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
"""添加多线程支持"""
    egg = getss()
    listdic = [eval(repr(x)) for x in egg()] 
    threads = []
    q = Queue.Queue()
    for worker in listdic:
        q.put(worker)

    def job():
        worker = q.get()
        test(worker)
        time.sleep(2)
        q.task_done()
    for worker in listdic:
        t = threading.Thread(target=job)
        threads.append(t)
    for i in threads:
        i.start()
    for j in threads:
        j.join()


if __name__ == '__main__':
    main()
