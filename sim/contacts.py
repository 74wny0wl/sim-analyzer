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


from sim import directory


class Contact:
    contact_name: str
    phone_number: str

    @staticmethod
    def empty():
        return Contact("", "")

    def __init__(self, contact_name, phone_number):
        self.contact_name = contact_name
        self.phone_number = phone_number

    def __str__(self):
        return self.to_string()

    def __unicode__(self):
        return self.to_string()

    def to_string(self):
        return f'{self.contact_name}::{self.phone_number}'


class ContactNameFactory:
    @staticmethod
    def create_contact_name(contact_name_entry) -> str:
        contact_name = contact_name_entry.replace(b'\xff', b'').decode('utf-8')
        return contact_name


class PhoneNumberFactory:
    @staticmethod
    def create_phone_number(phone_number_entry: bytes) -> str:
        phone_number = ""
        if phone_number_entry[0] == 0xa1:
            phone_number += '*'
            phone_number_entry = phone_number_entry[1::]
        if phone_number_entry[0] == 0x81:
            phone_number += "+"
            phone_number_entry = phone_number_entry[1::]

        for phone_number_entry_part in phone_number_entry:
            phone_number_element = ((phone_number_entry_part & 0x0F) << 4) | ((phone_number_entry_part & 0xF0) >> 4)
            phone_number_element = "{:02x}".format(phone_number_element)
            phone_number += phone_number_element
        if phone_number[-1] == 'f':
            phone_number = phone_number[:-1]
        return phone_number


class ContactFactory:
    contact_name_factory: ContactNameFactory
    phone_number_factory: PhoneNumberFactory

    def __init__(self, contact_name_factory, phone_number_factory):
        self.contact_name_factory = contact_name_factory
        self.phone_number_factory = phone_number_factory

    def create_contact(self, contact_bulk_data) -> Contact:
        contact_name = self.contact_name_factory.create_contact_name(contact_bulk_data[:16])

        phone_number_entry_size = contact_bulk_data[16]
        phone_number_entry = contact_bulk_data[17:17 + phone_number_entry_size]

        phone_number = self.phone_number_factory.create_phone_number(phone_number_entry)

        contact = Contact(contact_name=contact_name, phone_number=phone_number)
        return contact


def dump(sim_dump_directory_path: str, contacts_file_name="6F3A"):
    contacts_file_path = directory.find_file(sim_dump_directory_path, contacts_file_name)
    with open(contacts_file_path, 'rb') as contacts_file:
        contacts_file_content = contacts_file.read()

    contact_name_factory = ContactNameFactory()
    phone_number_factory = PhoneNumberFactory()
    contact_factory = ContactFactory(contact_name_factory, phone_number_factory)

    while contacts_file_content.count(b'\xff') != len(contacts_file_content):
        contact_bulk_data = contacts_file_content[:30]

        contact = contact_factory.create_contact(contact_bulk_data)

        contacts_file_content = contacts_file_content[30::]

        yield contact
