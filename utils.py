import time
from datetime import datetime
import subprocess
import os
from aip import AipOcr
import logging
from past.builtins import raw_input
import json
from IPython import embed
APP_ID = '22845809'
API_KEY = 'tG12dU6oMHaSrOvK62gShfGL'
SECRET_KEY = 'IYqIt6pyKqda2gdZhtUzgXx4RyKVbtzV'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
logger = logging.getLogger("auto_booking")


import requests
def send_error(pic_id):

    url = "http://upload.chaojiying.net/Upload/ReportError.php"

    payload={
        "user":"zhaosheng",
        "pass":"Nt3380517",
        "soft_id":937747,

        "id":pic_id
    }
    files=[

    ]
    headers = {
    'User-Agent': '<User-Agent>'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def get_code_result(filepath):
    url = "http://upload.chaojiying.net/Upload/Processing.php"
    filetype = filepath.split(".")[-1]
    payload={
        "user":"zhaosheng",
        "pass":"Nt3380517",
        "soft_id":937747,
        "codetype":1902,
        "len_min":6
    }
    files=[
    ('userfile',(filepath.split("/")[-1],open(filepath,'rb'),f"image/{filetype}"))
    ]
    headers = {
    'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    return response.json()

def get_file_content(filePath):
  with open(filePath, "rb") as fp:
     return fp.read()

def get_info(_list,num,hour):
    for _data in _list:
        if _data["yaxis"].startswith(str(hour)+":00") and _data["abscissa"].startswith(str(num)+"号"):
            logger.info(_data)
            return _data["time_id"],_data["sub_id"]
    return None,None

def get_png_picture(name,vjuid,vjvd,save_path):
    timestemp = int(time.mktime(time.localtime(time.time()))*1000)
    logger.info(f"* {name} Generating code :> *")
    logger.info(f"\t-> Time: {timestemp}")
    logger.info(f"\t-> Generating code png ... ")

    cmd_get_png = f"curl 'https://ehall3.nuaa.edu.cn/site/login/code?v={timestemp}' \
    -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
    -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'Cookie: iPlanetDirectoryPro=IbDFuwqyVjTD7daZpLbo1NakeSzjzIuK; PHPSESSID=ST-760434-2jZBzfxe2-mRHZR9nyY2faXN320authserver1; {vjuid}; {vjvd};' \
    -H 'Referer: https://ehall3.nuaa.edu.cn/v2/reserve/m_reserveDetail?id=20' \
    -H 'Sec-Fetch-Dest: image' \
    -H 'Sec-Fetch-Mode: no-cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' \
    --compressed \
    --output {save_path}"
    result = os.popen(cmd_get_png).readlines()
    logger.info(f"\t-> {result}")
    return f"{save_path}/{timestemp}_{name}.png"
        
def get_code_text(filepath):
    image = get_file_content(filepath)
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    res_image = client.basicAccurate(image, options)
    print(res_image)
    word = res_image["words_result"][0]['words'].replace(" ","")
    logger.info(f"\t-> Code : {word} ")
    return word

def booking(name,vjuid,vjvd,resource_id,period,sub_resource_id,date):
    cmd = f"curl 'https://ehall3.nuaa.edu.cn/site/reservation/launch' \
    -H 'Accept: application/json, text/plain, */*' \
    -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Cookie: iPlanetDirectoryPro=IbDFuwqyVjTD7daZpLbo1NakeSzjzIuK; PHPSESSID=ST-760434-2jZBzfxe2-mRHZR9nyY2faXN320authserver1; {vjuid};{vjvd};' \
    -H 'Origin: https://ehall3.nuaa.edu.cn' \
    -H 'Referer: https://ehall3.nuaa.edu.cn/v2/reserve/m_reserveDetail?id=20' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --data-raw 'resource_id={resource_id}&code={word}&remarks=&deduct_num=&data=%5B%7B%22date%22%3A%22{date}%22%2C%22period%22%3A{period}%2C%22sub_resource_id%22%3A{sub_resource_id}%7D%5D' \
    --compressed"
    result = os.popen(cmd).readlines()
    return result

def get_booking_cmd(name,vjuid,vjvd,resource_id,period,sub_resource_id,date,word):
    cmd = f"curl 'https://ehall3.nuaa.edu.cn/site/reservation/launch' \
    -H 'Accept: application/json, text/plain, */*' \
    -H 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Cookie: iPlanetDirectoryPro=IbDFuwqyVjTD7daZpLbo1NakeSzjzIuK; PHPSESSID=ST-760434-2jZBzfxe2-mRHZR9nyY2faXN320authserver1; {vjuid};{vjvd};' \
    -H 'Origin: https://ehall3.nuaa.edu.cn' \
    -H 'Referer: https://ehall3.nuaa.edu.cn/v2/reserve/m_reserveDetail?id=20' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --data-raw 'resource_id={resource_id}&code={word}&remarks=&deduct_num=&data=%5B%7B%22date%22%3A%22{date}%22%2C%22period%22%3A{period}%2C%22sub_resource_id%22%3A{sub_resource_id}%7D%5D' \
    --compressed"

    return cmd

def ready_to_book(info="狄兴|vjuid=166597|vjvd=ec67fc9bc953d12201b412a53a03b3ff|2102|13090|体育中心羽毛球6号场地下午1点|19",save_path = "./cmds/test.txt"):

    """
    name | vjuid | vjvd | period | sub_resource_id | messange | resource_id
    田锋|vjuid=150723;vjvd=43cdc35efc4fd8df5f899ddb5b94c59c|1421|11628|羽毛球东区6号场地6点|17
    狄兴|vjuid=166597;vjvd=31eb9b9bd5ddf5ecbb64a505cd8c68f3|1422|11629|羽毛球东区6号场地7点|17
    赵胜|vjuid=161684;vjvd=d31b0d0fdd8b2f5e16c82c0124886080|1421|11615|羽毛球东区5号场地6点|17
    孙章捷|vjuid=195005;vjvd=ab0ff62c44f254bba408b87ae3bec743|1422|11616|羽毛球东区5号场地7点|17
    田锋|vjuid=150723;vjvd=43cdc35efc4fd8df5f899ddb5b94c59c|1335|11151|网球东区5号场地6点|20
    狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|1336|11152|网球东区5号场地7点|20
    赵胜|vjuid=161684;vjvd=d31b0d0fdd8b2f5e16c82c0124886080|1335|11164|网球东区6号场地6点|20
    孙章捷|vjuid=195005;vjvd=ab0ff62c44f254bba408b87ae3bec743|1336|11165|网球东区6号场地7点|20
    "狄兴|vjuid=166597;vjvd=ec67fc9bc953d12201b412a53a03b3ff|2102|13090|体育中心羽毛球6号场地下午1点|19"
    #[fa:Light_Cog]配置Cookie|setting
    """

    name=info.split("|")[0]
    vjuid=info.split("|")[1]
    vjvd=info.split("|")[2]
    resource_id=info.split("|")[-1]
    period = info.split("|")[-4]
    sub_resource_id = info.split("|")[-3]
    date = datetime.now().strftime("%Y-%m-%d")
    filepath = get_png_picture(name,vjuid,vjvd,save_path=save_path.replace(".txt",".png"))
    word = raw_input('\nplease input auth code:')
    cmd = get_booking_cmd(name,vjuid,vjvd,resource_id,period,sub_resource_id,date,word)

    with open(save_path,'w') as f:
        f.write(cmd)
    return cmd


if __name__ == "__main__":
    get_code_result("/home/zhaosheng/auto_booking_server/code_pngs/1660492726000_狄兴.png")