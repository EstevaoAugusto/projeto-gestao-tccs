# Projeto de Gestão de TCCs

Sistema full stack para gerenciamento de Trabalhos de Conclusão de Curso (TCCs), alunos, professores, cursos, departamentos e unidades acadêmicas.

O projeto é composto por:

- **Frontend:** Vue.js 3 com Tailwind CSS, Chart.js e Heroicons
- **Backend:** Django REST Framework
- **Banco de dados:** PostgreSQL
- **Orquestração:** Docker Compose

## Funcionalidades

### Painel geral (Dashboard)

- Cartões de resumo com totais de TCCs, alunos, professores e cursos.
- Indicadores por status: em elaboração, enviados, aprovados e reprovados.
- Gráficos interativos com Chart.js: distribuição por status (rosca), por tipo (barras horizontais), por semestre (barras verticais) e por curso (rosca).

### CRUD completo

Todas as entidades possuem listagem, cadastro, edição e exclusão:

- **TCCs** — busca por título/resumo, exportação CSV, upload de arquivo PDF, seleção de aluno/orientador/banca, badge de status.
- **Alunos** — busca por nome/matrícula, seleção de curso.
- **Professores** — busca por nome, seleção de departamento.
- **Cursos** — nome, sigla e código.
- **Departamentos** — nome, sigla e unidade acadêmica.
- **Unidades acadêmicas** — nome e sigla.

### Interface

- Sidebar responsiva com navegação entre as 7 páginas.
- Modais para formulários de cadastro e edição.
- Diálogo de confirmação para exclusões.
- Notificações toast de sucesso e erro.
- Skeleton loading durante carregamento de dados.
- Validação inline de erros retornados pela API.

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

Para popular o banco com dados iniciais (~100 alunos, 20 professores, 100 TCCs):

```bash
docker compose exec backend python load.py
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
| `frontend` | Vue.js/Vite | `5173` | Interface web SPA |
| `backend` | Django REST Framework | `8000` | API REST |
| `db` | PostgreSQL | `5432` | Banco de dados persistente |

Volumes configurados:

- `postgres_data`: persiste os dados do PostgreSQL.
- `frontend_node_modules`: mantém as dependências Node instaladas dentro do container.
- `./frontend:/app`: sincroniza o código-fonte do frontend.
- `./backend:/app`: sincroniza o código-fonte do backend.

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

O endpoint abaixo retorna dados agregados usados pelo painel geral:

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

## Stack do Frontend

| Biblioteca | Versão | Uso |
| --- | --- | --- |
| Vue.js | 3.5 | Framework SPA com Composition API (`<script setup>`) |
| Vue Router | 5.1 | Roteamento SPA com lazy loading |
| Tailwind CSS | 4.3 | Estilização via classes utilitárias (plugin Vite) |
| Chart.js + vue-chartjs | 4.5 / 5.3 | Gráficos do painel geral |
| Heroicons | 2.2 | Ícones SVG (outline 24px e solid 20px) |
| Vite | 8.0 | Bundler e dev server |

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
│   │   ├── assets/
│   │   │   └── main.css
│   │   ├── components/
│   │   │   ├── AppLayout.vue
│   │   │   ├── BaseModal.vue
│   │   │   ├── ConfirmDialog.vue
│   │   │   ├── StatusBadge.vue
│   │   │   └── ToastContainer.vue
│   │   ├── composables/
│   │   │   ├── useApi.js
│   │   │   └── useToast.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── AlunosView.vue
│   │   │   ├── CursosView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── DepartamentosView.vue
│   │   │   ├── ProfessoresView.vue
│   │   │   ├── TccsView.vue
│   │   │   └── UnidadesView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── index.html
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
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)
- [Vite](https://vite.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker Compose](https://docs.docker.com/compose/)

## Responsáveis

- Estevão Augusto da Fonseca Santos
- Guilherme Luiz de Azevedo
- Gabriel Ferreira de Castro
