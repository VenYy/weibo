import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWX-G22uJocjsoTb0INHnxj5JpX5KMhUgL"
              ".FoqXSonfeozf1hB2dJLoI7Uc9g44wHvk; SINAGLOBAL=837450737521.9586.1686205626484; "
              "ULV=1686205626503:1:1:1:837450737521.9586.1686205626484:; UOR=login.sina.com.cn,s.weibo.com,"
              "127.0.0.1:5000; XSRF-TOKEN=GQDpOJPUcJ0bCUQX9nzqADbG; ALF=1689168117; SSOLoginState=1686576120; "
              "SCF=AhqtXeKjJ3bSlCXL9gem3W_9bEvXvqw6MRbaiUdWLfg1jxWhOGbXQrUiiZTDzdZZd5fUDy58-vvcs8QiLp8YLrY.; "
              "SUB=_2A25Jg2upDeRhGeBK7VoU8izJwziIHXVq-dphrDV8PUNbmtAGLXnSkW9NR5N03CUSO2nrXZ21n62HEzflELrqyklx; "
              "WBPSESS=U145v8ASbRNcx1JRlK7LypVEiUc5-j2"
              "-9ugePaXsbrydv4zTuNJu6PsSKYyOEDw8nn_48BNj2ZdOBX4HZHUqrrnGZabLtpM53Sh2pcPrpUm5H3xEHPesumVGAJkOtT_YGXdjAS1YwBNCsbCdGAP8fA=="
}


class Spider:
    def __init__(self):
        self.url = None
        self.headers = headers

    def parse(self):
        resp = requests.get(self.url, headers=self.headers)

        resp.encoding = "utf-8"
        html = etree.HTML(resp.text)
        return html

    def parse_json(self):
        resp = requests.get(self.url, headers=self.headers)
        resp.encoding = "utf-8"
        if resp.status_code == 200:
            return resp.json()
        else:
            print("Response error when parse json: ", resp.status_code)

    @staticmethod
    def saveAsCSV(path, item_list, data):

        with open(path, "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=item_list)
            writer.writeheader()
            writer.writerows(data)  # 按行写入数据
            print("Writing CSV--------")

    @staticmethod
    def saveAsJson(path, jData):
        try:
            with open(path, "w", encoding="utf-8") as f:
                jData = {"data": jData}
                json.dump(jData, f, ensure_ascii=False)
                print("Writing JSON-----")
        except Exception as e:
            print("Error On JSON：", e)
