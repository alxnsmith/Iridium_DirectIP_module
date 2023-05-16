from enum import Enum


class Field:
    """ Field of data in message """
    length: int or None
    target_length: str or list[str] or None
    expected: bytes or None
    prefix: bytes or None

    class InvalidFieldException(Exception):
        pass

    class Type(Enum):
        """ Field types """
        BYTES = 1
        LENGTH = 2

    def __init__(self,
                 length: int or None = None,
                 expected: bytes or None = None,
                 prefix: bytes or None = None,
                 target_length: str or list[str] or None = None,
                 field_type: Type = Type.BYTES):
        self.length = length
        self.target_length = target_length
        self.expected = expected
        self.prefix = prefix
        self.type = field_type

    def get_value(self, data: bytes) -> bytes:
        """ Get value of field from data """
        value = data[:self.length]
        if self.expected is not None and data != value:
            raise ValueError(f"Expected {self.expected}, got {value}")
        return value

    def make_value(self, value: int or str or bytes) -> bytes:
        bytes_value = b''
        if self.expected is not None:
            bytes_value = self.expected
        elif isinstance(value, bytes):
            bytes_value = value
        elif isinstance(value, str):
            bytes_value = value.encode()
            if self.prefix is not None and not bytes_value.startswith(self.prefix):
                bytes_value = self.prefix + bytes_value
        elif isinstance(value, int):
            if not isinstance(self.length, int):
                raise ValueError(
                    f"Length of field is not int, but {self.length}")
            bytes_value = value.to_bytes(self.length, 'big')

        if isinstance(self.length, int) and len(bytes_value) != self.length:
            raise ValueError(
                f"Value length is not match. Length must be {self.length}, got {len(bytes_value)}")

        return bytes_value
