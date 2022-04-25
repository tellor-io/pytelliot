import pytest
from brownie import accounts
from brownie import Autopay
from brownie import chain
from brownie import StakingToken
from brownie import TellorFlex
from brownie.network.account import Account
from eth_abi import encode_single
from web3 import Web3

from telliot_core.apps.core import TelliotCore
from telliot_core.data.query_catalog import query_catalog
from telliot_core.reporters.reporter_autopay_utils import autopay_suggested_report
from telliot_core.tellor.tellorflex.autopay import TellorFlexAutopayContract
from telliot_core.tellor.tellorflex.oracle import TellorFlexOracleContract
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp


@pytest.fixture(scope="module")
def mock_token_contract():
    """mock token to use for staking"""
    return accounts[0].deploy(StakingToken)


@pytest.fixture(scope="module")
def mock_flex_contract(mock_token_contract):
    """mock oracle(TellorFlex) contract to stake in"""
    return accounts[0].deploy(TellorFlex, mock_token_contract.address, accounts[0], 10e18, 60)


@pytest.fixture(scope="module")
def mock_autopay_contract(mock_flex_contract, mock_token_contract):
    """mock payments(Autopay) contract for tipping and claiming tips"""
    return accounts[0].deploy(Autopay, mock_flex_contract.address, mock_token_contract.address, accounts[0], 20)


