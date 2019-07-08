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
