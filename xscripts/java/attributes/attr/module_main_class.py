from .attribute_info import AttributeInfo


class ModuleMainClassAttributeInfo(AttributeInfo):
    """ Represents a module main class attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.27
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.main_class_index: int = self.parse_int(self.__raw[6:8])

    def get_main_class_index(self) -> int:
        return self.main_class_index

    def __repr__(self) -> str:
        return f"ModuleMainClassAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"main_class_index={self.main_class_index})"