@pytest.mark.asyncio
async def test_main(mumbai_test_cfg, mock_flex_contract, mock_autopay_contract, mock_token_contract):
    async with TelliotCore(config=mumbai_test_cfg) as core:
        # get PubKey and PrivKey from config files
        account = core.get_account()

        # connect oracle to telliot core
        oracle = TellorFlexOracleContract(core.endpoint, account)
        oracle.address = mock_flex_contract.address
        oracle.connect()

        # connect autopay to telliot core
        autopay = TellorFlexAutopayContract(core.endpoint, account)
        autopay.address = mock_autopay_contract.address
        autopay.connect()

        # mint token and send to reporter address
        mock_token_contract.mint(core.get_account().address, 1000e18)
        assert mock_token_contract.balanceOf(core.get_account().address) == 1000e18

        # send eth from brownie address to reporter address for txn fees
        accounts[0].transfer(core.get_account().address, "10 ether")
        assert Account(core.get_account().address).balance() == 10e18

        # check governance address is brownie address
        governance_address = await oracle.get_governance_address()
        assert governance_address == accounts[0]

        # check stake amount is ten
        stake_amount = await oracle.get_stake_amount()
        assert stake_amount == 10

        # approve token to be spent by oracle
        mock_token_contract.approve(mock_flex_contract.address, 50e18, {"from": core.get_account().address})

        # staking to oracle transaction
        timestamp = TimeStamp.now().ts
        _, status = await oracle.write("depositStake", gas_limit=350000, legacy_gas_price=1, _amount=10 * 10**18)
        # check txn is successful
        assert status.ok

        # check staker information
        staker_info, status = await oracle.get_staker_info(Web3.toChecksumAddress(core.get_account().address))
        assert isinstance(status, ResponseStatus)
        assert status.ok
        assert staker_info == [pytest.approx(timestamp, 200), 10e18, 0, 0, 0]

        # mkr query id and query data
        mkr_query_id = query_catalog._entries["mkr-usd-spot"].query_id
        mkr_query_data = "0x" + query_catalog._entries["mkr-usd-spot"].query.query_data.hex()
        # approve token to be spent by autopay contract
        mock_token_contract.approve(mock_autopay_contract.address, 500e18, {"from": core.get_account().address})
        _, status = await autopay.write(
            "tip",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=mkr_query_id,
            _amount=int(10e18),
            _queryData=mkr_query_data,
        )
        # check txn is successful
        assert status.ok

        # submit a tip in autopay for reporter to report mkr/usd price
        current_tip, status = await autopay.get_current_tip(query_catalog._entries["mkr-usd-spot"].query_id)
        # check success of txn
        assert status.ok
        # check tip amount
        assert current_tip == 10

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag == "mkr-usd-spot"
        assert tb_reward == 10e18

        # query id and query data for ric
        ric_query_id = query_catalog._entries["ric-usd-spot"].query_id
        ric_query_data = "0x" + query_catalog._entries["ric-usd-spot"].query.query_data.hex()

        _, status = await autopay.write(
            "tip",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=ric_query_id,
            _amount=int(20e18),
            _queryData=ric_query_data,
        )

        assert status.ok

        current_tip, status = await autopay.get_current_tip(query_catalog._entries["ric-usd-spot"].query_id)
        assert status.ok
        assert current_tip == 20

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag == "ric-usd-spot"
        assert tb_reward == 20e18

        # variables for feed setup and to get feedId
        query_id = query_catalog._entries["trb-usd-legacy"].query_id
        reward = 30 * 10**18
        start_time = timestamp
        interval = 5
        window = 4
        price_threshold = 0
        query_data = "0x" + query_catalog._entries["trb-usd-legacy"].query.query_data.hex()

        # setup a feed on autopay
        _, status = await autopay.write(
            "setupDataFeed",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=query_id,
            _reward=reward,
            _startTime=timestamp,
            _interval=interval,
            _window=window,
            _priceThreshold=price_threshold,
            _queryData=query_data,
        )
        assert status.ok

        # encode feed variables, then hash to get feed id
        feed_data = encode_single(
            "(bytes32,uint256,uint256,uint256,uint256,uint256)",
            [bytes.fromhex(query_id[2:]), reward, start_time, interval, window, price_threshold],
        )
        feed_id = Web3.keccak(feed_data).hex()

        # fund trb-usd-legacy feed on autopay
        _, status = await autopay.write(
            "fundFeed", gas_limit=350000, legacy_gas_price=1, _feedId=feed_id, _queryId=query_id, _amount=50 * 10**18
        )
        assert status.ok

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag == "trb-usd-legacy"
        assert tb_reward == 30e18

        # fast forward to avoid reporter time lock
        chain.sleep(60)

        # submit report to oracle to get tip
        _, status = await oracle.write(
            "submitValue",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=query_id,
            _value="0x" + encode_single("(uint256)", [3000]).hex(),
            _nonce=0,
            _queryData=query_data,
        )

        # fast forward to avoid claiming tips buffer 12hr
        chain.sleep(43201)

        # # get timestamp trb's reported value
        # read_timestamp, status = await autopay.read("getCurrentValue", _queryId=query_id)
        # assert status.ok

        # _, status = await autopay.write(
        #     "claimTip",
        #     gas_limit=350000,
        #     legacy_gas_price=1,
        #     _feedId=feed_id,
        #     _queryId=query_id,
        #     _timestamps=[read_timestamp[2]],
        # )
        # assert status.ok

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag == "ric-usd-spot"
        assert tb_reward == 20e18

        # get timestamp ric's reported value
        read_timestamp, status = await autopay.read("getCurrentValue", _queryId=query_id)
        assert status.ok

        # submit report for onetime tip to oracle
        # should reserve tip for first reporter
        _, status = await oracle.write(
            "submitValue",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=ric_query_id,
            _value="0x" + encode_single("(uint256)", [1000]).hex(),
            _nonce=0,
            _queryData=ric_query_data,
        )
        assert status.ok

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag == "mkr-usd-spot"
        assert tb_reward == 10e18

        # fast forward to avoid reporter time lock
        chain.sleep(60)

        # submit report for onetime tip to oracle
        # should reserve tip for first reporter
        _, status = await oracle.write(
            "submitValue",
            gas_limit=350000,
            legacy_gas_price=1,
            _queryId=mkr_query_id,
            _value="0x" + encode_single("(uint256)", [1000]).hex(),
            _nonce=0,
            _queryData=mkr_query_data,
        )
        assert status.ok

        # get suggestion from telliot on query with highest tip
        suggested_qtag, tb_reward = await autopay_suggested_report(autopay)
        assert suggested_qtag is None
        assert tb_reward is None