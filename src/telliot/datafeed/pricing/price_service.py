from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Optional

import requests
from telliot.answer import TimeStampedFloat


class PriceServiceInterface(ABC):
    """Price Service Interface

    Interface to get pricing information
    As an interface, this class stores no to_state and all methods are abstract.
    Classes that inherit this interface must provide concrete implementations
    of each method.
    """

    @abstractmethod
    async def get_price(self, asset: str, currency: str) -> Optional[TimeStampedFloat]:
        """Fetch the price of an coin

        TODO: Strictly specify compliant coin/currency symbols so concrete
            classes can comply.

        Args:
            asset: Asset (Ticker Symbol)
            currency: Currency of returned price (Ticker Symbol)

        Returns:
            Time-stamped coin price or None if an exception occurs
        """
        raise NotImplementedError


class WebPriceService(PriceServiceInterface, ABC):
    """Abstract Base CLass for a Web-based Pricing Service"""

    def __init__(self, name: str, url: str, timeout: float = 5.0):

        self.name = name
        self.url = url
        self.timeout = timeout

    def get_url(self, url: str = "") -> Dict[str, Any]:
        """Helper function to get URL JSON response while handling exceptions

        Args:
            url: URL to fetch

        Returns:
            A dictionary with the following (optional) keys:
                json (dict or list): Result, if no error occurred
                error (str): A description of the error, if one occurred
                exception (Exception): The exception, if one occurred
        """

        request_url = self.url + url

        with requests.Session() as s:
            try:
                r = s.get(request_url, timeout=self.timeout)
                json_data = r.json()
                return {"response": json_data}

            except requests.exceptions.ConnectTimeout as e:
                return {"error": "Timeout Error", "exception": e}

            except Exception as e:
                return {"error": str(type(e)), "exception": e}
