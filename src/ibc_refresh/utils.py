import logging
import os


def ensure_directory(path):
    if os.path.splitext(path)[1]:
        directory = os.path.dirname(path)
    else:
        directory = path
    try:
        os.makedirs(directory, exist_ok=True)
        return directory
    except OSError as e:
        fallback_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.logs')
        logging.error(f"Error creating directory {directory}: {e}, Fallback directory {fallback_dir}")
        os.makedirs(fallback_dir, exist_ok=True)
        return fallback_dir


def get_endpoint(config, endpoint_type, chain_id):
    """Fetches API or RPC endpoint for a given chain_id from config."""
    for entry in config["endpoints"].get(endpoint_type, []):
        if entry["chain_id"] == chain_id:
            return entry["endpoint_url"]
    return None  # Return None if no match found
