import logging
from typing import Optional

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.timestamp import TimeStamp

logger = logging.getLogger(__name__)


class TellorflexOracleContract(Contract):
    def __init__(self, node: RPCEndpoint, private_key: str = ""):
        chain_id = node.chain_id
        assert chain_id is not None

        contract_info = contract_directory.find(chain_id=chain_id, name="tellorflex-oracle")[0]
        if not contract_info:
            raise Exception(f"Tellorflex oracle contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            private_key=private_key,
        )

    async def get_governance_address(self) -> Optional[str]:

        governance_address, status = await self.read("getGovernanceAddress")

        if status.ok:
            return str(governance_address)
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None

    async def get_reporting_lock(self) -> Optional[int]:

        lock, status = await self.read("getReportingLock")

        if status.ok:
            return int(lock)
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None

    async def get_stake_amount(self) -> Optional[float]:

        stake, status = await self.read("getStakeAmount")

        if status.ok:
            stake_in_trb = int(stake) / 1.0e18
            return stake_in_trb
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None

    async def get_time_of_last_new_value(self) -> Optional[TimeStamp]:

        tlnv, status = await self.read("getTimeOfLastNewValue")

        if status.ok:
            return TimeStamp(tlnv)
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None

    async def get_token_address(self) -> Optional[str]:

        token_address, status = await self.read("getTokenAddress")

        if status.ok:
            return str(token_address)
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None

    async def get_total_stake_amount(self) -> Optional[float]:

        total_stake, status = await self.read("getTotalStakeAmount")

        if status.ok:
            total_stake_trb = int(total_stake) / 1.0e18
            return total_stake_trb
        else:
            logger.error("Error reading TellorflexOracleContract")
            logger.error(status)
            return None
