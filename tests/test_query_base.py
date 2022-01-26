from dataclasses import dataclass

from telliot_core.queries import LegacyRequest
from telliot_core.queries import SpotPrice
from telliot_core.queries.query import OracleQuery
from telliot_core.queries.query import query_from_descriptor
from telliot_core.queries.query import query_from_state


def test_main():
    @dataclass
    class MyQuery(OracleQuery):
        text: str
        val: int = 3

    q = MyQuery("asdf")
    state = q.get_state()
    print(state)
    assert state == {"type": "MyQuery", "text": "asdf", "val": 3}


def test_query_from_descriptor():
    d = '{"type":"LegacyRequest","legacy_id":1}'
    q = query_from_descriptor(d)
    print(q)
    assert isinstance(q, LegacyRequest)
    assert q.legacy_id == 1


def test_query_from_state():
    d = {"type": "SpotPrice", "asset": "ohm", "currency": "eth"}
    q = query_from_state(d)
    print(q)
    assert isinstance(q, SpotPrice)
    assert q.asset == "ohm"
