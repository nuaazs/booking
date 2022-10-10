# importing flask module
from logging.handlers import RotatingFileHandler
import logging
import os
from utils import ready_to_book,get_info
import info
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--student_id', type=int, default=0,help='')
parser.add_argument('--place_num', type=int, default=3,help='')
parser.add_argument('--time', type=int, default=17,help='')
parser.add_argument('--reload', action='store_true', default=False,help='reload code png')
args = parser.parse_args()

logger = logging.getLogger(f"auto_booking{args.student_id}")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s]  %(levelname)s  [%(filename)s]  #%(lineno)d <%(process)d:%(thread)d>  %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)
handler = RotatingFileHandler(
    f"./log/auto_booking{args.student_id}.log", maxBytes=20 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
handler.setFormatter(formatter)
handler.namer = lambda x: f"auto_booking{args.student_id}." + x.split(".")[-1]
logger.addHandler(handler)


def book_item(item,reload=False):
    i = 1
    if reload or (not os.path.exists(f"./cmds/{args.student_id}.txt")):
        cmd = ready_to_book(info=item,save_path=f"./cmds/{args.student_id}.txt")
    else:
        with open(f"./cmds/{args.student_id}.txt") as f:
            cmd = f.readlines()[0]
    while i<1000:
        logger.info(f"第{i}次尝试中 ... ")
        result = os.popen(cmd).readlines()
        logger.info(result[0])
        print(result[0])
        i += 1
    logger.info("预约成功")

def task(args):
    logger.info(f"* 开始自动预约")
    time_id_1,sub_id_1 = get_info(info.info,args.place_num,args.time)
    names = ["狄","赵","孙"]
    vjuids = [166597,161684,195005]
    vjvds = ["ec67fc9bc953d12201b412a53a03b3ff","c166fba59d187c38712805e1d9e57def","e6a815b9a60384b75ed828422b321218"]
    book_item(item=f"{names[args.student_id]}|vjuid={vjuids[args.student_id]};vjvd={vjvds[args.student_id]}|{time_id_1}|{sub_id_1}|体育中心羽毛球6号场地18点|19",reload=args.reload)
task(args)
