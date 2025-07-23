from .attribute_info import AttributeInfo


class RuntimeInvisibleParameterAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible parameter annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.19
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.number_of_parameters: int = self.parse_int(self.__raw[6:8])
        self.parameter_annotations: bytes = self.__raw[8:]

    def get_number_of_parameters(self) -> int:
        return self.number_of_parameters

    def get_parameter_annotations(self) -> bytes:
        return self.parameter_annotations

    def __repr__(self) -> str:
        return f"RuntimeInvisibleParameterAnnotationsAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_parameters={self.number_of_parameters})"
