#利用librados库连接Ceph集群读写数据
根据[Ceph架构](http://docs.ceph.com/docs/master/architecture/)，客户端应用程序可以通过调用librados库与Ceph集群建立连接，从而读写数据。librados库支持C/C++/Python/Java等编程语言，本文档以Python为例。
## 获取并安装librados
连接Ceph存储集群前，Client首先要安装librados库。
python的librados包安装如下
 - Ubuntu: sudo apt-get install python-rados
 - Centos: sudo yum install python-rados

## 配置一个集群句柄
为了连接集群，客户端应用程序需要知道在哪里找到monitor机器，这由集群句柄来配置，创建集群句柄后，应用程序通过句柄连接到集群。
RADOS提供了很多方式来设置，一个简单的方法是在ceph.conf中包含keyring和至少一个monitor地址，如下
```
[global]
mon host = 10.10.10.201
keyring = /etc/ceph/ceph.client.admin.keyring
```
创建句柄后，应用程序读取ceph.conf来配置句柄，然后通过connect()连接集群。
下面以python为例，默认用户名是client.admin，集群名为ceph。
如果rados.Rados中conffile参数为空字符串，rados.Rados会读取标准的ceph.conf文件。
```
import rados

try:
        cluster = rados.Rados(conffile='')
except TypeError as e:
        print 'Argument validation error: ', e
        raise e

print "Created cluster handle."

try:
        cluster.connect()
except Exception as e:
        print "connection error: ", e
        raise e
finally:
        print "Connected to the cluster."
```
连接到集群后，我们利用RADOS API来管理pools来存储数据，包括list,create,delete等操作。
```
cluster.create_pool('data') //Create 'data' pool
cluster.list_pool('data') //Verify 'data' pool
cluster.delete_pool('data') //Delete 'data' pool
```
## 创建I/O读写数据
Ceph存储集群将数据作为对象存储，我们可以同步或异步读写对象，每个对象都有名称（或称为键）和数据。
创建pool，写入数据对象
```
ioctx = cluster.open_ioctx('data')
print "\nWriting object 'hw' with contents 'Hello World!' to pool 'data'."
ioctx.write("hw", "Hello World!")

print "\nContents of object 'hw'\n------------------------"
print ioctx.read("hw")
```

## 关闭读写操作
```
print "\nClosing the connection."
ioctx.close()
print "Shutting down the handle."
cluster.shutdown()
```
## 问题
如果写入文件到集群中，上述方法中函数ioctx.write()好像不能够读入文件路径，一个很方便的方法是用[rados](http://docs.ceph.com/docs/firefly/man/8/rados/)命令，
```
rados mkpool pool_name //创建名为pool_name的pool
rados -p pool_name put object ceph.txt //把对象名为object的ceph.txt文件存入pool。
```
Client与集群建立连接后，就可以直接用rados进行读写操作，和hdfs一样方便。

##参考
 - [http://docs.ceph.com/docs/master/architecture/]()
 - [http://docs.ceph.com/docs/master/rados/api/librados-intro/]()
 - [http://docs.ceph.com/docs/firefly/man/8/rados/]()
