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


import json

from sim import iccidprovider, contacts, messages, printers
from sim.contacts import Contact
from sim.directory import tree
from sim.messages import Message
from sim.output_formats import OUTPUT_FORMAT_CSV, OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_JSON


class JSONObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        result = obj.__dict__
        result['__type__'] = obj.__class__.__name__
        return result


class Action:
    ITEM_CLASS = None
    SUPPORTED_OUTPUT_FORMATS = []

    def __init__(self, root_path, output_format):
        self.root_path = root_path
        self.output_format = output_format
        self.results = None

    def go(self):
        pass

    def print_results(self):
        if self.output_format not in self.SUPPORTED_OUTPUT_FORMATS:
            self.__non_supported_output_format()
            return

        if self.output_format == OUTPUT_FORMAT_DEFAULT:
            printers.print_default(self.results)
        elif self.output_format == OUTPUT_FORMAT_CSV:
            printers.print_csv(self.ITEM_CLASS, self.results)
        elif self.output_format == OUTPUT_FORMAT_JSON:
            printers.print_json(self.results)
        else:
            self.__non_supported_output_format()
            return

    def __non_supported_output_format(self):
        print(r'Selected output ({}) is not supported'.format(self.output_format))


class TreeAction(Action):
    ITEM_CLASS = None
    SUPPORTED_OUTPUT_FORMATS = [OUTPUT_FORMAT_DEFAULT]

    def go(self) -> Action:
        self.results = tree(self.root_path, ' ', list_files=True)
        return self


class ICCIDAction(Action):
    ITEM_CLASS = None
    SUPPORTED_OUTPUT_FORMATS = [OUTPUT_FORMAT_DEFAULT]

    def go(self) -> Action:
        self.results = iccidprovider.get_iccid(self.root_path)
        return self


class ContactsAction(Action):
    ITEM_CLASS = Contact
    SUPPORTED_OUTPUT_FORMATS = [OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_CSV, OUTPUT_FORMAT_JSON]

    def go(self) -> Action:
        self.results = list(contacts.dump(self.root_path))
        return self


class MessagesAction(Action):
    ITEM_CLASS = Message
    SUPPORTED_OUTPUT_FORMATS = [OUTPUT_FORMAT_DEFAULT, OUTPUT_FORMAT_CSV, OUTPUT_FORMAT_JSON]

    def go(self) -> Action:
        self.results = list(messages.dump(self.root_path))
        return self


def select(script_args) -> Action:
    if script_args.tree:
        return TreeAction(script_args.root, script_args.output)
    elif script_args.iccid:
        return ICCIDAction(script_args.root, script_args.output)
    elif script_args.contacts:
        return ContactsAction(script_args.root, script_args.output)
    elif script_args.messages:
        return MessagesAction(script_args.root, script_args.output)
