from typing import OrderedDict

from .Field import Field
from .types import BytesDict


class FieldsSchema:
    """ Iterable schema of fields """
    fields: OrderedDict[str, Field]

    def __init__(self, fields: OrderedDict):
        self.fields = fields

    def __iter__(self):
        for field in self.fields.items():
            yield field

    def get_field(self, name: str) -> Field:
        """ Retrieve field by name """
        field = self.fields.get(name)
        if field is None:
            raise IndexError(f'Field with name {name} not found')
        return field

    def make_field_value(self, name: str, value: int or str or bytes) -> bytes:
        """ Makes bytes value for field """
        try:
            if not isinstance(value, bytes):
                bytes_value = self.get_field(name).make_value(value)
            else:
                bytes_value = value
        except Exception as e:
            err_text = f"Field {name} error: {e}"
            raise Field.InvalidFieldException(err_text)
        return bytes_value

    def make_message_data(self, data: BytesDict) -> bytes:
        """ Makes bytes data for message """
        if data is None:
            raise ValueError("Message data is empty")
        result = b''

        def get_field_length(field_name: str) -> int:
            field = self.get_field(field_name)
            if field.type == Field.Type.LENGTH:
                if field.length is None:
                    raise ValueError(f"Field {field_name} length is None")
                return field.length
            elif field.type == Field.Type.BYTES and isinstance(field.length, int):
                return field.length
            return len(data[field_name])

        def get_length_field_value(field: Field) -> int:
            length = 0
            if isinstance(field.target_length, str):
                length = get_field_length(field.target_length)
            elif isinstance(field.target_length, list):
                for target_field_name in field.target_length:
                    length += get_field_length(target_field_name)
            else:
                raise ValueError(
                    f"Length field {field} has invalid target length")
            return length

        for field_name, field in self:
            if field.expected is not None:
                result += field.expected
                continue
            if field.type == Field.Type.LENGTH:
                if not isinstance(field.target_length, (str, list)):
                    raise ValueError(
                        f"Length field {field_name} must be string or list of strings, got {type(field.target_length)}")
                raw_value = get_length_field_value(field)
            else:
                raw_value = data.get(field_name)

            if raw_value is None:
                raise ValueError(f"Field {field_name} is not found in data")

            value = self.make_field_value(field_name, raw_value)

            if value is None:
                raise ValueError(f"Field {field_name} is empty")
            result += value
        return result
