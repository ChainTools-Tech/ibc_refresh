import requests
import logging
from datetime import datetime

logger = logging.getLogger("BlockchainClient")

class APIClient:
    """Handles REST API queries to CosmosSDK-based chains."""

    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_client_state(self, client_id):
        """Fetches the client state for the given IBC client."""
        url = f"{self.api_url}/ibc/core/client/v1/client_states/{client_id}"
        logger.debug(f"Fetching client state from: {url}")

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()["client_state"]

            # Extract required fields safely
            trusting_period = data["trusting_period"]
            latest_height = data["latest_height"]["revision_height"]
            proof_height = data.get("proof_height", {}).get("revision_height", None)  # ✅ Handle missing proof_height

            return {
                "trusting_period": trusting_period,
                "latest_height": int(latest_height),
                "proof_height": int(proof_height) if proof_height else None
            }

        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Failed to fetch client state for {client_id}: {e}")
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
