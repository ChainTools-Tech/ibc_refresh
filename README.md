# IBC Refresh

## Overview

**IBC Refresh** is an automation tool for IBC relayers, designed to simplify the management of inter-blockchain communication tasks. It supports packet clearance and client updates while integrating structured logging and notifications (Discord/Slack) for monitoring task execution.

## Features

- **Automated IBC Operations**: Handles `clear_packets` and `update_client` tasks based on a configuration file.
- **Configurable Task Execution**: Define tasks in `config.yaml` for multiple chains.
- **Comprehensive Logging**: Logs stored in a dedicated directory for troubleshooting and auditing.
- **Notifications**: Supports sending structured alerts to Discord and Slack upon task execution results.

## Prerequisites

- Python 3.8+
- Dependencies listed in `requirements.txt` (installed automatically during setup)
- Access to a terminal for CLI execution

## Installation

You can install **IBC Refresh** from source by following these steps:

### 1. Clone the Repository
```bash
git clone https://your-repository-url/ibc_refresh.git
cd ibc_refresh
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install the Package
```bash
python -m pip install .
```

## Usage

### Running the Tool
Execute IBC Refresh with the required configuration file:
```bash
ibc_refresh --config path/to/config.yaml --task clear_packets
```

### Supported Tasks
- `clear_packets`: Clears pending IBC packets.
- `update_client`: Updates client states between chains.

Example:
```bash
ibc_refresh --config config.yaml --task update_client
```

## Configuration

The `config.yaml` file contains settings for logging, notification methods, and task definitions.

### Example Configuration:
```yaml
log_directory: .logs/
task_log_file: task_execution.log
command_log_file: executed_commands.log
notification_log_file: notifications.log
hermes_path: /home/relayer/.local/bin/hermes

notifications:
  - type: discord
    webhook: "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
  - type: slack
    webhook: "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"

tasks:
  - type: clear_packets
    entries:
      - { chain: osmosis-1, port: transfer, channel: channel-490, destination_chain: acre_9052-1 }
  - type: update_client
    entries:
      - { host_chain: osmosis-1, client: 07-tendermint-2316, destination_chain: acre_9052-1 }
```

## Running as a Cron Job

To automate IBC Refresh execution, add the following cron jobs to your server's crontab:

```cron
*/2 * * * * /bin/bash -c "/home/relayer/.venv/bin/python -m ibc_refresh -c /home/relayer/scripts/ibc_refresh/config.yaml -t clear_packets  >> /home/relayer/.logs/cron/cron_clearing.log 2>&1"
0 */2 * * * /bin/bash -c "/home/relayer/.venv/bin/python -m ibc_refresh -c /home/relayer/scripts/ibc_refresh/config.yaml -t update_client  >> /home/relayer/.logs/cron/cron_update.log 2>&1"
```

These tasks:
- Run `clear_packets` every 2 minutes.
- Run `update_client` every 2 hours.
- Redirect output and errors to respective log files for monitoring.

## Notifications

IBC Refresh supports notifications via Discord and Slack for task results.

- **Discord Alerts:**
  - Webhook-based notifications
  - Embed messages with execution details
  
- **Slack Alerts:**
  - Message blocks with command execution summary

## Logs

Logs are stored in the directory specified in `config.yaml`.

- **Task Logs:** Recorded in `task_execution.log`.
- **Command Logs:** Logs executed commands.
- **Notification Logs:** Records sent notifications.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Internal tag: 001