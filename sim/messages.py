import binascii
import math
from datetime import datetime

from sim import directory, binary, bytes_vector


class MessagePDU:
    deleted: bool
    smsc_information_length: int
    smsc_address_type: hex
    service_center_number: str
    first_octet_of_sms_deliver_msg: int
    sender_number_length: int
    sender_number_type: hex
    sender_number: str
    tp_protocol_identifier: hex
    tp_data_coding_scheme: hex
    tp_sc_time_stamp: datetime
    user_data_length: hex
    user_data: bytearray


class Message:
    deleted: bool
    smsc_address_type: hex
    service_center_number: str
    sender_number_type: hex
    sender_number: str
    tp_protocol_identifier: hex
    tp_data_coding_scheme: hex
    tp_sc_time_stamp: datetime
    user_data: str
    bulk_data: str

    @staticmethod
    def empty():
        return Message(False, 0x0, "", 0x0, "", 0x0, 0x0, datetime.now(), "", "")

    def __init__(self,
                 deleted: bool,
                 smsc_address_type: hex,
                 service_center_number: str,
                 sender_number_type: hex,
                 sender_number: str,
                 tp_protocol_identifier: hex,
                 tp_data_coding_scheme: hex,
                 tp_sc_time_stamp: datetime,
                 user_data: str,
                 bulk_data: str):
        self.deleted = deleted
        self.smsc_address_type = smsc_address_type
        self.service_center_number = service_center_number
        self.sender_number_type = sender_number_type
        self.sender_number = sender_number
        self.tp_protocol_identifier = tp_protocol_identifier
        self.tp_data_coding_scheme = tp_data_coding_scheme
        self.tp_sc_time_stamp = tp_sc_time_stamp
        self.user_data = user_data
        self.bulk_data = bulk_data

    def __str__(self):
        return self.to_string()

    def __unicode__(self):
        return self.to_string()

    def to_string(self):
        return self.user_data


class MessagePDUFactory:
    @staticmethod
    def create_message_pdu(message_bulk_data: bytes) -> MessagePDU:
        MESSAGE_DELETED_OFFSET = 0
        MESSAGE_SMSC_INFORMATION_LENGTH_OFFSET = 1
        MESSAGE_SMSC_ADDRESS_TYPE_OFFSET = 2
        MESSAGE_SERVICE_CENTER_NUMBER_OFFSET = 3

        message = MessagePDU()
        message.deleted = message_bulk_data[MESSAGE_DELETED_OFFSET] == 0
        message.smsc_information_length = message_bulk_data[MESSAGE_SMSC_INFORMATION_LENGTH_OFFSET]

        MESSAGE_FIRST_OCTET_OF_SMS_DELIVER_MSG_OFFSET \
            = MESSAGE_SERVICE_CENTER_NUMBER_OFFSET + message.smsc_information_length - 1
        MESSAGE_SENDER_NUMBER_LENGTH_OFFSET = MESSAGE_FIRST_OCTET_OF_SMS_DELIVER_MSG_OFFSET + 1
        MESSAGE_SENDER_NUMBER_TYPE_OFFSET = MESSAGE_SENDER_NUMBER_LENGTH_OFFSET + 1

        message.smsc_address_type = message_bulk_data[MESSAGE_SMSC_ADDRESS_TYPE_OFFSET]
        message.service_center_number = bytes_vector.decode_vector_as_sim_string(
            message_bulk_data[MESSAGE_SERVICE_CENTER_NUMBER_OFFSET:MESSAGE_FIRST_OCTET_OF_SMS_DELIVER_MSG_OFFSET])

        message.first_octet_of_sms_deliver_msg = message_bulk_data[MESSAGE_FIRST_OCTET_OF_SMS_DELIVER_MSG_OFFSET]
        message.sender_number_length = message_bulk_data[MESSAGE_SENDER_NUMBER_LENGTH_OFFSET]

        MESSAGE_SENDER_NUMBER_LENGTH = math.ceil(message.sender_number_length / 2)
        MESSAGE_SENDER_NUMBER_OFFSET = MESSAGE_SENDER_NUMBER_TYPE_OFFSET + 1
        MESSAGE_TP_PROTOCOL_IDENTIFIER_OFFSET = MESSAGE_SENDER_NUMBER_OFFSET + MESSAGE_SENDER_NUMBER_LENGTH
        MESSAGE_TP_DATA_CODING_SCHEME_OFFSET = MESSAGE_TP_PROTOCOL_IDENTIFIER_OFFSET + 1
        MESSAGE_TP_SERVICE_CENTER_TIME_STAMP_OFFSET = MESSAGE_TP_DATA_CODING_SCHEME_OFFSET + 1
        MESSAGE_TP_USER_DATA_LENGTH_OFFSET = MESSAGE_TP_SERVICE_CENTER_TIME_STAMP_OFFSET + 7
        MESSAGE_USER_DATA_OFFSET = MESSAGE_TP_USER_DATA_LENGTH_OFFSET + 1

        message.sender_number_type = message_bulk_data[MESSAGE_SENDER_NUMBER_TYPE_OFFSET]

        message.sender_number = bytes_vector.decode_vector_as_sim_string(
            message_bulk_data[MESSAGE_SENDER_NUMBER_OFFSET:MESSAGE_TP_PROTOCOL_IDENTIFIER_OFFSET])

        message.tp_protocol_identifier = message_bulk_data[MESSAGE_TP_PROTOCOL_IDENTIFIER_OFFSET]

        message.tp_data_coding_scheme = message_bulk_data[MESSAGE_TP_DATA_CODING_SCHEME_OFFSET]
        message.tp_sc_time_stamp = bytes_vector.decode_vector_as_sim_string(
            message_bulk_data[MESSAGE_TP_SERVICE_CENTER_TIME_STAMP_OFFSET: MESSAGE_TP_USER_DATA_LENGTH_OFFSET])
        # TODO correct timestamp calculation
        # message.tp_sc_time_stamp = datetime.strptime(message.tp_sc_time_stamp, "%y%m%d%H%M%S")
        message.user_data_length = message_bulk_data[MESSAGE_TP_USER_DATA_LENGTH_OFFSET]

        message.user_data = message_bulk_data[
                            MESSAGE_USER_DATA_OFFSET:MESSAGE_USER_DATA_OFFSET + message.user_data_length]
        return message


