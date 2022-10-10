# importing flask module

from flask import Flask
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
import requests
from multiprocessing.dummy import Pool as ThreadPool
from logging.handlers import RotatingFileHandler
import logging
import time
import subprocess
import os
from aip import AipOcr
from utils import ready_to_book

aps = APScheduler()
app = Flask(__name__)



logger = logging.getLogger("auto_booking")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s]  %(levelname)s  [%(filename)s]  #%(lineno)d <%(process)d:%(thread)d>  %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)
handler = RotatingFileHandler(
    "./log/auto_booking.log", maxBytes=20 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
handler.setFormatter(formatter)
handler.namer = lambda x: "auto_booking." + x.split(".")[-1]
logger.addHandler(handler)
logger.info("qidong")

def book_item(item):
    i=1
    i = 1
    cmd = ready_to_book(info=item)
    result = os.popen(cmd).readlines()
    while ("验证码错误" in result[0]):
        try:
            cmd = ready_to_book(info=item)
            result = os.popen(cmd).readlines()
        except:
            continue
    logger.info("验证码破解成功")
    name = item.split("|"[0])
    # with open(f"/home/zhaosheng/auto_booking_server/code_txts/{name}.txt",'r') as f:
    #     cmd=f.read()
    # print(cmd)

    result = os.popen(cmd).readlines()
    while ("验证码错误" in result[0]):
        try:
            cmd = ready_to_book(info=item)
            result = os.popen(cmd).readlines()
        except:
            continue
    logger.info("验证码破解成功")
     
    
    while not ("成功" in result[0]):
        logger.info(f"第{i}次尝试中 ... ")
        result = os.popen(cmd).readlines()
        logger.info(result[0])
        i += 1
    logger.info("预约成功")

def task():
    print(str(datetime.now()) + ' execute booking task.')
    logger.info(f"* 开始自动预约")
    items = [ "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2100|13114|体育中心羽毛球7号场地18点|19"]
            # "赵胜|vjuid=161684|vjvd=c166fba59d187c38712805e1d9e57def|2095|13106|体育中心羽毛球7号场地13点|19"]
            # "狄兴|vjuid=166597|vjvd=ec67fc9bc953d12201b412a53a03b3ff|2102|13090|体育中心羽毛球6号场地13点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2095|13106|体育中心羽毛球7号场地13点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2094|13092|体育中心羽毛球6号场地12点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2094|13105|体育中心羽毛球7号场地12点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2100|13101|体育中心羽毛球6号场地18点|19",]
    if len(items) == 1:
        logger.info("{items[0]} 单线程模式")
        book_item(items[0])
    else:
        pool = ThreadPool(len(items))
        pool.map(book_item, items)
        pool.close()
        pool.join()


def task2():
    print(str(datetime.now()) + ' execute booking task.')
    logger.info(f"* 开始自动预约")
    items = [ "赵胜|vjuid=161684|vjvd=c166fba59d187c38712805e1d9e57def|2101|13115|体育中心羽毛球7号场地19点|19"]
            # "赵胜|vjuid=161684|vjvd=c166fba59d187c38712805e1d9e57def|2095|13106|体育中心羽毛球7号场地13点|19"]
            # "狄兴|vjuid=166597|vjvd=ec67fc9bc953d12201b412a53a03b3ff|2102|13090|体育中心羽毛球6号场地13点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2095|13106|体育中心羽毛球7号场地13点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2094|13092|体育中心羽毛球6号场地12点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2094|13105|体育中心羽毛球7号场地12点|19",
            # "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2100|13101|体育中心羽毛球6号场地18点|19",]
    if len(items) == 1:
        logger.info("{items[0]} 单线程模式")
        book_item(items[0])
    else:
        pool = ThreadPool(len(items))
        pool.map(book_item, items)
        pool.close()
        pool.join()

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'booking_server:task',
            'trigger': 'cron',
            'hour': 2,
            'minute':24,
            'second':50
        },
        {
            'id': 'job1',
            'func': 'booking_server:task2',
            'trigger': 'cron',
            'hour': 2,
            'minute':24,
            'second':50
        }
    ]
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
if __name__ == "__main__":
    
    app.run(port=8190,threaded=False, debug=False,)