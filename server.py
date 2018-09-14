# coding=utf-8
# @File  : server.py
# @Author: PuJi
# @Date  : 2018/4/10 0010
import json
import os
import socket
import sys
import time
from uuid import uuid1

from flask import request, g, jsonify

from DBhelper.manage import app, db, User, UserAddress, Claim, Order, Advertising
from config import base_config
from utils.FileHelper import udfs_utils
from utils.logUtils import logger
from utils.receipt_watcher import receipt_watcher

sys.path.append('../')


# app.config.from_object(DevConfig)

def auth_login_required():
    """check login"""
    head_token = request.form.get('token')
    logger.debug(request.form.to_dict())
    if not head_token:
        return {
            'result': 0,
            'msg': "need token"
        }
    address = request.form.get('address')
    if not address:
        return {
            'result': 0,
            'msg': "please send current address"
        }
    login_user = User.query.filter_by(token=head_token).first()
    if not login_user:
        return {
            'result': 0,
            'msg': "invalid token"
        }
    if int(login_user.timestamp) < time.time():
        return {
            'result': 0,
            'msg': "invalid token"
        }
    # save address - msg
    if UserAddress.query.filter_by(user_id=login_user.user_id, address=address).first() is None:
        user_address = UserAddress(user_id=login_user.user_id, address=address)
        db.session.add(user_address)
        db.session.commit()
    return login_user


@app.route('/', methods=['GET'])
def home():
    """Home page

    Test whether the service is started

    :param
        pass

    :return:
        pass
    """
    return 'server has running '


@app.route('/get/abi/<string:contract_name>', methods=['GET'])
def abi(contract_name):
    """Get contract ABI

    Gets the ABI of the contract based on the param.

    :param
        contract name

    :return:
        { 'result': 0/1, 'msg': the contract abi file }
    """
    try:
        abi_dir = os.path.join(base_config.CURR_DIR, "abi")
        abi_file = os.path.join(abi_dir, contract_name + ".abi")
        with open(abi_file, "r") as f:
            abi = json.load(f)
        return jsonify({
            'result': 1,
            'msg': abi
        })
    except:
        return jsonify({
            'result': 0,
            'msg': "wrong abi file name"
        })


@app.route('/get/config', methods=['GET'])
def config():
    """Get the configuration param address

    Returns the contract deployment address and the URL of the provider

    :return:
        {
            "msg": {
                "contract_addresses": {
                    "AdminModule": "0x5BfF5CE20D2fa962D1572B2538a2B0c661A51004",
                    "AuthorModule": "0x6225d3feF0fabd9FE2f687dA33fd348c5462D656",
                    "self": "0x035EB55d4260455075A8418C4B94Ba618C445537"
                    ...
                },
                "provider": "https://rinkeby.infura.io/v3/7226f0ad456a4f1189fee961011684ac"
            },
            "result": 1
        }
    """
    msg = {"provider": base_config.provider}
    with open(os.path.join(base_config.CURR_DIR, "contractAddresses.json")) as wf:
        contract_addr_list = json.load(wf)
    msg["contract_addresses"] = contract_addr_list
    return jsonify({
        'result': 1,
        'msg': msg
    })


@app.route('/post/user/register', methods=['POST'])
def register():
    """register a user

    :param
        username : The user name is also the user's id
        password : The password will encrypt the store
        address : Address of the current account in metamask

    :return:
        0 for missing arguments , existing username or illegal address
        success register :{ 'result': 1, 'msg': token }
    """
    username = request.form.get('username')
    password = request.form.get('password')
    address = request.form.get('address')
    if username is None or password is None or address is None:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': "missing arguments"
        })
    # check address
    if User.query.filter_by(username=username).first() is not None:
        # existing user
        return jsonify({
            'result': 0,
            'msg': "existing user"
        })
    # authentication address
    if receipt_watcher.valid_address(address) is None:
        return jsonify({
            'result': 0,
            'msg': "illegal address"
        })
    #
    user = User(username=username, password_hash=User.hash_password(password))
    user.timestamp = int(time.time()) + 24 * 60 * 60
    db.session.add(user)

    user = User.query.filter_by(username=username).first()

    if UserAddress.query.filter_by(address=address).first() is not None:
        user_addr = UserAddress(user_id=user.user_id, address=address)
        db.session.add(user_addr)

        # # send Token
        # if SentAddress.query.filter_by(address=address).first() is not None:
        #     receipt_watcher.send_newbie_token(address)
        #     sent_address = SentAddress(address=address)
        #     db.session.add(sent_address)

    token = str(uuid1())
    user.token = token
    db.session.commit()

    return jsonify({
        'result': 1,
        'msg': token
    })


