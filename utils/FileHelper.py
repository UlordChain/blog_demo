# coding=utf-8
# @File  : util.py
# @Author: PuJi
# @Date  : 2018/4/3 0003
import _thread
import os
import codecs
import threading
import time

import ipfsapi

from config import base_config
from utils.logUtils import logger
import threading
import time
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    try:
        _async_raise(thread.ident, SystemExit)
    except:
        pass


udfs_utils = ipfsapi.connect(host=base_config.ipfs_host, port=base_config.ipfs_port)
print(base_config.ipfs_host,base_config.ipfs_port)
udfs_utils.res = {}


def cat_part(_str):
    udfs_utils.res[_str] = udfs_utils.cat(_str)
    logger.debug("get info {} {}".format(_str, udfs_utils.res[_str]))
    return


def get_content(_str):
    udfs_utils.res[_str] = None
    c = threading.Thread(target=cat_part, args=(_str,))
    c.start()
    for i in range(5):
        time.sleep(1)
        if udfs_utils.res[_str] is not None:
            return udfs_utils.res.pop(_str)
    logger.error("can not find {}".format(_str))
    stop_thread(c)
    return b"{}"


udfs_utils.get_content = get_content


def get_size(filename):
    # get file size
    file_size = os.path.getsize(filename)
    return file_size


def get_type(filename):
    # get file type
    if '.' in filename:
        return filename.split('.')[-1]
    else:
        return 'NoType'


def get_pure_name(filename):
    # get file name
    if '.' in filename:
        filename = filename.split('.')[0]
    if '/' in filename:
        return filename.split('/')[-1]
    elif '\\' in filename:
        return filename.split('\\')[-1]
    else:
        return filename


def get_name(filename):
    # get file name
    # if '/' in filename:
    #     return filename.split('/')[-1]
    # elif '\\' in filename:
    #     return filename.split('\\')[-1]
    # else:
    #     return filename
    return os.path.split(filename)[-1]


def change_name(original_name, new_name):
    # change file name from a hash to filename
    if os.path.isfile(new_name):
        print("Error: File {} has exited!".format(new_name))
        return False
    if os.path.isfile(original_name):
        file_path, original_short_name = os.path.split(original_name)
        new_name = os.path.join(file_path, new_name)
        if os.path.isfile(new_name):
            print("Error: File {} has exited!".format(new_name))
            return False
        os.rename(original_name, new_name)
        return True
    else:
        print("Error: File {} doesn't exist!".format(original_name))
        return False


def save_file(filepath, source):
    # save source into a filepath
    dirpath = os.path.split(filepath)[0]
    if os.path.isdir(dirpath):
        pass
    else:
        os.makedirs(dirpath)
    try:
        with codecs.open(filepath, 'wb', encoding='utf-8') as target_file:
            for line in source:
                target_file.write(line)
            return True
    except Exception as e:
        print("saveFile error:{}".format(e))
        return False


def merge_file(file_path, chunks):
    # merge chunks into a file
    try:
        with open(file_path, 'wb') as target_file:
            for chunk in chunks:
                with open(chunk, 'rb') as source_file:
                    for line in source_file:
                        target_file.write(line)
                try:
                    os.remove(chunk)  # 删除该分片，节约空间
                except Exception as e:
                    print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
        return True
    except Exception as e:
        print("Error mergeFile:{}".format(e))
        return False


def read_file(file_path):
    # read file comment
    result = None
    try:
        with open(file_path, 'rb') as target_file:
            result = target_file
    except Exception as  e:
        print("Error: read file{0}:{1}".format(file_path, e))
    return result


def get_root_path():
    # get project root path
    return os.path.split(os.getcwd())[0]


if __name__ == '__main__':
    # print (get_pure_name('E:\ipfs\go-ipfs\ipfs.exe'))
    # print(get_size('E:\ipfs\go-ipfs\ipfs.exe'))
    # change_name(r'E:\ulord\app_server\aaa', 'test_change')
    print(get_root_path())
