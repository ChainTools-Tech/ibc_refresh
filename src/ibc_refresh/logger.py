import logging
import os

from ibc_refresh.utils import ensure_directory


def initialize_loggers(config):
    script_dir = os.path.dirname(os.path.realpath(__file__))

    log_directory = ensure_directory(config['log_directory'])
    task_log_file = os.path.join(log_directory, config['task_log_file'])
    cmd_log_file = os.path.join(log_directory, config['command_log_file'])

    cmd_logger = logging.getLogger('CommandLogger')
    cmd_logger.setLevel(logging.INFO)

    cmd_handler = logging.FileHandler(cmd_log_file, mode='w')
    cmd_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s'))
    cmd_logger.addHandler(cmd_handler)

    cmd_log_console_handler = logging.StreamHandler()
    cmd_log_console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s'))
    cmd_logger.addHandler(cmd_log_console_handler)

    task_logger = logging.getLogger('TaskLogger')
    task_logger.setLevel(logging.INFO)

    task_log_file_handler = logging.FileHandler(task_log_file, mode='w')
    task_log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s'))
    task_logger.addHandler(task_log_file_handler)

    task_log_console_handler = logging.StreamHandler()
    task_log_console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s'))
    task_logger.addHandler(task_log_console_handler)
