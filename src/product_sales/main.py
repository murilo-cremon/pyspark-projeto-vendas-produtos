from config.config import *
from utils.spark_session import create_spark_session
from ingestion.product_sales_ingestion import ingestion_file_raw_zone
from processing.bronze_to_silver_product_sales import save_parquet_csv_file_to_trusted_zone

spark = create_spark_session(APP_NAME)
# print(f'Funcionou: {spark}')

#ingestion_file_raw_zone(spark, LANDING_ZONE_FILE, RAW_ZONE)
save_parquet_csv_file_to_trusted_zone(spark, RAW_ZONE, TRUSTED_ZONE)

# TRUSTED_ZONE