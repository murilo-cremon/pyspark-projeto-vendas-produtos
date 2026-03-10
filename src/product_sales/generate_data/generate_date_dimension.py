import pandas as pd

start_date = '2023-01-01'
end_date = '2026-12-31'

# Criar sequência de datas e gera dataframe
datas = pd.date_range(start=start_date, end=end_date, freq='D')
dim_data = pd.DataFrame({'data': datas})

# Criar colunas da dimensão
dim_data['ano'] = dim_data['data'].dt.year
dim_data['mes'] = dim_data['data'].dt.month
dim_data['dia'] = dim_data['data'].dt.day
dim_data['trimestre'] = dim_data['data'].dt.quarter
dim_data['semestre'] = dim_data['mes'].apply(lambda x: 1 if x <= 6 else 2)
dim_data['sk_data'] = dim_data['data']

dim_data = dim_data[
    [
        'sk_data',
        'data',
        'ano',
        'mes',
        'dia',
        'trimestre',
        'semestre'
    ]
]
csv_file_path = '../../../medallion_architecture/refined_zone/date-dimension-csv/dim_data.csv'
parquet_file_path = '../../../medallion_architecture/refined_zone/date-dimension-parquet/dim_data.parquet'
dim_data.to_csv(csv_file_path, index=False)
dim_data.to_parquet(parquet_file_path, engine='pyarrow', index=False)