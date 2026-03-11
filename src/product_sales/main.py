import os
from config.config import *
from utils.spark_session import create_spark_session
from ingestion.product_sales_ingestion import ingestion_file_raw_zone
from processing.product_sales_trusted import process_trusted_product_sales
from processing.customer_dimension import customer_dimension
from processing.product_dimension import product_dimension
from processing.sales_fact import sales_fact

def job_execution():
    spark = create_spark_session(APP_NAME)

    if not os.path.exists(LANDING_ZONE_FILE):
        from generate_data.generate_fake_data import generate_fake_data
        generate_fake_data()

    ingestion_file_raw_zone(spark, LANDING_ZONE, RAW_ZONE)
    process_trusted_product_sales(spark, RAW_ZONE, TRUSTED_ZONE)
    customer_dimension(spark, TRUSTED_ZONE, REFINED_ZONE)
    product_dimension(spark, TRUSTED_ZONE, REFINED_ZONE)
    sales_fact(spark, TRUSTED_ZONE, REFINED_ZONE)

    spark.stop()

if __name__ == "__main__":
    job_execution()    