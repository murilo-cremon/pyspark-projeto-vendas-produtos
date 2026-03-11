from config.config import *
from utils.spark_session import create_spark_session
from ingestion.product_sales_ingestion import ingestion_file_raw_zone
from processing.bronze_to_silver_product_sales import save_parquet_csv_file_to_trusted_zone
from processing.customer_dimension import customer_dimension

spark = create_spark_session(APP_NAME)
# print(f'Funcionou: {spark}')

#ingestion_file_raw_zone(spark, LANDING_ZONE_FILE, RAW_ZONE)
customer_dimension(spark, TRUSTED_ZONE , REFINED_ZONE)

# TRUSTED_ZONE