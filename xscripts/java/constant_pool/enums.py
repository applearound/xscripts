from enum import IntEnum


class ConstantPoolInfoTags(IntEnum):
    """ Enum for constant pool info tags in Java class files.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4-140

    CONSTANT_Utf8 	                1 	45.3 	1.0.2
    CONSTANT_Integer 	            3 	45.3 	1.0.2
    CONSTANT_Float 	                4 	45.3 	1.0.2
    CONSTANT_Long 	                5 	45.3 	1.0.2
    CONSTANT_Double                 6 	45.3 	1.0.2
    CONSTANT_Class  	            7 	45.3 	1.0.2
    CONSTANT_String 	            8 	45.3 	1.0.2
    CONSTANT_Fieldref 	            9 	45.3 	1.0.2
    CONSTANT_Methodref 	            10 	45.3 	1.0.2
    CONSTANT_InterfaceMethodref 	11 	45.3 	1.0.2
    CONSTANT_NameAndType 	        12 	45.3 	1.0.2
    CONSTANT_MethodHandle 	        15 	51.0 	7
    CONSTANT_MethodType 	        16 	51.0 	7
    CONSTANT_Dynamic 	            17 	55.0 	11
    CONSTANT_InvokeDynamic       	18 	51.0 	7
    CONSTANT_Module 	            19 	53.0 	9
    CONSTANT_Package 	            20 	53.0 	9
    """
    UTF8 = 1
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    CLASS = 7
    STRING = 8
    FIELDREF = 9
    METHODREF = 10
    INTERFACE_METHODREF = 11
    NAME_AND_TYPE = 12
    METHOD_HANDLE = 15
    METHOD_TYPE = 16
    DYNAMIC = 17
    INVOKE_DYNAMIC = 18
    MODULE = 19
    PACKAGE = 20
