from .attribute_info import AttributeInfo


class RuntimeVisibleParameterAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime visible parameter annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.18

    RuntimeVisibleParameterAnnotations_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u1 num_parameters;
        {   u2         num_annotations;
            annotation annotations[num_annotations];
        } parameter_annotations[num_parameters];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

        self.number_of_parameters: int = self.parse_int(self.__raw[6:8])
        self.parameter_annotations: bytes = self.__raw[8:]

    def get_number_of_parameters(self) -> int:
        return self.number_of_parameters

    def get_parameter_annotations(self) -> bytes:
        return self.parameter_annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_parameters={self.number_of_parameters})"
