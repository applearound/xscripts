from .attributeinfo import AttributeInfo


class SignatureAttributeInfo(AttributeInfo):
    """ Represents a signature attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.9
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.signature_index: int = int.from_bytes(self.raw[6:8], 'big')

    def get_signature_index(self) -> int:
        return self.signature_index

    def __repr__(self) -> str:
        return f"SignatureAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"signature_index={self.signature_index})"
