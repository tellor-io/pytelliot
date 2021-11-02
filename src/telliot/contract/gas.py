import json
from typing import Literal

import requests

ethgastypes = Literal["fast", "fastest", "safeLow", "average"]


async def fetch_gas_price() -> int:
    """Estimate current ETH gas price

    Work In Progress - Just do something quick
    """
    return await ethgasstation("fast")


async def ethgasstation(style: ethgastypes = "fast") -> int:
    """Fetch gas price from ethgasstation"""
    rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    prices = json.loads(rsp.content)
    gas_price = int(prices[style])

    return gas_price
