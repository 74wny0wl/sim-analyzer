#  MIT License
#
#  Copyright (c) 2019 74wny0wl
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import argparse

from sim.output_formats import OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_CSV


def create_args_parser() -> argparse.ArgumentParser:
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--root', nargs='?', default=r'.\\',
                             help='path to dump root (this directory should contain \'3F00\' directory)')
    args_parser.add_argument('--tree', action='store_true', help='list contents of sim dump in a tree-like format')
    args_parser.add_argument('--iccid', action='store_true', help='read ICCID number')
    args_parser.add_argument('--contacts', action='store_true', help='read contacts')
    args_parser.add_argument('--messages', action='store_true', help='read messages')
    args_parser.add_argument('--output', nargs='?', default=OUTPUT_FORMAT_DEFAULT,
                             help='select output [{}, {}, {}]'.format(OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_JSON,
                                                                      OUTPUT_FORMAT_CSV))
    return args_parser
