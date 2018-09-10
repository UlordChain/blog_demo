# Get

## Abi(Get contract ABI)

#### url
- /get/abi/<string:contract_name>

#### method
- GET

#### doc
```
    Gets the ABI of the contract based on the param.

    :param
        contract name

    :return:
        { 'result': 0/1, 'msg': the contract abi file }
```


## Config(Get the configuration param address)

#### url
- /get/config

#### method
- GET

#### doc
```
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
```


## Download(Get string by udfs)

#### url
- /get/blog/download/<string:udfs>

#### method
- GET

#### doc
```
    Get the corresponding content based on the udfs hash .

    :param
        udfs
    :return:
        content
```



# Post

## Blog Claim(Blog info)

#### url
- /post/blog/info

#### method
- POST

#### doc
```
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
```


## Blog List(Get blog list)

#### url
- /post/blog/list

#### method
- POST

#### doc
```
 

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
```


## Blog Publish(Record a new blog)

#### url
- /post/blog/chain

#### method
- POST

#### doc
```
    Record information about published resources.

    :param
        address , tx_hash , token

    :return:
        { 'result': 0/1, 'msg': missing address or receipt / success }
```


## Blog Update(Record a new blog)

#### url
- /post/blog/update

#### method
- POST

#### doc
```
       Record information about update resources.
       The principle is: record the account that sends come.
           update the database according to the resource corresponding to the account after a period of time.

       :param
              address , tx_hash , token

       :return:
           { 'result': 0/1, 'msg': missing address or receipt / success }
```


## Login(login)

#### url
- /post/user/login

#### method
- POST

#### doc
```
    The login will remembers the sideChain address used by the current user . Token valid for 24 hours .

    :param
        username , password , address

    :return:
        {
            'result': 0/1,
            'msg': not register , error password or illegal address / success
        }
```


## Logout(log out)

#### url
- /post/user/logout

#### method
- POST

#### doc
```
        set user token Invalid

    :param
        token , address

    :return:
        {
            'result': 0/1,
            'msg': "Success"
        }
```


## Password(Record a new password)

#### url
- /post/user/password

#### method
- POST

#### doc
```
          Record information about update password.

          :param
               token , address , old_password , new_password

          :return:
              { 'result': 0/1, 'msg': missing password or receipt / success }
```


## Pay(Record blog payment)

#### url
- /post/blog/payment

#### method
- POST

#### doc
```
    Record the purchase action,server will query all the blog information under this address after a period of time

    :param
        tx_hash ,token , address

    :return:
    {
        "result": 1,
        "msg": "Success"
    }
```


## Register(register a user)

#### url
- /post/user/register

#### method
- POST

#### doc
```
    :param
        username : The user name is also the user's id
        password : The password will encrypt the store
        address : Address of the current account in metamask

    :return:
        0 for missing arguments , existing username or illegal address
        success register :{ 'result': 1, 'msg': token }
```


## Upload Ipfs(Publish content to udfs)

#### url
- /post/blog/content

#### method
- POST

#### doc
```
    Publish a string to UDFS

    :param
        title : Between 0 and 22 characters.
        description : description must be written.
        body

    :return:
        { 'result': 0/1, 'msg': udfs }
```


## User Info(Get a user's info)

#### url
- /post/user/info

#### method
- POST

#### doc
```
    
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
```



