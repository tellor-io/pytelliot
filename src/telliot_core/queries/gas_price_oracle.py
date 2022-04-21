import logging
from dataclasses import dataclass

from telliot_core.dtypes.value_type import ValueType
from telliot_core.queries.abi_query import AbiQuery

logger = logging.getLogger(__name__)


@dataclass
class GasPriceOracle(AbiQuery):
    """Returns the result for a given GasPriceOracle query.

    Attributes:
        version:
            A reference to GasPriceOracle data specifications found
            here: 
            https://github.com/tellor-io/dataSpecs/blob/main/types/GasPriceOracle.md

            More about gas/gas price/gas price oracles:
            https://ethereum.org/en/developers/docs/gas/
    """

    chainId: int
    timestamp: int

    #: ABI used for encoding/decoding parameters
    abi = [
        {
            "type": "uint256",
            "name": "chainId",
        },
        {
            "type": "uint256",
            "name": "timestamp",
        },
    ]

    @property
    def value_type(self) -> ValueType:
        """Data type returned for a GasPriceOracle query. Returns a gas price in gwei.

            - abi_type: ufixed256x18 (18 decimals of precision)
            - packed: false

        """
        return ValueType(abi_type="uint256x18", packed=False)