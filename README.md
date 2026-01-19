🖤 DarkIris Bot

DarkIris é uma assistente inteligente para Telegram, orientada a comunidades, lojas digitais e suporte híbrido (automático + humano).
Ela atua em grupos e privado, com memória persistente, comportamento estratégico e base preparada para multi-lojas, tickets e pagamentos.

🚀 Estado atual do projeto (FASE ATIVA)

✔ Bot Telegram operacional (Polling)
✔ Responde em privado e grupos
✔ Ativação por:

Reply direto à bot

Nome (DarkIris, Iris)

Palavras-chave estratégicas
✔ Memória persistente via Supabase
✔ Integração com OpenRouter (LLM)
✔ Infraestrutura pronta para:

Menus

Perfis (Admin / Cliente)
Lojas
Tickets
Pagamentos

🧠 Comportamento da DarkIris

Personalidade: discreta, firme e estratégica
Não inventa informações
Detecta intenção comercial
Redireciona para privado quando necessário
Mantém contexto por utilizador

📁 Estrutura do projeto
darkiris-bot/
│
├─ main.py                # Core do bot (handlers, IA, memória)
├─ menus.py               # Menus e navegação (em evolução)
├─ utils.py               # Funções utilitárias e helpers
│
├─ payments/
│   ├─ __init__.py        # Inicializador do módulo de pagamentos
│   ├─ misticpay.py       # Gateway fiat (planeado)
│   └─ crypto.py          # Crypto (USDT, TON – planeado)
│
├─ requirements.txt       # Dependências Python
├─ runtime.txt            # Versão Python
├─ README.md              # Documentação do projeto
└─ .gitignore

⚙️ Stack Tecnológica

Python 3.11
python-telegram-bot 21.x
OpenRouter (modelo atual: gpt-4o-mini)
Supabase (PostgreSQL + API)
Render (deploy)
Telegram Bot API

🔐 Variáveis de Ambiente (Render)

Obrigatórias:

BOT_TOKEN=telegram_bot_token
OPENROUTER_API_KEY=key_openrouter
OPENROUTER_MODEL=openai/gpt-4o-mini

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=service_role_key


⚠️ Usar SERVICE KEY (não anon) para permitir escrita na base.

🗄️ Base de Dados (Supabase)
Tabela principal (ativa)
darkiris_memory
Campo	Tipo	Descrição
id	uuid	PK
user_id	text	ID do utilizador Telegram
role	text	user ou assistant
content	text	Mensagem
created_at	timestamp	Data/hora UTC

A memória é carregada automaticamente nas interações.

💬 Ativação em Grupos

A DarkIris não fala sozinha.

Ela responde quando:

Alguém responde diretamente a uma mensagem dela

É mencionada (DarkIris, Iris)

Detecta palavras-chave estratégicas (preço, stock, ajuda, etc.)

🧩 Próximas Fases Planeadas

Menus interativos (InlineKeyboard)

Perfis:

Super_Admin

Admin (por loja/categoria)

Cliente

Multi-lojas:

XDeals

DarkMarket

AcademiaGhost

Sistema de tickets (manual + automático)

Pagamentos:

MisticPay (BRL / EUR)

Crypto (USDT TRC20, TON)

🧠 Filosofia do Projeto

DarkIris não é apenas um bot.
É uma interface inteligente entre comunidades, serviços e pessoas, com foco em:

Organização

Discrição

Escalabilidade

Controle humano quando necessário
## Status
Em desenvolvimento.
Powered by DarkLab | @AcademiaGhost