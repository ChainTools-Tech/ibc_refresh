import logging
import os
import subprocess
from datetime import datetime
from ibc_refresh.utils import ensure_directory


cmd_logger = logging.getLogger("CommandLogger")
task_logger = logging.getLogger("TaskLogger")


def execute_command(command, description, log_filename, config):
    command_string = ' '.join(command)
    cmd_logger.info(f"Executing command: {command_string}")
    log_path = log_filename
    cmd_logger.info(f"Starting: {description}")
    start_time = datetime.now()

    with open(log_path, 'w') as file:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = []
            for line in process.stdout:
                file.write(line)
                output.append(line)
            process.stdout.close()
            return_code = process.wait()
            end_time = datetime.now()
            if any("missing chain config" in line for line in output):
                task_logger.error(
                    f"ERROR: Chain configuration missing for {description}. Please verify the relayer setup.")
            if return_code:
                task_logger.info(f"Completed with error: {description} (Duration: {end_time - start_time})")
            else:
                task_logger.info(f"Completed successfully: {description} (Duration: {end_time - start_time})")
        except FileNotFoundError:
            task_logger.exception("Command not founds: {}".format(command_string))


def process_tasks(cmdargs, config):
    tasks_log_path = ensure_directory(os.path.join(config['log_directory'], 'task_output/'))
    task_logger.info(f"Output for tasks log checked: {tasks_log_path}")

    for task in cmdargs.task:
        task_specific_log_path = ensure_directory(os.path.join(tasks_log_path, task))
        task_logger.info(f"Output for task specific logs checked: {task_specific_log_path}/{task}")

    for task in config['tasks']:
        for entry in task['entries']:
            if task['type'] == 'clear_packets' and 'clear_packets' in cmdargs.task:
                cmd_output_log_filename = f"{tasks_log_path}/{task['type']}/{task['type']}_{entry['chain']}_{entry['channel']}_{entry['destination_chain']}.log"
                description = f"Clearing packets on {entry['chain']} channel {entry['channel']} to {entry['destination_chain']}"
                command = [
                    config['hermes_path'], 'clear', 'packets',
                    '--chain', entry['chain'], '--port', entry['port'], '--channel', entry['channel']
                ]
                execute_command(command, description, cmd_output_log_filename, config)
            elif task['type'] == 'update_client' and 'update_client' in cmdargs.task:
                cmd_output_log_filename = f"{tasks_log_path}/{task['type']}/{task['type']}_{entry['host_chain']}_{entry['client']}_{entry['destination_chain']}.log"
                description = f"Updating client {entry['client']} on {entry['host_chain']} for {entry['destination_chain']}"
                command = [
                    config['hermes_path'], 'update', 'client',
                    '--host-chain', entry['host_chain'], '--client', entry['client']
                ]
                execute_command(command, description, cmd_output_log_filename, config)