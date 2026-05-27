from fastapi import FastAPI

# Inicializa o microsserviço de Catálogo
app = FastAPI(
    title="Microsserviço de Catálogo - E-commerce SD",
    description="API para gestão e consulta de produtos (Entrega 1)",
    version="1.0.0"
)

# Simulando um banco de dados temporário (Mock de dados)
PRODUTOS_REPLICADOS = [
    {"id": 1, "nome": "Teclado Mecânico RGB", "preco": 349.90, "estoque": 15},
    {"id": 2, "nome": "Rato Gamer Wireless", "preco": 259.00, "estoque": 22},
    {"id": 3, "nome": "Monitor UltraGear 24' 180Hz", "preco": 899.00, "estoque": 8},
    {"id": 4, "nome": "Tapete para Rato XL", "preco": 79.90, "estoque": 50}
]

@app.get("/")
def read_root():
    return {"status": "Online", "servico": "Microsserviço de Catálogo Ativo"}

# Endpoint obrigatório para o Slide 5 (Listagem de Produtos)
@app.get("/produtos")
def listar_produtos():
    return {
        "mensagem": "Dados obtidos com sucesso do nó local (Catálogo)",
        "quantidade": len(PRODUTOS_REPLICADOS),
        "produtos": PRODUTOS_REPLICADOS
    }