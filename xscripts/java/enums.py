from enum import IntEnum, StrEnum


class ConstantPoolInfoTags(IntEnum):
    CLASS = 7
    FIELDREF = 9
    METHODREF = 10
    INTERFACE_METHODREF = 11
    STRING = 8
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    NAME_AND_TYPE = 12
    UTF8 = 1
    METHOD_HANDLE = 15
    METHOD_TYPE = 16
    DYNAMIC = 17
    INVOKE_DYNAMIC = 18
    MODULE = 19
    PACKAGE = 20


class AccessFlags(IntEnum):
    """ Access flags for classes and interfaces in Java.

    Reference: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html

    ACC_PUBLIC 	    0x0001  Declared public; may be accessed from outside its package.
    ACC_FINAL 	    0x0010 	Declared final; no subclasses allowed.
    ACC_SUPER 	    0x0020 	Treat superclass methods specially when invoked by the invokespecial instruction.
    ACC_INTERFACE 	0x0200 	Is an interface, not a class.
    ACC_ABSTRACT 	0x0400 	Declared abstract; must not be instantiated.
    ACC_SYNTHETIC 	0x1000 	Declared synthetic; not present in the source code.
    ACC_ANNOTATION 	0x2000 	Declared as an annotation interface.
    ACC_ENUM 	    0x4000 	Declared as an enum class.
    ACC_MODULE      0x8000 	Is a module, not a class or interface.
    """
    PUBLIC = 0x0001
    FINAL = 0x0010
    SUPER = 0x0020
    INTERFACE = 0x0200
    ABSTRACT = 0x0400
    SYNTHETIC = 0x1000
    ANNOTATION = 0x2000
    ENUM = 0x4000
    MODULE = 0x8000

    @staticmethod
    def parse_flags(value: int) -> tuple['AccessFlags', ...]:
        """Get all access flags that are satisfied by the given value."""
        return tuple(flag for flag in AccessFlags if flag & value != 0)

    @staticmethod
    def is_public(value: int) -> bool:
        """Check if the class or interface is public."""
        return (value & AccessFlags.PUBLIC) != 0

    @staticmethod
    def is_final(value: int) -> bool:
        """Check if the class or interface is final."""
        return (value & AccessFlags.FINAL) != 0

    @staticmethod
    def is_super(value: int) -> bool:
        """Check if the class or interface is a super class."""
        return (value & AccessFlags.SUPER) != 0

    @staticmethod
    def is_interface(value: int) -> bool:
        """Check if the class or interface is an interface."""
        return (value & AccessFlags.INTERFACE) != 0

    @staticmethod
    def is_abstract(value: int) -> bool:
        """Check if the class or interface is abstract."""
        return (value & AccessFlags.ABSTRACT) != 0

    @staticmethod
    def is_synthetic(value: int) -> bool:
        """Check if the class or interface is synthetic."""
        return (value & AccessFlags.SYNTHETIC) != 0

    @staticmethod
    def is_annotation(value: int) -> bool:
        """Check if the class or interface is an annotation."""
        return (value & AccessFlags.ANNOTATION) != 0

    @staticmethod
    def is_enum(value: int) -> bool:
        """Check if the class or interface is an enum."""
        return (value & AccessFlags.ENUM) != 0

    @staticmethod
    def is_module(value: int) -> bool:
        """Check if the class or interface is a module."""
        return (value & AccessFlags.MODULE) != 0


