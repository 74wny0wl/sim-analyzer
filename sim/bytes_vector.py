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


def mirror(byte):
    mirrored_byte = ((byte & 0x0F) << 4) | ((byte & 0xF0) >> 4)
    return mirrored_byte


def read_vector(bulk_data):
    for byte in bulk_data:
        yield mirror(byte)


def decode_vector(bulk_data):
    decoded_vector = ["{:02x}".format(mirrored_byte) for mirrored_byte in read_vector(bulk_data)]
    return decoded_vector


def decode_vector_as_sim_string(bulk_data):
    sim_string = ''.join(decode_vector(bulk_data))
    return sim_string.rstrip('f')
