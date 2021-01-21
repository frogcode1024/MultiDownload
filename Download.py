#! -coding:utf8 -*-
import threading
import requests
import os
from urllib.parse import urljoin
import random

'''
下载大于1M的文件
单个文件进行分割，每个线程下载一部分
'''
class MulThreadDownloadSingle(threading.Thread):
    def __init__(self,zip_url,startpos,endpos,file_dup):
        super(MulThreadDownloadSingle,self).__init__()
        self.zip_url = zip_url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = file_dup
       
    def parse(self):
        headers = {
            "Range":"bytes=%s-%s"%(self.startpos,self.endpos) 
        }
        response = requests.get(self.zip_url,headers=headers)
        self.fd.seek(self.startpos)
        self.fd.write(response.content)

    def run(self):
        self.parse()

'''
下载小于1M的文件
一个线程下载一个文件，同时开启多个线程下载多个文件
'''
class MulThreadDownload(threading.Thread):
    def __init__(self,zip_url, zip_dir):
        super(MulThreadDownload,self).__init__()
        self.zip_url = zip_url
        self.zip_dir = zip_dir
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2995.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.0 Safari/537.36'
        ]
       
    def parse(self):
        
        headers = {
            "User-Agent": random.choice(self.ua)
        }
        #获取文件的大小
        filesize = int(requests.head(self.zip_url).headers['Content-Length'])
        if filesize > (1024*1024):
            downloadSingle(self.zip_url, self.zip_dir, filesize)
        else:
            response = requests.get(self.zip_url,headers=headers)
            f = open(self.zip_dir, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        print("finish:%s"%(self.zip_url))

    def run(self):
        self.parse()

def downloadSingle(zip_url, file_name, file_size):
    threadNum = 3
    threading.BoundedSemaphore(threadNum)
    step = file_size // threadNum
    thread_list = []
    start = 0
    end = -1
    with open(file_name,'rb+') as f:
        fileno = f.fileno()
        while end < file_size -1:
            start = end +1
            end = start + step -1
            if end > file_size:
                end = file_size
            dup = os.dup(fileno)
            file_dup = os.fdopen(dup,'rb+',-1)
            # print(fd)
            thread = MulThreadDownloadSingle(zip_url,start,end,file_dup)
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()

def download(baseUrl, zipList, threadNum):
    threading.BoundedSemaphore(threadNum)
    thread_list = []
    for each in zipList:
        # 请空并生成文件
        temp_file = open(each,'w')
        temp_file.close()
        zip_url = urljoin(baseUrl, each)
        thread = MulThreadDownload(zip_url, each)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
        threadNum = 4 #线程数
        baseUrl = "https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_104-e/Docs/"
        zipList = [ 
            "R1-2101376.zip",
            "R1-2101457.zip",
            "R1-2101609.zip",
            "R1-2100853.zip",
            "R1-2100896.zip",
            "R1-2101112.zip",
            "R1-2101198.zip",
            "R1-2100741.zip",
            "R1-2100050.zip",
            "R1-2100605.zip",
            "R1-2100261.zip"
            ]
        download(baseUrl, zipList, threadNum)

        



