"""
How to Use the Script:

    No Arguments: If the script is run without any arguments, it will execute all tasks in the configuration file:

        python3 script.py

    Specific Task: If you want to execute only specific tasks, pass the task type as an argument:

        python3 script.py clear_packets

        or

        python3 script.py update_client

    Multiple Tasks: To execute multiple specific tasks, list them all:

        python3 script.py clear_packets update_client
"""

import yaml
import subprocess
import os
import sys
import logging
from datetime import datetime

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

# Determine the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Load the configuration file from the same directory as the script
config_path = os.path.join(script_dir, 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Ensure directories exist for all log paths specified in the configuration
log_directory = ensure_directory(config['log_directory'])
task_log_directory = ensure_directory(config['task_log_path'])
command_log_directory = ensure_directory(config['command_log_path'])

# Setup logging with the verified directories
logger = logging.getLogger('TaskLogger')
logger.setLevel(logging.INFO)

task_log_file = os.path.join(task_log_directory, os.path.basename(config['task_log_path']))
cmd_log_file = os.path.join(command_log_directory, os.path.basename(config['command_log_path']))

# Setup file handlers to overwrite logs each time
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

def execute_command(command, log_filename, description):
    # Join the command list into a single string to log it properly
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

# Get command-line arguments to filter tasks
task_filter = sys.argv[1:] if len(sys.argv) > 1 else []

# Iterate over tasks and execute them if they match the filter or if no filter is provided
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
                execute_command(command, log_filename, description)

            elif task['type'] == 'update_client':
                log_filename = f"{task['type']}_{entry['host_chain']}_{entry['client']}_{entry['destination_chain']}.log"
                description = f"Updating client {entry['client']} on {entry['host_chain']} for {entry['destination_chain']}"
                command = [
                    config['hermes_path'], 'update', 'client',
                    '--host-chain', entry['host_chain'], '--client', entry['client']
                ]
                execute_command(command, log_filename, description)

if not task_filter or len(task_filter) == 0:
    logger.info("All tasks completed successfully!")
else:
    logger.info(f"Tasks {', '.join(task_filter)} completed successfully!")
