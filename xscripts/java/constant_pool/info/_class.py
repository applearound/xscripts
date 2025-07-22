from .constant_pool_info import ConstantPoolInfo


class ClassConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.name_index_segment = self.info_segment
        self.name_index: int = self.parse_int(self.info_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index})"
