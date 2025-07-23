from .constant_pool_info import ConstantPoolInfo


class LongConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.high_bytes_segment: bytes = self.info_segment[:4]
        self.low_bytes_segment: bytes = self.info_segment[4:]

        self.value: int = (
                (self.parse_int(self.high_bytes_segment) << 32) | self.parse_int(self.low_bytes_segment)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
