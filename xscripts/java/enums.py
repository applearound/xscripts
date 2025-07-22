from enum import IntEnum


class ClassAccessFlags(IntEnum):
    """ Access flags for classes and interfaces in Java.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.1-200-E.1

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
    def parse_flags(value: int) -> tuple['ClassAccessFlags', ...]:
        """Get all access flags that are satisfied by the given value."""
        return tuple(flag for flag in ClassAccessFlags if flag & value != 0)

    @staticmethod
    def is_public(value: int) -> bool:
        """Check if the class or interface is public."""
        return (value & ClassAccessFlags.PUBLIC) != 0

    @staticmethod
    def is_final(value: int) -> bool:
        """Check if the class or interface is final."""
        return (value & ClassAccessFlags.FINAL) != 0

    @staticmethod
    def is_super(value: int) -> bool:
        """Check if the class or interface is a super class."""
        return (value & ClassAccessFlags.SUPER) != 0

    @staticmethod
    def is_interface(value: int) -> bool:
        """Check if the class or interface is an interface."""
        return (value & ClassAccessFlags.INTERFACE) != 0

    @staticmethod
    def is_abstract(value: int) -> bool:
        """Check if the class or interface is abstract."""
        return (value & ClassAccessFlags.ABSTRACT) != 0

    @staticmethod
    def is_synthetic(value: int) -> bool:
        """Check if the class or interface is synthetic."""
        return (value & ClassAccessFlags.SYNTHETIC) != 0

    @staticmethod
    def is_annotation(value: int) -> bool:
        """Check if the class or interface is an annotation."""
        return (value & ClassAccessFlags.ANNOTATION) != 0

    @staticmethod
    def is_enum(value: int) -> bool:
        """Check if the class or interface is an enum."""
        return (value & ClassAccessFlags.ENUM) != 0

    @staticmethod
    def is_module(value: int) -> bool:
        """Check if the class or interface is a module."""
        return (value & ClassAccessFlags.MODULE) != 0


class FieldAccessFlags(IntEnum):
    """ Access flags for fields in Java.

    Reference: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.5-200-A.1

    ACC_PUBLIC 	    0x0001 	Declared public; may be accessed from outside its package.
    ACC_PRIVATE 	0x0002  Declared private; accessible only within the defining class and other classes belonging to the same nest (§5.4.4).
    ACC_PROTECTED 	0x0004 	Declared protected; may be accessed within subclasses.
    ACC_STATIC 	    0x0008 	Declared static.
    ACC_FINAL 	    0x0010 	Declared final; never directly assigned to after object construction (JLS §17.5).
    ACC_VOLATILE 	0x0040 	Declared volatile; cannot be cached.
    ACC_TRANSIENT 	0x0080 	Declared transient; not written or read by a persistent object manager.
    ACC_SYNTHETIC 	0x1000 	Declared synthetic; not present in the source code.
    ACC_ENUM 	    0x4000 	Declared as an element of an enum class.
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


class MethodAccessFlags(IntEnum):
    """ Access flags for methods in Java.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.6-200-A.1

    ACC_PUBLIC 	        0x0001 	Declared public; may be accessed from outside its package.
    ACC_PRIVATE 	    0x0002 	Declared private; accessible only within the defining class and other classes belonging to the same nest.
    ACC_PROTECTED 	    0x0004 	Declared protected; may be accessed within subclasses.
    ACC_STATIC 	        0x0008 	Declared static.
    ACC_FINAL 	        0x0010 	Declared final; must not be overridden (§5.4.5).
    ACC_SYNCHRONIZED    0x0020 	Declared synchronized; invocation is wrapped by a monitor use.
    ACC_BRIDGE  	    0x0040 	A bridge method, generated by the compiler.
    ACC_VARARGS 	    0x0080 	Declared with variable number of arguments.
    ACC_NATIVE 	        0x0100 	Declared native; implemented in a language other than the Java programming language.
    ACC_ABSTRACT 	    0x0400 	Declared abstract; no implementation is provided.
    ACC_STRICT 	        0x0800 	In a class file whose major version number is at least 46 and at most 60: Declared strictfp.
    ACC_SYNTHETIC 	    0x1000 	Declared synthetic; not present in the source code.
    """
    PUBLIC = 0x0001
    PRIVATE = 0x0002
    PROTECTED = 0x0004
    STATIC = 0x0008
    FINAL = 0x0010
    SYNCHRONIZED = 0x0020
    BRIDGE = 0x0040
    VARARGS = 0x0080
    NATIVE = 0x0100
    ABSTRACT = 0x0400
    STRICT = 0x0800
    SYNTHETIC = 0x1000

    @staticmethod
    def parse_flags(value: int) -> tuple['MethodAccessFlags', ...]:
        """Get all access flags that are satisfied by the given value."""
        return tuple(flag for flag in MethodAccessFlags if flag & value != 0)

    @staticmethod
    def is_public(value: int) -> bool:
        """Check if the method is public."""
        return (value & MethodAccessFlags.PUBLIC) != 0

    @staticmethod
    def is_private(value: int) -> bool:
        """Check if the method is private."""
        return (value & MethodAccessFlags.PRIVATE) != 0

    @staticmethod
    def is_protected(value: int) -> bool:
        """Check if the method is protected."""
        return (value & MethodAccessFlags.PROTECTED) != 0

    @staticmethod
    def is_static(value: int) -> bool:
        """Check if the method is static."""
        return (value & MethodAccessFlags.STATIC) != 0

    @staticmethod
    def is_final(value: int) -> bool:
        """Check if the method is final."""
        return (value & MethodAccessFlags.FINAL) != 0

    @staticmethod
    def is_synchronized(value: int) -> bool:
        """Check if the method is synchronized."""
        return (value & MethodAccessFlags.SYNCHRONIZED) != 0

    @staticmethod
    def is_bridge(value: int) -> bool:
        """Check if the method is a bridge method."""
        return (value & MethodAccessFlags.BRIDGE) != 0

    @staticmethod
    def is_varargs(value: int) -> bool:
        """Check if the method is declared with variable number of arguments."""
        return (value & MethodAccessFlags.VARARGS) != 0

    @staticmethod
    def is_native(value: int) -> bool:
        """Check if the method is native."""
        return (value & MethodAccessFlags.NATIVE) != 0

    @staticmethod
    def is_abstract(value: int) -> bool:
        """Check if the method is abstract."""
        return (value & MethodAccessFlags.ABSTRACT) != 0

    @staticmethod
    def is_strict(value: int) -> bool:
        """Check if the method is declared strictfp."""
        return (value & MethodAccessFlags.STRICT) != 0

    @staticmethod
    def is_synthetic(value: int) -> bool:
        """Check if the method is synthetic."""
        return (value & MethodAccessFlags.SYNTHETIC) != 0
