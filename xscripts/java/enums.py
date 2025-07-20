from enum import IntEnum
from typing import ClassVar

from .constant_pool import *


class ConstantPoolInfoTag(IntEnum):
    CLASS = 7
    FIELDREF = 9
    METHODREF = 10
    INTERFACE_METHODREF = 11
    STRING = 8
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    NAME_AND_TYPE = 12
    UTF8 = 1
    METHOD_HANDLE = 15
    METHOD_TYPE = 16
    DYNAMIC = 17
    INVOKE_DYNAMIC = 18
    MODULE = 19
    PACKAGE = 20

    def get_size(self) -> int:
        """Returns the size of the constant pool entry based on its tag.

        The size is determined by the type of constant pool entry:
        - INTEGER and FLOAT: 5 bytes
        - LONG and DOUBLE: 9 bytes
        - CLASS, METHOD_TYPE, STRING, MODULE, PACKAGE: 3 bytes
        - FIELDREF, NAME_AND_TYPE, METHODREF, INTERFACE_METHODREF: 5 bytes
        - METHOD_HANDLE: 4 bytes
        - UTF8: 0 bytes (the size is variable and depends on the length of the UTF-8 string)
        - All other tags: -1 (indicating an unknown or unsupported tag)

        Returns:
            int: The size of the constant pool entry in bytes.
        """

        if self in (self.INTEGER, self.FLOAT):
            return 5
        elif self in (self.LONG, self.DOUBLE):
            return 9
        elif self in (self.CLASS, self.METHOD_TYPE, self.STRING, self.MODULE, self.PACKAGE):
            return 3
        elif self in (self.FIELDREF, self.NAME_AND_TYPE, self.METHODREF, self.INVOKE_DYNAMIC, self.INVOKE_DYNAMIC,
                      self.INTERFACE_METHODREF):
            return 5
        elif self is self.METHOD_HANDLE:
            return 4
        elif self is self.UTF8:
            return 0
        else:
            return -1
