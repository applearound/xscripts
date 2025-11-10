from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from typing import Union, override

from .attribute_info import AttributeInfo


class ElementValueTag(IntEnum):
    """ Enum for element value tags. """
    BYTE = 66  # b'B'
    CHAR = 67  # b'C'
    DOUBLE = 68  # b'D'
    FLOAT = 70  # b'F'
    INT = 73  # b'I'
    LONG = 74  # b'J'
    SHORT = 83  # b'S'
    BOOLEAN = 90  # b'Z'
    STRING = 115  # b's'
    ENUM_CLASS = 101  # b'e'
    CLASS = 99  # b'c'
    ANNOTATION_INTERFACE = 64  # b'@'
    ARRAY_TYPE = 91  # b'['


@dataclass(frozen=True)
class EnumConstValue:
    type_name_index: int
    const_name_index: int


class ElementValue(metaclass=ABCMeta):
    @property
    def tag(self) -> int:
        return self.element_value_tag.value

    @property
    @abstractmethod
    def element_value_tag(self) -> ElementValueTag:
        pass

    @property
    @abstractmethod
    def value(self) -> Union[int, EnumConstValue, "Annotation", tuple["ElementValue", ...]]:
        pass


class ConstValueIndexElementValue(ElementValue):
    """ Represents a constant value element. """

    def __init__(self, tag: int, const_value_index: int) -> None:
        self.__tag = tag
        self.__const_value_index = const_value_index

    @override
    @property
    def element_value_tag(self) -> ElementValueTag:
        return ElementValueTag(self.__tag)

    @override
    @property
    def value(self) -> int:
        return self.__const_value_index


class EnumConstValueElementValue(ElementValue):
    """ Represents an enum constant value element. """

    def __init__(self, enum_const_value: EnumConstValue) -> None:
        self.__enum_const_value = enum_const_value

    @override
    @property
    def element_value_tag(self) -> ElementValueTag:
        return ElementValueTag.ENUM_CLASS

    @override
    @property
    def value(self) -> EnumConstValue:
        return self.__enum_const_value


class ClassInfoIndexElementValue(ElementValue):
    """ Represents a class info element. """

    def __init__(self, class_info_index: int) -> None:
        self.__class_info_index = class_info_index

    @override
    @property
    def element_value_tag(self) -> ElementValueTag:
        return ElementValueTag.CLASS

    @override
    @property
    def value(self) -> int:
        return self.__class_info_index


class AnnotationValueElementValue(ElementValue):
    """ Represents a nested annotation element. """

    def __init__(self, annotation: "Annotation") -> None:
        self.__annotation = annotation

    @override
    @property
    def element_value_tag(self) -> ElementValueTag:
        return ElementValueTag.ANNOTATION_INTERFACE

    @override
    @property
    def value(self) -> "Annotation":
        return self.__annotation


class ArrayValueElementValue(ElementValue):
    """ Represents an array element value. """

    def __init__(self, values: tuple[ElementValue, ...]) -> None:
        self.__values = values

    @override
    @property
    def element_value_tag(self) -> ElementValueTag:
        return ElementValueTag.ARRAY_TYPE

    @override
    @property
    def value(self) -> tuple[ElementValue, ...]:
        return self.__values


@dataclass(frozen=True)
class ElementValuePair:
    element_name_index: int
    value: ElementValue


@dataclass(frozen=True)
class Annotation:
    type_index: int
    num_element_value_pairs: int
    element_value_pairs: tuple[ElementValuePair, ...]


class AnnotationBase(metaclass=ABCMeta, AttributeInfo):
    """ Represents an annotation in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.16

    annotation {
        u2 type_index;
        u2 num_element_value_pairs;
        {   u2            element_name_index;
            element_value value;
        } element_value_pairs[num_element_value_pairs];
    }

    element_value {
        u1 tag;
        union {
            u2 const_value_index;

            {   u2 type_name_index;
                u2 const_name_index;
            } enum_const_value;

            u2 class_info_index;

            annotation annotation_value;

            {   u2            num_values;
                element_value values[num_values];
            } array_value;
        } value;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def _parse_annotation(self, start: int) -> tuple[int, Annotation]:
        """ Parse an annotation starting from the given byte index.

        annotation {
            u2 type_index;
            u2 num_element_value_pairs;
            {   u2            element_name_index;
                element_value value;
            } element_value_pairs[num_element_value_pairs];
        }

        Return:
            A tuple containing the size of the parsed annotation(in bytes) and the Annotation object.
        """
        current_pos = start

        # Parse type_index (u2)
        type_index = self.parse_int(self.raw[current_pos:current_pos + 2])
        current_pos += 2

        # Parse num_element_value_pairs (u2)
        num_element_value_pairs = self.parse_int(self.raw[current_pos:current_pos + 2])
        current_pos += 2

        # Parse element_value_pairs
        element_value_pairs = []
        for _ in range(num_element_value_pairs):
            # Parse element_name_index (u2)
            element_name_index = self.parse_int(self.raw[current_pos:current_pos + 2])
            current_pos += 2

            # Parse element value
            value_size, element_value = self._parse_element_value(current_pos)
            current_pos += value_size

            element_value_pairs.append(self.ElementValuePair(element_name_index, element_value))

        total_size = current_pos - start
        annotation = self.Annotation(type_index, num_element_value_pairs, tuple(element_value_pairs))

        return total_size, annotation

    def _parse_element_value(self, start: int) -> tuple[int, ElementValue]:
        """ Parse an element value starting from the given byte index.

        Return:
            A tuple containing the size of the parsed element value(in bytes) and the ElementValue object.
        """
        tag = self.raw[start]
        current_pos = start + 1

        if tag in [ElementValueTag.BYTE, ElementValueTag.CHAR, ElementValueTag.DOUBLE,
                   ElementValueTag.FLOAT, ElementValueTag.INT, ElementValueTag.LONG,
                   ElementValueTag.SHORT, ElementValueTag.BOOLEAN, ElementValueTag.STRING]:
            # Constant value: u2 const_value_index
            const_value_index = self.parse_int(self.raw[current_pos:current_pos + 2])
            return 3, self.ElementValue(tag, const_value_index)

        elif tag == ElementValueTag.ENUM_CLASS:
            # Enum constant: u2 type_name_index, u2 const_name_index
            type_name_index = self.parse_int(self.raw[current_pos:current_pos + 2])
            const_name_index = self.parse_int(self.raw[current_pos + 2:current_pos + 4])
            enum_value = self.EnumConstValue(type_name_index, const_name_index)
            return 5, self.ElementValue(tag, enum_value)

        elif tag == ElementValueTag.CLASS:
            # Class info: u2 class_info_index
            class_info_index = self.parse_int(self.raw[current_pos:current_pos + 2])
            return 3, self.ElementValue(tag, class_info_index)

        elif tag == ElementValueTag.ANNOTATION_INTERFACE:
            # Nested annotation
            annotation_size, annotation = self._parse_annotation(current_pos)
            return 1 + annotation_size, self.ElementValue(tag, annotation)

        elif tag == ElementValueTag.ARRAY_TYPE:
            # Array: u2 num_values, element_value values[num_values]
            num_values = self.parse_int(self.raw[current_pos:current_pos + 2])
            current_pos += 2
            values = []

            for _ in range(num_values):
                value_size, element_value = self._parse_element_value(current_pos)
                values.append(element_value)
                current_pos += value_size

            total_size = current_pos - start
            return total_size, self.ElementValue(tag, tuple(values))

        else:
            raise ValueError(f"Unknown element value tag: {tag}")
