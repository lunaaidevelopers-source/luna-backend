# 🚀 Guia de Deployment - Luna Backend

## ✅ Correções Aplicadas

1. **Procfile criado** - Necessário para plataformas como Railway, Render, etc.
2. **Gunicorn adicionado** - Servidor WSGI para produção
3. **Tratamento de erros melhorado** - Verificações de configuração mais robustas
4. **Suporte a variáveis de ambiente** - Firebase pode ser configurado via env vars

## 📋 Variáveis de Ambiente Necessárias

Configure estas variáveis no painel do seu provedor de deployment:

### Obrigatórias:
- `GEMINI_API_KEY` - Chave da API do Google Gemini
- `PORT` - Porta do servidor (geralmente definida automaticamente pela plataforma)

### Firebase (escolha uma opção):

**Opção 1: Arquivo de configuração**
- Faça upload do arquivo `luna_config.json` para o servidor
- Configure `FIREBASE_CONFIG_PATH=luna_config.json` (ou deixe o padrão)

**Opção 2: Variável de ambiente (recomendado)**
- Configure `FIREBASE_CREDENTIALS_JSON` com o conteúdo JSON completo do arquivo de credenciais do Firebase
- Exemplo: `FIREBASE_CREDENTIALS_JSON='{"type":"service_account",...}'`

### Opcionais:
- `STRIPE_SECRET_KEY` - Chave secreta do Stripe (para pagamentos)
- `STRIPE_PUBLISHABLE_KEY` - Chave pública do Stripe
- `STRIPE_WEBHOOK_SECRET` - Secret do webhook do Stripe
- `FRONTEND_URLS` - URLs do frontend separadas por vírgula (ex: `https://tudominio.com,https://www.tudominio.com`)
- `FRONTEND_URL` - URL principal do frontend (para redirects do Stripe)
- `DEBUG` - `true` ou `false` (padrão: `true`)
- `RATE_LIMIT_STORAGE` - `memory://` para desenvolvimento ou `redis://...` para produção

## 🔧 Configuração no Railway/Render

### Railway:
1. Conecte o repositório GitHub
2. Adicione as variáveis de ambiente no painel
3. O Railway detectará automaticamente o `Procfile`

### Render:
1. Crie um novo "Web Service"
2. Conecte o repositório
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Adicione as variáveis de ambiente

## 🐛 Troubleshooting

### Erro: "Exited with status 1"
- Verifique se todas as variáveis de ambiente obrigatórias estão configuradas
- Verifique os logs para ver qual configuração está faltando
- Certifique-se de que o arquivo `luna_config.json` existe (se usar Opção 1)

### Erro: "Database not configured"
- Configure o Firebase usando uma das opções acima
- Verifique se as credenciais do Firebase estão corretas

### Erro: "Gemini API not configured"
- Configure a variável `GEMINI_API_KEY` com uma chave válida

### Build bem-sucedido mas deployment falha
- Verifique se o `Procfile` está na raiz do projeto
- Verifique se o `gunicorn` está no `requirements.txt`
- Verifique os logs de runtime para erros de inicialização

## 📝 Checklist de Deployment

- [ ] `Procfile` criado na raiz
- [ ] `gunicorn` adicionado ao `requirements.txt`
- [ ] `GEMINI_API_KEY` configurada
- [ ] Firebase configurado (arquivo ou variável de ambiente)
- [ ] `FRONTEND_URLS` configurada com os domínios de produção
- [ ] `PORT` será definida automaticamente pela plataforma
- [ ] Testar endpoint `/health` após deployment

## 🔍 Verificar Deployment

Após o deployment, teste:

```bash
curl https://seu-dominio.com/health
```

Deve retornar:
```json
{"status": "ok", "service": "Luna Backend"}
```


