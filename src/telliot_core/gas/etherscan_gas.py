import json
from dataclasses import dataclass
from typing import List

import requests

from telliot_core.datasource import DataSource
from telliot_core.datasource import OptionalDataPoint
from telliot_core.utils.timestamp import now


@dataclass
class EtherscanGasPrice:
    LastBlock: int
    SafeGasPrice: float
    ProposeGasPrice: float
    FastGasPrice: float
    suggestBaseFee: float
    gasUsedRatio: List[float]


@dataclass
class EtherscanGasPriceSource(DataSource[EtherscanGasPrice]):

    # Use an API key if higher rate limit is required
    api_key: str = ""

    async def fetch_new_datapoint(self) -> OptionalDataPoint[EtherscanGasPrice]:
        """Fetch new value and store it for later retrieval"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"
        }
        msg = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"

        if self.api_key:
            msg = msg + f"&apikey={self.api_key}"

        rsp = requests.get(msg, headers=headers)
        response = json.loads(rsp.content)
        status = response["status"]
        if int(status) == 1:
            gp_result = response["result"]
            gas_used_ratio_str = gp_result["gasUsedRatio"]
            gas_used_ratio = [float(num) for num in gas_used_ratio_str.split(",")]
            gp = EtherscanGasPrice(
                LastBlock=int(gp_result["LastBlock"]),
                SafeGasPrice=float(gp_result["SafeGasPrice"]),
                ProposeGasPrice=float(gp_result["ProposeGasPrice"]),
                FastGasPrice=float(gp_result["FastGasPrice"]),
                suggestBaseFee=float(gp_result["suggestBaseFee"]),
                gasUsedRatio=gas_used_ratio,
            )
            return gp, now()
        else:
            return None, None
