# -*- coding: UTF-8 -*-
####################################
# TODO：从license.lic中解密出MAC地址
####################################
import os
import sys
import base64
import socket
import struct
import fcntl
import psutil
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex,Error as BinasciiError

seperateKey = "d#~0^38J:" 
aesKey = "rlbINxpoedvMPhZX" 
aesIv = "EI9z8Ayf4ubQlADq" 
aesMode = AES.MODE_CBC  # 使用CBC模式

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24]) 
   

def decrypt(text):
    try:
        cryptor = AES.new(aesKey.encode("utf8"), aesMode, aesIv.encode("utf8"))
        plain_text = cryptor.decrypt(a2b_hex(text)).decode('utf8')
        return plain_text.rstrip('\0')
    except UnicodeDecodeError as e:
        print(e)
        return ""
    except BinasciiError as e:
        print(e)
        return ""


#获取网卡名称和其ip地址，不包括回环
def get_netcard():
    info = psutil.net_if_addrs()
    for k,v in info.items():
        for item in v:
            # ubuntu20物理网卡命名以ens开头
            if k.startswith('ens') and item[0] == 2 and not item[1]=='127.0.0.1':
                return k
    return 'error'
    

def getLicenseInfo(filePath = None):
    if filePath == None:
        filePath = "./license.lic"
    
    if not os.path.isfile(filePath):
        return False, "license file not existed"
    
    encryptText = ""
    with open(filePath, "rb") as licFile:
        encryptText = licFile.read()
        licFile.close()
    ifname=get_netcard()

    hostInfo = "38:f9:d3:2e:9a:14"
    
    decryptText = decrypt(encryptText.decode("utf8"))
    pos = decryptText.find(seperateKey)
    if -1 == pos:
        return False, "invalid"
    licHostInfo = decrypt(decryptText[0:pos])
    licenseStr = decryptText[pos + len(seperateKey):]
    # print licHostInfo, licenseStr
    
    if licHostInfo == hostInfo:
        return True, licenseStr
    else:
        return False, "invalid"

if __name__ == "__main__":
    status, licInfo = getLicenseInfo()
    print(status,licInfo)
