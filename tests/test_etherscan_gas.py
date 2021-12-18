from telliot_core.gas.etherscan_gas import EtherscanGasPriceSource, EtherscanGasPrice
import pytest


@pytest.mark.asyncio
async def test_etherscan_gas():
    c = EtherscanGasPriceSource()
    result = await c.fetch_new_datapoint()
    assert isinstance(result[0], EtherscanGasPrice)
