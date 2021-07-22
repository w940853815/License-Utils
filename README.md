# python代码的License控制

## Overview
- License控制：只有获得你授权的计算机才能运行写的python代码


## Requirement
系统要求:ubtuntu20

需安装：
- python3-dev
- gcc

  ```bash
  sudo apt-get install python3-dev gcc
  ```
  
python3需安装的第三方库：
  ```bash
  pip3 install -r requirements.txt
  ```
  
## GetHostInfo打包为二进制可执行文件（获取mac地址）
```bash
pyinstaller -F GetHostInfo.py
```
## 生成license
```bash
python3 CreateLicense.py mac地址
```
## 验证license
python3 GetLicense.py
