#!/usr/bin/python3
# encoding: utf-8 
# @author  : zza
# @Email   : 740713651@qq.com
# @Time    : 2018/8/24 0024
"""合约信息监测，hash_tx监测"""
import socket
import threading
import time

from DBhelper.manage import Order, db, Claim, Advertising
from utils.FileHelper import udfs_utils
from utils.logUtils import logger

"""合约操作 基本工具"""
import json
import os
from web3.middleware import geth_poa_middleware
from web3 import Web3
from web3 import HTTPProvider
from web3.eth import Eth
from eth_account import Account
from functools import wraps

from config import base_config

GAS_PRICE = Web3.toWei('2', 'gwei')


def check_account(func):
    """检查在调用转账等操作前, 是否设置了account"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not hasattr(self, "account") or not self.account:
            raise ValueError(
                "No account is set, use the set_account_* to set the account, "
                "or use the create() to new an account."
            )
        return func(*args, **kwargs)

    return wrapper


class ContentContract(object):
    """Content contract"""

    def __init__(self, keystore_file=None, keystore_pwd=None,
                 private_key=None,
                 provider=base_config.provider,
                 gas_price=GAS_PRICE, ):
        """ 合约方法调用类
        参数有可能会变化, 所以调用时最好指定参数名
        :param keystore_file: user account keystore file, which include user account private key
        :param keystore_pwd: user account keystore password
        :param provider: Ulord side provider, such as http://xxxx:yyy, which is a RPC endpoint
        """
        self.web3 = Web3(HTTPProvider(provider))
        self.gas_limit = base_config.BLOCK_GAS_LIMIT
        self.gas_price = gas_price

        self.last_tx = None

        self.main_address = None
        if private_key:
            self.set_account_from_private_key(private_key)
        elif keystore_file and keystore_pwd:
            self.set_account_from_wallet(keystore_file, keystore_pwd)

        # Rinkeby 测试网络使用的是POA权威证明, 需要使用这个插件才能正常工作
        # http://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
        if provider.startswith("https://rinkeby"):
            self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.eth = Eth(self.web3)

        # 装载所有合约
        self.reloading_contract()

    @staticmethod
    def _load_wallet(wallet_file):
        if not os.path.isfile(wallet_file):
            wallet_file = os.path.join(base_config.CURR_DIR, 'resources', 'keystore', wallet_file)
            if not os.path.isfile(wallet_file):
                raise ValueError("Wallet file not a valid path.")
        with open(wallet_file) as wf:
            wallet = json.load(wf)
        return wallet

    @staticmethod
    def _save_wallet(wallet, file_name):
        wf = os.path.join(base_config.CURR_DIR, 'resources', 'keystore', "{}.json".format(file_name))
        print("Wallet file address:\n{}".format(wf))
        with open(wf, "w") as f:
            json.dump(wallet, f)

    @staticmethod
    def valid_address(address):
        """验证是否是一个以太坊地址, 用EIP55校验和返回给定的地址。"""
        if not Web3.isAddress(address):
            return None
        address = Web3.toChecksumAddress(address)
        return address

    def _load_abi(self):
        abi_path = os.path.join(base_config.CURR_DIR, 'abi')
        file_list = os.listdir(abi_path)
        self.abi_files = {}
        for i in file_list:
            if not i.endswith(".abi"):
                continue
            with open(os.path.join(abi_path, i)) as cp:
                cp_abi = cp.read()
                self.abi_files[i[:-4]] = json.loads(cp_abi)

    def _nonce(self, value=0, address=None):
        if address is None:
            address = self.account.address
        nonce = self.eth.getTransactionCount(address) + value
        return nonce

    def _build_transaction(self, func, gas_limit=None, gas_price=None, nonce=None):
        """将合约方法的调用构建为离线交易对象"""
        return func.buildTransaction({"nonce": nonce if nonce else self._nonce(),
                                      "gas": gas_limit if gas_limit else self.gas_limit,
                                      "gasPrice": gas_price if gas_price else self.gas_price, })

    def _sign_and_send_rawtransaction(self, transaction):
        signed = self.account.signTransaction(transaction)
        tx_hash = Web3.toHex(self.eth.sendRawTransaction(signed.rawTransaction))
        return tx_hash

    def create(self, wallet_password):
        """创建一个账户, 保存key file到对应目录的json文件中, 且返回私钥和地址"""
        setattr(self, "account", Account.create())
        wallet = self.account.encrypt(wallet_password)
        self._save_wallet(wallet, self.account.address)
        return dict(
            privateKey=Web3.toHex(self.account.privateKey),
            address=self.account.address,
        )

    def set_account_from_private_key(self, private_key, wallet_password=None):
        """如果有钱包密码, 则创建对应的keystore文件. 反之 ,则不新建"""
        setattr(self, "account", Account.privateKeyToAccount(private_key))
        if wallet_password:
            wallet = self.account.encrypt(wallet_password)
            self._save_wallet(wallet, self.account.address)
        self.main_address = self.web3.eth.account.privateKeyToAccount(private_key).address

        # self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        return dict(
            privateKey=Web3.toHex(self.account.privateKey),
            address=self.account.address,
        )

    def set_account_from_wallet(self, wallet_file, wallet_password):
        """从密钥文件加载 account 对象"""
        wallet = self._load_wallet(wallet_file)
        private_key = Account.decrypt(wallet, wallet_password)
        setattr(self, "account", Account.privateKeyToAccount(private_key))
        self.main_address = self.web3.eth.account.privateKeyToAccount(private_key).address
        # print(self.web3.eth.defaultAccount, self.web3.eth.accounts,self.web3.eth.account)
        self.web3.eth.defaultAccount = self.web3.eth.account
        return dict(
            privateKey=Web3.toHex(private_key), address=self.account.address
        )

    def get_for_receipt(self, tx_hash):
        """ 获取交易回执
        :param tx_hash: 获取交易回执(只有已打包的交易才有数据,否则返回None)
        :return:
        """
        return self.web3.eth.getTransactionReceipt(tx_hash)

    def get_gas_balance(self, address):
        """ 获取侧链余额
        """
        if address is None:
            address = self.main_address
        address = self.valid_address(address)
        balance = self.web3.eth.getBalance(address, 'latest')
        return self.web3.fromWei(balance, 'ether')

    @check_account
    def transfer_gas(self, to_address, value):
        """ gas就是侧链的币,

        :param to_address: 接收地址
        :param value: 转账金额(wei)
        :return: 交易hash
        """
        print("nonce:", self._nonce())
        to_address = self.valid_address(to_address)
        payload = {
            "to": to_address,
            "value": value,
            "gas": self.gas_limit,
            "gasPrice": self.gas_price,
            "nonce": self._nonce(),
        }
        res = self._sign_and_send_rawtransaction(payload)
        self.last_tx = res
        return res

    def transfer_tokens(self, addresses, qualitys):
        """ 多地址结算
        :param addresses: List, 结算的地址列表
        :param qualitys: List, 结算地址列表对应的金额
        """
        for i, address in enumerate(addresses):
            addresses[i] = self.valid_address(address)
        for i, quality in enumerate(qualitys):
            qualitys[i] = int(quality)
        publish_tx = self.contract["MulTransfer"].functions.mulPayDiff(addresses, qualitys).buildTransaction({
            "nonce": self._nonce(), "gas": self.gas_limit, "gasPrice": self.gas_price})
        res = self._sign_and_send_rawtransaction(publish_tx)
        self.last_tx = res
        return res

    # zza write

    def reloading_contract(self):
        try:
            # 所有合约的abi
            self._load_abi()
            # 所有合约
            self._load_contract()
        except FileNotFoundError:
            print("Please use the deploy_contract command to deploy the contract first, or manually prepare the "
                  "contract address。")

    def _load_contract(self):
        # 读取合约地址
        with open(os.path.join(base_config.CURR_DIR, "contractAddresses.json")) as wf:
            contract_addr_list = json.load(wf)
        self.contract = {}
        # 装载合约
        for contract, addr in contract_addr_list.items():
            try:
                self.contract[contract] = self.web3.eth.contract(address=self.valid_address(addr),
                                                                 abi=self.abi_files[contract])
            except:
                continue
            view_funcs = []
            abi = {}
            for func in self.abi_files[contract]:
                if func['type'] == 'function':
                    if func.get('constant') and func.get("stateMutability") == 'view':
                        view_funcs.append(func["name"])
                    abi[func['name']] = func
            self.contract[contract].view_funcs = view_funcs
            self.contract[contract].abi = abi

    @check_account
    def func_call(self, contract_name, function, param):
        # 找到合约中对应的函数
        contract = self.contract[contract_name]
        try:
            func = contract.functions.__getattribute__(function)
        except AttributeError:
            return "{} there is no {} function".format(contract_name, function)
        # 准备参数
        inputs = contract.abi[function]['inputs']
        param = self.format_param(param, inputs)
        # 增加参数
        func = func() if len(param) == 0 else func(*param)
        # 静态函数
        if function in self.contract[contract_name].view_funcs:
            return func.call({"from": base_config.main_address})
        # 需要上链的函数
        if self.last_tx is None or self.get_for_receipt(self.last_tx) is not None:
            tx = self._build_transaction(func)
            res = self._sign_and_send_rawtransaction(transaction=tx)
            self.last_tx = res
            print("Call successful , transaction hash:")
            return res
        else:
            print("The last transaction was not confirmed , please call get_for_receipt to view the last transaction")
            return self.last_tx

    def format_param(self, param, inputs):
        if isinstance(param, list):
            res = param
        else:
            res = list(param)
        if len(param) != len(inputs):
            return "Less parameters"
        for i in range(len(inputs)):
            _type = inputs[i].get('type')
            # if _type.endswith("[]"):
            #     return "Array arguments are not recommended for command-line input, use http://remix.ethereum.org/ " \
            #            "manually "
            if _type in ['uint256', 'uint8']:
                res[i] = int(param[i])
            elif 'bool' == _type:
                res[i] = bool(param[i])
            elif 'address' == _type:
                res[i] = self.valid_address(param[i])
            elif 'bytes16' == _type:
                # res[i] = self.web3.toHex(hexstr=param[i])
                res[i] = param[i]
            else:
                continue
        return res

    def get_last_call_info(self):
        if self.last_tx is None:
            return None
        return self.get_for_receipt(self.last_tx)


class ReceiptWatcher(ContentContract):
    query_list = set()
    query_late = set()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listen_list = []

        self.running = threading.Thread(target=self.run, args=())
        self.running.start()
        self.running2 = threading.Thread(target=self.send_pay, args=())
        self.running2.start()

    def background_update(self, method, *args):
        logger.debug(args)
        self.query_list.add((method, args))
        return True

    def run(self, *args):
        while True:
            try:
                time.sleep(base_config.receipt_watcher_sleep_time)
                listen_list = self.query_late
                self.query_late = self.query_list
                self.query_list = set()
                for i in listen_list:
                    logger.debug("start running")
                    # func(*param)
                    logger.debug(i[1])
                    i[0](*i[1])
            except Exception as e:
                logger.error(e)

    def send_pay(self, *args):
        while True:
            time.sleep(base_config.receipt_watcher_sleep_time)
            ad_count = Advertising.query.filter_by(payment=False).count()
            self.last_send_time = 5
            if time.time() - self.last_send_time > 15 or ad_count > 200:
                self.send_pay_user()
                self.last_send_time = time.time()

    def send_newbie_token(self, address):
        receipt = self.func_call("UshareToken", "transfer", [address, base_config.newbie_token])
        return receipt

    def get_order_address_list(self, claim_id):
        res = self.func_call('AuthorModule', 'consumerByClaim', [claim_id])
        return res

    def get_claim_info(self, claim_id):
        res = self.func_call("ClaimDB", "getClaimInfoByID", [claim_id])
        return res

    def check_order(self, claim_id, address):
        if self.valid_address(address) in self.get_order_address_list(claim_id):
            return True
        return False

    def update_order(self, claim_id):
        address_list = self.func_call("AuthorModule", "consumerByClaim", [claim_id])
        # Querying existing orders
        db_address = Order.query.filter_by(claim_id=claim_id).all()
        db_address = [order.address for order in db_address]
        for address in address_list:
            if address not in db_address:
                c = Order(claim_id=claim_id, address=address)
                db.session.add(c)
        db.session.commit()
        return True

    def update_claim(self, author=None, claim_id=None, receipt=None):
        logger.debug("{} {} {}".format(author, claim_id, receipt))
        if receipt:
            if not self.get_for_receipt(receipt):
                self.background_update(self.update_claim, author, claim_id, receipt)
                return
        if author:
            claim_list = self.func_call("AuthorModule", "claimsByAddress", [author])
            claim_list = ["0x" + claim.hex() for claim in claim_list]
            claim_list.reverse()
            [self.update_claim(None, i) for i in claim_list]
        if claim_id:
            claim_info = self.func_call("AuthorModule", "findClaimInfo", [claim_id])
            if claim_info[1] == "Null":
                return
            # body = json.loads(udfs_utils.get_content(claim_info[1]).decode())
            body = json.loads(udfs_utils.get_content(claim_info[1]).decode())
            title = body.get("title")
            description = body.get("description")
            body = body.get("body")
            claim_dict = {"claim_id": claim_id,
                          "author": claim_info[0],
                          "udfs": claim_info[1],
                          "initDate": claim_info[2],
                          "deposit": claim_info[3],
                          "price": claim_info[4],
                          "body": body,
                          "description": description,
                          "title": title,
                          "waive": claim_info[5],
                          "type": claim_info[6]}
            c = Claim(**claim_dict)
            db.session.merge(c)
            db.session.commit()
        return

    def update_all_by_address(self, address):
        logger.debug(address)
        claim_list = self.func_call("InfoDB", "getClaimsByUser", [address])
        claim_list = ["0x" + claim.hex() for claim in claim_list]
        claim_list.reverse()
        for claim_id in claim_list:
            self.update_order(claim_id)
            # self.update_claim(None, claim_id)
        return True

    def send_pay_user(self):

        ad = Advertising.query.filter_by(payment=False).all()
        addr_list = list(set([i.address for i in ad]))
        addrs=[]
        claimId_list = list(set([i.claim_id for i in ad]))
        if len(ad) == 0:
            return True
        for claim_id in claimId_list:
            res = self.func_call("CenterControl", "getADBalance", [claim_id])
            c = 0
            for i in ad:
                c += i.price
            if res > c:
                div = len(addr_list) // 200
                for i in range(div + 1):
                    j = i * 200
                    s = addr_list[j:j + 200]
                    for addr in s:
                        new_addr = ContentContract.valid_address(addr)
                        addrs.append(new_addr)
                    transfer = self.func_call("CenterControl", "deductAdFee", [claim_id, addrs])
                logger.info("{} send ad fee : {}".format(claim_id, s))
                Advertising.query.filter_by(claim_id=claim_id, payment=False).update({"payment": True})
                db.session.commit()
                return True
            else:
                logger.error("not sufficient funds  {}".format(res))
                return res


receipt_watcher = ReceiptWatcher(private_key=base_config.root_private_keys)
if __name__ == '__main__':
    print("over")
