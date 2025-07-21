import logging

from xscripts.java import JavaClassDumpPipeline

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_java_class_dump_pipeline():
    pipeline = JavaClassDumpPipeline(r"tests_resources/GatewayServer.class")

    java_clss = pipeline.run()

    logger.info("Magic: %s", java_clss.get_magic())
    logger.info("Minor version: %s", java_clss.get_minor_version())
    logger.info("Major version: %s", java_clss.get_major_version())
    logger.info("Constant pool count: %s", java_clss.get_constant_pool_count())

    logger.info("----------- Constant pool info -----------")
    for constant_pool_info in java_clss.constant_pool_info():
        logger.info("Constant pool info: %s", constant_pool_info)
    logger.info("----------- Constant pool info end -----------")

    logger.info("Access flags: %s", java_clss.get_access_flags())
    logger.info("This class: %s", java_clss.get_class_name())
    logger.info("Super class: %s", java_clss.get_super_class_name())
    logger.info("Interfaces count: %s", java_clss.get_interfaces_count())
