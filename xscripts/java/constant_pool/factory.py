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
    def make_constant_pool_info(tag_segment: bytes, info_segment: bytes) -> ConstantPoolInfo:
        """ Create a ConstantPoolInfo instance based on the tag.
        """
        tag = ConstantPoolInfoTags(ConstantPoolInfo.parse_int(tag_segment))

        if tag is ConstantPoolInfoTags.CLASS:
            return ClassConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.FIELDREF:
            return FieldrefConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.METHODREF:
            return MethodrefConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.INTERFACE_METHODREF:
            return InterfaceMethodrefConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.STRING:
            return StringConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.INTEGER:
            return IntegerConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.FLOAT:
            return FloatConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.LONG:
            return LongConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.DOUBLE:
            return DoubleConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.NAME_AND_TYPE:
            return NameAndTypeConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.METHOD_HANDLE:
            return MethodHandleConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.METHOD_TYPE:
            return MethodTypeConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.DYNAMIC:
            return DynamicConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.INVOKE_DYNAMIC:
            return InvokeDynamicConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.MODULE:
            return ModuleConstantPoolInfo(tag_segment, info_segment)
        elif tag is ConstantPoolInfoTags.PACKAGE:
            return PackageConstantPoolInfo(tag_segment, info_segment)
        else:
            raise ValueError(f"Unknown size constant pool tag: {tag}")

    @staticmethod
    def make_constant_pool(constant_pool_segment: bytes) -> ConstantPool:
        constant_pool = []

        with BytesIO(constant_pool_segment) as segment_io:
            processing = True

            while processing:
                tag_segment = segment_io.read(1)

                if not tag_segment:
                    processing = False
                    continue

                tag = ConstantPoolInfoTags(ConstantPoolInfo.parse_int(tag_segment))

                if tag is ConstantPoolInfoTags.UTF8:
                    # For UTF8, we need to read the length first
                    utf8_length_segment = segment_io.read(2)
                    utf8_length = ConstantPoolInfo.parse_int(utf8_length_segment)
                    info_segment = utf8_length_segment + segment_io.read(utf8_length)

                    constant_pool.append(Utf8ConstantPoolInfo(tag_segment, info_segment))
                else:
                    info_segment = segment_io.read(ConstantPoolFactory.sizeof(tag) - 1)

                    constant_pool.append(ConstantPoolFactory.make_constant_pool_info(tag_segment, info_segment))

        return ConstantPool(constant_pool)
