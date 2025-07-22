from typing import Iterable, Iterator

from .info import *


class ConstantPool:
    def __init__(self, pool: Iterable[ConstantPoolInfo]) -> None:
        self.pool: dict[int, ConstantPoolInfo] = dict()

        index = 1
        for info in pool:
            self.pool[index] = info
            if isinstance(info, LongConstantPoolInfo) or isinstance(info, DoubleConstantPoolInfo):
                self.pool[index + 1] = info
                index += 2
            else:
                index += 1

    def __iter__(self) -> Iterator[ConstantPoolInfo]:
        """Iterate over the constant pool entries."""
        return iter(self.pool.values())

    def get(self, index: int) -> ConstantPoolInfo:
        """Get a constant pool entry by its index.
        Attention: The constant_pool table is indexed from 1 to constant_pool_count - 1.
        """
        if index < 1 or index > len(self.pool):
            raise IndexError(
                f"Constant pool index {index} out of range. Valid range is 1 to {len(self.pool)}.")
        return self.pool[index]

    def get_class_constant_pool_info(self, index: int) -> ClassConstantPoolInfo:
        """Get a ClassConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, ClassConstantPoolInfo):
            raise TypeError(f"Expected ClassConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_field_ref_constant_pool_info(self, index: int) -> FieldrefConstantPoolInfo:
        """Get a FieldRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, FieldrefConstantPoolInfo):
            raise TypeError(f"Expected FieldRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_ref_constant_pool_info(self, index: int) -> MethodrefConstantPoolInfo:
        """Get a MethodRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodrefConstantPoolInfo):
            raise TypeError(f"Expected MethodRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_interface_ref_constant_pool_info(self, index: int) -> InterfaceMethodrefConstantPoolInfo:
        """Get a InterfaceRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, InterfaceMethodrefConstantPoolInfo):
            raise TypeError(f"Expected InterfaceRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_string_constant_pool_info(self, index: int) -> StringConstantPoolInfo:
        """Get a StringConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, StringConstantPoolInfo):
            raise TypeError(f"Expected StringConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_integer_constant_pool_info(self, index: int) -> IntegerConstantPoolInfo:
        """Get a IntegerConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, IntegerConstantPoolInfo):
            raise TypeError(f"Expected IntegerConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_float_constant_pool_info(self, index: int) -> FloatConstantPoolInfo:
        """Get a FloatConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, FloatConstantPoolInfo):
            raise TypeError(f"Expected FloatConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_long_constant_pool_info(self, index: int) -> LongConstantPoolInfo:
        """Get a LongConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, LongConstantPoolInfo):
            raise TypeError(f"Expected LongConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_double_constant_pool_info(self, index: int) -> DoubleConstantPoolInfo:
        info = self.get(index)
        if not isinstance(info, DoubleConstantPoolInfo):
            raise TypeError(f"Expected DoubleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_name_and_type_constant_pool_info(self, index: int) -> NameAndTypeConstantPoolInfo:
        """Get a NameAndTypeConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, NameAndTypeConstantPoolInfo):
            raise TypeError(f"Expected NameAndTypeConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_utf8_constant_pool_info(self, index: int) -> Utf8ConstantPoolInfo:
        """Get a Utf8ConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, Utf8ConstantPoolInfo):
            raise TypeError(f"Expected Utf8ConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_handle_constant_pool_info(self, index: int) -> MethodHandleConstantPoolInfo:
        """Get a MethodHandleConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodHandleConstantPoolInfo):
            raise TypeError(f"Expected MethodHandleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_type_constant_pool_info(self, index: int) -> MethodTypeConstantPoolInfo:
        """Get a MethodTypeConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodTypeConstantPoolInfo):
            raise TypeError(f"Expected MethodTypeConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_dynamic_constant_pool_info(self, index: int) -> DynamicConstantPoolInfo:
        """Get a DynamicConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, DynamicConstantPoolInfo):
            raise TypeError(f"Expected DynamicConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_invoke_dynamic_constant_pool_info(self, index: int) -> InvokeDynamicConstantPoolInfo:
        """Get a InvokeDynamicConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, InvokeDynamicConstantPoolInfo):
            raise TypeError(f"Expected InvokeDynamicConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_package_constant_pool_info(self, index: int) -> PackageConstantPoolInfo:
        """Get a PackageConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, PackageConstantPoolInfo):
            raise TypeError(f"Expected PackageConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_module_constant_pool_info(self, index: int) -> ModuleConstantPoolInfo:
        """Get a ModuleConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, ModuleConstantPoolInfo):
            raise TypeError(f"Expected ModuleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info
