# 🎮 GameVault — Plataforma de Jogos Online

## 1. Tema Escolhido

**GameVault** é uma plataforma de jogos online onde usuários podem se cadastrar, explorar um catálogo de jogos, escrever reviews e adicionar amigos para receber recomendações. O sistema utiliza **Polyglot Persistence** com 4 bancos de dados diferentes, cada um escolhido pelo tipo de dado que armazena.

---

## 2. Justificativa dos Bancos de Dados e Definição do Backend

### 🗄️ PostgreSQL (Banco Relacional — RDB)
**Dados armazenados:** Usuários (nome, email, senha, avatar, data de cadastro)

**Justificativa:** Dados de usuários possuem estrutura fixa e restrições de integridade como unicidade de email. O banco relacional garante transações ACID, constraints (PRIMARY KEY, UNIQUE, NOT NULL) e é ideal para dados estruturados que não mudam de schema. Operações de autenticação e atualização de perfil exigem consistência forte, que o PostgreSQL oferece nativamente.

### 📄 MongoDB (NoSQL — Document Storage — DB1)
**Dados armazenados:** Catálogo de jogos (nome, descrição, gêneros, plataformas, desenvolvedor, ano, imagem)

**Justificativa:** Jogos possuem dados semi-estruturados que variam entre si — um jogo de PC tem requisitos de sistema, um jogo mobile tem tamanho do app, um jogo de console tem classificação etária diferente. O modelo de documentos JSON permite campos flexíveis por documento sem necessidade de ALTER TABLE ou migrations. Índices em arrays (gêneros, plataformas) otimizam buscas com filtros múltiplos. A query `find({genres: "Ação"})` retorna todos os jogos de ação sem JOINs.

### 🔑 Redis (NoSQL — Key-Value Store — DB2)
**Dados armazenados:** Reviews/avaliações dos jogos e rankings de notas

**Justificativa:** Reviews são dados de leitura frequente que precisam de alta velocidade. Redis oferece estruturas de dados especializadas:
- **Hashes** para armazenar cada review (game_id, user_name, rating, comment)
- **Sets** para agrupar reviews por jogo (`game_reviews:{id}`)
- **Sorted Sets** para ranquear jogos por nota média (`game_ratings`)

A performance de O(1) para leitura/escrita é ideal para exibir ratings em tempo real. O Sorted Set permite consultar o top 10 jogos por nota com `ZREVRANGE` em O(log N).

### 🕸️ Neo4j (NoSQL — Graph Database — DB3)
**Dados armazenados:** Rede social de jogadores (amizades e recomendações)

**Justificativa:** Relações de amizade são naturalmente modeladas como grafos. Queries como:
- "Quem são meus amigos?" → traversal de 1 nível
- "Amigos em comum entre dois jogadores?" → interseção de vizinhos
- "Sugestões de amigos (amigos dos amigos)?" → traversal de 2 níveis

Estas operações são extremamente eficientes em bancos de grafos com complexidade O(k) onde k é o número de conexões, enquanto em bancos relacionais exigiriam múltiplos JOINs custosos. Neo4j usa a linguagem Cypher que expressa traversals de forma declarativa e intuitiva.

### Definição do Backend

O backend é implementado em **Node.js com Express**, dividido em 4 módulos de rotas independentes, cada um responsável por um domínio de dados:

| Serviço | Rota Base | Banco | Operações CRUD |
|---------|-----------|-------|----------------|
| Usuários | `/api/users` | PostgreSQL | POST, GET, GET/:id, PUT/:id, DELETE/:id |
| Jogos | `/api/games` | MongoDB | POST, GET (com filtros), GET/:id, PUT/:id, DELETE/:id |
| Reviews | `/api/reviews` | Redis | POST, GET/game/:id, GET/top, PUT/:id, DELETE/:id |
| Social | `/api/social` | Neo4j | POST/friends, GET/friends/:id, GET/suggestions/:id, DELETE/friends/:id1/:id2 |

**Arquitetura:**
```
Frontend (HTML/CSS/JS)
        ↕
Backend (Node.js + Express)
   ↕        ↕        ↕        ↕
PostgreSQL  MongoDB  Redis   Neo4j
(Usuários)  (Jogos) (Reviews)(Amizades)
```

---

## 3. Como Executar o Projeto

### Pré-requisitos

Instale na sua máquina:
- **Node.js** (v18 ou superior): https://nodejs.org

Crie contas gratuitas nos seguintes serviços online:

