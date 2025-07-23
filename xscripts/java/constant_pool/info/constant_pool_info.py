from abc import ABCMeta


class ConstantPoolInfo(metaclass=ABCMeta):
    @staticmethod
    def parse_int(segment: bytes) -> int:
        """ Parse an integer from a byte segment.
        """
        return int.from_bytes(segment, byteorder='big', signed=False)

    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        self.tag_segment: bytes = tag_segment
        self.info_segment: bytes = info_segment

        self.tag: int = self.parse_int(tag_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag})"
