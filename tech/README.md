# Projeto FIAP

Este projeto é uma aplicação feita pelo aluno Kauan Silva para o Tech Challenge e utiliza Poetry para gerenciamento de dependências e Docker para facilitar o deploy e a configuração do ambiente.

## Pré-requisitos

Certifique-se de que você possui os seguintes itens instalados no seu sistema:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

## Passo a Passo para Configuração e Inicialização

### 1. Navegue para a pasta `tech`

```bash
cd tech
```

### 2. Caso seja a primeira vez configurando o ambiente, instale as dependências do projeto com:

```bash
poetry install
poetry shell
```

### 3. Para subir o aplicativo e todos os serviços associados (como o banco de dados) no Docker, execute:
```bash
docker-compose up
```

### 4. Após iniciar o Docker Compose, a aplicação estará disponível em:

- API: http://localhost:8000
- Documentação da API (Swagger): http://localhost:8000/docs
- Documentação da API (Redoc): http://localhost:8000/redoc