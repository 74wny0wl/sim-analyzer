import argparse

from sim.output_formats import OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_CSV


def create_args_parser() -> argparse.ArgumentParser:
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--root', nargs='?', default=r'.\\',
                             help='path to dump root (this directory should contain \'3F00\' directory')
    args_parser.add_argument('--tree', action='store_true', help='list contents of sim dump in a tree-like format')
    args_parser.add_argument('--iccid', action='store_true', help='reads ICCID number')
    args_parser.add_argument('--contacts', action='store_true', help='reads contacts')
    args_parser.add_argument('--messages', action='store_true', help='reads messages')
    args_parser.add_argument('--output', nargs='?', default=OUTPUT_FORMAT_DEFAULT,
                             help='select output [{}, {}, {}]'.format(OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_JSON,
                                                                      OUTPUT_FORMAT_CSV))
    return args_parser
