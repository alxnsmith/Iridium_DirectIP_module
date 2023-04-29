from enum import Enum
from typing import OrderedDict

from .AbstractMessage import AbstractMessage
from .FieldsSchema import FieldsSchema
from .Field import Field


class MT_Message(AbstractMessage):
    """ MT message """
    HEADER_LENGTH = b'\x21'

    class HEADER_IDS(Enum):
        """ Header IDs """
        HEADER = b'\x41'
        PAYLOAD = b'\x42'
        CONFIRMATION = b'\x43'
        PRIORITY = b'\x46'

    class DISPOSITION_FLAGS(Enum):
        """ Disposition flags """
        FLUSH_MT_QUEUE = b'\x01'
        SEND_RING_ALERT = b'\x02'
        UPDATE_SSD_LOCATION = b'\x08'
        HIGH_PRIORITY_MESSAGE = b'\x16'
        ASSIGN_MTMSN = b'\x32'

    @classmethod
    def get_schema(cls):
        """ Get schema of message """
        return FieldsSchema(OrderedDict(
            protocol_version=Field(1, cls.PROTOCOL_REVISION_NUMBER),
            overage_message_length=Field(2, target_length=[
                'header_id',
                'header_length',
                'client_id',
                'imei',
                'flags',
                'message_id',
                'message_length',
                'message_data'],
                field_type=Field.Type.LENGTH),
            header_id=Field(1, cls.HEADER_IDS.HEADER.value),
            header_length=Field(
                2, target_length=['client_id', 'imei', 'flags'], field_type=Field.Type.LENGTH),
            client_id=Field(4),
            imei=Field(15),
            flags=Field(2),
            message_id=Field(1, cls.HEADER_IDS.PAYLOAD.value),
            message_length=Field(
                2, target_length='message_data', field_type=Field.Type.LENGTH),
            message_data=Field(),
        ))

    @classmethod
    def create(cls, client_id: str, imei: str, flags: bytes, message_data: str):
        """ Create new MT_Message instance and return it """
        schema = cls.get_schema()
        data_values = {
            'protocol': schema.make_field_value('protocol', cls.PROTOCOL_REVISION_NUMBER),
            'client_id': schema.make_field_value('client_id', client_id),
            'imei': schema.make_field_value('imei', imei),
            'flags': schema.make_field_value('flags', flags),
            'message_data': schema.make_field_value('message_data', message_data),
        }

        return MT_Message(data_values)
