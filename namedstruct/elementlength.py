"""NamedStruct element class."""

import struct
import re

from namedstruct.element import Element
from namedstruct.modes import Mode


class ElementLength(Element):
    """
    The length NamedStruct element class.
    """

    def __init__(self, field, mode=Mode.Native):
        """Initialize a NamedStruct element object."""

        # All of the type checks have already been performed by the class
        # factory
        self.name = field[0]
        self.ref = field[2]

        # Validate that the format specifiers are valid struct formats, this
        # doesn't have to be done now because the format will be checked when
        # any struct functions are called, but it's better to inform the user of
        # any errors earlier.
        # The easiest way to perform this check is to create a "Struct" class
        # instance, this will also increase the efficiency of all struct related
        # functions called.
        self._mode = mode
        self.format = mode.value + field[1]
        self._struct = struct.Struct(self.format)

    @staticmethod
    def valid(field):
        """
        Validation function to determine if a field tuple represents a valid
        enum element type.

        The basics have already been validated by the Element factory class,
        validate that the struct format is a valid unsigned numeric value.
        """
        return len(field) == 3 \
            and isinstance(field[1], str) \
            and re.match(r'[BHILQ]', field[1]) \
            and isinstance(field[2], str) and len(field[2])

    def changemode(self, mode):
        """change the mode of the struct format"""
        self._mode = mode
        self.format = mode.value + self.format[1:]
        # recreate the struct with the new format
        self._struct = struct.Struct(self.format)

    def pack(self, msg):
        """Pack the provided values into the supplied buffer."""
        # When packing a length element, use the length of the referenced
        # element not the value of the current element in the supplied object.
        return self._struct.pack(len(msg[self.ref]))

    def unpack(self, msg, buf):
        """Unpack data from the supplied buffer using the initialized format."""
        ret = self._struct.unpack_from(buf, 0)
        unused = buf[struct.calcsize(self.format):]
        return (ret[0], unused)
