// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {console} from "forge-std/console.sol";
import {stdStorage, StdStorage, Test} from "forge-std/Test.sol";

import {Utils} from "./utils/Utils.sol";
import {Stablecoin} from "../src/Stablecoin.sol";

contract BaseSetup is Stablecoin, Test {
    Utils internal _utils;
    address payable[] internal _users;

    address internal _alice;
    address internal _bob;

    constructor() Stablecoin("Test Token", "TST") {}

    function setUp() public virtual {
        _utils = new Utils();
        _users = _utils.createUsers(2);

        _alice = _users[0];
        vm.label(_alice, "_Alice");
        _bob = _users[1];
        vm.label(_bob, "_Bob");
    }
}

contract WhenTransferringTokens is BaseSetup {
    uint256 internal _maxTransferAmount = 12e18;

    function setUp() public virtual override {
        BaseSetup.setUp();
        console.log("When transferring tokens");
    }

    function transferToken(
        address from,
        address to,
        uint256 transferAmount
    ) public returns (bool) {
        vm.prank(from);
        return this.transfer(to, transferAmount);
    }
}

contract WhenAliceHasSufficientFunds is WhenTransferringTokens {
    using stdStorage for StdStorage;
    uint256 internal _mintAmount = _maxTransferAmount;

    function setUp() public override {
        WhenTransferringTokens.setUp();
        console.log("When _Alice has sufficient funds");
        _mint(_alice, _mintAmount);
    }

    function itTransfersAmountCorrectly(
        address from,
        address to,
        uint256 transferAmount
    ) public {
        uint256 fromBalanceBefore = balanceOf(from);
        bool success = transferToken(from, to, transferAmount);

        assertTrue(success);
        assertEqDecimal(
            balanceOf(from),
            fromBalanceBefore - transferAmount,
            decimals()
        );
        assertEqDecimal(balanceOf(to), transferAmount, decimals());
    }

    function testTransferAllTokens() public {
        itTransfersAmountCorrectly(_alice, _bob, _maxTransferAmount);
    }

    function testTransferHalfTokens() public {
        itTransfersAmountCorrectly(_alice, _bob, _maxTransferAmount / 2);
    }

    function testTransferOneToken() public {
        itTransfersAmountCorrectly(_alice, _bob, 1);
    }

    function testTransferWithFuzzing(uint64 transferAmount) public {
        vm.assume(transferAmount != 0);
        itTransfersAmountCorrectly(
            _alice,
            _bob,
            transferAmount % _maxTransferAmount
        );
    }

    function testTransferWithMockedCall() public {
        vm.prank(_alice);
        vm.mockCall(
            address(this),
            abi.encodeWithSelector(
                this.transfer.selector,
                _bob,
                _maxTransferAmount
            ),
            abi.encode(false)
        );
        bool success = this.transfer(_bob, _maxTransferAmount);
        assertTrue(!success);
        vm.clearMockedCalls();
    }

    // example how to use https://github.com/foundry-rs/forge-std stdStorage
    function testFindMapping() public {
        uint256 slot = stdstore
            .target(address(this))
            .sig(this.balanceOf.selector)
            .with_key(_alice)
            .find();
        bytes32 data = vm.load(address(this), bytes32(slot));
        assertEqDecimal(uint256(data), _mintAmount, decimals());
    }
}

contract WhenAliceHasInsufficientFunds is WhenTransferringTokens {
    uint256 internal _mintAmount = _maxTransferAmount - 1e18;

    function setUp() public override {
        WhenTransferringTokens.setUp();
        console.log("When _Alice has insufficient funds");
        _mint(_alice, _mintAmount);
    }

    function itRevertsTransfer(
        address from,
        address to,
        uint256 transferAmount,
        string memory expectedRevertMessage
    ) public {
        vm.expectRevert(abi.encodePacked(expectedRevertMessage));
        transferToken(from, to, transferAmount);
    }

    function testCannotTransferMoreThanAvailable() public {
        itRevertsTransfer({
            from: _alice,
            to: _bob,
            transferAmount: _maxTransferAmount,
            expectedRevertMessage: "ERC20: transfer amount exceeds balance"
        });
    }

    function testCannotTransferToZero() public {
        itRevertsTransfer({
            from: _alice,
            to: address(0),
            transferAmount: _mintAmount,
            expectedRevertMessage: "ERC20: transfer to the zero address"
        });
    }
}
