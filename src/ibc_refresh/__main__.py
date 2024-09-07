from ibc_refresh.cli import command_line_parser
from ibc_refresh.config import load_config
from ibc_refresh.logger import initialize_loggers
from ibc_refresh.executor import process_tasks


def main():
    cmdargs = command_line_parser()
    config = load_config(cmdargs.config)
    initialize_loggers(config)
    process_tasks(cmdargs, config)


if __name__ == '__main__':
    main()