| Banco | Serviço Online Gratuito | Link |
|-------|------------------------|------|
| PostgreSQL | Neon (Free Tier) | https://neon.tech |
| MongoDB | MongoDB Atlas (M0 Free) | https://www.mongodb.com/atlas |
| Redis | Redis Cloud (Free 30MB) | https://redis.com/try-free/ |
| Neo4j | Neo4j AuraDB (Free) | https://console.neo4j.io |

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/GameVault.git
cd GameVault
```

### Passo 2 — Configurar as credenciais dos bancos

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cd backend
copy .env.example .env
```

Abra o arquivo `.env` e preencha com as URLs obtidas nos serviços online:

```env
POSTGRES_URL=postgresql://usuario:senha@host/neondb?sslmode=require
MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/gamevault
REDIS_URL=redis://default:senha@host:porta
NEO4J_URI=neo4j+s://id.databases.neo4j.io
NEO4J_USER=seu_usuario
NEO4J_PASSWORD=sua_senha
PORT=3000
```

#### Como obter cada credencial:

**PostgreSQL (Neon):**
1. Acesse https://console.neon.tech
2. Crie um projeto
3. Copie a Connection String em Dashboard → Connection Details

**MongoDB (Atlas):**
1. Acesse https://cloud.mongodb.com
2. Crie um cluster M0 Free
3. Crie um Database User (username e senha)
4. Em Network Access, adicione o IP `0.0.0.0/0`
5. Clique Connect → Drivers → copie a connection string
6. Substitua `<password>` pela senha criada e adicione `/gamevault` antes do `?`

**Redis (Redis Cloud):**
1. Acesse https://app.redislabs.com
2. Crie um database Free
3. Copie o Public Endpoint (host:porta) e a Default User Password
4. Monte a URL: `redis://default:SENHA@HOST:PORTA`

**Neo4j (AuraDB):**
1. Acesse https://console.neo4j.io
2. Crie uma instância AuraDB Free
3. **Salve imediatamente** o username e password (aparece só uma vez!)
4. Copie a Connection URI nos detalhes da instância

### Passo 3 — Instalar dependências

```bash
cd backend
npm install
```

### Passo 4 — Iniciar o servidor

```bash
node server.js
```

Se tudo estiver correto, aparece:
```
✅ PostgreSQL conectado — tabela users pronta
✅ MongoDB conectado — coleção games pronta
✅ Redis conectado
✅ Neo4j conectado

🎮 GameVault API rodando em http://localhost:3000
```

### Passo 5 — Abrir o frontend

Abra o arquivo `frontend/index.html` diretamente no navegador (duplo clique no arquivo).

### Passo 6 — Testar as funcionalidades

A interface possui 4 abas, cada uma conectada a um banco diferente:

| Aba | Banco | O que testar |
|-----|-------|-------------|
| 👤 Usuários | PostgreSQL | Cadastrar, editar, excluir usuários |
| 🎮 Jogos | MongoDB | Cadastrar jogos com gêneros e plataformas |
| ⭐ Reviews | Redis | Avaliar jogos com estrelas (1-5) e comentários |
| 🤝 Social | Neo4j | Adicionar amizades e ver sugestões de amigos |

---

## 4. Estrutura do Projeto

```
GameVault/
├── .gitignore
├── README.md
├── backend/
│   ├── .env.example          # Modelo de configuração (sem senhas)
│   ├── package.json          # Dependências do Node.js
│   ├── server.js             # Servidor Express principal
│   ├── config/
│   │   ├── postgres.js       # Conexão PostgreSQL
│   │   ├── mongodb.js        # Conexão MongoDB
│   │   ├── redis.js          # Conexão Redis
│   │   └── neo4j.js          # Conexão Neo4j
│   └── routes/
│       ├── users.js          # CRUD usuários (PostgreSQL)
│       ├── games.js          # CRUD jogos (MongoDB)
│       ├── reviews.js        # CRUD reviews (Redis)
│       └── social.js         # Amizades e recomendações (Neo4j)
└── frontend/
    └── index.html            # Interface completa do usuário
```

## 5. Tecnologias Utilizadas

| Camada | Tecnologia | Versão | Finalidade |
|--------|-----------|--------|------------|
| Frontend | HTML, CSS, JavaScript | - | Interface do usuário |
| Backend | Node.js + Express | 18+ | API REST |
| RDB | PostgreSQL | 17 | Dados de usuários (estruturados) |
| DB1 (NoSQL) | MongoDB | 8.0 | Catálogo de jogos (documentos) |
| DB2 (NoSQL) | Redis | 8.4 | Reviews e rankings (key-value) |
| DB3 (NoSQL) | Neo4j | 2026 | Amizades e recomendações (grafos) |

## 6. Dependências (package.json)

```json
{
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.21.0",
    "mongodb": "^6.9.0",
    "neo4j-driver": "^5.25.0",
    "pg": "^8.13.0",
    "redis": "^4.7.0"
  }
}
```

Todas as dependências são instaladas automaticamente com `npm install`.