class FieldAccessFlags(IntEnum):
    """ Access flags for fields in Java.

    Reference: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html

    ACC_PUBLIC 	    0x0001  Declared public; may be accessed from outside its package.
    ACC_PRIVATE 	0x0002  Declared private; accessible only within its class.
    ACC_PROTECTED 	0x0004  Declared protected; may be accessed within subclasses.
    ACC_STATIC 	    0x0008  Declared static; not instance-specific.
    ACC_FINAL 	    0x0010  Declared final; value cannot change after initialization.
    ACC_VOLATILE 	0x0040  Declared volatile; may be changed by multiple
    """
    PUBLIC = 0x0001
    PRIVATE = 0x0002
    PROTECTED = 0x0004
    STATIC = 0x0008
    FINAL = 0x0010
    VOLATILE = 0x0040
    TRANSIENT = 0x0080
    SYNTHETIC = 0x1000
    ENUM = 0x4000

    @staticmethod
    def parse_flags(value: int) -> tuple['FieldAccessFlags', ...]:
        """Get all access flags that are satisfied by the given value."""
        return tuple(flag for flag in FieldAccessFlags if flag & value != 0)

    @staticmethod
    def is_public(value: int) -> bool:
        """Check if the field is public."""
        return (value & FieldAccessFlags.PUBLIC) != 0

    @staticmethod
    def is_private(value: int) -> bool:
        """Check if the field is private."""
        return (value & FieldAccessFlags.PRIVATE) != 0

    @staticmethod
    def is_protected(value: int) -> bool:
        """Check if the field is protected."""
        return (value & FieldAccessFlags.PROTECTED) != 0

    @staticmethod
    def is_static(value: int) -> bool:
        """Check if the field is static."""
        return (value & FieldAccessFlags.STATIC) != 0

    @staticmethod
    def is_final(value: int) -> bool:
        """Check if the field is final."""
        return (value & FieldAccessFlags.FINAL) != 0

    @staticmethod
    def is_volatile(value: int) -> bool:
        """Check if the field is volatile."""
        return (value & FieldAccessFlags.VOLATILE) != 0

    @staticmethod
    def is_transient(value: int) -> bool:
        """Check if the field is transient."""
        return (value & FieldAccessFlags.TRANSIENT) != 0

    @staticmethod
    def is_synthetic(value: int) -> bool:
        """Check if the field is synthetic."""
        return (value & FieldAccessFlags.SYNTHETIC) != 0

    @staticmethod
    def is_enum(value: int) -> bool:
        """Check if the field is an enum."""
        return (value & FieldAccessFlags.ENUM) != 0


class AttributesTypes(StrEnum):
    """ Enum for attribute types in Java class files.

    """
    CONSTANT_VALUE = "ConstantValue"
    CODE = "Code"
    STACK_MAP_TABLE = "StackMapTable"
    EXCEPTIONS = "Exceptions"
    INNER_CLASSES = "InnerClasses"
    SYNTHETIC = "Synthetic"
    SIGNATURE = "Signature"
    SOURCE_FILE = "SourceFile"
    SOURCE_DEBUG_EXTENSION = "SourceDebugExtension"
    LINE_NUMBER_TABLE = "LineNumberTable"
    LOCAL_VARIABLE_TABLE = "LocalVariableTable"
    LOCAL_VARIABLE_TYPE_TABLE = "LocalVariableTypeTable"
    DEPRECATED = "Deprecated"
    RUNTIME_VISIBLE_ANNOTATIONS = "RuntimeVisibleAnnotations"
    RUNTIME_INVISIBLE_ANNOTATIONS = "RuntimeInvisibleAnnotations"
    RUNTIME_VISIBLE_PARAMETER_ANNOTATIONS = "RuntimeVisibleParameterAnnotations"
    RUNTIME_INVISIBLE_PARAMETER_ANNOTATIONS = "RuntimeInvisibleParameterAnnotations"
    RUNTIME_VISIBLE_TYPE_ANNOTATIONS = "RuntimeVisibleTypeAnnotations"
    RUNTIME_INVISIBLE_TYPE_ANNOTATIONS = "RuntimeInvisibleTypeAnnotations"
    ANNOTATION_DEFAULT = "AnnotationDefault"
    BOOTSTRAP_METHODS = "BootstrapMethods"
    METHOD_PARAMETERS = "MethodParameters"
    MODULE = "Module"
    MODULE_PACKAGES = "ModulePackages"
    MODULE_MAIN_CLASS = "ModuleMainClass"
    NEST_HOST = "NestHost"
    NEST_MEMBERS = "NestMembers"
    RECORD = "Record"
    PERMITTED_SUBCLASSES = "PermittedSubclasses"
