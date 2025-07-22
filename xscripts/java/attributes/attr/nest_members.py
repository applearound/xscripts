from .attribute import Attribute


class NestMembersAttribute(Attribute):
    """ Represents a nest members attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.29
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.nest_member_count: int = self.parse_int(self.raw[6:8])
        self.nest_members: bytes = self.raw[8:]

    def get_nest_member_count(self) -> int:
        return self.nest_member_count

    def get_nest_members(self) -> bytes:
        return self.nest_members

    def __repr__(self) -> str:
        return f"NestMembersAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"nest_member_count={self.nest_member_count})"
