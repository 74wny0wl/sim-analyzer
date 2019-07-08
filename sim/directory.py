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


import os

from sim.errors import LoggableError

ERROR_SIM_DUMP_DIRECTORY_NOT_EXISTS = 0x8001
ERROR_SIM_DUMP_DIRECTORY_IS_NOT_DIRECTORY = 0x8002


def tree(dir_root: str, padding: str, list_files=False):
    result = list()
    result.append(padding[:-1] + '+-' + os.path.basename(os.path.abspath(dir_root)) + '/')
    padding = padding + ' '
    if list_files:
        files = os.listdir(dir_root)
    else:
        files = [x for x in os.listdir(dir_root) if os.path.isdir(dir_root + os.sep + x)]
    files.sort()
    count = 0
    for file in files:
        count += 1
        path = dir_root + os.sep + file
        if os.path.isdir(path):
            if count == len(files):
                result.extend(tree(path, padding + ' ', list_files))
            else:
                result.extend(tree(path, padding + '|', list_files))
        else:
            result.append(padding + '+-' + file)
    return result


def find_file(search_root, file_name):
    for root, dirs, files in os.walk(search_root):
        for file in files:
            if file == file_name:
                return os.sep.join([root, file])


def is_valid(dir_path):
    if not os.path.exists(dir_path):
        return LoggableError(msg=f"{dir_path} doesn't exists", code=ERROR_SIM_DUMP_DIRECTORY_NOT_EXISTS)
    if not os.path.isdir(dir_path):
        return LoggableError(msg=f'{dir_path} is not a directory',
                             code=ERROR_SIM_DUMP_DIRECTORY_IS_NOT_DIRECTORY)
    return None
