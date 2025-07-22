from .constant_pool_info import ConstantPoolInfo


class Utf8ConstantPoolInfo(ConstantPoolInfo):
    """ Represents a UTF-8 constant pool entry in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.7
    """

    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.length_segment = self.info_segment[:2]
        self.bytes_segment = self.info_segment[2:]

        self.length: int = self.parse_int(self.length_segment)
        self.string: str = self.bytes_segment.decode('UTF-8')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(length={self.length}, string='{self.string}')"
