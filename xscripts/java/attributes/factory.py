import logging
from io import BytesIO
from typing import Generator, Callable

from .attr import *
from .enums import AttributesTypes
from ..constant_pool import ConstantPool

logger = logging.getLogger(__name__)


class AttributeFactory:
    """ Factory class for creating attribute instances.
    """

    def __init__(self, constant_pool: ConstantPool):
        self.constant_pool = constant_pool

    def __load_attributes(self, count: int, raw_bytes: bytes, factory_fn: Callable[[str, bytes], AttributeInfo]) -> \
            Generator[
                AttributeInfo]:
        with BytesIO(raw_bytes) as reader:
            for _ in range(count):
                attribute_name_index_segment = reader.read(2)
                attribute_name_index = AttributeInfo.parse_int(attribute_name_index_segment)

                utf8_info = self.constant_pool.get_utf8_constant_pool_info(attribute_name_index)
                attribute_name = utf8_info.string

                attribute_length_segment = reader.read(4)
                attribute_length = AttributeInfo.parse_int(attribute_length_segment)

                logger.debug(
                    f"Processing attribute: %s(index: %s, length: %s)", attribute_name,
                    attribute_name_index, attribute_length)

                raw_attribute_bytes = attribute_name_index_segment + attribute_length_segment + reader.read(
                    attribute_length)

                yield factory_fn(attribute_name, raw_attribute_bytes)

    def load_class_file_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Load class file attributes from raw bytes.

        Args:
            count (int): Number of attributes.
            raw_bytes (bytes): Raw bytes containing the attributes.
        Returns:
            tuple[AttributeInfo, ...]: Tuple of AttributeInfo objects.
        """

        def factory_fn(attribute_name: str, raw_attribute_bytes: bytes) -> AttributeInfo:
            """ See: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7-320

            SourceFile 	                                                    ClassFile                                                           45.3
            InnerClasses 	                                                ClassFile 	                                                        45.3
            EnclosingMethod 	                                            ClassFile 	                                                        49.0
            SourceDebugExtension 	                                        ClassFile 	                                                        49.0
            BootstrapMethods 	                                            ClassFile 	                                                        51.0
            Module, ModulePackages, ModuleMainClass                         ClassFile 	                                                        53.0
            NestHost, NestMembers                                           ClassFile 	                                                        55.0
            Record                                                          ClassFile 	                                                        60.0
            PermittedSubclasses                                             ClassFile 	                                                        61.0
            Synthetic 	                                                    ClassFile, field_info, method_info                              	45.3
            Deprecated 	                                                    ClassFile, field_info, method_info 	                                45.3
            Signature 	                                                    ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleAnnotations, RuntimeInvisibleAnnotations          ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleTypeAnnotations, RuntimeInvisibleTypeAnnotations 	ClassFile, field_info, method_info, Code, record_component_info     52.0
            """
            if attribute_name == AttributesTypes.SOURCE_FILE:
                attribute = SourceFileAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.INNER_CLASSES:
                attribute = InnerClassesAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.ENCLOSING_METHOD:
                attribute = EnclosingMethodAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SOURCE_DEBUG_EXTENSION:
                attribute = SourceDebugExtensionAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.BOOTSTRAP_METHODS:
                attribute = BootstrapMethodsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.MODULE:
                attribute = ModuleAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.MODULE_PACKAGES:
                attribute = ModulePackagesAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.MODULE_MAIN_CLASS:
                attribute = ModuleMainClassAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.NEST_HOST:
                attribute = NestHostAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.NEST_MEMBERS:
                attribute = NestMembersAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RECORD:
                attribute = RecordAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.PERMITTED_SUBCLASSES:
                attribute = PermittedSubclassesAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SYNTHETIC:
                attribute = SyntheticAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.DEPRECATED:
                attribute = DeprecatedAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SIGNATURE:
                attribute = SignatureAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                attribute = RuntimeVisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                attribute = RuntimeInvisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            else:
                logger.error(f"Unsupported attribute type: {attribute_name}")
                raise ValueError(f"Unsupported attribute type: {attribute_name}")

            return attribute

        return tuple(self.__load_attributes(count, raw_bytes, factory_fn))

    def load_field_info_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Load field attributes from raw bytes.

        Args:
            count (int): Number of attributes.
            raw_bytes (bytes): Raw bytes containing the attributes.

        Returns:
            tuple[AttributeInfo, ...]: Tuple of AttributeInfo objects.
        """

        def factory_fn(attribute_name: str, raw_attribute_bytes: bytes) -> AttributeInfo:
            """ See: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7-320

            ConstantValue 	                                                field_info                                                 	        45.3
            Synthetic 	                                                    ClassFile, field_info, method_info 	                                45.3
            Deprecated 	                                                    ClassFile, field_info, method_info 	                                45.3
            Signature 	                                                    ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleAnnotations, RuntimeInvisibleAnnotations 	        ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleTypeAnnotations, RuntimeInvisibleTypeAnnotations 	ClassFile, field_info, method_info, Code, record_component_info     52.0
            """
            if attribute_name == AttributesTypes.CONSTANT_VALUE:
                attribute = ConstantValueAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SYNTHETIC:
                attribute = SyntheticAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.DEPRECATED:
                attribute = DeprecatedAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SIGNATURE:
                attribute = SignatureAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                attribute = RuntimeVisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                attribute = RuntimeInvisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            else:
                raise ValueError(f"Unsupported attribute type: {attribute_name}")

            return attribute

        return tuple(self.__load_attributes(count, raw_bytes, factory_fn))

    def load_method_info_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Load method attributes from raw bytes.

        Args:
            count (int): Number of attributes.
            raw_bytes (bytes): Raw bytes containing the attributes.
        Returns:
            tuple[AttributeInfo, ...]: Tuple of AttributeInfo objects.
        """

        def factory_fn(attribute_name: str, raw_attribute_bytes: bytes) -> AttributeInfo:
            """ See: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7-320

            Code                                                                        method_info                                                         45.3
            Exceptions                                                                  method_info                                                         45.3
            RuntimeVisibleParameterAnnotations, RuntimeInvisibleParameterAnnotations    method_info                                                         49.0
            AnnotationDefault                                                           method_info                                                         49.0
            MethodParameters                                                            method_info                                                         52.0
            Synthetic                                                                   ClassFile, field_info, method_info                                  45.3
            Deprecated                                                                  ClassFile, field_info, method_info                                  45.3
            Signature                                                                   ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleAnnotations, RuntimeInvisibleAnnotations                      ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleTypeAnnotations, RuntimeInvisibleTypeAnnotations              ClassFile, field_info, method_info, Code, record_component_info     52.0
            """

            if attribute_name == AttributesTypes.CODE:
                attribute = CodeAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.EXCEPTIONS:
                attribute = ExceptionsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_PARAMETER_ANNOTATIONS:
                attribute = RuntimeVisibleParameterAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_PARAMETER_ANNOTATIONS:
                attribute = RuntimeInvisibleParameterAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.ANNOTATION_DEFAULT:
                attribute = AnnotationDefaultAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.METHOD_PARAMETERS:
                attribute = MethodParametersAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SYNTHETIC:
                attribute = SyntheticAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.DEPRECATED:
                attribute = DeprecatedAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.SIGNATURE:
                attribute = SignatureAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                attribute = RuntimeVisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                attribute = RuntimeInvisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            else:
                raise ValueError(f"Unsupported method info attribute type: {attribute_name}")

            return attribute

        return tuple(self.__load_attributes(count, raw_bytes, factory_fn))

    def load_code_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Load code attributes from raw bytes.

        Args:
            count (int): Number of attributes.
            raw_bytes (bytes): Raw bytes containing the attributes.
        Returns:
            tuple[AttributeInfo, ...]: Tuple of AttributeInfo objects.
        """

        def factory_fn(attribute_name: str, raw_attribute_bytes: bytes) -> AttributeInfo:
            """ See: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7-320

            LineNumberTable 	                                            Code 	                                                            45.3
            LocalVariableTable 	                                            Code 	                                                            45.3
            LocalVariableTypeTable 	                                        Code 	                                                            49.0
            StackMapTable 	                                                Code 	                                                            50.0
            RuntimeVisibleTypeAnnotations, RuntimeInvisibleTypeAnnotations 	ClassFile, field_info, method_info, Code, record_component_info     52.0
	        """

            if attribute_name == AttributesTypes.LINE_NUMBER_TABLE:
                attribute = LineNumberTableAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.LOCAL_VARIABLE_TABLE:
                attribute = LocalVariableTableAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.LOCAL_VARIABLE_TYPE_TABLE:
                attribute = LocalVariableTypeTableAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.STACK_MAP_TABLE:
                attribute = StackMapTableAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            else:
                raise ValueError(f"Unsupported code attribute type: {attribute_name}")

            return attribute

        return tuple(self.__load_attributes(count, raw_bytes, factory_fn))

    def load_record_component_info_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Load record component attributes from raw bytes.

        Args:
            count (int): Number of attributes.
            raw_bytes (bytes): Raw bytes containing the attributes.
        Returns:
            tuple[AttributeInfo, ...]: Tuple of AttributeInfo objects.
        """

        def factory_fn(attribute_name: str, raw_attribute_bytes: bytes) -> AttributeInfo:
            """ See: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7-320

            Signature                                                           ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleAnnotations, RuntimeInvisibleAnnotations              ClassFile, field_info, method_info, record_component_info           49.0
            RuntimeVisibleTypeAnnotations, RuntimeInvisibleTypeAnnotations 	    ClassFile, field_info, method_info, Code, record_component_info     52.0
            """

            if attribute_name == AttributesTypes.SIGNATURE:
                attribute = SignatureAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                attribute = RuntimeVisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                attribute = RuntimeInvisibleAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
            else:
                raise ValueError(f"Unsupported record component info attribute type: {attribute_name}")

            return attribute

        return tuple(self.__load_attributes(count, raw_bytes, factory_fn))
