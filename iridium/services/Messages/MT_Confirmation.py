from typing import OrderedDict

from .AbstractMessage import AbstractMessage
from .FieldsSchema import FieldsSchema
from .Field import Field


class MT_Confirmation(AbstractMessage):
    HEADER_ID = b'\x44'

    @classmethod
    def get_schema(cls):
        """ Get schema of message """
        return FieldsSchema(OrderedDict(
            protocol_version=Field(1, cls.PROTOCOL_REVISION_NUMBER),
            overall_message_length=Field(2, target_length=[
                'header_id',
                'header_length',
                'client_id',
                'imei',
                'flags',
                'message_id',
                'message_length',
                'message_data'],
                field_type=Field.Type.LENGTH),

            header_id=Field(1, cls.HEADER_ID),
            receipt_length=Field(
                2, target_length=['client_id', 'imei', 'flags'], field_type=Field.Type.LENGTH),
            message_uid=Field(4),
            imei=Field(15),
            message_id=Field(4),
            status=Field(2),
        ))
