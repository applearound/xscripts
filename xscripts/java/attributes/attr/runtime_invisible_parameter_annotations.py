from functools import cached_property

from .attribute_info import AttributeInfo


class RuntimeInvisibleParameterAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible parameter annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.19

    RuntimeInvisibleParameterAnnotations_attribute {
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

    @cached_property
    def number_of_parameters(self) -> int:
        return self.number_of_parameters

    @cached_property
    def parameter_annotations(self) -> bytes:
        return self.parameter_annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_parameters={self.number_of_parameters})"
