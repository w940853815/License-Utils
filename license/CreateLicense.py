# -*- coding: UTF-8 -*-
import os
import sys
import base64

from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex

'''
TODO: 
    使用密钥将MAC加密

USAGE:
    python CreateLicense.py <MAC地址>
'''

seperateKey = "d#~0^38J:" 
aesKey = "rlbINxpoedvMPhZX" 
aesIv = "EI9z8Ayf4ubQlADq"      
aesMode = AES.MODE_CBC          # 使用CBC模式

def encrypt(text):
    #参考：https://www.cnblogs.com/loleina/p/8418108.html
    cryptor = AES.new(aesKey.encode("utf8"), aesMode, aesIv.encode("utf8")) 
    
    # padding
    add, length = 0, 16
    count = len(text)
    if count % length != 0:
        add = length - (count % length)
    text = text + ('\0' * add)      # '\0'*add 表示add个空格,即填充add个直至符合16的倍数

    ciphertext = cryptor.encrypt(text.encode("utf8"))
    #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题  
    #所以这里统一把加密后的字符串转化为16进制字符串 ,当然也可以转换为base64加密的内容，可以使用b2a_base64(self.ciphertext)
    resr = b2a_hex(ciphertext).upper()
    resr = resr.decode('utf8')
    return resr



if __name__ == "__main__":
    argLen = len(sys.argv)
    # 无参数输入则退出
    if argLen != 2: 
        print("usage: python {} hostInfo".format(sys.argv[0]))
        sys.exit(0)
    
    hostInfo = sys.argv[1]              # hostInfo是运行此脚本时传入的mac地址
    
    encryptText = encrypt(hostInfo)     # 将mac地址第一次加密
    encryptText = encryptText + seperateKey + "valid" 
    encryptText = encrypt(encryptText)  # 将加密之后的密文再次加密
    print(encryptText)
    with open("./license.lic", "w+") as licFile:
        licFile.write(encryptText)
        licFile.close()
    
    print("生成license成功!")
