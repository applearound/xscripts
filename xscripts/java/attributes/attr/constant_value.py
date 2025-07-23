from .attribute_info import AttributeInfo


class ConstantValueAttributeInfo(AttributeInfo):
    """ Represents a constant value attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.2

    ConstantValue_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 constantvalue_index;
    }
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int,
                 constantvalue_index: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.constantvalue_index: int = constantvalue_index

    def get_constant_value_index(self) -> int:
        return self.constantvalue_index

    def __repr__(self) -> str:
        return f"ConstantValueAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"constant_value_index={self.constantvalue_index})"
