# Backend para Estações Meteorológicas com FastAPI

Este projeto implementa um backend para coletar e gerenciar dados de estações meteorológicas, utilizando FastAPI para a API, SQLAlchemy como ORM e PostgreSQL como banco de dados.

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.8+**
* **PostgreSQL**: Um servidor PostgreSQL em execução.

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/pedroruthes/estacao_backend.git](https://github.com/pedroruthes/estacao_backend.git)
    cd estacao_backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto (na mesma pasta deste `README.md`) e adicione a URL de conexão do seu banco de dados PostgreSQL. Substitua `user`, `password`, `host`, `port` e `database_name` pelas suas credenciais.

    ```
    # .env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    ```

## Como Rodar o Backend

1.  **Certifique-se que seu servidor PostgreSQL está em execução.**

2.  **Rode a aplicação FastAPI:**
    Com o ambiente virtual ativado, execute o seguinte comando na raiz do projeto:

    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Acesse a documentação da API:**
    Uma vez que o servidor esteja rodando, você pode acessar a documentação interativa da API (Swagger UI) em:
    `http://127.0.0.1:8000/docs`

    Você também pode ver a documentação ReDoc em:
    `http://127.0.0.1:8000/redoc`