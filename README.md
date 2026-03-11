# 📊 Projeto de Vendas: Arquitetura Medalhão com PySpark

Este projeto implementa um pipeline de dados robusto utilizando **PySpark**, seguindo os princípios da **Arquitetura Medalhão** (Raw/Bronze, Trusted/Silver e Refined/Gold). O objetivo é transformar dados brutos de vendas em um modelo dimensional (Star Schema) otimizado para análise e estudos.



---

## 🚀 Sobre o Projeto

A aplicação processa dados de vendas desde a sua origem até a camada final de consumo. Todo o processamento é feito em **PySpark puro**, garantindo escalabilidade e performance no tratamento de grandes volumes de dados.

Os dados finais são disponibilizados em formatos **CSV** (para portabilidade) e **Parquet** (para alta performance), permitindo que estudantes e profissionais de dados pratiquem modelagem, consultas SQL e criação de dashboards.

---

## 🏗️ Arquitetura de Dados

O projeto é dividido em três camadas lógicas de processamento:

1.  **Raw (Bronze):** Ingestão dos dados brutos exatamente como chegam da fonte. Sem tratamento, servindo como histórico e ponto de recuperação.
2.  **Trusted (Silver):** Dados limpos, tipados e filtrados. Aqui é feita a remoção de duplicatas, tratamento de nulos e padronização de formatos.
3.  **Refined (Gold):** Camada de negócios. Os dados são agregados e organizados em um **Modelo Dimensional**.



---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **PySpark** (Spark SQL & DataFrame API)
* **Apache Parquet** (Armazenamento colunar)

---

## 📂 Estrutura do Modelo Dimensional (Camada Gold)

Na camada **Refined**, os dados são estruturados seguindo o conceito de *Star Schema*:

| Tipo | Tabela | Descrição |
| :--- | :--- | :--- |
| **Fato** | `sales_fact` | Métricas de venda e chaves estrangeiras (FKs). |
| **Dimensão** | `product_dimension` | Detalhamento dos produtos (Nome, Categoria, Custo). |
| **Dimensão** | `customer_dimension` | Informações cadastrais dos clientes. |
| **Dimensão** | `date_dimension` | Atributos temporais (Ano, Mês, Dia, Trimestre, Dia da Semana). |

---

## ⚙️ Configuração e Execução

### 1. Pré-requisitos
Certifique-se de ter o **Java 8 ou superior** instalado e configurado no seu `PATH` (necessário para o Spark).

### 2. Instalação das Dependências
Clone o repositório e instale as bibliotecas necessárias utilizando o arquivo `requirements.txt`:

```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/projeto-vendas-pyspark.git](https://github.com/seu-usuario/projeto-vendas-pyspark.git)
cd projeto-vendas-pyspark

# Instale as dependências
pip install -r requirements.txt