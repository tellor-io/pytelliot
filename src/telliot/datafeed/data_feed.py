""" :mod:`telliot.datafeed.data_feed`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
import asyncio
from abc import ABC
from typing import Any
from typing import Dict

from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_source import DataSource
from telliot.queries.query import OracleQuery
from typing import List
from pydantic import Field


class DataFeed(DataSource, ABC):
    """Data feed

    A data feed creates a response value for an
    :class:`~telliot.queries.query.OracleQuery`.
    """

    #: Data feed sources
    sources: List[DataSource] = Field(default_factory=list)

    #: Query supported by this data feed
    query: OracleQuery

    async def update_sources(self) -> List[TimeStampedAnswer[Any]]:
        """Update data feed sources

        Returns:
            Dictionary of updated source values, mapping data source UID
            to the time-stamped answer for that data source
        """


        async def gather_inputs() -> List[TimeStampedAnswer[Any]]:
            sources = self.sources
            values = await asyncio.gather(
                *[source.update_value() for source in sources]
            )
            return values

        return await gather_inputs()
