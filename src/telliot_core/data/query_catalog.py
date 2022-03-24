from telliot_core.queries.catalog import Catalog
from telliot_core.queries.legacy_query import LegacyRequest
from telliot_core.queries.price.aws_spot_price import AwsSpotPrice
from telliot_core.queries.price.spot_price import SpotPrice

"""Main instance of the Query Catalog."""
query_catalog = Catalog()

# --------------------------------------------------------------------------------------
# Query Catalog Entries
# --------------------------------------------------------------------------------------

query_catalog.add_entry(
    tag="eth-usd-legacy",
    title="Legacy ETH/USD spot price",
    q=LegacyRequest(legacy_id=1),
)

query_catalog.add_entry(
    tag="btc-usd-legacy",
    title="Legacy BTC/USD spot price",
    q=LegacyRequest(legacy_id=2),
)

query_catalog.add_entry(
    tag="ampl-legacy",
    title="Legacy AMPL/USD custom price",
    q=LegacyRequest(legacy_id=10),
)

query_catalog.add_entry(tag="uspce-legacy", title="Legacy USPCE value", q=LegacyRequest(legacy_id=41))

query_catalog.add_entry(
    tag="trb-usd-legacy",
    title="Legacy TRB/USD spot price",
    q=LegacyRequest(legacy_id=50),
)

query_catalog.add_entry(
    tag="eth-jpy-legacy",
    title="Legacy ETH/JPY spot price",
    q=LegacyRequest(legacy_id=59),
)

query_catalog.add_entry(
    tag="ohm-eth-spot",
    title="OHM/ETH spot price",
    q=SpotPrice(asset="ohm", currency="eth"),
    active=True,
)

query_catalog.add_entry(
    tag="vsq-usd-spot",
    title="VSQ/USD spot price",
    q=SpotPrice(asset="vsq", currency="usd"),
)

query_catalog.add_entry(
    tag="aws-spot-zone-us-east-1f-instance-i3.16xlarge",
    title="AWS Spot Price",
    q=AwsSpotPrice(zone="us-east-1f", instance="i3.16xlarge"),
)

query_catalog.add_entry(
    tag="bct-usd-spot",
    title="BCT/USD spot price",
    q=SpotPrice(asset="bct", currency="usd"),
)

query_catalog.add_entry(
    tag="dai-usd-spot",
    title="DAI/USD spot price",
    q=SpotPrice(asset="dai", currency="usd"),
)

query_catalog.add_entry(
    tag="ric-usd-spot",
    title="RIC/USD spot price",
    q=SpotPrice(asset="ric", currency="usd"),
)

query_catalog.add_entry(
    tag="idle-usd-spot",
    title="IDLE/USD spot price",
    q=SpotPrice(asset="idle", currency="usd"),
)

query_catalog.add_entry(
    tag="mkr-usd-spot",
    title="MKR/USD spot price",
    q=SpotPrice(asset="mkr", currency="usd"),
)

query_catalog.add_entry(
    tag="sushi-usd-spot",
    title="SUSHI/USD spot price",
    q=SpotPrice(asset="sushi", currency="usd"),
)

query_catalog.add_entry(
    tag="matic-usd-spot",
    title="MATIC/USD spot price",
    q=SpotPrice(asset="matic", currency="usd"),
)

query_catalog.add_entry(
    tag="usdc-usd-spot",
    title="USDC/USD spot price",
    q=SpotPrice(asset="usdc", currency="usd"),
)
