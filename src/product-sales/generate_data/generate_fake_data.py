import csv
from random import choice, randint, uniform
from faker import Faker

fake = Faker("pt_BR")

# Produtos (10 tipos fixos)
produtos = [
    {"id_produto": 1, "nome": "Notebook Pro 15", "categoria": "Computadores", "subcategoria": "Notebook", "fabricante": "Dell", "custo": 4200},
    {"id_produto": 2, "nome": "Smartphone X", "categoria": "Smartphones", "subcategoria": "Android", "fabricante": "Samsung", "custo": 2100},
    {"id_produto": 3, "nome": "Tablet Plus", "categoria": "Tablets", "subcategoria": "Tablet", "fabricante": "Apple", "custo": 3000},
    {"id_produto": 4, "nome": "Monitor 27 4K", "categoria": "Periféricos", "subcategoria": "Monitor", "fabricante": "LG", "custo": 1200},
    {"id_produto": 5, "nome": "Mouse Gamer", "categoria": "Periféricos", "subcategoria": "Mouse", "fabricante": "Logitech", "custo": 120},
    {"id_produto": 6, "nome": "Teclado Mecânico", "categoria": "Periféricos", "subcategoria": "Teclado", "fabricante": "Razer", "custo": 400},
    {"id_produto": 7, "nome": "Cadeira Gamer", "categoria": "Móveis", "subcategoria": "Cadeira", "fabricante": "DXRacer", "custo": 1500},
    {"id_produto": 8, "nome": "Headset Pro", "categoria": "Áudio", "subcategoria": "Headset", "fabricante": "HyperX", "custo": 300},
    {"id_produto": 9, "nome": "SSD 1TB", "categoria": "Armazenamento", "subcategoria": "SSD", "fabricante": "Kingston", "custo": 450},
    {"id_produto": 10, "nome": "Impressora Laser", "categoria": "Impressoras", "subcategoria": "Laser", "fabricante": "HP", "custo": 1100},
]

# Gerar clientes
clientes = []
for i in range(1, 31):  # 20 clientes únicos
    clientes.append({
        "id_cliente": 100 + i,
        "nome_cliente": fake.name(),
        "email_cliente": fake.email(),
        "data_cadastro": fake.date_between(start_date="-3y", end_date="today"),
        "estado_civil": choice(["Solteiro", "Casado", "Divorciado", "Viúvo"]),
        "genero": choice(["M", "F"])
    })

# Gerar pedidos
linhas = []
for pedido_id in range(1, 501):
    cliente = choice(clientes)
    produto = choice(produtos)
    data_pedido = fake.date_between(start_date=cliente["data_cadastro"], end_date="today")
    quantidade = randint(1, 3)
    valor_venda = round(produto["custo"] * uniform(1.1, 1.5), 2) * quantidade
    linhas.append({
        "id_pedido": pedido_id,
        "data_pedido": data_pedido,
        "id_cliente": cliente["id_cliente"],
        "nome_cliente": cliente["nome_cliente"],
        "email_cliente": cliente["email_cliente"],
        "data_cadastro_cliente": cliente["data_cadastro"],
        "estado_civil_cliente": cliente["estado_civil"],
        "genero_cliente": cliente["genero"],
        "id_produto": produto["id_produto"],
        "nome_produto": produto["nome"],
        "categoria_produto": produto["categoria"],
        "subcategoria_produto": produto["subcategoria"],
        "fabricante_produto": produto["fabricante"],
        "valor_venda": round(valor_venda, 2),
        "quantidade_venda": quantidade,
        "custo_produto": produto["custo"]
    })

# Salvar CSV
file_path = '../../../data/landing_zone/product-sales.csv'
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=linhas[0].keys())
    writer.writeheader()
    writer.writerows(linhas)

print(f"CSV gerado com sucesso: {file_path}")