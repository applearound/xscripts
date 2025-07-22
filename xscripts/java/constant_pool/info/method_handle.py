from .constant_pool_info import ConstantPoolInfo


class MethodHandleConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.reference_kind_segment = self.info_segment[:1]
        self.reference_index_segment = self.info_segment[1:]

        self.reference_kind: int = self.parse_int(self.reference_kind_segment)
        self.reference_index: int = self.parse_int(self.reference_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(reference_kind={self.reference_kind}, reference_index={self.reference_index})"