@app.route('/post/user/login', methods=['POST'])
def login():
    """login

    The login will remembers the sideChain address used by the current user . Token valid for 24 hours .

    :param
        username , password , address

    :return:
        {
            'result': 0/1,
            'msg': not register , error password or illegal address / success
        }
    """
    username = request.form.get('username')
    password = request.form.get('password')
    address = request.form.get('address')

    if username is None or password is None or address is None:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': "missing arguments"
        })
    login_user = User.query.filter_by(username=username).first()
    if not login_user:
        # no user
        return jsonify({
            'result': 0,
            'msg': "not register"
        })
    if not login_user.verify_password(password):
        # error password
        return jsonify({
            'result': 0,
            'msg': "error password"
        })
    if receipt_watcher.valid_address(address) is None:
        return jsonify({
            'result': 0,
            'msg': "illegal address"
        })
    token = str(uuid1())
    login_user.token = token
    login_user.timestamp = int(time.time()) + 24 * 60 * 60

    if UserAddress.query.filter_by(user_id=login_user.user_id, address=address).first() is not None:
        user_address = UserAddress(user_id=login_user.user_id, address=address)
        db.session.add(user_address)
    db.session.commit()

    return jsonify({
        'result': 1,
        'msg': token
    })


@app.route('/post/user/logout', methods=['POST'])
def logout():
    """log out

        set user token Invalid

    :param
        token , address

    :return:
        {
            'result': 0/1,
            'msg': "Success"
        }
    """
    current_user = auth_login_required()
    if type(current_user) is dict:
        return jsonify(current_user)
    current_user.timestamp = int(time.time()) - 1
    db.session.commit()
    return jsonify({
        'result': 1,
        'msg': "Success"
    })


@app.route('/post/user/password', methods=['POST'])
def password():
    """Record a new password

          Record information about update password.

          :param
               token , address , old_password , new_password

          :return:
              { 'result': 0/1, 'msg': missing password or receipt / success }
    """
    address = request.form.get('address')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if address is None or old_password is None or new_password is None:
        return jsonify({
            'result': 0,
            'msg': "missing arguments"
        })
    user_address = UserAddress.query.filter_by(address=address).first()
    user = User.query.filter_by(user_id=user_address.user_id).first()
    if not user:
        # no user
        return jsonify({
            'result': 0,
            'msg': "not change password"
        })
    if not user.verify_password(old_password):
        # error password
        return jsonify({
            'result': 0,
            'msg': "error password"
        })
    if receipt_watcher.valid_address(address) is None:
        return jsonify({
            'result': 0,
            'msg': "illegal address"
        })
    pwd_hash = user.hash_password(new_password)
    user.password_hash = pwd_hash
    db.session.commit()

    return jsonify({
        'result': 1,
        'msg': "success"
    })


@app.route('/post/blog/content', methods=['POST'])
def upload_ipfs():
    """Publish content to udfs

    Publish a string to UDFS

    :param
        title : Between 0 and 22 characters.
        description : description must be written.
        body

    :return:
        { 'result': 0/1, 'msg': udfs }
    """
    auth_login_required()
    body = request.form.get('body')
    title = request.form.get('title')
    description = request.form.get('description')
    if len(title) > base_config.title_length or len(title) == 0:
        return jsonify({
            'result': 0,
            'msg': "title is between 1 and 22"
        })
    if description == 0:
        return jsonify({
            'result': 0,
            'msg': "need description"
        })
    msg = udfs_utils.add_str(json.dumps({"title": title, "description": description, "body": body}))

    return jsonify({
        'result': 1,
        'msg': msg
    })


