# IBC Refresh

## Overview

**IBC Refresh** is an automation tool for IBC relayers, designed to simplify the management of inter-blockchain communication tasks. It supports packet clearance, client updates, and client expiration tracking while integrating structured logging and notifications (Discord/Slack) for monitoring task execution.

## Features

- **Automated IBC Operations**: Supports `clear_packets`, `update_client`, and `client_expiration` tasks based on a configuration file.
- **Failure Tracking**: Implements automatic failure counting and retries with threshold-based notifications.
- **Client Expiration Monitoring**: Detects and alerts about expiring IBC clients before they become invalid.
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
- `client_expiration`: Checks and alerts about upcoming client expirations.

Example:
```bash
ibc_refresh --config config.yaml --task update_client client_expiration
```

## Configuration

The `config.yaml` file contains settings for logging, failure tracking, notification methods, and task definitions.

### Example Configuration:
```yaml
log_directory: .logs/
task_log_file: task_execution.log
command_log_file: executed_commands.log
notification_log_file: notifications.log
failure_tracker_log_file: failure_tracker.json
hermes_path: /home/relayer/.local/bin/hermes

notifications:
  - type: discord
    webhook: "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
  - type: slack
    webhook: "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"

tasks:
  - type: clear_packets
    failure_threshold: 2
    entries:
      - { chain: osmosis-1, port: transfer, channel: channel-490, destination_chain: acre_9052-1 }
  - type: update_client
    failure_threshold: 2
    entries:
      - { host_chain: osmosis-1, client: 07-tendermint-2316, destination_chain: acre_9052-1 }
  - type: client_expiration
    entries:
      - { src_chain: osmosis-1, client: 07-tendermint-2154, dst_chain: beezee-1, avg_block_time: 6 }

endpoints:
  api:
    - { chain_id: osmosis-1, endpoint_url: "https://lcd.osmosis.zone" }
  rpc:
    - { chain_id: osmosis-1, endpoint_url: "https://rpc.osmosis.zone" }
```

## Running as a Cron Job

To automate IBC Refresh execution, add the following cron jobs to your server's crontab:

```cron
*/2 * * * * /bin/bash -c "/home/relayer/.venv/bin/python -m ibc_refresh -c /home/relayer/scripts/ibc_refresh/config.yaml -t clear_packets  >> /home/relayer/.logs/cron/cron_clearing.log 2>&1"
0 */2 * * * /bin/bash -c "/home/relayer/.venv/bin/python -m ibc_refresh -c /home/relayer/scripts/ibc_refresh/config.yaml -t update_client  >> /home/relayer/.logs/cron/cron_update.log 2>&1"
0 0 * * * /bin/bash -c "/home/relayer/.venv/bin/python -m ibc_refresh -c /home/relayer/scripts/ibc_refresh/config.yaml -t client_expiration  >> /home/relayer/.logs/cron/cron_expiration.log 2>&1"
```

## Failure Notification

IBC Refresh tracks task failures and notifies the user when a failure threshold is reached. The notification system supports:

- **Discord Alerts:** Webhook-based notifications with error details.
- **Slack Alerts:** Message blocks summarizing execution failures.

## Logs

Logs are stored in the directory specified in `config.yaml`.

- **Task Logs:** Recorded in `task_execution.log`.
- **Command Logs:** Logs executed commands.
- **Notification Logs:** Records sent notifications.
- **Failure Tracker Logs:** Maintains failure counts and resets upon successful execution.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

