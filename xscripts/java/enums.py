from enum import IntEnum
from typing import ClassVar

from .constant_pool import *


class ConstantPoolInfoTag(IntEnum):
    CLASS = 7
    FIELD_REF = 9
    METHOD_REF = 10
    INTERFACE_METHOD_REF = 11
    STRING = 8
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    NAME_AND_TYPE = 12
    UTF8 = 1
    METHOD_HANDLE = 15
    METHOD_TYPE = 16
    INVOKE_DYNAMIC = 18
    MODULE = 19
    PACKAGE = 20

    def get_size(self) -> int:
        """Returns the size of the constant pool entry based on its tag.

        The size is determined by the type of constant pool entry:
        - INTEGER and FLOAT: 5 bytes
        - LONG and DOUBLE: 9 bytes
        - CLASS, STRING, NAME_AND_TYPE, MODULE, PACKAGE: 3 bytes
        - FIELD_REF, METHOD_REF, INTERFACE_METHOD_REF: 5 bytes
        - METHOD_HANDLE, METHOD_TYPE, INVOKE_DYNAMIC: 4 bytes
        - UTF8: 0 bytes (the size is variable and depends on the length of the UTF-8 string)
        - All other tags: -1 (indicating an unknown or unsupported tag)

        Returns:
            int: The size of the constant pool entry in bytes.
        """

        if self in (self.INTEGER, self.FLOAT):
            return 5
        elif self in (self.LONG, self.DOUBLE):
            return 9
        elif self in (self.CLASS, self.STRING, self.NAME_AND_TYPE, self.MODULE, self.PACKAGE):
            return 3
        elif self in (self.FIELD_REF, self.METHOD_REF, self.INTERFACE_METHOD_REF):
            return 5
        elif self in (self.METHOD_HANDLE, self.METHOD_TYPE, self.INVOKE_DYNAMIC):
            return 4
        elif self is self.UTF8:
            return 0
        else:
            return -1
