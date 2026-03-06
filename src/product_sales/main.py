from config.config import *
from utils.spark_session import create_spark_session
from ingestion.product_sales_ingestion import ingestion_file_raw_zone

spark = create_spark_session(APP_NAME)
print(f'Funcionou: {spark}')

ingestion_file_raw_zone(spark, LANDING_ZONE_FILE, RAW_ZONE)