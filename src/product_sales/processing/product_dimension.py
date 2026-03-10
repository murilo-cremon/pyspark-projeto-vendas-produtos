from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window

def read_trusted_file_parquet(spark, trusted_path: str):
    trusted_path = trusted_path + '/product-sales-trusted-parquet/'

    df = (
        spark.read
        .format('parquet')
        .load(trusted_path)
    )

    return df


def select_fields(dataframe):
    df = dataframe

    column_list = [
        'id_produto',
        'produto',
        'categoria',
        'subcategoria',
        'fabricante',
        'custo'
    ]

    df = (
        df
        .select(column_list)
        .drop_duplicates()
    )

    return df


def generate_surrogate_key(dataframe,):
    df = dataframe

    column_list = [
        'sk_produto',
        'id_produto',
        'produto',
        'categoria',
        'subcategoria',
        'fabricante',
        'custo'
    ]

    window = Window.orderBy('id_produto')

    df = (
        df
        .withColumn('sk_produto', row_number().over(window))
        .select(column_list)
    )

    return df


def save_parquet_csv_file_to_product_dimension(spark, trusted_path, refined_path):
    df = read_trusted_file_parquet(spark, trusted_path)
    df = select_fields(df)
    df = generate_surrogate_key(df)

    
    csv_file_name = refined_path + '/product-dimension-csv'
    parquet_file_name = refined_path + '/product-dimension-parquet'

    df.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    df.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)
