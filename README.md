# BI Perdas - Sistema Integrado

Sistema de Business Intelligence para controle de perdas por setor, filial e período.

## Funcionalidades

- Dashboard interativo com gráficos e métricas
- Controle de perdas por setor e filial
- Análise temporal (semanal, mensal, anual)
- Importação/exportação de dados CSV
- Gerenciamento de filiais
- Interface responsiva

## Tecnologias

- **Frontend**: React + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Flask + Python
- **Banco de Dados**: Supabase (PostgreSQL)
- **Deploy**: Vercel

## Configuração do Banco de Dados (Supabase)

1. Crie um projeto no [Supabase](https://supabase.com)
2. Execute o SQL do arquivo `supabase_schema.sql` no SQL Editor
3. Anote a URL do projeto e a Service Role Key

## Deploy no Vercel

### 1. Preparação

1. Faça fork deste repositório no GitHub
2. Clone o repositório localmente
3. Instale as dependências:
   ```bash
   cd bi-perdas-backend
   pip install -r requirements.txt
   ```

### 2. Configuração das Variáveis de Ambiente

No painel do Vercel, configure as seguintes variáveis de ambiente:

- `SUPABASE_URL`: URL do seu projeto Supabase
- `SUPABASE_KEY`: Service Role Key do Supabase
- `SECRET_KEY`: Chave secreta para o Flask (gere uma aleatória)

### 3. Deploy

1. Conecte seu repositório GitHub ao Vercel
2. Configure o projeto:
   - **Framework Preset**: Other
   - **Root Directory**: `bi-perdas-backend`
   - **Build Command**: (deixe vazio)
   - **Output Directory**: (deixe vazio)
3. Adicione as variáveis de ambiente
4. Faça o deploy

## Desenvolvimento Local

### Backend

```bash
cd bi-perdas-backend
source venv/bin/activate
pip install -r requirements.txt

# Crie um arquivo .env com as configurações
cp .env.example .env
# Edite o .env com suas configurações

python src/main.py
```

### Frontend (desenvolvimento separado)

```bash
cd bi-perdas-corrigido
pnpm install
pnpm run dev
```

## Estrutura do Projeto

```
bi-perdas-backend/
├── src/
│   ├── main.py          # Aplicação Flask principal
│   └── static/          # Arquivos estáticos do frontend
├── vercel.json          # Configuração do Vercel
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md

bi-perdas-corrigido/     # Código fonte do frontend
├── src/
│   ├── App.jsx          # Componente principal
│   └── ...
├── dist/                # Build de produção
└── package.json
```

## Schema do Banco de Dados

### Tabela: filiais
- id (bigserial, primary key)
- nome (text, not null, unique)
- endereco (text)
- cidade (text)
- estado (text)
- telefone (text)
- gerente (text)
- created_at (timestamptz)

### Tabela: lancamentos
- id (bigserial, primary key)
- data (date, not null)
- setor (text, not null)
- filial (text, not null)
- precoPerda (numeric, not null)
- precoVenda (numeric, not null)
- observacoes (text)
- created_at (timestamptz)

## API Endpoints

- `GET /api/lancamentos` - Lista todos os lançamentos
- `POST /api/lancamentos` - Cria novo lançamento
- `PUT /api/lancamentos/:id` - Atualiza lançamento
- `DELETE /api/lancamentos/:id` - Remove lançamento
- `GET /api/filiais` - Lista todas as filiais
- `POST /api/filiais` - Cria nova filial
- `PUT /api/filiais/:id` - Atualiza filial
- `DELETE /api/filiais/:id` - Remove filial
- `GET /api/health` - Health check

## Melhorias Implementadas

### Segurança
- Variáveis de ambiente para configurações sensíveis
- Validação de dados de entrada
- Tratamento adequado de erros
- CORS configurado adequadamente

### Performance
- Build otimizado para produção
- Componentes React otimizados
- Loading states implementados

### UX/UI
- Interface responsiva
- Feedback visual para ações
- Validação de formulários
- Estados de loading e erro

### Código
- Estrutura modular
- Tratamento de erros robusto
- Código limpo e documentado
- Separação adequada frontend/backend