@app.route('/post/blog/chain', methods=['POST'])
def blog_publish():
    """Record a new blog

    Record information about published resources.

    :param
        address , tx_hash , token

    :return:
        { 'result': 0/1, 'msg': missing address or receipt / success }
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    param_dict = request.form.to_dict()
    # todo title1 stuff
    if not {'address', "tx_hash"}.issubset(set(param_dict.keys())):
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': "missing address or receipt"
        })
    receipt_watcher.background_update(receipt_watcher.update_claim, param_dict['address'], None, param_dict['tx_hash'])
    return jsonify({
        'result': 1,
        'msg': "success"
    })


@app.route('/post/blog/update', methods=['POST'])
def blog_update():
    """Record a new blog

       Record information about update resources.
       The principle is: record the account that sends come.
           update the database according to the resource corresponding to the account after a period of time.

       :param
              address , tx_hash , token

       :return:
           { 'result': 0/1, 'msg': missing address or receipt / success }
       """
    return blog_publish()


@app.route('/post/blog/list', methods=['POST'])
def blog_list():
    """ Get blog list

    Query the list of items recorded in the database. One page have ten blog.
    Purchased resources will be given udfs and resource content

    :param
        address : Address of the current account in metamask
        page , token

    :return:
        {
            "msg": {
                "list": [
                    {
                        "author": "0x035EB55d4260455075A8418C4B94Ba618C445536",
                        "claim_id": "0xf716254b5ab98fa69c564676fcd0742a",
                        "deposit": 0,
                        "description": null,
                        "initDate": 1535591915,
                        "price": 1,
                        "title": null,
                        "type": 1,
                        "views": 0,
                        "waive": false
                    }
                ],
                "total": 0
            },
            "result": 1
        }
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = int(request.form.get('page'))
    except TypeError:
        page = 1
    # get data
    blogs_list_paginate = Claim.query.paginate(int(page), 10, False)
    blogs_list = blogs_list_paginate.items
    total, pages = blogs_list_paginate.total, blogs_list_paginate.pages
    msg = {
        'list': [],
        'total': total,
        'pages ': pages
    }

    address = UserAddress.query.filter_by(user_id=current_user.user_id).all()
    address = list({i.address for i in address})
    [receipt_watcher.background_update(receipt_watcher.update_claim, i) for i in address]
    # remove body
    for blog in blogs_list:
        if blog.waive:
            continue
        blog_dict = blog.to_dict()

        if str(blog_dict["author"]) not in address and blog_dict['type'] != 2:
            order = db.session.query(Order) \
                .filter(Order.address.in_(address)) \
                .filter(Order.claim_id == blog_dict['claim_id']) \
                .first()
            if order is None:
                print(order is None, blog_dict['type'] != 2)
                blog_dict.pop("body")
                blog_dict.pop("udfs")
        msg["list"].append(blog_dict)
    return jsonify({
        'result': 1,
        'msg': msg
    })


@app.route('/post/blog/info', methods=['POST'])
def blog_claim():
    """Blog info

    If the user (check the username) has already bought the item or its author, To display the content of the article .

    :param
        blog_id ,token , address

    :return:
        {
            "msg": {
                "author": "0x035EB55d4260455075A8418C4B94Ba618C445537",
                "body": null,
                "claim_id": "0x909b2af19d778cd804f3ad8bf1161397",
                "deposit": 0,
                "description": "Sphinx is a tool that makes it easy to create intelligent and beautiful documentation"
                "initDate": 1535600331,
                "price": 0,
                "title": "sphinx,
                "type": 1,
                "udfs": null or ",
                "views": 3,
                "waive": false
            },
            "result": 1
        }
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    claim_id = request.form.get("blog_id")
    address = request.form.get('address')
    if claim_id is None or address is None:
        return jsonify({
            "result": 0,
            "msg": "need claim_id and address"
        })
    receipt_watcher.background_update(receipt_watcher.update_order, claim_id)
    current_blog = Claim.query.filter_by(claim_id=claim_id).first()
    if current_blog is not None:
        # Forbidden claim
        if current_blog.waive:
            return jsonify({
                "result": 0,
                "msg": "Forbidden claim"
            })
        current_blog.views = current_blog.views + 1
        current_blog = current_blog.__dict__
        current_blog.pop("_sa_instance_state")

        if current_blog['type'] == 2:
            ad = Advertising(address=address, claim_id=claim_id, price=current_blog['price'])
            ad.initDate = int(time.time()) + 24 * 60 * 60
            db.session.merge(ad)
            db.session.commit()
            return jsonify({
                "result": 1,
                "msg": current_blog
            })
        if current_blog.get("author") == address or Order.query.filter_by(claim_id=claim_id, address=address).first() is not None:
            return jsonify({
                "result": 1,
                "msg": current_blog
            })

        else:  # not buy
            current_blog["body"] = None
            current_blog["udfs"] = None
            return jsonify({
                "result": 1,
                "msg": current_blog
            })
    return jsonify({
        "result": 0,
        "msg": "error claim_id"
    })


@app.route('/post/blog/payment', methods=['POST'])
def pay():
    """Record blog payment

    Record the purchase action,server will query all the blog information under this address after a period of time

    :param
        tx_hash ,token , address

    :return:
    {
        "result": 1,
        "msg": "Success"
    }
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    claim_id = request.form.get('claim_id')
    # address = request.form.get('address')
    # tx_hash = request.form.get('tx_hash')
    receipt_watcher.background_update(receipt_watcher.update_order, claim_id)
    return jsonify({
        "result": 1,
        "msg": "Success"
    })


