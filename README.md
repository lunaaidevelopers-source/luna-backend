# 🌙 Luna AI - Backend

Backend Flask para a aplicação Luna AI, fornecendo API para chat com IA, gestão de subscrições e integração com serviços externos.

## 🚀 Funcionalidades

- 💬 API de chat usando Google Gemini
- 🔐 Integração com Firebase Authentication
- 💳 Sistema de pagamentos com Stripe
- 📊 Rate limiting e segurança
- 🗄️ Armazenamento de conversas no Firestore
- 🔒 Headers de segurança configurados

## 📋 Pré-requisitos

- Python 3.8+
- Conta Google Cloud com Gemini API ativada
- Projeto Firebase configurado
- Conta Stripe (para pagamentos)

## 🛠️ Instalação Rápida

Para setup rápido, ver `SETUP.md`.

### Passos Detalhados

1. **Criar ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente:**
Cria um ficheiro `.env` na raiz do projeto (usa `env.template` como template):
```bash
# Google Gemini API
GEMINI_API_KEY=sua_chave_aqui

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend URLs (separadas por vírgula)
FRONTEND_URLS=http://localhost:3000

# Opcional
PORT=5001
DEBUG=true
RATE_LIMIT_STORAGE=memory://  # Para produção: redis://localhost:6379
```

4. **Configurar Firebase:**
- Coloca o ficheiro `luna_config.json` na raiz do projeto
- Este ficheiro NÃO deve ser commitado (já está no .gitignore)

5. **Iniciar o servidor:**
```bash
python3 app.py
```

Ou usando o script:
```bash
./start_backend.sh
```

O servidor estará disponível em `http://127.0.0.1:5001`

## 📡 Endpoints da API

### Chat
- `POST /api/v1/chat` - Enviar mensagem e receber resposta da IA
  - Body: `{ "message": "...", "persona": "...", "userId": "..." }`
  - Rate limit: 10 requests/minuto

### Histórico
- `GET /api/v1/chat/history?userId=...&persona=...` - Obter histórico de conversas
  - Rate limit: 30 requests/minuto

### Pagamentos
- `POST /api/v1/payment/create-checkout` - Criar sessão de checkout Stripe
- `POST /api/v1/payment/webhook` - Webhook do Stripe (não chamar diretamente)
- `GET /api/v1/payment/subscription-status?userId=...` - Verificar status de subscrição
- `POST /api/v1/payment/create-portal-session` - Criar sessão do Customer Portal

### Health Check
- `GET /health` - Verificar se o servidor está online

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `GEMINI_API_KEY` | Chave da API do Google Gemini | Sim |
| `STRIPE_SECRET_KEY` | Chave secreta do Stripe | Sim (para pagamentos) |
| `STRIPE_PUBLISHABLE_KEY` | Chave pública do Stripe | Sim (para pagamentos) |
| `STRIPE_WEBHOOK_SECRET` | Secret do webhook Stripe | Sim (para pagamentos) |
| `FRONTEND_URLS` | URLs do frontend (separadas por vírgula) | Não |
| `PORT` | Porta do servidor (padrão: 5001) | Não |
| `DEBUG` | Modo debug (true/false) | Não |
| `RATE_LIMIT_STORAGE` | Storage para rate limiting | Não |

### CORS

O CORS está configurado para permitir apenas:
- `http://localhost:3000` (desenvolvimento)
- `http://127.0.0.1:3000` (desenvolvimento)
- URLs configuradas em `FRONTEND_URLS` (produção)

### Rate Limiting

- **Chat**: 10 requests por minuto por IP
- **Histórico**: 30 requests por minuto por IP
- **Geral**: 200 requests por dia, 50 por hora

Para produção, recomenda-se usar Redis:
```bash
pip install redis
# E no .env: RATE_LIMIT_STORAGE=redis://localhost:6379
```

## 🚢 Deployment

### Opções Recomendadas

#### 1. Heroku
```bash
# Instalar Heroku CLI
heroku create luna-backend
heroku config:set GEMINI_API_KEY=...
heroku config:set STRIPE_SECRET_KEY=...
# ... outras variáveis
git push heroku main
```

#### 2. Railway
- Conecta o repositório
- Configura variáveis de ambiente
- Deploy automático

#### 3. DigitalOcean App Platform
- Conecta o repositório
- Configura variáveis de ambiente
- Define o comando de start: `python3 app.py`

#### 4. VPS (Ubuntu/Debian)
```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Configurar aplicação
# ... (ver guia de deployment completo)
```

### Configuração de Produção

1. **Desativar debug:**
```bash
DEBUG=false
```

2. **Configurar CORS:**
```bash
FRONTEND_URLS=https://tudominio.com,https://www.tudominio.com
```

3. **Usar Redis para rate limiting:**
```bash
RATE_LIMIT_STORAGE=redis://localhost:6379
```

4. **Configurar webhook do Stripe:**
- No Stripe Dashboard, configura o webhook para: `https://seu-dominio.com/api/v1/payment/webhook`
- Copia o webhook secret para `STRIPE_WEBHOOK_SECRET`

5. **HTTPS:**
- Usa um reverse proxy (Nginx) com certificado SSL
- Ou usa um serviço que fornece HTTPS automaticamente

## 🔒 Segurança

- ✅ CORS restritivo configurado
- ✅ Rate limiting ativado
- ✅ Validação de inputs
- ✅ Headers de segurança configurados
- ✅ Secrets em variáveis de ambiente
- ⚠️ Em produção, usar Redis para rate limiting
- ⚠️ Usar HTTPS obrigatório
- ⚠️ Configurar firewall adequadamente

## 🐛 Troubleshooting

### Erro "Firebase Connection"
- Verifica se `luna_config.json` existe e está correto
- Verifica permissões do ficheiro

### Erro "Gemini API"
- Verifica se `GEMINI_API_KEY` está correto
- Verifica quota da API no Google Cloud Console

### Erro "Stripe Webhook"
- Verifica se `STRIPE_WEBHOOK_SECRET` está correto
- Usa Stripe CLI para testar localmente: `stripe listen --forward-to localhost:5001/api/v1/payment/webhook`

### Rate Limiting não funciona
- Verifica se `flask-limiter` está instalado
- Em produção, configura Redis

## 📝 Estrutura do Projeto

```
Luna_Backend/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── luna_config.json       # Configuração Firebase (não commitado)
├── .env                  # Variáveis de ambiente (não commitado)
├── start_backend.sh      # Script para iniciar servidor
└── README.md             # Este ficheiro
```

## 📄 Licença

Este projeto é privado e proprietário.

## 🤝 Suporte

Para questões ou problemas, consulta a documentação no diretório do projeto ou contacta a equipa de desenvolvimento.
