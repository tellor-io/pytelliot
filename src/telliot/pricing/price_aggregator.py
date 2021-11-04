import asyncio
import logging
import statistics
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import List

from telliot.data_source import DataSource
from telliot.pricing.price_source import PriceSource
from telliot.types.datapoint import datetime_now_utc
from telliot.types.datapoint import OptionalDataPoint
from typing import Literal

logger = logging.getLogger(__name__)


@dataclass
class PriceAggregator(DataSource[float], ABC):

    #: Asset
    asset: str = ""

    #: Currency of returned price
    currency: str = ""

    #: Callable algorithm that accepts an iterable of floats
    algorithm: Literal['median', 'average'] = 'median'

    #: Private storage for actual algorithm function
    _algorithm: Callable[..., float] = field(default=statistics.median, init=False, repr=False)

    #: Data feed sources
    sources: List[PriceSource] = field(default_factory=list)

    def __post_init__(self):
        if self.algorithm == 'median':
            self._algorithm = statistics.median
        elif self.algorithm == 'average':
            self._algorithm = statistics.average

    async def update_sources(self) -> List[OptionalDataPoint[float]]:
        """Update data feed sources

        Returns:
            Dictionary of updated source values, mapping data source UID
            to the time-stamped answer for that data source
        """

        async def gather_inputs() -> List[OptionalDataPoint[float]]:
            sources = self.sources
            datapoints = await asyncio.gather(
                *[source.fetch_new_datapoint() for source in sources]
            )
            return datapoints

        inputs = await gather_inputs()

        return inputs

    async def fetch_new_datapoint(self) -> OptionalDataPoint[float]:
        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        datapoints = await self.update_sources()

        prices = []
        for datapoint in datapoints:
            v, _ = datapoint  # Ignore input timestamps
            # Check for valid answers
            if v is not None:
                prices.append(v)

        # Run the algorithm on all valid prices
        print(f"Running {self.algorithm} on {prices}")
        result = self._algorithm(prices)
        datapoint = (result, datetime_now_utc())
        self.store_datapoint(datapoint)

        print("Feed Price: {} reported at time {}".format(datapoint[0], datapoint[1]))

        return datapoint