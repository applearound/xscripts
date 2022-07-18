from .magic                import Magic
from .version              import Version
from .constant_pool        import ConstantPool
from .access_flags         import AccessFlags
from .this_and_super_class import ThisAndSuperClass
from .interfaces           import Interfaces
from .fields               import Fields
from .methods              import Methods
from .attributes           import Attributes


class JavaClass:
    def __init__(self, magic: Magic, version: Version, constant_pool: ConstantPool,
                    access_flags: AccessFlags, this_and_super_class: ThisAndSuperClass,
                    interfaces: Interfaces, fields: Fields, methods: Methods, attribues: Attributes) -> None:
        if not isinstance(magic, Magic)                            : raise Exception()
        if not isinstance(version, Version)                        : raise Exception()
        if not isinstance(constant_pool, ConstantPool)             : raise Exception()
        if not isinstance(access_flags, AccessFlags)               : raise Exception()
        if not isinstance(this_and_super_class, ThisAndSuperClass) : raise Exception()
        if not isinstance(interfaces, Interfaces)                  : raise Exception()
        if not isinstance(fields, Fields)                          : raise Exception()
        if not isinstance(methods, Methods)                        : raise Exception()
        if not isinstance(attribues, Attributes)                   : raise Exception()
        
        self.magic                = magic
        self.version              = version
        self.constant_pool        = constant_pool
        self.access_flags         = access_flags
        self.this_and_super_class = this_and_super_class
        self.interfaces           = interfaces
        self.fields               = fields
        self.methods              = methods
        self.attribues            = attribues