from .constant_pool_info import ConstantPoolInfo


class MethodTypeConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.descriptor_index_segment = self.info_segment

        self.descriptor_index: int = self.parse_int(self.descriptor_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(descriptor_index={self.descriptor_index})"
