from typing import OrderedDict

from .AbstractMessage import AbstractMessage
from .FieldsSchema import FieldsSchema
from .Field import Field


class MO_Message(AbstractMessage):
    @classmethod
    def get_schema(cls):
        """ Get schema of message """
        return FieldsSchema(OrderedDict(
            protocol_version=Field(1, cls.PROTOCOL_REVISION_NUMBER),
            overage_message_length=Field(2),
            header_id=Field(1),
            header_length=Field(2),
            cdr_reference=Field(4),
            imei=Field(15),
            session_status=Field(1),
            MOSMSN=Field(2),
            MTMSN=Field(2),
            time_of_session=Field(4),
            location_info_iei=Field(1),
            location_info_length=Field(2),
            lat_long=Field(7),
            CEP_radius=Field(4),
            payload_iei=Field(1),
            payload_length=Field(2),
            payload=Field(),
        ))
