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
        'id_cliente',
        'nome',
        'email',
        'dt_cadastro',
        'tipo_estado_civil',
        'genero'
    ]

    df = (
        df
        .select(column_list)
        .drop_duplicates()
    )

    return df


def generate_surrogate_key(dataframe):
    df = dataframe

    column_list = [
        'sk_cliente',
        'id_cliente',
        'nome',
        'email',
        'dt_cadastro',
        'tipo_estado_civil',
        'genero'
    ]

    window = Window.orderBy('id_cliente')

    df = (
        df
        .withColumn('sk_cliente', row_number().over(window))
        .select(column_list)
    )

    return df


def save_parquet_csv_file_to_customer_dimension(spark, trusted_path, refined_path):
    df = read_trusted_file_parquet(spark, trusted_path)
    df = select_fields(df)
    df = generate_surrogate_key(df)

    csv_file_name = refined_path + '/customer-dimension-csv'
    parquet_file_name = refined_path + '/customer-dimension-parquet'

    df.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    df.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)