from pyspark.sql.functions import *
from pyspark.sql.window import Window

def read_trusted_parquet_file(spark, trusted_path):
    path = trusted_path + '/product-sales-trusted-parquet/'
    return spark.read.parquet(path)

def select_fields(dataframe):
    column_list = [
        'id_produto', 'produto', 'categoria', 'subcategoria', 'fabricante', 'custo'
    ]

    return dataframe.select(column_list).drop_duplicates()
    

def generate_sk(dataframe):
    column_list = [
        'sk_produto', 'id_produto', 'produto', 'categoria', 'subcategoria', 'fabricante', 'custo'
    ]

    window = Window.orderBy('id_produto')

    df = dataframe \
        .withColumn('sk_produto', row_number().over(window)) \
        .select(column_list)

    return df


def save_product_dimension(dataframe, refined_path):
    csv_file_name = refined_path + '/product-dimension-csv'
    parquet_file_name = refined_path + '/product-dimension-parquet'

    dataframe.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    dataframe.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)
    

def product_dimension(spark, trusted_path, refined_path):
    df = read_trusted_parquet_file(spark, trusted_path)
    df = select_fields(df)
    df = generate_sk(df)    
    save_product_dimension(df, refined_path)