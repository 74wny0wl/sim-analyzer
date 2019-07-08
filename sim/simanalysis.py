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


import logging
import traceback

from sim import directory, argparsers, actions


def main():
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparsers.create_args_parser()
    script_args = arg_parser.parse_args()
    logging.log(level=logging.DEBUG, msg=str(script_args))

    dir_error = directory.is_valid(script_args.root)
    if dir_error is not None:
        logging.log(level=logging.ERROR, msg=dir_error.msg)
        exit(dir_error.code)

    try:
        actions.select(script_args).go().print_results()

    except AttributeError as e:
        print(e)
        traceback.print_exc()
        arg_parser.print_usage()


if __name__ == "__main__":
    main()
