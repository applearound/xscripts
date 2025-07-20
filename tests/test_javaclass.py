import logging

from xscripts.java import JavaClassDumpPipeline

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def test_java_class_dump_pipeline():
    pipeline = JavaClassDumpPipeline(r"D:\Dev\mine\DataStructureAndAlgorithm\target\classes\me\zyz\dsal\collection\deque\ArrayDeque.class")
    java_clss = pipeline.run()

    logger.info(java_clss.get_major_version())