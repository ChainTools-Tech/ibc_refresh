import requests
import logging

logger = logging.getLogger("RPCClient")

def get_latest_block_height(rpc_url):
    """Fetch the latest block height from an RPC endpoint."""
    try:
        response = requests.get(f"{rpc_url}/status", timeout=5)
        response.raise_for_status()
        data = response.json()
        return int(data["result"]["sync_info"]["latest_block_height"])
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error(f"Failed to fetch latest block height from {rpc_url}: {e}")
        return None