class MessageReader:
    def __init__(self):
        self.SEPTET_SELECTOR_INIT = 0x7F
        self.RESIDUUM_SELECTOR_INIT = 0x80
        self.residuum = 0
        self.septet_selector = self.SEPTET_SELECTOR_INIT
        self.residuum_selector = self.RESIDUUM_SELECTOR_INIT

    def reset_masks_state(self):
        self.residuum = 0
        self.septet_selector = self.SEPTET_SELECTOR_INIT
        self.residuum_selector = self.RESIDUUM_SELECTOR_INIT

    def next_masks_state(self, octet_letter):
        self.residuum = (octet_letter & self.residuum_selector) >> binary.count_zeros(self.residuum_selector)
        self.septet_selector = self.septet_selector >> 1
        self.residuum_selector = (self.residuum_selector >> 1) + self.RESIDUUM_SELECTOR_INIT

    def get_message(self, message_pdu: MessagePDU) -> str:
        decoded_string = ""
        self.reset_masks_state()
        for octet_letter in list(filter(None, message_pdu.user_data.split(b'\xff')))[0]:
            left_shifter = binary.count_zeros(self.septet_selector) - 1
            septet_letter = ((octet_letter & self.septet_selector) << left_shifter) + self.residuum
            decoded_string += chr(septet_letter)

            self.next_masks_state(octet_letter)

            if self.septet_selector == 0:
                decoded_string += chr(self.residuum)
                self.reset_masks_state()
        return decoded_string


class MessageConverter:
    __message_reader = MessageReader()
    __message_pdu_factory = MessagePDUFactory()

    def convert_bulk_data_to_message(self, message_bulk_data: bytes) -> Message:
        message_pdu = self.__message_pdu_factory.create_message_pdu(message_bulk_data)
        message = Message(
            deleted=message_pdu.deleted,
            smsc_address_type=message_pdu.smsc_address_type,
            service_center_number=message_pdu.service_center_number,
            sender_number_type=message_pdu.sender_number_type,
            sender_number=message_pdu.sender_number,
            tp_protocol_identifier=message_pdu.tp_protocol_identifier,
            tp_data_coding_scheme=message_pdu.tp_data_coding_scheme,
            tp_sc_time_stamp=message_pdu.tp_sc_time_stamp,
            user_data=self.__message_reader.get_message(message_pdu),
            bulk_data=binascii.hexlify(message_bulk_data).decode()
        )
        return message


def dump_bulk_data(sim_dump_directory_path: str, messages_file_name="6F3C"):
    messages_file_path = directory.find_file(sim_dump_directory_path, messages_file_name)
    with open(messages_file_path, 'rb') as messages_file:
        messages_bulk_data = messages_file.read()

    MESSAGE_BULK_DATA_LEN = 176
    messages_count = math.floor(len(messages_bulk_data) / MESSAGE_BULK_DATA_LEN)
    splitted_messages_bulk_data = [
        messages_bulk_data[MESSAGE_BULK_DATA_LEN * i:MESSAGE_BULK_DATA_LEN * i + MESSAGE_BULK_DATA_LEN]
        for i in range(0, messages_count)]

    return splitted_messages_bulk_data


def dump_pdu(sim_dump_directory_path: str, messages_file_name="6F3C"):
    message_pdu_factory = MessagePDUFactory()
    for message_bulk_data in dump_bulk_data(sim_dump_directory_path, messages_file_name):
        yield message_pdu_factory.create_message_pdu(message_bulk_data)


def dump(sim_dump_directory_path: str, messages_file_name="6F3C"):
    message_converter = MessageConverter()
    for message_bulk_data in dump_bulk_data(sim_dump_directory_path, messages_file_name):
        yield message_converter.convert_bulk_data_to_message(message_bulk_data)
