pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract AutoFax is ERC721Full {
    constructor() public ERC721Full("AutoFaxToken", "AFT") {}

    struct Autos {
        string vin;
        string make;
        string status;
        uint256 initialPurchasePrice;
    }

    mapping(uint256 => Autos) public autoCollection;

    event AutoRegistration(uint256 tokenId, string status, string reportURI);

    function registerPurchase(
        address owner,
        string memory vin,
        string memory make,
        string memory status,
        uint256 initialPurchasePrice,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        autoCollection[tokenId] = Autos(vin, make, status, initialPurchasePrice);

        return tokenId;
    }

    function renewRegistration(
        uint256 tokenId,
        string memory renewalStatus,
        string memory reportURI
    ) public returns (string memory) {
        
       // if renewalStatus == "YES":
       //     autoCollection[tokenId].status = "CURRENT"
       // else autoCollection[tokenId].status = "INVALID"
        
        autoCollection[tokenId].status = renewalStatus;

        emit AutoRegistration(tokenId, renewalStatus, reportURI);

        return autoCollection[tokenId].status;
    }
}
