from pyspark.sql.types import *
from pyspark.sql.functions import *

def struct_type_definition() -> StructType:
    schema_landing_zone = StructType([
        StructField('id_pedido', StringType(), True),
        StructField('data_pedido', StringType(), True),
        StructField('nome_cliente', StringType(), True),
        StructField('email_cliente', StringType(), True),
        StructField('data_cadastro_cliente', StringType(), True),
        StructField('estado_civil_cliente', StringType(), True),
        StructField('genero_cliente', StringType(), True),
        StructField('nome_produto', StringType(), True),
        StructField('categoria_produto', StringType(), True),
        StructField('subcategoria_produto', StringType(), True),
        StructField('fabricante_produto', StringType(), True),
        StructField('valor_venda', StringType(), True),
        StructField('quantidade_venda', StringType(), True),
        StructField('custo_produto', StringType(), True)
    ])

    return schema_landing_zone


def read_csv_file(spark, file_ingestion: str):
    df = (
        spark.read
        .option('header', 'true')
        .option('sep', ',')
        .schema(struct_type_definition())
        .csv(file_ingestion)
    )

    return df


def ingestion_file_raw_zone(spark, file_ingestion: str, raw_zone_path: str):
    df = read_csv_file(spark, file_ingestion)
    csv_file_name = raw_zone_path + 'product-sales-raw-csv'
    parquet_file_name = raw_zone_path + 'product-sales-raw-parquet'
    
    df.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    df.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)