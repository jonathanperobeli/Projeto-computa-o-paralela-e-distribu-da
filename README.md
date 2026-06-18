# E-Commerce - Sistemas Distribuídos (Etapa 1)

Repositório destinado ao desenvolvimento do projeto prático da disciplina de Sistemas Distribuídos. O sistema consiste em uma arquitetura de e-commerce baseada em microsserviços desacoplados.

## 🚀 Status do Projeto (Entrega 1)
- [x] Microsserviço de Catálogo (Python + FastAPI) - **Operacional**
- [ ] Microsserviço de Carrinho - **Etapa 2**
- [ ] Microsserviço de Pagamento - **Etapa 2**
- [ ] Containerização com Docker Compose - **Etapa 2**

## 🛠️ Como Executar o Protótipo Localmente (Windows)

1. Certifique-se de ter o Python 3.11+ instalado.
2. Clone o repositório:
   ```bash
   git clone https://github.com/jonathanperobeli/Projeto-computa-o-paralela-e-distribu-da.git](https://github.com/jonathanperobeli/Projeto-computa-o-paralela-e-distribu-da.git))
   cd projeto_ecommerce_sd

   # 🛒 TechStore — Microsserviços para E-commerce

![Status](https://img.shields.io/badge/status-funcionando-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![License](https://img.shields.io/badge/license-academic-lightgrey)

Sistema distribuído de e-commerce desenvolvido para a disciplina de **Computação Paralela e Distribuída** — IFSP, Câmpus São Paulo.

Composto por **3 microsserviços independentes** (Catálogo, Carrinho e Pagamento), cada um com seu próprio banco PostgreSQL, comunicando-se via **REST/HTTP** dentro de uma rede Docker isolada.

> 📄 Trabalho individual — Jonathan Campos Machado Perobeli (SP3217639)

---

## 📸 Demonstração

![TechStore Screenshot](docs/screenshot.png)

---

## 🧭 Índice

- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Como Executar](#-como-executar)
- [Endpoints da API](#-endpoints-da-api)
- [Documentação Interativa](#-documentação-interativa-swagger)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Comunicação Entre Serviços](#-comunicação-entre-serviços)
- [Testes Realizados](#-testes-realizados)
- [Autor](#-autor)

---

## 🏗️ Arquitetura

```
                         ┌──────────────────────────────┐
                         │   Front-End  (nginx :3000)   │
                         └───────────────┬───────────────┘
                 ┌─────────────────────────────────────────┐
                 ▼                       ▼                  ▼
      ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
      │  Catálogo :8001   │   │  Carrinho :8002   │   │  Pagamento :8003  │
      └─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
                ▼                       ▼                       ▼
      ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
      │ PostgreSQL        │   │ PostgreSQL        │   │ PostgreSQL        │
      │ catalogo_db       │   │ carrinho_db       │   │ pagamento_db      │
      └──────────────────┘   └──────────────────┘   └──────────────────┘

         Todos os containers compartilham a rede virtual isolada
                          "ecommerce_net"
```

**Princípios aplicados:**
- 🔒 **Isolamento de falhas** — a queda de um serviço não derruba os demais
- 📈 **Escalabilidade independente** — cada serviço pode escalar separadamente
- 🗄️ **Banco de dados por serviço** — sem acoplamento direto entre schemas
- 🔁 **Consistência eventual** — reserva de estoque com rollback automático em caso de falha (padrão Saga simplificado)

---

## 🛠️ Tecnologias

| Camada | Tecnologia | Por quê |
|---|---|---|
| Linguagem | **Python 3.11** | Suporte nativo a `async/await` |
| Framework | **FastAPI** | Alta performance, documentação automática via Swagger |
| ORM | **SQLAlchemy 2.0** | Transações ACID, controle de concorrência (`SELECT FOR UPDATE`) |
| Banco de dados | **PostgreSQL 15** | Isolamento por serviço, propriedades ACID |
| Comunicação | **REST + httpx** | Baixo acoplamento, stateless, chamadas assíncronas entre serviços |
| Containerização | **Docker + Compose** | Ambientes idênticos, orquestração simplificada |
| Front-end | **HTML/CSS/JS + nginx** | Sem dependências externas; nginx como proxy reverso |

---

## 🚀 Como Executar

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado (inclui Docker Compose v2)

### Passo a passo

```bash
# 1. Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd ecommerce

