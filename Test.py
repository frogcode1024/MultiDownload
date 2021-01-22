import requests
import random
import zipfile
import io
import os
from urllib.parse import urljoin

class TGPP():
    def __init__(self):
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
        ]
       
        # 获取随机的User-Agent
        self.headers = {
            "User-Agent": random.choice(self.ua)
        }

    # 请求相应URL
    def parse_url(self, zip_url, zip_dir):
        response = requests.get(zip_url, headers=self.headers, stream=True)
        
        if response.status_code != 200:
            print('parsing not success!--', zip_url)
        else:
            # 请求成功
            print('parsing success!--', zip_url)
            f = open(zip_dir, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)


if __name__ == '__main__':
    spider = TGPP()
    baseUrl = "https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_104-e/Docs/" # 下载网址
    baseDir = r"D:\threeGPP" # 下载本地目录
    zipList = ['R1-2100073.zip'] # 下载文件
    for each in zipList:
        zip_url = urljoin(baseUrl, each)
        zip_dir = os.path.join(baseDir, each) 
        spider.parse_url(zip_url, zip_dir)