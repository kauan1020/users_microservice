# Documentação do Projeto

## Desenho da Arquitetura

Este sistema foi projetado para resolver os problemas enfrentados por um restaurante que está expandindo, mas sofre com dificuldades no gerenciamento de pedidos devido ao aumento na demanda. A solução é composta por uma aplicação de autoatendimento integrada a uma infraestrutura escalável, utilizando **FastAPI** como framework backend, **SQLAlchemy** e **Alembic** para manipulação de dados e migração de banco, e **Kubernetes** (via Minikube) para orquestração de contêineres.

---

## 1. Requisitos do Negócio

### Melhoria na Experiência do Cliente:
- Totens de autoatendimento para permitir que os clientes façam seus pedidos sem intervenção de atendentes.
- Apresentação de produtos (lanche, bebida, acompanhamento, sobremesa) com preço e descrição.
- Sistema de pagamento integrado via QR Code (Mercado Pago).
- Rastreamento do status do pedido pelo cliente em tempo real: **Recebido → Em preparação → Pronto → Finalizado**.
- Notificação do cliente quando o pedido estiver pronto para retirada.

### Gestão para a Cozinha e Administração:
- Garantir que os pedidos pagos sejam enviados automaticamente para a cozinha, com visibilidade em painéis administrativos.
- Sistema administrativo para gerenciar produtos, clientes e promoções.

### Problema Atual de Performance:
- **Totem de autoatendimento enfrenta lentidão em horários de pico.**
- **Solução proposta**: Implementação de um sistema escalável, que usa Kubernetes e Horizontal Pod Autoscaler (HPA), garantindo maior disponibilidade e desempenho durante picos de uso.

---

## 2. Requisitos de Infraestrutura

### 2.1 Cluster Kubernetes
- **Orquestrador**: Minikube (ambiente local para desenvolvimento).
- **Recursos Kubernetes**:
  - **Deployments**: Cada serviço possui réplicas gerenciadas para disponibilidade.
  - **Horizontal Pod Autoscaler (HPA)**: Escala os pods de acordo com a carga da aplicação (CPU/memória).
  - **Secrets**: Para armazenar dados sensíveis, como credenciais do banco de dados e chave da API do Mercado Pago.
  - **ConfigMaps**: Para armazenar configurações não sensíveis, como categorias fixas (lanche, bebida, etc.).
  - **Persistent Volume (PV)** e **Persistent Volume Claim (PVC)**: Para garantir persistência de dados do PostgreSQL.

### 2.2 Serviços da Aplicação
O sistema é dividido em **quatro serviços principais**:

#### **2.2.1 Serviço de Pedidos**
- **API**: `/orders`
- **Funcionalidade**:
  - Realiza o checkout do pedido.
  - Retorna o status do pedido.
  - Atualiza o status do pedido conforme ele avança no fluxo.
  - Exclui pedidos.
- **Banco de Dados**:
  - Relaciona os pedidos aos produtos (muitos-para-muitos).
  - Salva histórico de status.
- **Exemplo**:
  - **POST** `/orders/checkout`: Cria um pedido.
  - **GET** `/orders`: Lista pedidos com prioridade (**Pronto > Em preparação > Recebido**).

#### **2.2.2 Serviço de Pagamento**
- **API**: `/payments`
- **Funcionalidade**:
  - Integração com Mercado Pago para gerar QR Code.
  - Gerencia o status do pagamento.
  - Recebe atualizações via Webhook.
- **Banco de Dados**:
  - Armazena transações e status (**Aprovado/Rejeitado**).
- **Exemplo**:
  - **POST** `/payments`: Gera QR Code.
  - **POST** `/payments/webhook`: Atualiza status do pagamento.

#### **2.2.3 Serviço de Produtos**
- **API**: `/products`
- **Funcionalidade**:
  - Gerencia produtos disponíveis no sistema (CRUD completo).
  - Filtra produtos por categoria.
- **Banco de Dados**:
  - Armazena categorias, descrições, preços e imagens.
- **Exemplo**:
  - **POST** `/products`: Cria novo produto.
  - **GET** `/products/{categoria}`: Lista produtos por categoria.

#### **2.2.4 Serviço de Usuários**
- **API**: `/users`
- **Funcionalidade**:
  - Gerencia o cadastro e dados de clientes.
  - Recupera informações por CPF.
- **Banco de Dados**:
  - Relaciona clientes aos pedidos realizados.
- **Exemplo**:
  - **POST** `/users`: Cadastra cliente.
  - **GET** `/users/cpf/{cpf}`: Busca cliente pelo CPF.

### 2.3 Banco de Dados
- **PostgreSQL**:
  - Gerenciado dentro do cluster Kubernetes, com armazenamento persistente configurado via PV/PVC.
  - Esquema relacional projetado para suportar consultas rápidas e integridade de dados.
  - **Migrações de Esquema**: Feitas utilizando **Alembic**, garantindo versionamento do banco.

---

## 3. Diagrama de Arquitetura

## 4. Configurações Detalhadas

### **ConfigMap**
- Contém informações não sensíveis:
  - URLs da API do Mercado Pago.
  - Categorias de produtos.

### **Secrets**
- Armazena credenciais e chaves sensíveis:
  - Credenciais do PostgreSQL.
  - Chave da API Mercado Pago.

### **Horizontal Pod Autoscaler (HPA)**
- Configurado para escalar dinamicamente:
  - **Pedidos API**: De 2 a 5 réplicas com base em 50% de uso da CPU.
  - **Pagamento API**: De 1 a 5 réplicas com base em 70% de uso da CPU.

### **Persistent Volume (PV)**
- Garante persistência dos dados do banco, mesmo em caso de reinicialização:
  - 10 GB de armazenamento local configurado no Minikube.

---

## 5. Solução para Problema de Performance

- **Problema**: Totem de autoatendimento sofre com lentidão durante picos de tráfego.
- **Solução**:
  - Implementação de **HPA** para escalar automaticamente o backend.
  - Configuração de **Ingress Controller** para balancear o tráfego entre os pods.
  - Banco de dados com armazenamento persistente para maior confiabilidade.

---

## 6. Tecnologias Utilizadas

- **Backend**: FastAPI, SQLAlchemy, Alembic.
- **Banco de Dados**: PostgreSQL.
- **Orquestração**: Kubernetes (via Minikube).
- **Integração de Pagamento**: Mercado Pago.