from functools import cached_property
from typing import Iterable

from .attributes import AttributeInfo
from .enums import MethodAccessFlags
from .utils import parse_int


class Method:
    """ Represents a Java class method.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.6

    method_info {
        u2             access_flags;
        u2             name_index;
        u2             descriptor_index;
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    @cached_property
    def access_flags(self) -> int:
        return parse_int(self.raw[0:2])

    @cached_property
    def name_index(self) -> int:
        return parse_int(self.raw[2:4])

    @cached_property
    def descriptor_index(self) -> int:
        return parse_int(self.raw[4:6])

    @cached_property
    def attributes_count(self) -> int:
        return parse_int(self.raw[6:8])

    @cached_property
    def attributes(self) -> tuple[AttributeInfo, ...]:
        ...

    def method_access_flags(self) -> tuple[MethodAccessFlags, ...]:
        return MethodAccessFlags.parse_flags(self.access_flags)

    def is_public(self) -> bool:
        return MethodAccessFlags.is_public(self.access_flags)

    def is_private(self) -> bool:
        return MethodAccessFlags.is_private(self.access_flags)

    def is_protected(self) -> bool:
        return MethodAccessFlags.is_protected(self.access_flags)

    def is_static(self) -> bool:
        return MethodAccessFlags.is_static(self.access_flags)

    def is_final(self) -> bool:
        return MethodAccessFlags.is_final(self.access_flags)

    def is_synchronized(self) -> bool:
        return MethodAccessFlags.is_synchronized(self.access_flags)

    def is_bridge(self) -> bool:
        return MethodAccessFlags.is_bridge(self.access_flags)

    def is_varargs(self) -> bool:
        return MethodAccessFlags.is_varargs(self.access_flags)

    def is_native(self) -> bool:
        return MethodAccessFlags.is_native(self.access_flags)

    def is_abstract(self) -> bool:
        return MethodAccessFlags.is_abstract(self.access_flags)

    def is_strict(self) -> bool:
        return MethodAccessFlags.is_strict(self.access_flags)

    def is_synthetic(self) -> bool:
        return MethodAccessFlags.is_synthetic(self.access_flags)

    def __repr__(self) -> str:
        return f"Method(access_flags={self.access_flags}, name_index={self.name_index}, " \
               f"descriptor_index={self.descriptor_index}, attributes_count={self.attributes_count})"


def load_methods(count: int, raw_bytes: bytes, constant_pool) -> Iterable[Method]:
    """Dump bytes into a tuple of Method objects."""
    ...
