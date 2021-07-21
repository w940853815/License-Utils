# coding:utf-8
from distutils.core import setup
from Cython.Build import cythonize
import os
import shutil

build_dir = 'build'
currdir = os.path.abspath('.')
build_dir_tmp = os.path.join(build_dir, 'temp')

ignore_file_list = [
    'wsgi.py',
    'asgi.py',
    'manage.py',
    'setup.py',
    'scheduler.py',
    'gunicorn.conf.py'
]

# 在列表中输入需要加密的py文件
key_funs = ['get_time.py']
def getpylist(basedir, excepts, excepts_dir=[]):
    for root, _, files in os.walk(basedir):
        for file in files:
            if os.path.splitext(file)[1] == '.py' and (file not in excepts):
                yield os.path.abspath(os.path.join(root, file))


moudle_list = list(getpylist(currdir,excepts=ignore_file_list))
try:
    setup(
        name="license", 
        ext_modules = cythonize(module_list=moudle_list),
        script_args=["build_ext", "-b", build_dir, "-t", build_dir_tmp]
    )

    print('Done!')
except Exception as e:
    print("build error")
    raise e
finally:
    os.system("find ./ -name '*.c' |xargs rm")

    if os.path.exists(build_dir_tmp):
        shutil.rmtree(build_dir_tmp)
