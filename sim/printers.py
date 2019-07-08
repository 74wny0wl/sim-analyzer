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


import csv
import json
import sys
from collections import Iterable


class JSONObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        result = obj.__dict__
        result['__type__'] = obj.__class__.__name__
        return result


def print_default(data):
    if isinstance(data, str) or not isinstance(data, Iterable):
        print(data)
    else:
        for entry in data:
            print(entry)


def print_json(data):
    output = json.dumps(data, indent=4, sort_keys=True, cls=JSONObjectEncoder)
    print(output)


def print_csv(class_name, data):
    json_object_encoder = JSONObjectEncoder()
    empty = getattr(class_name, 'empty')()
    contact_header = json_object_encoder.default(empty)

    writer = csv.DictWriter(
        f=sys.stdout,
        fieldnames=contact_header.keys(),
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        lineterminator='\n')

    writer.writeheader()

    for entry in data:
        row = json_object_encoder.default(entry)
        writer.writerow(row)
