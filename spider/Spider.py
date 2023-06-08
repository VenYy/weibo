import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWX-G22uJocjsoTb0INHnxj5JpX5KMhUgL"
              ".FoqXSonfeozf1hB2dJLoI7Uc9g44wHvk; XSRF-TOKEN=io-W92rUoCwy9XET5ru04vBy; ALF=1688734904; "
              "SSOLoginState=1686142906; "
              "SCF=AhqtXeKjJ3bSlCXL9gem3W_9bEvXvqw6MRbaiUdWLfg1xR019BywkPVeHbzsSZMhWToJfUNDVu6e3c4U4fUb1g8.; "
              "SUB=_2A25JhA_sDeRhGeBK7VoU8izJwziIHXVq8GYkrDV8PUNbmtANLUHZkW9NR5N03GpS8Mr4NvDEFOv3z-cUbPFgCLS_; "
              "WBPSESS=U145v8ASbRNcx1JRlK7LypVEiUc5-j2"
              "-9ugePaXsbrydv4zTuNJu6PsSKYyOEDw8nn_48BNj2ZdOBX4HZHUqrq9sAj9nwHLBcSNFiplU73PQQ6lALqV29uZ"
              "-jsU0zxtldiakIA1I8QqM-9QxUDN-Iw=="
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
