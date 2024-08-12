import logging
import os

logger = logging.getLogger(__name__)


def ensure_directory(path):
    if os.path.splitext(path)[1]:  # Checks if the path has a file extension
        directory = os.path.dirname(path)
    else:
        directory = path
    try:
        os.makedirs(directory, exist_ok=True)
        return directory
    except OSError as e:
        logging.error(f"Error creating directory {directory}: {e}")
        fallback_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
        os.makedirs(fallback_dir, exist_ok=True)
        return fallback_dir