from pyspark.sql import SparkSession

def create_spark_session(app_name: str) -> SparkSession:
    return SparkSession.builder \
            .appName(app_name) \
            .config("spark.executor.memory", "2g") \
            .config("spark.sql.shuffle.partitions", "4") \
            .getOrCreate()