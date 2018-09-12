pragma solidity ^0.4.24;

import "./SafeMath.sol";
import "./WhiteMange.sol";


contract ClaimDB is WhiteMange {
    using SafeMath for uint256;

    struct Claim {
        uint256     initDate;      // date of resource upload
        uint256     deposit;       // declare a deposit required for a resource
        uint256     pricing;       // pricing of resource
        address     author;        // owner of the resource
        uint8       types;          // type of resource
        bool        waive;         // the flag that the author gave up
        string      udfs;          // the HASH value of the resource in the UDFS
    }

    mapping (bytes16 => Claim) private store_;


    /* Successfully claimed a new resource. */
    event LogNewClaim(bytes16 _claimId, address indexed _author);

    /* Update the content of the resource. */
    event LogUpdateClaimUdfs(bytes16 _claimId, address indexed _author, uint256 _pricing);

    /* Update an attribute in a resource. */
    event LogUpdateClaimAuthor(bytes16 _claimId, address indexed _author, address indexed _newAuthor);
    event LogUpdateClaimPricing(bytes16 _claimId, address indexed _author, uint256 _newPricinge);
    event LogUpdateClaimWaive(bytes16 _claimId, address indexed _author, bool _waive);

    /* Delete a resource that has already been claimed. */
    event LogDeleteClaim(bytes16 _claimId);


    /**
     * @dev Constructor.
     * @param _owner address : The address of the contract owner.
     */
    constructor(address _owner) public {
        owner = _owner;
        whitelist_[msg.sender] = true;
    }

    /**
     * @dev Insert a new resource.
     * @param _cid     bytes16  : Resource index(ClaimID).
     * @param _udfs    string   : The UDFS Hash value of the resource.
     * @param _author  address  : Declare the address of the resource.
     * @param _pricing uint256  : Pricing of resources.
     * @param _deposit uint256  : Declare a deposit required for a resource.
     * @param _type    uint8    : Type of resource.
     * @return         bool     : The successful call returns true.
     */
    function insertClaim(bytes16 _cid, string _udfs, address _author, uint256 _pricing, uint256 _deposit, uint8 _type)
        public
        returns(bool)
    {
        if (whitelist_[msg.sender] != true){
            emit LogError(RScorr.Insufficient);
            return false;
        } // Check the caller's whitelist permission.

        if (isExist(_cid)){
            emit LogError(RScorr.ObjExist);
            return false;
        } // Check if the resource exists.

        store_[_cid].author    = _author;
        store_[_cid].udfs      = _udfs;
        store_[_cid].initDate  = now;
        store_[_cid].deposit   = _deposit;
        store_[_cid].pricing   = _pricing;
        store_[_cid].waive     = false;
        store_[_cid].types      = _type;

        emit LogNewClaim(_cid, _author);

        return true;
    }

    /**
     * @dev Update the content of the resource (UDFS hash) and the pricing.
     * @param _cid       bytes16  : Resource index(ClaimID).
     * @param _author    address  : Declare the address of the resource.
     * @param _udfs      string   : The UDFS Hash value of the resource.
     * @param _pricing   uint256  : New pricing of resources.
     * @return           bool     : The successful call returns true.
     */
    function updateClaim(bytes16 _cid, address _author, string _udfs, uint256 _pricing)
        public
        returns(bool)
    {
        if (whitelist_[msg.sender] != true){
            emit LogError(RScorr.Insufficient);
            return false;
        } // Check the caller's whitelist permission.

        if(store_[_cid].author != _author) {
            emit LogError(RScorr.IdCertifyFailed);
            return false;
        } // Verify that the resource is the caller's.


        store_[_cid].udfs    = _udfs;
        store_[_cid].pricing = _pricing;

        emit LogUpdateClaimUdfs(_cid, _author, _pricing);

        return true;
    }


    /**
     * @dev Update the author address of the resource.
     * @param _cid       bytes16  : Resource index(ClaimID).
     * @param _author    address  : Claim the address of the resource.
     * @param _newAuthor address  : New owners of resources.
     * @return           bool     : The successful call returns true.
     */
    function updateClaimAuthor(bytes16 _cid, address _author, address _newAuthor)
        public
        returns(bool)
    {
        if (whitelist_[msg.sender] != true){
            emit LogError(RScorr.Insufficient);
            return false;
        } // Check the caller's whitelist permission.

        if(store_[_cid].author != _author) {
            emit LogError(RScorr.IdCertifyFailed);
            return false;
        } // Verify that the resource is the caller's.

        if(_newAuthor == address(0)) {
            emit LogError(RScorr.InvalidAddr);
            return false;
        } // The owner of the resource cannot be empty.

        if(store_[_cid].author == _newAuthor){
            emit LogError(RScorr.Insignificance);
            return false;
        } // The updated content should not be the same.

        emit LogUpdateClaimAuthor(_cid, _author, _newAuthor);

        store_[_cid].author = _newAuthor;
        return true;
    }


    /**
     * @dev Update the pricing of the resource.
     * @param _cid        bytes16  : Resource index(ClaimID).
     * @param _author     address  : Claim the address of the resource.
     * @param _newPricing address  : New pricing of resources.
     * @return            bool     : The successful call returns true.
     */
    function updateClaimPricing(bytes16 _cid, address _author, uint256 _newPricing)
        public
        returns(bool)
    {
        if (whitelist_[msg.sender] != true){
            emit LogError(RScorr.Insufficient);
            return false;
        } // Check the caller's whitelist permission.

        if(store_[_cid].author != _author){
            emit LogError(RScorr.IdCertifyFailed);
            return false;
        } // Verify that the resource is the caller's.

        if(store_[_cid].pricing == _newPricing){
            emit LogError(RScorr.Insignificance);
            return false;
        } // The updated content should not be the same.

        emit LogUpdateClaimPricing(_cid, _author, _newPricing);

        store_[_cid].pricing = _newPricing;
        return true;
    }

    /**
     * @dev The author abandons a resource.
     * @notice Canceling resource abandonment cannot be invoked by the author.
     * @param _cid     bytes16  : Resource index(ClaimID).
     * @param _author  address  : Claim the address of the resource.
     * @param _waive    bool    : True means give up, false means cancel.
     * @return          bool    : The successful call returns true.
     */
    function updateClaimWaive(bytes16 _cid, address _author, bool _waive)
        public
        returns(bool)
    {
        if (whitelist_[msg.sender] != true){
            emit LogError(RScorr.Insufficient);
            return false;
        } // Check the caller's whitelist permission.

        if(store_[_cid].author != _author) {
            emit LogError(RScorr.IdCertifyFailed);
            return false;
        } // Verify that the resource is the caller's.

        if(store_[_cid].waive == _waive) {
            emit LogError(RScorr.Insignificance);
            return false;
        } // The updated content should not be the same.

        emit LogUpdateClaimWaive(_cid, _author, _waive);
        store_[_cid].waive = _waive;
        store_[_cid].deposit = 0;

        return true;
    }

    /**
     * @dev Admin delete resources.
     * @notice This function is limited to calls only by the admin or owner.
     * @param _cid      bytes16  : Resource index(ClaimID).
     * @return          bool     : The successful call returns true.
     */
    function deleteClaim(bytes16 _cid)
        public
        returns(bool)
    {
        if(msg.sender != owner && msg.sender != admin){
            emit LogError(RScorr.PermissionDenied);
            return false;
        } // Check if the caller is an administrator.

        if(store_[_cid].author == address(0)) {
            emit LogError(RScorr.ObjNotExist);
            return false;
        } // Check if the resource exists.

        delete store_[_cid];

        emit LogDeleteClaim(_cid);

        return true;
    }

    /////////////////////////
    /// View
    /////////////////////////

    /**
     * @dev Find details of a specified resource
     * @notice Only allowed to be called by the address in the whitelist.
     * @param _claimId   bytes16 : Resource index(ClaimID).
     * @return                   : Specify the resource details.
     *                    author : owner of the resource
     *                      udfs : the HASH value of the resource in the UDFS
     *                  initDate : release time
     *                   deposit : declare a deposit required for a resource
     *                   pricing : pricing
     *                     waive : the flag that the author gave up
     *                     types : type of resource
     */
    function getClaimInfoByID(bytes16 _claimId) public view returns(
        address author,   string udfs, uint256 initDate, uint256 deposit,
        uint256 pricing,  bool  waive, uint8   types)
    {
//        if(store_[_claimId].author == address(0) || whitelist_[msg.sender] == false) {
//            return (0,"Null",0,0,0,true,0);
//        }

        return (store_[_claimId].author,
        store_[_claimId].udfs,
        store_[_claimId].initDate,
        store_[_claimId].deposit,
        store_[_claimId].pricing,
        store_[_claimId].waive,
        store_[_claimId].types);
    }


    /**
     * @dev Check if the resource exists
     * @param _claimId bytes16  : Resource index(ClaimID).
     * @return            bool  : True means resources exist
     */
    function isExist(bytes16 _claimId)
        view
        public
        returns(bool)
    {
        if (store_[_claimId].author != address(0)){
            return true;
        }
        return false;
    }


    /**
     * @dev Check if resources can be purchased
     *  1. Resources do not exist.
     *  2. When the pricing is zero, it means free
     *  3. When the waive is true ，the author has removed this resource.
     * @param _claimId bytes16  : Resource index(ClaimID).
     * @return         bool     : True is purchasable.
     */
    function isSaleable(bytes16 _claimId)
        view
        public
        returns(bool)
    {
        if (store_[_claimId].author == address(0) ||
        store_[_claimId].pricing == 0             ||
        store_[_claimId].waive   == true )
        {
            return false;
        }
        return true;
    }


    /**
     * @dev Get purchase information for the resource.
     * @notice It is recommended to judge with `isSaleable` first.
     * @param _claimId bytes16  : Resource index(ClaimID).
     * @return                  : Purchasing resources is required information.
     *          author address  : Owner of the resource.
     *         pricing uint256  : Pricing of resource.
     */
    function getGoodsInfo(bytes16 _claimId)
        view
        public
        returns(address author, uint256 pricing)
    {
        return (store_[_claimId].author, store_[_claimId].pricing);
    }

    /**
     * @dev Get purchase information for the resource.
     * @param _claimId bytes16  : Resource index(ClaimID).
     * @return                  : Purchasing resources is required information.
     *          author address  : Owner of the resource.
     */
    function getDeposit(bytes16 _claimId)
        view
        public
        returns(uint256 deposit)
    {
        return store_[_claimId].deposit;
    }

    /**
     * @dev Get types of resource.
     * @param _claimId bytes16  : Resource index(ClaimID).
     * @return types uint8      :
     */
    function getClaimType(bytes16 _claimId)
        view
        public
        returns(uint8 types)
    {
        return store_[_claimId].types;
    }

    /**
     * @dev Get pricing for resources
     * @param _claimId bytes16 : Resource index(ClaimID)
     * @return Pricing of resources
     */
    function getClaimPricing(bytes16 _claimId)
        view
        public
        returns(uint256 pricing)
    {
        return store_[_claimId].pricing;
    }

}