import logging
import os
import re
import subprocess
from datetime import datetime, timedelta
from ibc_refresh.failure_tracker import FailureTracker
from ibc_refresh.notification import NotificationHandler
from ibc_refresh.rpc_client import get_latest_block_height
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

                    # ✅ Reset failure count after sending notification
                    failure_tracker.reset_failure(task_key)

            else:
                # ✅ Reset failure count on success
                failure_tracker.reset_failure(task_key)
                cmd_logger.info(f"Completed successfully: {description} (Duration: {end_time - start_time})")

        except FileNotFoundError:
            cmd_logger.exception(f"Command not found: {command_string}")


def check_client_expiration(entry, config):
    """Check the expiration of an IBC client and send a notification."""
    chain = entry["chain"]
    client = entry["client"]
    rpc_url = entry["rpc_endpoint"]

    # Run Hermes command to get client state
    command_string = [config['hermes_path'], 'query', 'client', 'state', '--chain', chain, '--client', client]
    result = subprocess.run(command_string, capture_output=True, text=True)

    if result.returncode != 0:
        return f"Failed to query client state for {chain} - {client}"

    # Extract trusting period & chain_id
    output = result.stdout

    try:
        trusting_period_seconds = int(output.split("trusting_period: ")[1].split("s")[0])  # Extract trusting period
        trusting_period_days = trusting_period_seconds // 86400  # Convert to days

        # Extract destination chain_id using regex
        match = re.search(r'chain_id: ChainId \{\s*id: "(.*?)"', output)
        destination_chain = match.group(1) if match else "Unknown"

    except (IndexError, ValueError, AttributeError):
        return f"Error extracting client state details for {chain} - {client}"

    # Fetch latest block height
    latest_block_height = get_latest_block_height(rpc_url)
    if latest_block_height is None:
        return f"Failed to fetch latest block height for {chain}"

    # Get current date and estimate expiration
    current_date = datetime.utcnow()
    expiration_date = current_date + timedelta(days=trusting_period_days)
    days_remaining = (expiration_date - current_date).days

    # Determine severity level
    if days_remaining > 7:
        severity = "info"  # Green (Safe)
        color_icon = "🟢"
    elif 3 <= days_remaining <= 7:
        severity = "warning"  # Yellow (Warning)
        color_icon = "🟡"
    else:
        severity = "critical"  # Red (Urgent)
        color_icon = "🔴"

    # Send notification with chain_id and checked height
    notifier = NotificationHandler(config)
    notifier.send_notification(
        title=f"{color_icon} Client Expiration Notice: {chain}",
        description=f"Client `{client}` will expire in `{days_remaining}` days.\n"
                    f"🔹 Destination Chain: `{destination_chain}`\n"
                    f"🔹 Checked at height: `{latest_block_height}`",
        severity=severity,
        command=command_string,
        chain=chain,
        dst_chain=destination_chain
    )

    return f"Client {client} on {chain} expires in {days_remaining} days. Checked at height: {latest_block_height}."


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

            elif task['type'] == 'client_expiration' and 'client_expiration' in cmdargs.task:
                client_key = (entry["chain"], entry["client"])  # Unique key per client

                task_logger.info(f"Checking expiration for client {client_key}")  # ✅ Log each client check
                result = check_client_expiration(entry, config)
                task_logger.info(result)