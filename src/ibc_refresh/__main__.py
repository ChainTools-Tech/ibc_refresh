from ibc_refresh.cli import command_line_parser


def main():
    cmdargs = command_line_parser()
    print(cmdargs.config)
    print(cmdargs.task)


if __name__ == '__main__':
    main()