import logging


from ibc_refresh.cli import command_line_parser
from ibc_refresh.config import load_config


def main():
    cmdargs = command_line_parser()
    print(cmdargs.config)
    print(cmdargs.task)

    config = load_config(cmdargs.config)
    print(config)

    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()