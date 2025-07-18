from xscripts.java import JavaClassDumpPipeline


def test_java_class_dump_pipeline():
    pipeline = JavaClassDumpPipeline("/home/yezhou/Dev/work/api-gateway/target/classes/com/zcsy/saasgateway/util/ChannelUtils.class")
    pipeline.run()