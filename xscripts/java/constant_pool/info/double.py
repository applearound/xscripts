from .constant_pool_info import ConstantPoolInfo

from struct import unpack


class DoubleConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: float = unpack('>d', self.high_bytes_segment + self.low_bytes_segment)[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
