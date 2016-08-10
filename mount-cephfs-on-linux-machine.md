# 在 Linux 机器挂载 Ceph Filesystem


目的：在 Linux 机器挂载 Ceph FS (Filesystem)

## 查看 Ceph FS 信息

1. Ceph cluster 信息，其中有 fsmap 信息，只有一个 MDS，启动在 hostname 为 00-25-90-c0-f7-80 的 node 上。

   ```
   $ docker exec -it ceph_mon ceph -s
    cluster c85fcc38-e6b7-464b-9968-eaa38eff3660
     health HEALTH_OK
     monmap e1: 3 mons at {00-25-90-c0-f6-d6=10.10.10.203:6789/0,00-25-90-c0-f6-ee=10.10.10.202:6789/0,00-25-90-c0-f7-80=10.10.10.201:6789/0}
            election epoch 20, quorum 0,1,2 00-25-90-c0-f7-80,00-25-90-c0-f6-ee,00-25-90-c0-f6-d6
      fsmap e5: 1/1/1 up {0=mds-00-25-90-c0-f7-80=up:active}
     osdmap e133: 11 osds: 11 up, 11 in
            flags sortbitwise
      pgmap v4710: 152 pgs, 12 pools, 156 MB data, 108 objects
            862 MB used, 10185 GB / 10186 GB avail
                 152 active+clean

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

1. 确认kernel 加载 ceph 模块

    ```
    $ lsmod | grep ceph
    ceph                  305045  1
    libceph               244999  2 rbd,ceph
    dns_resolver           13140  2 nfsv4,libceph
    libcrc32c              12644  3 xfs,libceph,dm_persistent_data
    ```

1. 创建目录，挂载，Ceph MON 的IP, 以cephx 验证的方式挂载，name 为 admin， 秘钥

   ```
   # mkdir /mnt/cephfs
   #  mount -t ceph 10.10.10.201:6789:/ /mnt/cephfs -o name=admin,secret=AQCeqZFXl96IFhAAWfONQRkve0PALi4meb5ICw==
   # df -h
   Filesystem          Size  Used Avail Use% Mounted on
   /dev/sda5           101G  9.4G   91G  10% /
   devtmpfs             24G     0   24G   0% /dev
   tmpfs                24G     0   24G   0% /dev/shm
   tmpfs                24G   18M   24G   1% /run
   tmpfs                24G     0   24G   0% /sys/fs/cgroup
   /dev/sda1           197M  103M   95M  53% /boot
   tmpfs               4.7G     0  4.7G   0% /run/user/1000
   10.10.10.201:6789:/   10T  864M   10T   1% /mnt/cephfs
   ```

1. 挂载完成，可以看到 cephfs 大小为10T的空间

## 卸载


1. umount 目录

    ```
    # umount /mnt/cephfs
    ```



## 自动挂载

## 参考

1. http://docs.ceph.com/docs/hammer/cephfs/kernel/
