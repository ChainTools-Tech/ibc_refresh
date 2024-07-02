# IBC Relayer Automation Script

This Python script automates tasks related to the Inter-Blockchain Communication (IBC) protocol, such as clearing packets and updating clients across different blockchain networks. The script dynamically handles tasks based on a user-defined configuration and logs operations with enhanced traceability.

## Features

- **Dynamic Configuration**: Manage task configurations through a YAML file.
- **Enhanced Logging**: Log files include detailed identifiers, such as chain, channel, and destination chain, for better traceability.
- **Error Handling**: Gracefully handles and logs errors, such as missing chain configurations.
- **Selective Execution**: Ability to execute specified tasks selectively based on command-line input.

## Prerequisites

- Python 3.x installed.
- `yaml` library for Python.
- Access to Hermes binary for IBC operations.

## Configuration

Create a `config.yaml` file in the same directory as the script. Here is a template:

```yaml
log_directory: /path/to/your/logs
task_log_path: /path/to/your/task_execution.log
command_log_path: /path/to/your/executed_commands.log
hermes_path: /path/to/your/hermes

tasks:
  - type: clear_packets
    entries:
      - chain: chain-name
        port: transfer
        channel: channel-id
        destination_chain: destination-chain-name
  - type: update_client
    entries:
      - host_chain: host-chain-name
        client: client-id
        destination_chain: destination-chain-name
```

Replace placeholders with actual data corresponding to your blockchain configurations.
Installation
- Ensure Python and the necessary packages are installed.
- Place the script and the `config.yaml` in the same directory.
- Modify `config.yaml` to reflect your specific IBC setup and paths.

## Usage

Run the script from your command line:

```bash
python3 ibc_relayer_script.py
```

To execute specific tasks, pass the task type as an argument:

```bash
python3 ibc_relayer_script.py clear_packets
python3 ibc_relayer_script.py update_client
```

## Logs
- Task Execution Logs: Logged to the path specified in `task_log_path`.
- Command Execution Logs: Detailed command execution logs are stored at the path specified in `command_log_path`.
- Each run overwrites the previous logs to ensure only the most recent data is kept.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests if you have improvements or bug fixes.


## License

This project is open-source and available under the MIT License.
