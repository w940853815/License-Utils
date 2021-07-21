# 获取计算机的物理地址

import fcntl
import socket
import struct
import psutil


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])

#获取网卡名称和其ip地址，不包括回环
def get_netcard():
    info = psutil.net_if_addrs()
    for k,v in info.items():
        for item in v:
            # ubuntu20物理网卡命名以ens开头
            if k.startswith('ens') and item[0] == 2 and not item[1]=='127.0.0.1':
                return k
    return 'error'

if __name__ == '__main__':
    ifname=get_netcard()
    res=getHwAddr(ifname)
    print(res)