// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract SportEducation is ERC1155{
    address public owner;
    // average score per address per quiz (we have 3 quizzes for now)
    mapping(address => mapping(uint16=> uint16)) public averageScores;
    address[] public addresses;
    uint16[] public quizIds;

    constructor() ERC1155("ipfs://QmPoRZnBUradn6gyzgDzeuAwsaBBi9sqMU4gA7DhM9NuDt/{id}.json") {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner!");
        _;
    }

    function uploadScoreOfQuiz(uint16 _quizId, uint16 _score) public {
        // add address if it doesnt exist already
        bool isAddressInArray = false;
        for (uint256 i = 0; i < addresses.length; i++) {
            if (addresses[i] == msg.sender) {
                isAddressInArray = true;
            }
        }
        if (isAddressInArray == false) {
            addresses.push(msg.sender);
        }

        // add quizId if it doesnt exist already
        bool isQuizIdInArray = false;
        for (uint256 i = 0; i < quizIds.length; i++) {
            if (quizIds[i] == _quizId) {
                isQuizIdInArray = true;
            }
        }
        if (isQuizIdInArray == false) {
            quizIds.push(_quizId);
        }

        // add average score
        averageScores[msg.sender][_quizId] = _score;
    }
    function getAverageScoreOfAddressOfQuiz(address _address, uint16 _quizId) public view returns (uint16) {
        return averageScores[_address][_quizId];
    }
    function getAddresses() public view returns (address[] memory) {
        return addresses;
    }
    function getQuizIds() public view returns (uint16[] memory) {
        return quizIds;
    }
    function mintCertificate() public {
        uint256 _averageScore = 0;
        for (uint256 i = 0; i < quizIds.length; ++i) {
            _averageScore += averageScores[msg.sender][quizIds[i]];
        }
        require(balanceOf(msg.sender, 1) == 0, "You already minted your certificate!");
        require(quizIds.length >= 3, "You didn't do every quiz!");
        _averageScore = _averageScore / quizIds.length;
        require(_averageScore >= 75, "Not high enough score on all quizzes!");
        _mint(msg.sender, 1, 1, "");
    }
}