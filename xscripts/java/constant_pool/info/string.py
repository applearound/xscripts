from .constant_pool_info import ConstantPoolInfo


class StringConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.string_index_segment = self.info_segment

        self.string_index: int = self.parse_int(self.string_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(string_index={self.string_index})"
