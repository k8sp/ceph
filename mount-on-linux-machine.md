# 在 Linux 机器挂载 Ceph RBD


目的：在 Linux 机器挂载 Ceph RBD (RADOS block device)

## 创建 RBD

1. 只保留 layering feature, 默认的 pool 是 rbd

    ```
    $ docker exec ceph_mon rbd create liuqsrbd0 --size 1024 --image-feature layering
    ```

1. RBD 信息

   ```
   $ docker exec ceph_mon rbd --image liuqsrbd0 info
     rbd image 'liuqsrbd0':
        size 1024 MB in 256 objects
        order 22 (4096 kB objects)
        block_name_prefix: rbd_data.12d16b8b4567
        format: 2
        features: layering
        flags:
   ```

1. 查看 Ceph admin 秘钥信息，供挂载使用

     ```
     $ cat /etc/ceph/ceph.client.admin.keyring
   [client.admin]
          key = AQCeqZFXl96IFhAAWfONQRkve0PALi4meb5ICw==
          auid = 0
          caps mds = "allow"
          caps mon = "allow *"
          caps osd = "allow *"
     ```

## 挂载

1. 确认kernel 加载 rbd 模块

    ```
    $ modprobe rbd
    ```

1. Ceph MON 的IP, admin 秘钥，默认的 pool 是 rbd，RBD 是 liuqsrbd0

   ```
   #  echo "10.10.10.201,10.10.10.202,10.10.10.203  name=admin,secret=AQCeqZFXl96IFhAAWfONQRkve0PALi4meb5ICw== rbd liuqsrbd0" > /sys/bus/rbd/add
   ```    

1. 查看 RBD， 首个编号 rbd0

    ```
    # ll /dev/rbd*
    brw-rw---- 1 root disk 252, 0 Jul 31 17:53 /dev/rbd0
    ```  

1. xfs 格式化，-L 是添加label

   ```
   # mkfs.xfs -L liuqsrbd0 /dev/rbd0
   meta-data=/dev/rbd0              isize=256    agcount=9, agsize=31744 blks
          =                       sectsz=512   attr=2, projid32bit=1
          =                       crc=0        finobt=0
   data     =                       bsize=4096   blocks=262144, imaxpct=25
          =                       sunit=1024   swidth=1024 blks
   naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
   log      =internal log           bsize=4096   blocks=2560, version=2
          =                       sectsz=512   sunit=8 blks, lazy-count=1
   realtime =none                   extsz=4096   blocks=0, rtextents=0
   ```

1. 创建目录，挂载

   ```
   # mkdir /mnt/rbd0
   # mount /dev/rbd0 /mnt/rbd0
   # df -h
   Filesystem          Size  Used Avail Use% Mounted on
   /dev/sda5           101G  9.4G   91G  10% /
   devtmpfs             24G     0   24G   0% /dev
   tmpfs                24G     0   24G   0% /dev/shm
   tmpfs                24G   18M   24G   1% /run
   tmpfs                24G     0   24G   0% /sys/fs/cgroup
   /dev/sda1           197M  103M   95M  53% /boot
   tmpfs               4.7G     0  4.7G   0% /run/user/1000
   /dev/rbd0          1014M   33M  982M   4% /mnt/rbd0
   ```

## 卸载


1. umount 目录，并 remove RBD， “0” 代表 RBD 的序号

    ```
    # umount /mnt/rbd0
    # echo "0" >/sys/bus/rbd/remove
    ```



## 自动挂载

## 参考

1. http://www.virtualtothecore.com/en/adventures-with-ceph-storage-part-6-mount-ceph-as-a-block-device-on-linux-machines/
