from dataclasses import dataclass
from functools import cached_property
from io import BytesIO

from .attribute_info import AttributeInfo


@dataclass(frozen=True)
class BootstrapMethod:
    """ Represents a single bootstrap method in the BootstrapMethods attribute.
    """
    bootstrap_method_ref: int
    num_bootstrap_arguments: int
    bootstrap_arguments: tuple[int, ...]


class BootstrapMethodsAttributeInfo(AttributeInfo):
    """ Represents a bootstrap methods attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.23

    BootstrapMethods_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 num_bootstrap_methods;
        {   u2 bootstrap_method_ref;
            u2 num_bootstrap_arguments;
            u2 bootstrap_arguments[num_bootstrap_arguments];
        } bootstrap_methods[num_bootstrap_methods];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_bootstrap_methods(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def bootstrap_methods(self) -> tuple[BootstrapMethod, ...]:
        """ Parses the bootstrap methods from the raw bytes.
        """
        start = 8
        methods = []
        for _ in range(self.number_of_bootstrap_methods):
            method = self.__parse_bootstrap_method(start)
            methods.append(method)
            start += 4 + method.num_bootstrap_arguments * 2
        return tuple(methods)

    def __parse_bootstrap_method(self, start: int) -> BootstrapMethod:
        """ Helper method to parse a single bootstrap method.
        """
        with BytesIO(self.raw[start:]) as stream:
            bootstrap_method_ref = self.parse_int(stream.read(2))
            num_bootstrap_arguments = self.parse_int(stream.read(2))
            bootstrap_arguments = tuple(
                self.parse_int(stream.read(2)) for _ in range(num_bootstrap_arguments)
            )

            return BootstrapMethod(
                bootstrap_method_ref, num_bootstrap_arguments, bootstrap_arguments
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_bootstrap_methods={self.number_of_bootstrap_methods}), bootstrap_methods={self.bootstrap_methods})"
