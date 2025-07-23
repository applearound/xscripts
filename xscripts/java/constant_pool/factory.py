from io import BytesIO

from .enums import ConstantPoolInfoTags
from .pool import ConstantPool
from .info import *


class ConstantPoolFactory:
    """ Factory class for creating instances of ConstantPoolInfo.
    """

    @staticmethod
    def sizeof(tag: ConstantPoolInfoTags) -> int:
        """ Returns the size of the constant pool entry based on its tag.

        Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4

        The size is determined by the type of constant pool entry:
        - INTEGER and FLOAT: 5 bytes
        - LONG and DOUBLE: 9 bytes
        - CLASS, METHOD_TYPE, STRING, MODULE, PACKAGE: 3 bytes
        - FIELDREF, NAME_AND_TYPE, METHODREF, INTERFACE_METHODREF: 5 bytes
        - METHOD_HANDLE: 4 bytes
        - UTF8: 0 bytes (the size is variable and depends on the length of the UTF-8 string)
        - All other tags: -1 (indicating an unknown or unsupported tag)

        Returns:
            int: The size of the constant pool entry in bytes.
        """
        if tag in (ConstantPoolInfoTags.INTEGER, ConstantPoolInfoTags.FLOAT):
            return 5
        elif tag in (ConstantPoolInfoTags.LONG, ConstantPoolInfoTags.DOUBLE):
            return 9
        elif tag in (ConstantPoolInfoTags.CLASS, ConstantPoolInfoTags.METHOD_TYPE, ConstantPoolInfoTags.STRING,
                     ConstantPoolInfoTags.MODULE, ConstantPoolInfoTags.PACKAGE):
            return 3
        elif tag in (ConstantPoolInfoTags.FIELDREF, ConstantPoolInfoTags.NAME_AND_TYPE, ConstantPoolInfoTags.METHODREF,
                     ConstantPoolInfoTags.INVOKE_DYNAMIC, ConstantPoolInfoTags.INVOKE_DYNAMIC,
                     ConstantPoolInfoTags.INTERFACE_METHODREF):
            return 5
        elif tag is ConstantPoolInfoTags.METHOD_HANDLE:
            return 4
        elif tag is ConstantPoolInfoTags.UTF8:
            return 0
        else:
            return -1

    @staticmethod
    def make_constant_pool_info(tag_value: int, constant_pool_info_segment: bytes) -> ConstantPoolInfo:
        """ Create a ConstantPool instance from a list of ConstantPoolInfo.
        """
        if tag_value == ConstantPoolInfoTags.CLASS:
            return ClassConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.FIELDREF:
            return FieldrefConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.METHODREF:
            return MethodrefConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.INTERFACE_METHODREF:
            return InterfaceMethodrefConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.STRING:
            return StringConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.INTEGER:
            return IntegerConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.FLOAT:
            return FloatConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.LONG:
            return LongConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.DOUBLE:
            return DoubleConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.NAME_AND_TYPE:
            return NameAndTypeConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.METHOD_HANDLE:
            return MethodHandleConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.METHOD_TYPE:
            return MethodTypeConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.DYNAMIC:
            return DynamicConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.INVOKE_DYNAMIC:
            return InvokeDynamicConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.MODULE:
            return ModuleConstantPoolInfo(constant_pool_info_segment)
        elif tag_value == ConstantPoolInfoTags.PACKAGE:
            return PackageConstantPoolInfo(constant_pool_info_segment)
        else:
            raise ValueError(f"Unsupported constant pool tag: {tag_value}")

    @classmethod
    def make_constant_pool(cls, constant_pool_segment: bytes) -> ConstantPool:
        constant_pool = []

        with BytesIO(constant_pool_segment) as segment_io:
            while True:
                tag_segment = segment_io.read(1)

                if not tag_segment:
                    break

                tag = ConstantPoolInfoTags(ConstantPoolInfo.parse_int(tag_segment))

                if tag is ConstantPoolInfoTags.UTF8:
                    # For UTF8, we need to read the length first
                    utf8_length_segment = segment_io.read(2)
                    utf8_length = ConstantPoolInfo.parse_int(utf8_length_segment)
                    utf8_segment = segment_io.read(utf8_length)

                    pool_info = Utf8ConstantPoolInfo(tag_segment + utf8_length_segment + utf8_segment)
                else:
                    info_segment = segment_io.read(cls.sizeof(tag) - 1)

                    pool_info = cls.make_constant_pool_info(tag.value, tag_segment + info_segment)

                constant_pool.append(pool_info)

        return ConstantPool(constant_pool)
