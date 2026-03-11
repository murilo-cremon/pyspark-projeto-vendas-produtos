from pyspark.sql import functions as F

def read_dimension(spark, refined_path, trusted_path):
    date_dimension = refined_path + '/date-dimension-parquet/'
    product_dimension = refined_path + '/product-dimension-parquet/'
    customer_dimension = refined_path + '/customer-dimension-parquet/'
    temp_fact = trusted_path + '/product-sales-trusted-parquet/'

    date_df = spark.read.parquet(date_dimension)
    product_df = spark.read.parquet(product_dimension)
    customer_df = spark.read.parquet(customer_dimension)
    fact_df = spark.read.parquet(temp_fact)

    return date_df, product_df, customer_df, fact_df

def sales_fact_trasform(dataframe):
    column_list =[
        'id_cliente', 'id_produto', 'dt_pedido', 'vl_venda', 'qt_venda'
    ]

    df = (
        dataframe
        .select(column_list)
        .groupBy(column_list)
        .agg(
            F.sum('vl_venda').alias('vl_vendas'),
            F.sum('qt_venda').alias('qt_vendas')
        )
        .withColumn(
            'vl_total',
            F.col('vl_venda') * F.col('qt_venda')
        )
    )

    return df
    
def return_sk(spark, refined_path, trusted_path):
    _, _, _, fact_df = read_dimension(spark, refined_path, trusted_path)
    sales_fact_trasform(fact_df)