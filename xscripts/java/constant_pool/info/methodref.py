from .constant_pool_info import ConstantPoolInfo


class MethodrefConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = self.parse_int(self.class_index_segment)
        self.name_and_type_index: int = self.parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"