@app.route('/post/user/info', methods=['POST'])
def user_info():
    """Get a user's info
    
    The data in the database is immediately returned to the caller and later synchronized with the chain. 
    Returns all the addresses under the current user, the resources purchased with those addresses, and the resources whose addresses have been published.

    :param 
        username , token , address

    :return: 
        {
            "msg": {
                "address": [
                    "0x035eb55d4260455075a8418c4b94ba618c445537"
                ],
                "order": [],
                "publish": [
                    {
                        "author": "0x035EB55d4260455075A8418C4B94Ba618C445537",
                        "claim_id": "0xf716254b5ab98fa69c564676fcd0742a",
                        "deposit": 0,
                        "description": null,
                        "initDate": 1535591915,
                        "price": 1,
                        "title": null,
                        "type": 1,
                        "views": 0,
                        "waive": false
                    }
                ]
            },
            "result": 1
        }
    """
    current_user = auth_login_required()
    if type(current_user) is dict:
        return jsonify(current_user)
    msg = {
        'publish': [],
        "order": [],
        'address': []
    }
    username = request.form.get('username')
    # search for other user
    if username and username != "undefined":
        current_user = User.query.filter_by(username=username).first()
        if current_user is None:
            return jsonify({
                'msg': "no user {}".format(username),
                "result": 0,
            })

    # address
    address = UserAddress.query.filter_by(user_id=current_user.user_id).all()
    address = [i.address for i in address]
    msg['address'] = address = list(set(address))
    # update author
    [receipt_watcher.background_update(receipt_watcher.update_claim, i) for i in msg['address']]
    # publish claim
    claims = []
    for i in msg['address']:
        c = Claim.query.filter_by(author=i).all()
        claims += c
    for claim in claims:
        c = claim.to_dict()
        if username:
            c.pop("body")
            c.pop("udfs")
        msg["publish"].append(c)
    # order
    for i in address:
        # update orders and the corresponding merchandise.
        receipt_watcher.background_update(receipt_watcher.update_all_by_address, i)
        order = Order.query.filter_by(address=i).all()
        claims = set([Claim.query.filter_by(claim_id=i.claim_id).first() for i in order])
        for claim in claims:
            if claim is None:
                continue
            c = claim.to_dict()
            c["order_from_address"] = i
            if username:
                c.pop("body")
                c.pop("udfs")
            msg['order'].append(c)
    return jsonify({
        'msg': msg,
        "result": 1,
    })


@app.route('/get/blog/download/<string:udfs>', methods=['GET'])
def download(udfs):
    """Get string by udfs
    Get the corresponding content based on the udfs hash .

    :param
        udfs
    :return:
        content
    """
    return jsonify(json.loads(udfs_utils.cat(udfs).decode()))


@app.route('/get/user/nonce/<string:address>', methods=['GET'])
def get_nonce(address):
    return jsonify(receipt_watcher._nonce(address=address))


if __name__ == '__main__':
    if os.path.isfile(r'DBhelper/sqlite.db') is False:
        db.create_all()
    host_ip = socket.gethostbyname(socket.gethostname())
    #host_ip = "172.27.0.48"
    app.run(host=host_ip, port=5000)
