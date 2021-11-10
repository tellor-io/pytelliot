from dataclasses import dataclass
from dataclasses import field

from telliot.datasource import DataSource
from telliot.pricing.price_service import WebPriceService
from telliot.types.datapoint import OptionalDataPoint


@dataclass
class PriceSource(DataSource[float]):
    """Current Asset Price

    The Current Asset Price data source retrieves the price of a coin
    in the specified current from a `WebPriceService`.
    """

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Service
    service: WebPriceService = field(default_factory=WebPriceService)  # type: ignore

    async def fetch_new_datapoint(self) -> OptionalDataPoint[float]:
        """Update current value with time-stamped value fetched from source

        Returns:
            New datapoint
        """
        datapoint = await self.service.get_price(self.asset, self.currency)
        v, t = datapoint
        if v is not None and t is not None:
            self.store_datapoint((v, t))

        return datapoint
