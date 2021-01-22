# MultiDownload
python多线程下载网页上文件

下载网址：https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_104-e/Docs/

![1611293445158](\img\readme1.png)



Download.py 是多线程下载文件的工程，包含MulThreadDownload类（多线程下载多个url）和MulThreadDownloadSingle类（多线程下载一个大文件），直接运行即可。

## class MulThreadDownload

MulThreadDownload 类是多个线程下载多个文件（单个文件小于1M）

针对每一个url开启一个线程，4个线程轮流使用

1、将列表中所有url分成4份，每个线程下载一份

2、每个线程用wb模式写入文件

例如：

将下载任务加入线程列表

```python
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
```

requests请求文件，write写入保存

```python
response = requests.get(self.zip_url,headers=headers)
f = open(self.zip_dir, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        f.write(chunk)
```



## class MulThreadDownloadSingle

MulThreadDownloadSingle 类是多个线程下载单个文件（单个文件大于1M）

1、将单个文件分割，每个线程下载一部分字节

2、每个线程用rb+模式打开文件

3、每个线程下载数据后，用f.seek()到相应的位置，然后再写数据。



例如：

文件test.zip大小是37964字节

假如我们用3个线程去下载test.zip，那么我们会用线程1去下载1260x10=12600字节，线程2下载12601-25200字节，以此类推，还不够就用线程1再去下载。

但是get请求是直接下载test.zip文件,这里每次只获取一部分文件的数据，可以在get请求的head部分加入“Range: bytes=0-12599”

```python
headers = {"Range":"bytes=0-12599"}
response = requests.get(self.url,headers=headers)
# response.text 是将get获取的byte类型数据自动编码成str类型， response.content是原始的byte类型数据
# 所以下面是直接write(response.content)
with open(self.filename,'wb') as f:
	f.write(res.content)
```

多线程下载时，用open('file','rb+')保存文件，前面已经下载了0-12599字节的数据，继续上面下载文件， 那这次从第26000字节处开始下载26000-37694，f.seek(26000)定位后开始保存下载的文件

```python
headers = {"Range":"bytes=26000-37694"}
response = requests.get(self.url,headers=headers)
with open(self.filename,'rb+') as f:
    f.seek(26000) #定位开始保存位置
    f.write(response.content)
```