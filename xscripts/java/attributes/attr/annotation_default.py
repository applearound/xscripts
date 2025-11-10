from functools import cached_property

from ._annotations import AnnotationBase


class AnnotationDefaultAttributeInfo(AnnotationBase):
    """ Represents an annotation default attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.22

    AnnotationDefault_attribute {
        u2            attribute_name_index;
        u4            attribute_length;
        element_value default_value;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def default_value(self) -> "AnnotationBase.ElementValue":
        """ Parses the default value of the annotation.

        Returns:
            ElementValue: The parsed default value.
        """
        return self._parse_element_value(6)[1]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}), " \
               f"default_value={self.default_value})"
