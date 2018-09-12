pragma solidity ^0.4.24;

import "./ClaimDB.sol";
import "./OrderDB.sol";
import "./InfoDB.sol";


import "./CenterControl.sol";
import "./AuthorModule.sol";
import "./UserModule.sol";
import "./AdminModule.sol";

import "./MulTransfer.sol";


contract DeployDB is OwnPlus{

    address public ClaimDB_;
    address public OrderDB_;
    address public InfoDB_;

    address public OwnerAddr_;

    constructor() public{
        OwnerAddr_ = msg.sender;
        _deployDB();
    }

    function _deployDB()
         internal
    {
        ClaimDB_ = new ClaimDB(OwnerAddr_);
        OrderDB_ = new OrderDB(OwnerAddr_);
        InfoDB_  = new InfoDB(OwnerAddr_);
     }

    bool public initFlag_ = false;
    function init() public{
        require(!initFlag_);
        admin = msg.sender;
        initFlag_ = true;
    }

    function claimWhite(address _target, bool _allow) onlyAdmin public returns(bool){
        require(ClaimDB(ClaimDB_).mangeWhiteList(_target, _allow));
        return true;
    }

    function orderWhite(address _target, bool _allow) onlyAdmin public returns(bool){
        require(OrderDB(OrderDB_).mangeWhiteList(_target, _allow));
        return true;
    }

    function infoWhite(address _target, bool _allow) onlyAdmin public returns(bool){
        require(InfoDB(InfoDB_).mangeWhiteList(_target, _allow));
        return true;
    }

    function end(address _newAdmin) public onlyAdmin returns(bool){
        ClaimDB(ClaimDB_).transferAdminship(_newAdmin);
        OrderDB(OrderDB_).transferAdminship(_newAdmin);
        InfoDB(InfoDB_).transferAdminship(_newAdmin);
        return true;
    }
}

contract DeployCenter is OwnPlus{
    address public CenterControl_;
    address  _claimPool = 0x9C301D8b430952565aa4233E1B27c5ee50E890bf;
    address public OwnerAddr_;

    constructor() public{
        OwnerAddr_ = msg.sender;
        CenterControl_ = new CenterControl(_claimPool ,OwnerAddr_);
    }

    bool public initFlag_ = false;
    function init() public{
        require(!initFlag_);
        admin = msg.sender;
        initFlag_ = true;
    }

    function centerWhite(address _target, bool _allow) onlyAdmin public returns(bool){
        require(CenterControl(CenterControl_).mangeWhiteList(_target, _allow));
        return true;
    }

    function centerInit(address _claim, address _order, address _info) onlyAdmin public returns(bool){
        CenterControl(CenterControl_).initialize(_claim, _order, _info);
        return true;
    }

    function end(address _newAdmin) public onlyAdmin returns(bool){
        CenterControl(CenterControl_).transferAdminship(_newAdmin);
        return true;
    }
}

contract DeployUser is OwnPlus{
    DeployDB public DeployDB_;
    DeployCenter public DeployCenter_;

    address public claimDB_;
    address public orderDB_;
    address public infoDB_;

    address public centerControl_;

    address public AuthorModule_;
    address public AdminModule_;
    address public UserModule_;

    address public MulTransfer_;

    address public OwnerAddr_;

    constructor(address _db, address _center) public{
        OwnerAddr_ = msg.sender;

        DeployDB_ = DeployDB(_db);
        DeployCenter_ = DeployCenter(_center);

        _getContractAddress();
        _deploy();
        //_deployModule();
    }

    bool public initFlag_ = false;
    function init() public{
        require(!initFlag_);
        admin = msg.sender;
        initFlag_ = true;

        DeployDB_.init();
        DeployCenter_.init();
        _init();
    }

    function _getContractAddress() internal{
        claimDB_ = DeployDB_.ClaimDB_();
        orderDB_ = DeployDB_.OrderDB_();
        infoDB_  = DeployDB_.InfoDB_();

        centerControl_ = DeployCenter_.CenterControl_();
    }


    function _deploy()
        internal
    {
        //CenterPublish_ = new CenterControl(_claimPool, OwnerAddr_);
        AuthorModule_ = new AuthorModule(centerControl_, infoDB_);
        UserModule_ = new UserModule(centerControl_, infoDB_);
        AdminModule_ = new AdminModule(claimDB_, orderDB_, OwnerAddr_);
        MulTransfer_ = new MulTransfer(OwnerAddr_);
    }


    function _init() internal{
        DeployCenter_.centerInit(claimDB_, orderDB_, infoDB_);

        // 1. claim的白名单中添加 center
        DeployDB_.claimWhite(centerControl_, true);
        // 1. claim的白名单中添加admin
        DeployDB_.claimWhite(AdminModule_, true);
        // 1. order的白名单中添加 center
        DeployDB_.orderWhite(centerControl_, true);
        // 1. info的白名单中添加 center
        DeployDB_.infoWhite(centerControl_, true);

        // 1. center的白名单中添加 author
        DeployCenter_.centerWhite(AuthorModule_, true);
        // 1. center的白名单中添加 user
        DeployCenter_.centerWhite(UserModule_, true);

    }

    function _end(address _newAdmin) internal {
        //CenterControl(centerControl_).transferAdminship(_newAdmin);
        AdminModule(AdminModule_).transferAdminship(_newAdmin);
        MulTransfer(MulTransfer_).transferAdminship(_newAdmin);
    }

    function end(address _newAdmin) public onlyAdmin returns(bool){
        DeployDB_.end(_newAdmin);
        DeployCenter_.end(_newAdmin);
        _end(_newAdmin);
        return true;
    }

}

