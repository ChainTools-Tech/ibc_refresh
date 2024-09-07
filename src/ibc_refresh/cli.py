import argparse


def command_line_parser():
    parser = argparse.ArgumentParser(prog='ibc_refresh',
                                     prefix_chars='-',
                                     description='IBC Refresh helps to process IBC Relayer tasks.',
                                     epilog='...and Relayer is happy!')
    parser.add_argument('-c', '--config',
                        type=str,
                        required=True,
                        action='store',
                        dest='config',
                        help='Path to the configuration file.')
    parser.add_argument('-t', '--task',
                        type=str,
                        nargs='*',
                        required=True,
                        action='store',
                        dest='task',
                        choices=['clear_packets', 'update_client'],
                        help='List of tasks to execute (e.g., clear_packets, update_client)')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='1.0')
    return parser.parse_args()
