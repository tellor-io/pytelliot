""" Unit tests for Morphware queries.

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
import json

from eth_abi import decode_abi
from eth_abi import decode_single

from telliot_core.queries.morphware import Morphware


def test_query_constructor():
    """Validate Morphware query."""
    q = Morphware(version=1)

    exp_query_data = (
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tMorphwar"
        b"e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x01"
    )

    assert q.query_data == exp_query_data

    query_type, encoded_param_vals = decode_abi(["string", "bytes"], q.query_data)
    assert query_type == "Morphware"

    version = decode_single("uint256", encoded_param_vals)
    assert isinstance(version, int)
    assert version == 1

    exp = "bf7f9942188d84961cf2a01ec68c42ef000d5b0fb5ca7dc0fcf1ceee5164811c"
    assert q.query_id.hex() == exp


def test_encode_decode_reported_val():
    """Ensure expected encoding/decoding behavior."""
    q = Morphware(version=1)

    # JSON string containing data specified by Morphware and
    # referenced in Tellor /dataSpecs:
    # https://github.com/tellor-io/dataSpecs/blob/main/types/Morphware.md
    data = '{"zone": "us-east-1", "instance_types": ["t2.micro", "t2.small"], "provider": "Amazon"}'

    submit_value = q.value_type.encode(data)
    assert isinstance(submit_value, bytes)

    decoded_data = q.value_type.decode(submit_value)
    assert isinstance(decoded_data, str)

    d = json.loads(decoded_data)
    assert d["zone"] == "us-east-1"
    assert d["instance_types"] == ["t2.micro", "t2.small"]
