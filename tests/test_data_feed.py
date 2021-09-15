""" Simple example of creating a "plug-in" data feed

"""
import statistics

import pytest
import telliot.registry


@pytest.mark.asyncio
async def test_AssetPriceFeed():
    btc_usd_median = telliot.registry.data_feeds["btc-usd-median"]

    price = await btc_usd_median.update_value()

    # Get list of data sources from sources dict
    sources = [source.value for source in btc_usd_median.sources.values()]

    # Make sure error is less than decimal tolerance
    assert (price.val - statistics.median([s.val for s in sources])) < 10 ** -6
