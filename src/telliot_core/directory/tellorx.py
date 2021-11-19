import json
from pathlib import Path

from telliot_core.directory.base import ContractDirectory
from telliot_core.directory.base import ContractInfo

__all__ = ["tellor_directory"]

_tellor_address_mainnet = {
    "master": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
    "oracle": "",
    "governance": "",
    "treasury": "",
}

_tellor_address_rinkeby = {
    "master": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
    "oracle": "0x18431fd88adF138e8b979A7246eb58EA7126ea16",
    "governance": "0xA64Bb0078eB80c97484f3f09Adb47b9B73CBcA00",
    "treasury": "0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147",
}

# Read contract ABIs from json files
_abi_folder = Path(__file__).resolve().parent / "_tellorx"
_abi_dict = {}
for name in ["master", "oracle", "governance", "treasury"]:
    with open(_abi_folder / f"{name}_abi.json", "r") as f:
        _abi_dict[name] = json.load(f)

# Create default tellor directory
tellor_directory = ContractDirectory()

for name in ["master", "oracle", "governance", "treasury"]:
    # Add maininet contract info entry
    tellor_directory.add_contract(
        ContractInfo(
            chain_id=1,
            org="tellor",
            name=name,
            address=_tellor_address_mainnet[name],
            abi=_abi_dict[name],
        )
    )

    # Add rinkeby contract info entry
    tellor_directory.add_contract(
        ContractInfo(
            chain_id=4,
            org="tellor",
            name=name,
            address=_tellor_address_rinkeby[name],
            abi=_abi_dict[name],
        )
    )
