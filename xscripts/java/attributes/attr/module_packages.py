from .attribute_info import AttributeInfo


class ModulePackagesAttributeInfo(AttributeInfo):
    """ Represents a module packages attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.26
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.number_of_packages: int = self.parse_int(self.__raw[6:8])
        self.packages: bytes = self.__raw[8:]

    def get_number_of_packages(self) -> int:
        return self.number_of_packages

    def get_packages(self) -> bytes:
        return self.packages

    def __repr__(self) -> str:
        return f"ModulePackagesAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_packages={self.number_of_packages})"
