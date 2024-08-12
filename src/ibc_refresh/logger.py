import logging
import os

from ibc_refresh.utils import ensure_directory

def initialize_loggers(config):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Ensure directories exist for all log paths specified in the configuration
    log_directory = ensure_directory(config['log_directory'])

    task_log_file = os.path.join(log_directory, config['task_log_file'])
    cmd_log_file = os.path.join(log_directory, config['command_log_file'])

    logger = logging.getLogger('TaskLogger')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(task_log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    cmd_logger = logging.getLogger('CommandLogger')
    cmd_logger.setLevel(logging.INFO)
    cmd_handler = logging.FileHandler(cmd_log_file, mode='w')
    cmd_handler.setFormatter(logging.Formatter('%(message)s'))
    cmd_logger.addHandler(cmd_handler)