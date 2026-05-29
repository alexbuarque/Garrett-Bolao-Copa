# Bolão da Copa 2026 ⚽

Aplicativo de bolão para a Copa do Mundo 2026, construído com **Streamlit** e **Supabase**.

## Funcionalidades

- 🔐 Cadastro e login com email/senha (Supabase Auth)
- ⚽ Palpites para todos os 72 jogos da fase de grupos (12 grupos × 6 jogos)
- 🌟 Palpites especiais: Artilheiro, MVP e Melhor Goleiro (10 pts cada)
- 🏆 Ranking em tempo real com breakdown de pontos
- 🔧 Painel admin para inserir resultados e recalcular pontos automaticamente

## Sistema de Pontuação

| Acerto | Pontos |
|--------|--------|
| Placar exato | **5 pts** |
| Vencedor/empate (placar errado) | **3 pts** |
| Gols de um time corretos (sem placar exato) | **+1 pt por time** |
| Artilheiro correto | **10 pts** |
| MVP correto | **10 pts** |
| Melhor Goleiro correto | **10 pts** |

## Configuração

### 1. Supabase

1. Crie um projeto em [supabase.com](https://supabase.com)
2. Vá em **SQL Editor** e execute o arquivo `schema.sql` completo
3. Em **Authentication → Settings**, desative "Email Confirm" se quiser registro imediato (para um bolão interno)
4. Anote as chaves em **Project Settings → API**:
   - `URL` → `SUPABASE_URL`
   - `anon public` → `SUPABASE_KEY`
   - `service_role secret` → `SUPABASE_SERVICE_KEY`

### 2. Secrets do Streamlit

Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e preencha:

```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "eyJ..."          # anon key
SUPABASE_SERVICE_KEY = "eyJ..."  # service_role key
ADMIN_PASSWORD = "senha-secreta"
```

> ⚠️ Nunca faça commit do `secrets.toml` real. Ele já está no `.gitignore`.

### 3. Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 4. Deploy no Streamlit Community Cloud

1. Faça push do repositório para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte o repo
3. Configure os secrets em **App settings → Secrets** (cole o conteúdo do `secrets.toml`)
4. Deploy!

### 5. Inicializar os jogos

Após o primeiro deploy:
1. Acesse o **Painel Admin** (`/admin`)
2. Digite a senha do admin
3. Na aba **⚙️ Inicializar**, clique em "Inicializar jogos" para popular a tabela `matches`

## Estrutura do Projeto

```
├── app.py                    # Ponto de entrada + navegação
├── pages/
│   ├── login.py              # Login e cadastro
│   ├── palpites.py           # Palpites dos jogos
│   ├── especiais.py          # Palpites especiais
│   ├── ranking.py            # Ranking
│   └── admin.py              # Painel admin
├── utils/
│   ├── supabase_client.py    # Clientes Supabase
│   ├── auth.py               # Helpers de autenticação
│   ├── data.py               # Operações de banco
│   └── scoring.py            # Cálculo de pontos
├── data/
│   └── matches.py            # Fixtures dos 72 jogos
├── schema.sql                # Schema SQL para o Supabase
├── requirements.txt
└── .streamlit/
    └── secrets.toml.example  # Template de secrets
```

## Grupos da Copa 2026

| Grupo | Times |
|-------|-------|
| A | USA, El Salvador, Polônia, Austrália |
| B | México, Jamaica, Sérvia, Argélia |
| C | Canadá, Honduras, Croácia, Costa do Marfim |
| D | Argentina, Panamá, Turquia, Japão |
| E | Brasil, Trindade e Tobago, Holanda, Marrocos |
| F | Colômbia, Costa Rica, Bélgica, Coreia do Sul |
| G | Uruguai, Nova Zelândia, Alemanha, Nigéria |
| H | Equador, Portugal, Irã, Senegal |
| I | Chile, França, Arábia Saudita, Egito |
| J | Paraguai, Inglaterra, Catar, Camarões |
| K | Venezuela, Espanha, Iraque, Mali |
| L | Itália, Suíça, Uzbequistão, África do Sul |

> ⚠️ Os grupos acima são uma aproximação com base nos classificados confirmados. A distribuição exata por grupo pode ser ajustada diretamente no banco de dados Supabase (tabela `matches`) após o sorteio oficial.
