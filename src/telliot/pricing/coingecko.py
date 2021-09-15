from typing import Any
from typing import Optional
from urllib.parse import urlencode

from telliot.base import TimeStampedFloat
from telliot.pricing.price_service import WebPriceService

# Coinbase API uses the 'id' field from /coins/list.
# Using a manual mapping for now.
coingecko_coin_id = {"btc": "bitcoin"}


class CoinGeckoPriceService(WebPriceService):
    """CoinGecko Price Service"""

    def __init__(self, **kwargs: Any) -> None:
        kwargs["name"] = "CoinGecko Price Service"
        kwargs["url"] = "https://api.coingecko.com"
        super().__init__(**kwargs)

    async def get_price(self, asset: str, currency: str) -> Optional[TimeStampedFloat]:
        """Implement PriceServiceInterface

        This implementation gets the price from the Coingecko API

        Note that coingecko does not return a timestamp so one is
        locally generated.
        """

        asset = asset.lower()
        currency = currency.lower()

        coin_id = coingecko_coin_id.get(asset, None)
        if not coin_id:
            raise Exception("Asset not supported: {}".format(asset))

        url_params = urlencode({"ids": coin_id, "vs_currencies": currency})
        request_url = "/api/v3/simple/price?{}".format(url_params)

        d = self.get_url(request_url)

        if "error" in d:
            print(d)  # TODO: Log
            return None

        elif "response" in d:
            response = d["response"]

            try:
                price = float(response[coin_id][currency])
            except KeyError as e:
                msg = "Error parsing Coingecko API response: KeyError: {}".format(e)
                print(msg)

        else:
            raise Exception("Invalid response from get_url")

        return TimeStampedFloat(price)
