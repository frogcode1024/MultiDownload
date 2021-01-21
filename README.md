# MultiDownload
python多线程下载网页上文件

## class MulThreadDownload

MulThreadDownload 类是多个线程下载多个文件（单个文件小于1M）

针对每一个url开启一个线程，4个线程轮流使用

## class MulThreadDownloadSingle

MulThreadDownloadSingle 类是多个线程下载单个文件（单个文件大于1M）

将单个文件分割，每个线程下载一部分字节

例如：

文件test.zip大小是37964字节

假如我们用3个线程去下载test.zip，那么我们会用线程1去下载1260x10=12600字节，线程2下载12601-25200字节，以此类推，还不够就用线程1再去下载。

但是get请求是直接下载test.zip文件,这里每次只获取一部分文件的数据，可以在get请求的head部分加入“Range: bytes=0-12599”

如果是多线程的而下载的话，我们用open('file','rb+')，我先用这种模式继续上面下载文件，上面下载到了25199字节，

那这次我从26000开始下载，f.seek(26000)后开始保存下载的文件，看文件是否能保存，看到的文件是否会中间出现空白：

https://www.cnblogs.com/owasp/p/6413480.html

