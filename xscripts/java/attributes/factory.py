import logging
from io import BytesIO

from .attr import *
from .enums import AttributesTypes
from ..constant_pool import ConstantPool

logger = logging.getLogger(__name__)


class AttributeFactory:
    """ Factory class for creating attribute instances.
    """

    def __init__(self, constant_pool: ConstantPool):
        self.constant_pool = constant_pool

    def make_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Dump bytes into a tuple of Attribute objects.
        """
        attributes = []

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

                if attribute_name == AttributesTypes.CONSTANT_VALUE:
                    attribute = ConstantValueAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.CODE:
                    attribute = CodeAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.STACK_MAP_TABLE:
                    attribute = StackMapTableAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.EXCEPTIONS:
                    attribute = ExceptionsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.INNER_CLASSES:
                    attribute = InnerClassesAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SYNTHETIC:
                    attribute = SyntheticAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SIGNATURE:
                    attribute = SignatureAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SOURCE_FILE:
                    attribute = SourceFileAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SOURCE_DEBUG_EXTENSION:
                    attribute = SourceDebugExtensionAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.LINE_NUMBER_TABLE:
                    attribute = LineNumberTableAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.LOCAL_VARIABLE_TABLE:
                    attribute = LocalVariableTableAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.LOCAL_VARIABLE_TYPE_TABLE:
                    attribute = LocalVariableTypeTableAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.DEPRECATED:
                    attribute = DeprecatedAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                    attribute = RuntimeVisibleAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                    attribute = RuntimeInvisibleAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_PARAMETER_ANNOTATIONS:
                    attribute = RuntimeVisibleParameterAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_PARAMETER_ANNOTATIONS:
                    attribute = RuntimeInvisibleParameterAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                    attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS:
                    attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.ANNOTATION_DEFAULT:
                    attribute = AnnotationDefaultAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.BOOTSTRAP_METHODS:
                    attribute = BootstrapMethodsAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.METHOD_PARAMETERS:
                    attribute = MethodParametersAttributeInfo(raw_attribute_bytes)
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
                else:
                    logger.warning(f"Unknown attribute type: {attribute_name}")

                attributes.append(attribute)

        return tuple(attributes)
