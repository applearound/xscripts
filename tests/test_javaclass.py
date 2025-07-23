import logging

from xscripts.java import JavaClassDumpPipeline, JavaClass

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_java_class_dump_pipeline():
    pipeline = JavaClassDumpPipeline(r"tests_resources/DefaultPileConfigurationService.class")

    java_clss = JavaClass(pipeline.run())

    logger.info("Magic: %s", java_clss.get_magic())
    logger.info("Minor version: %s", java_clss.get_minor_version())
    logger.info("Major version: %s", java_clss.get_major_version())
    logger.info("Constant pool count: %s", java_clss.get_constant_pool_count())

    logger.info("----------- Constant pool info -----------")
    for constant_pool_info in java_clss.get_constant_pool():
        logger.info("Constant pool info: %s", constant_pool_info)
    logger.info("----------- Constant pool info ends -----------")

    logger.info("Access flags: %s", java_clss.get_access_flags())
    logger.info("This class: %s", java_clss.get_class_name())
    logger.info("Super class: %s", java_clss.get_super_class_name())
    logger.info("Interfaces count: %s", java_clss.get_interfaces_count())

    logger.info("----------- Interfaces info -----------")
    for interface in java_clss.get_interfaces():
        logger.info("Interface: %s", interface)
    logger.info("----------- Interfaces info ends -----------")

    logger.info("Fields count: %s", java_clss.get_fields_count())

    logger.info("----------- Fields info -----------")
    for field in java_clss.get_fields():
        logger.info("Field: %s", field)
    logger.info("----------- Fields info ends -----------")

    logger.info("Methods count: %s", java_clss.get_methods_count())

    logger.info("----------- Methods info -----------")
    for method in java_clss.get_methods():
        logger.info("Method: %s", method)
        name_info = java_clss.get_constant_pool_info(method.name_index)
        logger.info("Method Name: %s", name_info)
        descriptor_info = java_clss.get_constant_pool_info(method.descriptor_index)
        logger.info("Method Descriptor: %s", descriptor_info)
    logger.info("----------- Methods info ends -----------")

    logger.info("Attributes count: %s", java_clss.get_attributes_count())

    logger.info("----------- Attribute info -----------")
    for attribute in java_clss.get_attributes():
        logger.info("Attribute: %s", attribute)
    logger.info("----------- Attribute info ends -----------")