# 2. Suba todos os containers
docker compose up --build
```

Aguarde até ver as mensagens de conexão bem-sucedida:

```
catalogo-1   | ✅ Catálogo: banco conectado
catalogo-1   | 🌱 Produtos de exemplo inseridos
carrinho-1   | ✅ Carrinho: banco conectado
pagamento-1  | ✅ Pagamento: banco conectado
```

### Acessar o sistema

Abra o navegador em:

```
http://localhost:3000
```

As bolinhas verdes no topo confirmam que os 3 microsserviços estão online.

### Parar os serviços

```bash
docker compose down        # mantém os dados
docker compose down -v     # remove containers + volumes (apaga dados)
```

---

## 📡 Endpoints da API

### Catálogo — `/api/catalogo`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/produtos` | Lista todos os produtos |
| `GET` | `/produtos?categoria=Eletrônicos` | Filtra por categoria |
| `GET` | `/produtos/{id}` | Busca produto por ID |
| `POST` | `/produtos` | Cria novo produto |
| `PATCH` | `/produtos/{id}/estoque?delta=-1` | Atualiza estoque (incremento/decremento) |

### Carrinho — `/api/carrinho`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/carrinho/{sessao_id}` | Visualiza itens do carrinho |
| `POST` | `/carrinho/{sessao_id}/itens` | Adiciona item (valida no Catálogo) |
| `DELETE` | `/carrinho/{sessao_id}/itens/{item_id}` | Remove item específico |
| `DELETE` | `/carrinho/{sessao_id}` | Limpa o carrinho |

### Pagamento — `/api/pagamento`

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/pagamento/processar` | Processa pagamento (orquestra Carrinho + Catálogo) |
| `GET` | `/pagamento/historico/{sessao_id}` | Histórico de transações |
| `GET` | `/pagamento/transacao/{id}` | Detalhe de uma transação |

---

## 📘 Documentação Interativa (Swagger)

Cada microsserviço expõe sua própria documentação OpenAPI:

- 📦 Catálogo: [http://localhost:3000/api/catalogo/docs](http://localhost:3000/api/catalogo/docs)
- 🛒 Carrinho: [http://localhost:3000/api/carrinho/docs](http://localhost:3000/api/carrinho/docs)
- 💳 Pagamento: [http://localhost:3000/api/pagamento/docs](http://localhost:3000/api/pagamento/docs)

---

## 📂 Estrutura do Projeto

```
ecommerce/
├── catalogo/
│   ├── main.py          # CRUD de produtos + controle de estoque
│   └── Dockerfile
├── carrinho/
│   ├── main.py          # Gerenciamento de sessões e itens
│   └── Dockerfile
├── pagamento/
│   ├── main.py          # Orquestração da transação (Saga simplificado)
│   └── Dockerfile
├── front/
│   ├── index.html        # Interface web (sem frameworks)
│   └── nginx.conf         # Proxy reverso para os 3 microsserviços
├── docker-compose.yml    # Orquestração dos 7 containers + rede isolada
└── README.md
```

---

## 🔄 Comunicação Entre Serviços

Fluxo completo de uma compra, demonstrando a comunicação distribuída:

1. **Adicionar ao carrinho** → `Carrinho` consulta o `Catálogo` via HTTP para validar preço e estoque
2. **Finalizar compra** → `Pagamento` consulta o `Carrinho` via HTTP para obter os itens
3. **Reserva de estoque** → `Pagamento` decrementa o estoque no `Catálogo`, item por item
4. **Falha na reserva?** → Rollback automático: todas as reservas anteriores são desfeitas
5. **Aprovado** → Transação registrada no banco de `Pagamento` e o carrinho é limpo

```
Cliente → Carrinho ──valida produto──► Catálogo
Cliente → Pagamento ──busca itens────► Carrinho
                     ──reserva estoque► Catálogo (com rollback em caso de falha)
```

---

## ✅ Testes Realizados

- **Funcionais** — todos os endpoints testados via Swagger e requisições reais
- **Tolerância a falhas** — Catálogo parado manualmente (`docker stop`): front exibiu erro isolado, demais serviços continuaram operando
- **Consistência de estoque** — compra aprovada decrementou o estoque corretamente no banco do Catálogo

---

## 👤 Autor

**Jonathan Campos Machado Perobeli** — SP3217639  
Computação Paralela e Distribuída — IFSP, Câmpus São Paulo  
Junho de 2026
