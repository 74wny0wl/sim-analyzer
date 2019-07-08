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


import sim
from sim import directory, bytes_vector


def get_iccid(sim_dump_directory_path: str, iccid_file_name='2FE2') -> str:
    iccid_file_path = directory.find_file(sim_dump_directory_path, file_name=iccid_file_name)
    with open(iccid_file_path, 'rb') as iccid_file:
        iccid_bulk_data = iccid_file.read()

    _iccid = ""
    for i in range(10):
        iccid_byte = "{:02x}".format(sim.bytes_vector.mirror(iccid_bulk_data[i]))
        _iccid += iccid_byte

    return _iccid
