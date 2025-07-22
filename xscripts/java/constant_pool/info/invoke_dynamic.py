from .constant_pool_info import ConstantPoolInfo


class InvokeDynamicConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.bootstrap_method_attr_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.bootstrap_method_attr_index: int = self.parse_int(self.bootstrap_method_attr_index_segment)
        self.name_and_type_index: int = self.parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"
