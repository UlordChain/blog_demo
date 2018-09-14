# coding=utf-8
# @File  : config.py
# @Author: PuJi
# @Date  : 2018/4/12 0012
"""常用配置"""
import os
from appdirs import AppDirs


class BaseConfig(object):

    def __init__(self):
        self.ipfs_host = '127.0.0.1'
        self.ipfs_port = 5001

        # web3
        self.BLOCK_GAS_LIMIT = 6800000
        self.GAS_LIMIT = 6800000
        # contract will sand token to new user
        self.root_private_keys = '622C5B7B7BC8B728E07F6E04A9FDC5F46EC6273574E06D86AAA66259B3ECDD95'
        self.main_address = "0x24736c9d1a4bef7483281f914206ba70be08c099"
        # self.root_private_keys = '93072BA0A53E6DA43526B5728B7D029A5ABE7F0E806A8D7A50CEB43423DF1052'
        #self.main_address = "0x035EB55d4260455075A8418C4B94Ba618C445537"
        self.newbie_token = 5000
        self.provider = "http://192.168.12.231"
        #"http://testnet.usc.ulord.one:58858"
        # self.provider = "https://rinkeby.infura.io/v3/7226f0ad456a4f1189fee961011684ac"
        self.title_length = 22
        # for solidity
        # todo
        USER_DATA_DIR = AppDirs("UlordPySdk", "").user_data_dir
        CURR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sols")
        if os.path.isdir(USER_DATA_DIR) is False:
            import shutil
            shutil.copytree(CURR_DIR, USER_DATA_DIR)
        self.CURR_DIR = CURR_DIR
        # for log
        self.curr_dir = os.getcwd()

        self.receipt_watcher_sleep_time = 1


base_config = BaseConfig()


# config for db
class DevConfig(object):
    Debug = True
    SECRET_KEY = "ulord platform is good"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@182.61.28.33:3306/blog_demo'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JSON_AS_ASCII = False  # support chinese
