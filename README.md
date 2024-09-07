# IBC Refresh

This tool automates tasks for IBC relayers, such as clearing packets and updating clients between blockchain networks. It's designed to simplify the management of IBC relayer functions through a command-line interface.

## Features

- **Automated Task Execution**: Automate the execution of tasks like `clear_packets` and `update_client` based on configurations specified in a YAML file.
- **Configurable**: Easily configurable to handle different chains and tasks using a YAML file.
- **Logging**: Detailed logging of task execution results, helping in troubleshooting and monitoring the operations.

## Prerequisites

- Python 3.8 or newer.
- PyYAML for YAML file processing.
- Access to command line or terminal.

## Installation

This application can be packaged and installed from source. Here are the steps to package the application and install it:

### Packaging the Application

1. **Clone the repository**:
   ```bash
   git clone https://your-repository-url/ibc_refresh.git
   cd ibc_refresh
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```
   This command creates a distribution package in the `dist` directory.

3. **Install the package**:
   ```bash
   python -m pip install dist/ibc_refresh-0.1.0-py3-none-any.whl
   ```
   Replace the filename with the actual filename generated in the `dist` directory.

### Installing on a New System

To install this application on a new system, ensure Python 3.8+ is installed, then follow the packaging instructions above or use pip to install directly from a hosted package on PyPI (if available):

```bash
pip install ibc_refresh
```

## Usage

Once installed, you can run the application using the command line. Here’s how to execute tasks:

```bash
ibc_refresh --config path/to/your/config.yaml --task clear_packets
```

### Configuration

Edit the `config.yaml` file to specify the tasks and parameters for your IBC operations. Example configuration details might include:

```yaml
log_directory: .logs/
task_log_file: task_execution.log
command_log_file: executed_commands.log
hermes_path: /home/relayer/.local/bin/hermes

tasks:
  - type: clear_packets
    entries:
      - { chain: archway-1, port: transfer, channel: channel-147, destination_chain: beezee-1 }
      - { chain: beezee-1, port: transfer, channel: channel-2, destination_chain: archway-1 }
      - { chain: beezee-1, port: transfer, channel: channel-0, destination_chain: osmosis-1 }
      - { chain: osmosis-1, port: transfer, channel: channel-340, destination_chain: beezee-1 }

  - type: update_client
    entries:
      - { host_chain: archway-1, client: 07-tendermint-114, destination_chain: beezee-1 }
      - { host_chain: beezee-1, client: 07-tendermint-2, destination_chain: osmosis-1 }
      - { host_chain: beezee-1, client: 07-tendermint-8, destination_chain: archway-1 }
      - { host_chain: osmosis-1, client: 07-tendermint-2154, destination_chain: beezee-1 }
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your suggested changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
