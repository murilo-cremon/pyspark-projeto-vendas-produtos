from pyspark.sql import functions as F
from pyspark.sql.functions import broadcast

def read_dimension(spark, trusted_path, refined_path):
    date_dimension = refined_path + '/date-dimension-parquet/'
    product_dimension = refined_path + '/product-dimension-parquet/'
    customer_dimension = refined_path + '/customer-dimension-parquet/'
    temp_fact = trusted_path + '/product-sales-trusted-parquet/'

    date_df = spark.read.parquet(date_dimension)
    product_df = spark.read.parquet(product_dimension)
    customer_df = spark.read.parquet(customer_dimension)
    fact_df = spark.read.parquet(temp_fact)

    return date_df, product_df, customer_df, fact_df


def aggregate_sales_fact(dataframe):
    column_list =[
        'id_cliente', 'id_produto', 'dt_pedido', 'vl_venda', 'qt_venda'
    ]

    group_by_list =[
        'id_cliente', 'id_produto', 'dt_pedido'
    ]    

    df = (
        dataframe
        .select(column_list)
        .groupBy(group_by_list)
        .agg(
            F.sum('vl_venda').alias('vl_vendas'),
            F.sum('qt_venda').alias('qt_vendas')
        )
        .withColumn(
            'vl_total',
            F.col('vl_vendas') * F.col('qt_vendas')
        )
        .drop('vl_venda', 'qt_venda')
    )

    return df
    

def return_sk(date_df, product_df, customer_df, fact_df):  
    date_df = date_df.select(F.col('data').alias('dt_pedido'), 'sk_data')
    product_df = product_df.select('id_produto', 'sk_produto')
    customer_df = customer_df.select('id_cliente', 'sk_cliente')
    
    fact_df = (
        fact_df
        .join(broadcast(date_df), 'dt_pedido', 'left')
        .join(broadcast(product_df), 'id_produto', 'left')
        .join(broadcast(customer_df), 'id_cliente', 'left')
    )

    return fact_df


def reshape_sales_fact(dataframe):
    column_list = [
        'sk_data', 'sk_cliente', 'sk_produto', 'vl_vendas', 'qt_vendas', 'vl_total'
    ]

    return dataframe.select(column_list)


def save_sales_fact(dataframe, refined_path):
    csv_file_name = refined_path + '/sales-fact-csv'
    parquet_file_name = refined_path + '/sales-fact-parquet'

    dataframe.write \
        .option('header', 'true') \
        .option('sep', ',') \
        .mode('overwrite') \
        .csv(csv_file_name)
    
    dataframe.write \
        .mode('overwrite') \
        .parquet(parquet_file_name)


def sales_fact(spark, trusted_path, refined_path):
    date_df, product_df, customer_df, fact_df = read_dimension(spark, trusted_path, refined_path)
    fact_df = aggregate_sales_fact(fact_df)
    df = return_sk(date_df, product_df, customer_df, fact_df)
    df = reshape_sales_fact(df)
    save_sales_fact(df, refined_path)