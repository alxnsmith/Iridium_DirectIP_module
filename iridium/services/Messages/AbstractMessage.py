from abc import abstractmethod
from enum import Enum

from .types import BytesDict


class AbstractMessage:
    """ Abstract message class """
    _data: bytes or None = None
    _data_parts: BytesDict or None = None
    PROTOCOL_REVISION_NUMBER = b'\x01'

    class RECEIPT:
        class HEADER_IDS(Enum):
            HEADER = b'\x44'

    def __init__(self, data: bytes or BytesDict):
        if isinstance(data, dict):
            self._data_parts = data
        else:
            self._data = data

    @abstractmethod
    def get_schema(self):
        """ Get schema of message """
        raise NotImplementedError

    def parse(self):  # TODO: move to schema
        """ Parse message """
        if isinstance(self._data_parts, dict):
            return self._data_parts
        if self._data is None:
            raise ValueError("Message data is empty")
        data = self._data
        parsed_data = {}
        schema = self.get_schema()
        for field_name, field in schema:
            length = field.length
            if isinstance(length, str):
                name_of_field_that_value_is_length = length
                length_bytes = parsed_data[name_of_field_that_value_is_length]
                length = int(length_bytes.hex(), 16)
            parsed = data[:length]
            parsed_data[field_name] = parsed
            data = data[length:]
        self._data_parts = parsed_data
        return parsed_data

    def make(self):
        schema = self.get_schema()
        data = schema.make_message_data(self._data_parts)
        return data
