import logging
import os
import subprocess
from datetime import datetime
from ibc_refresh.failure_tracker import FailureTracker
from ibc_refresh.notification import NotificationHandler
from ibc_refresh.utils import ensure_directory


cmd_logger = logging.getLogger("CommandLogger")
task_logger = logging.getLogger("TaskLogger")


def execute_command(command, description, log_filename, config, task_key, failure_threshold):
    command_string = ' '.join(command)
    cmd_logger.info(f"Executing command: {command_string}")
    start_time = datetime.now()

    failure_tracker = FailureTracker(config)  # Pass config

    with open(log_filename, 'w') as file:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = []
            for line in process.stdout:
                file.write(line)
                output.append(line)
            process.stdout.close()
            return_code = process.wait()
            end_time = datetime.now()

            if return_code != 0:
                current_failures = failure_tracker.increment_failure(task_key)
                error_message = f"ERROR in Hermes execution: {description} (Failures: {current_failures}/{failure_threshold})"
                cmd_logger.error(error_message)

                if current_failures >= failure_threshold:
                    notifier = NotificationHandler(config)
                    notifier.send_notification(
                        title="🚨 Hermes Execution Failed!",
                        description=f"{error_message}\nNotification sent after {current_failures} failed attempts.",
                        severity="critical",
                        command=command_string
                    )

            else:
                failure_tracker.reset_failure(task_key)
                cmd_logger.info(f"Completed successfully: {description} (Duration: {end_time - start_time})")

        except FileNotFoundError:
            cmd_logger.exception(f"Command not found: {command_string}")


def process_tasks(cmdargs, config):
    tasks_log_path = ensure_directory(os.path.join(config['log_directory'], 'task_output/'))

    for task in config['tasks']:
        failure_threshold = task.get("failure_threshold", 1)

        for entry in task['entries']:
            task_key = f"{task['type']}:{entry.get('chain', entry.get('host_chain'))}:{entry.get('channel', entry.get('client'))}"

            if task['type'] == 'clear_packets' and 'clear_packets' in cmdargs.task:
                cmd_output_log_filename = f"{tasks_log_path}/{task['type']}/{task['type']}_{entry['chain']}_{entry['channel']}_{entry['destination_chain']}.log"
                description = f"Clearing packets on {entry['chain']} channel {entry['channel']} to {entry['destination_chain']}"
                command = [
                    config['hermes_path'], 'clear', 'packets',
                    '--chain', entry['chain'], '--port', entry['port'], '--channel', entry['channel']
                ]
                execute_command(command, description, cmd_output_log_filename, config, task_key, failure_threshold)

            elif task['type'] == 'update_client' and 'update_client' in cmdargs.task:
                cmd_output_log_filename = f"{tasks_log_path}/{task['type']}/{task['type']}_{entry['host_chain']}_{entry['client']}_{entry['destination_chain']}.log"
                description = f"Updating client {entry['client']} on {entry['host_chain']} for {entry['destination_chain']}"
                command = [
                    config['hermes_path'], 'update', 'client',
                    '--host-chain', entry['host_chain'], '--client', entry['client']
                ]
                execute_command(command, description, cmd_output_log_filename, config, task_key, failure_threshold)