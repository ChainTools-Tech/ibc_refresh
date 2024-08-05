import yaml
import subprocess
import os
import sys
import logging
from datetime import datetime
import argparse

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

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def setup_logging(config):
    log_directory = ensure_directory(config['log_directory'])
    task_log_directory = ensure_directory(config['task_log_path'])
    command_log_directory = ensure_directory(config['command_log_path'])

    logger = logging.getLogger('TaskLogger')
    logger.setLevel(logging.INFO)

    task_log_file = os.path.join(task_log_directory, os.path.basename(config['task_log_path']))
    cmd_log_file = os.path.join(command_log_directory, os.path.basename(config['command_log_path']))

    file_handler = logging.FileHandler(task_log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    cmd_logger = logging.getLogger('CommandLogger')
    cmd_logger.setLevel(logging.INFO)
    cmd_handler = logging.FileHandler(cmd_log_file, mode='w')
    cmd_handler.setFormatter(logging.Formatter('%(message)s'))
    cmd_logger.addHandler(cmd_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger, cmd_logger, log_directory

def execute_command(command, log_filename, description, logger, cmd_logger, log_directory):
    command_string = ' '.join(command)
    cmd_logger.info(f"Executing command: {command_string}")  # Log the command before execution

    log_path = os.path.join(log_directory, log_filename)
    logger.info(f"Starting: {description}")
    start_time = datetime.now()

    with open(log_path, 'w') as file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = []
        for line in process.stdout:
            file.write(line)
            output.append(line)
        process.stdout.close()
        return_code = process.wait()
    end_time = datetime.now()

    if any("missing chain config" in line for line in output):
        logger.error(f"ERROR: Chain configuration missing for {description}. Please verify the relayer setup.")
    if return_code:
        logger.info(f"Completed with error: {description} (Duration: {end_time - start_time})")
    else:
        logger.info(f"Completed successfully: {description} (Duration: {end_time - start_time})")

def execute_tasks(config, task_filter, logger, cmd_logger, log_directory):
    for task in config['tasks']:
        if not task_filter or task['type'] in task_filter:
            for entry in task['entries']:
                if task['type'] == 'clear_packets':
                    log_filename = f"{task['type']}_{entry['chain']}_{entry['channel']}_{entry['destination_chain']}.log"
                    description = f"Clearing packets on {entry['chain']} channel {entry['channel']} to {entry['destination_chain']}"
                    command = [
                        config['hermes_path'], 'clear', 'packets',
                        '--chain', entry['chain'], '--port', entry['port'], '--channel', entry['channel']
                    ]
                    execute_command(command, log_filename, description, logger, cmd_logger, log_directory)

                elif task['type'] == 'update_client':
                    log_filename = f"{task['type']}_{entry['host_chain']}_{entry['client']}_{entry['destination_chain']}.log"
                    description = f"Updating client {entry['client']} on {entry['host_chain']} for {entry['destination_chain']}"
                    command = [
                        config['hermes_path'], 'update', 'client',
                        '--host-chain', entry['host_chain'], '--client', entry['client']
                    ]
                    execute_command(command, log_filename, description, logger, cmd_logger, log_directory)

    if not task_filter or len(task_filter) == 0:
        logger.info("All tasks completed successfully!")
    else:
        logger.info(f"Tasks {', '.join(task_filter)} completed successfully!")

def main():
    parser = argparse.ArgumentParser(description='Script to execute tasks based on configuration file.')
    parser.add_argument('-t', '--task', nargs='*', required=True, help='Task types to execute (e.g., clear_packets, update_client)')
    parser.add_argument('-c', '--config', required=True, help='Path to the configuration file')

    args = parser.parse_args()

    config_path = args.config
    task_filter = args.task if args.task else []

    config = load_config(config_path)
    logger, cmd_logger, log_directory = setup_logging(config)

    execute_tasks(config, task_filter, logger, cmd_logger, log_directory)

if __name__ == "__main__":
    main()
