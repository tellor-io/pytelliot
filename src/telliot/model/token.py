from collections import namedtuple
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from telliot.model.base import Base


@dataclass
class ERC20Token(Base):
    """Representation of an ERC20 token"""

    #: Chain ID
    chain_id: int

    #: Contract address on chain
    address: str

    #: Token Symbol
    symbol: str

    #: Conversion factor in currency calculations
    decimals: int

    #: Descriptive name
    name: str

    #: Logo URI
    logo_uri: Optional[str]


TokenListVersion = namedtuple(
    "TokenListVersion", ["major", "minor", "patch"], defaults=[0, 0, 0]
)


@dataclass
class ERC20TokenList(Base):
    """ERC-20 Token List"""

    #: Token list name
    name: str

    #: Token list
    tokens: List[ERC20Token]

    version: Optional[TokenListVersion]

    @classmethod
    def from_uniswap(cls, jsn: Dict[str, Any]) -> "ERC20TokenList":
        """Create a token list from uniswap format

        See `https://tokenlists.org/` for more information
        """

        name = jsn["name"]
        version = TokenListVersion(
            major=jsn["version"]["major"],
            minor=jsn["version"]["minor"],
            patch=jsn["version"]["patch"],
        )

        jtokens = jsn.get("tokens", [])
        if not jtokens:
            raise Exception("Token List is empty")

        tokens = []
        for token in jtokens:
            tokens.append(
                ERC20Token(
                    name=token.get("name", None),
                    symbol=token.get("symbol", None),
                    chain_id=token.get("chainId", None),
                    address=token.get("address", None),
                    decimals=token.get("decimals", None),
                    logo_uri=token.get("logoURI", None),
                )
            )

        return cls(name=name, tokens=tokens, version=version)
