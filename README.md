# Projeto de Gestão de TCCs

Sistema full stack para gerenciamento de Trabalhos de Conclusão de Curso (TCCs), alunos, professores, cursos, departamentos e unidades acadêmicas.

O projeto é composto por:

- **Frontend:** Vue.js com Vite
- **Backend:** Django REST Framework
- **Banco de dados:** PostgreSQL
- **Orquestração:** Docker Compose

Além da API principal, o projeto possui uma página inicial de verificação em `http://localhost:5173` que confirma se frontend, backend e banco de dados estão funcionando corretamente após a subida dos containers.

## Funcionalidades

- Listagem e busca de alunos, professores, cursos, departamentos, unidades acadêmicas e TCCs.
- Cadastro e edição de TCCs.
- Upload de arquivo PDF no cadastro de TCC.
- Alteração de status do TCC.
- Endpoint de estatísticas para dashboard.
- Endpoint de saúde da aplicação.
- Ambiente Docker com containers separados para frontend, backend e banco de dados.

## Requisitos Mínimos

Para executar com Docker:

- Docker
- Docker Compose v2, usando o comando `docker compose`

Para execução manual, sem Docker:

- Python 3.13 ou compatível com Django 6
- Node.js 22.18 ou superior, conforme definido em `frontend/package.json`
- PostgreSQL 16 ou SQLite para desenvolvimento local
- `pip`
- `npm`

## Como Executar com Docker

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Após a inicialização, acesse:

- Frontend: `http://localhost:5173`
- Backend/API: `http://localhost:8000/api/`
- Health check da API: `http://localhost:8000/api/health/`
- PostgreSQL: `localhost:5432`

Durante a execução, os containers exibem mensagens de saúde no terminal, por exemplo:

```text
[health] db=starting postgres_port=5432
[health] backend=starting django_port=8000 waiting_for_database=db:5432
[health] backend=healthy database=connected
[health] frontend=starting vite_port=5173 backend_url=http://backend:8000
[health] frontend=healthy vite_port=5173
```

Para parar os containers:

```bash
docker compose down
```

Para remover também os volumes persistentes, incluindo os dados do PostgreSQL:

```bash
docker compose down -v
```

## Variáveis de Ambiente

O Docker Compose já define valores padrão para desenvolvimento. O arquivo de exemplo do backend está em:

```text
backend/.env.example
```

Exemplo:

```env
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=*

POSTGRES_DB=tcc_db
POSTGRES_USER=tcc_user
POSTGRES_PASSWORD=tcc_password
DB_HOST=db
DB_PORT=5432
```

No ambiente Docker, o serviço `backend` usa `db` como host do PostgreSQL porque os containers se comunicam pela rede interna do Compose.

## Serviços Docker

O arquivo `docker-compose.yml` define três serviços principais:

| Serviço | Tecnologia | Porta | Descrição |
| --- | --- | --- | --- |
| `frontend` | Vue.js/Vite | `5173` | Interface web e página de status da aplicação |
| `backend` | Django REST Framework | `8000` | API REST e endpoint de saúde |
| `db` | PostgreSQL | `5432` | Banco de dados persistente |

Volumes configurados:

- `postgres_data`: persiste os dados do PostgreSQL.
- `frontend_node_modules`: mantém as dependências Node instaladas dentro do container.
- `./frontend:/app`: sincroniza o código-fonte do frontend.
- `./backend:/app`: sincroniza o código-fonte do backend.

## Página de Saúde

A página inicial do frontend, disponível em `http://localhost:5173`, mostra o estado de:

- Vue.js/Vite
- Django REST Framework
- PostgreSQL

Ela consulta o endpoint:

```text
GET /api/health/
```

Resposta esperada:

```json
{
  "status": "healthy",
  "services": {
    "backend": {
      "status": "healthy",
      "message": "Django REST Framework respondendo."
    },
    "database": {
      "status": "healthy",
      "message": "PostgreSQL conectado e respondendo."
    }
  }
}
```

## Endpoints da API

Base URL local:

```text
http://localhost:8000/api/
```

| Recurso | Endpoint | Métodos principais |
| --- | --- | --- |
| Health check | `/api/health/` | `GET` |
| Unidades Acadêmicas | `/api/unidades-academicas/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Departamentos | `/api/departamentos/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Cursos | `/api/cursos/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Alunos | `/api/alunos/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Professores | `/api/professores/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| TCCs | `/api/tccs/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Estatísticas | `/api/tccs/estatisticas/` | `GET` |

Os endpoints de alunos, professores e TCCs possuem busca via query string:

```text
/api/alunos/?search=nome-ou-matricula
/api/professores/?search=nome
/api/tccs/?search=titulo-ou-resumo
```

## Cadastro de TCCs

Ao enviar um TCC com arquivo PDF, use `multipart/form-data` para o campo `arquivo`.

Campos principais do modelo `TCC`:

- `titulo`
- `resumo`
- `palavras_chave`
- `tipo`
- `idioma`
- `aluno`
- `orientador`
- `coorientador`
- `presidente`
- `primeiro_membro`
- `segundo_membro`
- `semestre_letivo_defesa`
- `status`
- `arquivo`

Status disponíveis:

| Valor | Status |
| --- | --- |
| `0` | Em Elaboração |
| `1` | Enviado |
| `2` | Aprovado |
| `3` | Reprovado |

Tipos disponíveis:

| Valor | Tipo |
| --- | --- |
| `MONOGRAFIA` | Monografia |
| `RELATORIO_ESTAGIO` | Relatório de Estágio |
| `RELATORIO_TECNICO` | Relatório Técnico |
| `ARTIGO` | Artigo |

Idiomas disponíveis:

| Valor | Idioma |
| --- | --- |
| `PT` | Português |
| `EN` | Inglês |

## Estatísticas

O endpoint abaixo retorna dados agregados para dashboards:

```text
GET /api/tccs/estatisticas/
```

Exemplo de resposta:

```json
{
  "total_geral": 10,
  "por_status": {
    "Aprovado": 3,
    "Em Elaboração": 2
  },
  "por_tipo": {
    "Monografia": 4,
    "Artigo": 2
  },
  "por_idioma": {
    "Português": 8,
    "Inglês": 2
  },
  "por_orientador": {
    "Prof. Dr. Ricardo": 4
  }
}
```

## Como Executar Manualmente

O uso recomendado é com Docker. Ainda assim, é possível executar os serviços manualmente.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python load.py
python manage.py runserver 0.0.0.0:8000
```

No Windows, a ativação do ambiente virtual é:

```bash
.venv\Scripts\activate
```

Sem variáveis PostgreSQL definidas, o Django usa SQLite como fallback de desenvolvimento.

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Estrutura do Projeto

```text
.
├── backend/
│   ├── core/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── tcc_project/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── load.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── assets/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── README.md
└── README.old.md
```

## Comandos Úteis

Subir o projeto:

```bash
docker compose up --build
```

Subir em segundo plano:

```bash
docker compose up --build -d
```

Ver logs:

```bash
docker compose logs -f
```

Ver status dos containers:

```bash
docker compose ps
```

Executar migrações manualmente no container:

```bash
docker compose exec backend python manage.py migrate
```

Popular dados iniciais:

```bash
docker compose exec backend python load.py
```

Abrir shell Django:

```bash
docker compose exec backend python manage.py shell
```

## Material de Apoio

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [Vue.js](https://vuejs.org/)
- [Vite](https://vite.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker Compose](https://docs.docker.com/compose/)

## Responsáveis

- Estevão Augusto da Fonseca Santos
- Guilherme Luiz de Azevedo
- Gabriel Ferreira de Castro