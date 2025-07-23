from .attribute_info import AttributeInfo


class ModuleAttributeInfo(AttributeInfo):
    """ Represents a module attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.25
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.module_name_index: int = self.parse_int(self.__raw[6:8])
        self.module_flags: int = self.parse_int(self.__raw[8:10])
        self.module_version_index: int = self.parse_int(self.__raw[10:12])
        self.number_of_exports: int = self.parse_int(self.__raw[12:14])
        self.exports: bytes = self.__raw[14:]

    def get_module_name_index(self) -> int:
        return self.module_name_index

    def get_module_flags(self) -> int:
        return self.module_flags

    def get_module_version_index(self) -> int:
        return self.module_version_index

    def get_number_of_exports(self) -> int:
        return self.number_of_exports

    def get_exports(self) -> bytes:
        return self.exports

    def __repr__(self) -> str:
        return (f"ModuleAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, "
                f"module_name_index={self.module_name_index}, module_flags={self.module_flags}, "
                f"module_version_index={self.module_version_index}, number_of_exports={self.number_of_exports})")
