# 📝 Taskly — Task Manager API & Web App

Aplicação full-stack de gerenciamento de tarefas, construída para praticar e demonstrar conceitos usados no mercado: API REST com autenticação, banco de dados relacional, testes automatizados e um frontend completo consumindo tudo isso em tempo real.

🔗 **[Acesse a aplicação ao vivo](https://task-manager-zeta-ecru-68.vercel.app)**
📘 **[Documentação interativa da API (Swagger)](https://task-manager-api-9tvh.onrender.com/docs)**

> ⚠️ O backend está hospedado no plano gratuito do Render, que "dorme" após um período de inatividade. A primeira requisição pode levar até 1 minuto para responder enquanto o servidor reinicia.

---

## ✨ Funcionalidades

### Autenticação e segurança
- Cadastro e login de usuários com **JWT** (JSON Web Token)
- Senhas protegidas com **hash bcrypt** (nunca armazenadas em texto puro)
- Rotas protegidas — cada usuário só acessa suas próprias tarefas
- Segredos (chaves, credenciais de banco) mantidos fora do código-fonte via variáveis de ambiente

### Gerenciamento de tarefas (CRUD completo)
- Criar, listar, editar, excluir e marcar tarefas como concluídas
- **Prioridade** (baixa / média / alta) com indicação visual
- **Data de vencimento**, com destaque para tarefas atrasadas
- **Busca** de tarefas por texto em tempo real
- Filtros por status: todas / pendentes / concluídas
- **Sugestões de tarefas** baseadas no período do dia (manhã / tarde / noite), evitando repetir tarefas já existentes

### Interface e experiência do usuário
- Tema **claro/escuro** com preferência salva
- Notificações toast para ações (criar, editar, excluir)
- Estados de carregamento (skeleton loading e spinners)
- Modais de confirmação customizados para ações destrutivas
- Atalhos de teclado (`/` para buscar, `N` para nova tarefa, `Esc` para fechar modais)
- Painel lateral com progresso visual (anel de conclusão) e estatísticas
- Design responsivo

---

## 🛠️ Tecnologias

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — framework web assíncrono em Python
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para acesso ao banco de dados
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [PostgreSQL](https://www.postgresql.org/) (produção) / SQLite (desenvolvimento local)
- [Passlib](https://passlib.readthedocs.io/) + bcrypt — hash de senhas
- [python-jose](https://github.com/mpdavis/python-jose) — geração e validação de tokens JWT
- [Pytest](https://docs.pytest.org/) — testes automatizados

**Frontend**
- HTML5, CSS3 e JavaScript puro (sem frameworks)
- Fetch API para comunicação assíncrona com o backend
- CSS moderno: variáveis customizadas, animações, `conic-gradient`, `backdrop-filter`

**Infraestrutura**
- Backend hospedado no [Render](https://render.com/)
- Frontend hospedado na [Vercel](https://vercel.com/)
- Versionamento com Git/GitHub

---

## 📂 Estrutura do projeto
task-manager/
├── main.py # Rotas da API e configuração do FastAPI
├── models.py # Modelos do banco de dados (SQLAlchemy)
├── schemas.py # Schemas de validação (Pydantic)
├── database.py # Configuração da conexão com o banco
├── auth.py # Lógica de hash de senha e tokens JWT
├── requirements.txt # Dependências Python
├── tests/
│ └── test_main.py # Testes automatizados (Pytest)
├── conftest.py # Configuração de testes
└── frontend/
├── index.html # Tela de login e cadastro
├── dashboard.html # Painel principal de tarefas
├── css/
│ └── style.css # Estilos da aplicação
└── js/
├── api.js # Comunicação com a API
├── auth.js # Lógica de login/cadastro
├── app.js # Lógica do dashboard
└── theme.js # Alternância de tema


---

## 🚀 Rodando localmente

### Pré-requisitos
- Python 3.10+
- Git

### Backend

```bash
# Clone o repositório
git clone https://github.com/PedroSchimidt/task-manager.git
cd task-manager

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env na raiz com:
# SECRET_KEY=uma_chave_secreta_aleatoria

# Rode o servidor
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

### Frontend

Abra `frontend/index.html` com uma extensão como o **Live Server** do VS Code (ou qualquer servidor estático). Por padrão, o frontend aponta para a API em produção — para testar contra o backend local, altere a constante `API_URL` em `frontend/js/api.js` para `http://127.0.0.1:8000`.

### Rodando os testes

```bash
pytest
```

---

## 📌 Sobre este projeto

Este projeto foi construído como parte de um processo de retomada e aprofundamento de conhecimentos em Python e desenvolvimento web, cobrindo desde os fundamentos de uma API REST até práticas usadas em ambientes profissionais: autenticação segura, testes automatizados, variáveis de ambiente, CORS, banco de dados relacional e deploy em produção.
