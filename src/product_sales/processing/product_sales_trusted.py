from pyspark.sql.types import *
from pyspark.sql.functions import *

def read_raw_file_parquet(spark, raw_path):
    path = raw_path + '/product-sales-raw-parquet/'
    return spark.read.parquet(path)

def change_data_type(dataframe):   
    df = (
        dataframe
        .withColumn('id_pedido', col('id_pedido').cast('int'))
        .withColumn('data_pedido', to_date(col('data_pedido'), 'yyyy-mm-dd'))
        .withColumn('data_cadastro_cliente', to_date(col('data_cadastro_cliente'), 'yyyy-mm-dd'))
        .withColumn('id_cliente', col('id_cliente').cast('int'))
        .withColumn('id_produto', col('id_produto').cast('int'))
        .withColumn('valor_venda', col('valor_venda').cast(DecimalType(10, 2)))
        .withColumn('quantidade_venda', col('quantidade_venda').cast('int'))
        .withColumn('custo_produto', col('custo_produto').cast(DecimalType(10,2)))
    )

    return df


def reaname_column(dataframe):
    df = dataframe
    
    rename_col = {
        'data_pedido': 'dt_pedido',
        'data_cadastro_cliente': 'dt_cadastro',
        'email_cliente': 'email',
        'nome_cliente': 'nome',
        'estado_civil_cliente': 'tipo_estado_civil',
        'genero_cliente': 'genero',
        'nome_produto': 'produto',
        'categoria_produto': 'categoria',
        'subcategoria_produto': 'subcategoria',
        'fabricante_produto': 'fabricante',
        'valor_venda': 'vl_venda',
        'quantidade_venda': 'qt_venda',
        'custo_produto': 'custo'
    }

    for old_name, new_name in rename_col.items():
        df = df.withColumnRenamed(old_name, new_name)

    return df


def data_transformation(dataframe):
    df = (
        dataframe
        .withColumn(
            'genero',
            when(trim(col('genero')) == 'M', 'Masculino')
            .when(trim(col('genero')) == 'F', 'Feminino')
            .otherwise('Não declarado')
        )
        .withColumn(
            'tipo_estado_civil',
            initcap(trim(col('tipo_estado_civil')))
        )
        .withColumn(
            'nome',
            initcap(trim(col('nome')))
        )
        .withColumn(
            'email',
            lower(trim(col('email')))
        )
        .withColumn(
            'fabricante',
            initcap(trim(col('fabricante')))
        )       
    )

    return df


def save_product_sales_trusted_zone(dataframe, trusted_path):
    csv_file_name = trusted_path + '/product-sales-trusted-csv'
    parquet_file_name = trusted_path + '/product-sales-trusted-parquet'

    dataframe.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    dataframe.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)
    

def process_trusted_product_sales(spark, raw_path, trusted_path):
    df = read_raw_file_parquet(spark, raw_path)
    df = change_data_type(df)
    df = reaname_column(df)
    df = data_transformation(df)
    save_product_sales_trusted_zone(df, trusted_path)