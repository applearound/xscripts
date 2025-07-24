from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable

from .attribute_info import AttributeInfo


class BootstrapMethodsAttributeInfo(AttributeInfo):
    """ Represents a bootstrap methods attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.23
    """

    @dataclass(frozen=True)
    class BootstrapMethod:
        """ Represents a single bootstrap method in the BootstrapMethods attribute.
        """
        bootstrap_method_ref: int = field(init=True)
        num_bootstrap_arguments: int = field(init=True)
        bootstrap_arguments: tuple[int, ...] = field(init=True)

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_bootstrap_methods(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def bootstrap_methods(self) -> Iterable[BootstrapMethod]:
        """ Parses the bootstrap methods from the raw bytes.
        """
        offset = 8
        for i in range(self.number_of_bootstrap_methods):
            offset += i * 4
            bootstrap_method_ref = self.parse_int(self.raw[offset:offset + 2])
            num_bootstrap_arguments = self.parse_int(self.raw[offset + 2:offset + 4])
            bootstrap_arguments = tuple(
                self.parse_int(self.raw[offset + 4 + j * 2:offset + 6 + j * 2]) for j in range(num_bootstrap_arguments)
            )
            yield self.BootstrapMethod(bootstrap_method_ref, num_bootstrap_arguments, bootstrap_arguments)

    def __repr__(self) -> str:
        return f"BootstrapMethodsAttributeInfo(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_bootstrap_methods={self.number_of_bootstrap_methods}), bootstrap_methods={self.bootstrap_methods})"
