import requests
import logging
from datetime import datetime

logger = logging.getLogger("BlockchainClient")

class APIClient:
    """Handles REST API queries to CosmosSDK-based chains."""

    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_trusting_period(self, client_id):
        """Fetches the trusting period for the given IBC client."""
        try:
            response = requests.get(f"{self.api_url}/ibc/core/client/v1/client_states/{client_id}", timeout=5)
            response.raise_for_status()
            data = response.json()
            trusting_period = int(data["client_state"]["trusting_period"].replace("s", ""))  # Convert to seconds
            return trusting_period
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Failed to fetch trusting period for client {client_id}: {e}")
            return None

    def fetch_last_header_time(self, client_id):
        """Fetches the last header update timestamp for the given IBC client."""
        try:
            response = requests.get(f"{self.api_url}/ibc/core/client/v1/consensus_states/{client_id}/latest", timeout=5)
            response.raise_for_status()
            data = response.json()
            timestamp = datetime.strptime(data["consensus_state"]["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
            return timestamp
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Failed to fetch last header time for client {client_id}: {e}")
            return None


class RPCClient:
    """Handles RPC queries to CosmosSDK-based chains."""

    def __init__(self, rpc_url):
        self.rpc_url = rpc_url

    def get_latest_block_height(self):
        """Fetches the latest block height from an RPC endpoint."""
        try:
            response = requests.get(f"{self.rpc_url}/status", timeout=5)
            response.raise_for_status()
            data = response.json()
            return int(data["result"]["sync_info"]["latest_block_height"])
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Failed to fetch latest block height from {self.rpc_url}: {e}")
            return None
