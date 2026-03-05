from config.config import APP_NAME
from utils.spark_session import create_spark_session

spark = create_spark_session(APP_NAME)
print(f'Funcionou: {spark}')