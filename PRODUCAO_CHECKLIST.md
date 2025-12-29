# 🚀 Checklist Completo para Lançamento em Produção

## 📋 Pré-requisitos

### 1. Domínio e DNS
- [ ] Comprar domínio (ex: `luna-ai.com`)
- [ ] Configurar DNS apontando para:
  - Frontend: `www.luna-ai.com` → Servidor de hospedagem do frontend
  - Backend: `api.luna-ai.com` → Servidor de hospedagem do backend
- [ ] Configurar certificado SSL/HTTPS (geralmente automático em plataformas modernas)

### 2. Contas e Serviços Externos

#### Google Cloud / Gemini API
- [ ] Verificar quota da API Gemini (aumentar se necessário)
- [ ] Usar chave de produção (não de teste)
- [ ] Configurar limites de uso e alertas

#### Firebase
- [ ] Verificar regras de segurança do Firestore
- [ ] Configurar domínios autorizados no Firebase Console
- [ ] Adicionar domínio de produção nas configurações do Firebase
- [ ] Verificar limites de uso

#### Stripe
- [ ] Mudar de modo teste para modo produção
- [ ] Obter chaves de produção (`sk_live_...` e `pk_live_...`)
- [ ] Configurar webhook de produção:
  - URL: `https://api.luna-ai.com/api/v1/payment/webhook`
  - Eventos: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
- [ ] Copiar webhook secret de produção (`whsec_...`)
- [ ] Configurar produtos e preços no Stripe Dashboard

---

## 🔧 Configuração do Backend

### 1. Variáveis de Ambiente (`.env`)

Cria/atualiza o ficheiro `.env` no backend:

```bash
# Google Gemini API (PRODUÇÃO)
GEMINI_API_KEY=sua_chave_producao_aqui

# Stripe (PRODUÇÃO - chaves live)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...  # Secret do webhook de produção

# Frontend URLs (PRODUÇÃO)
FRONTEND_URLS=https://luna-ai.com,https://www.luna-ai.com

# Servidor
PORT=5001
DEBUG=false  # ⚠️ IMPORTANTE: false em produção!

# Rate Limiting (PRODUÇÃO - usar Redis)
RATE_LIMIT_STORAGE=redis://localhost:6379
```

### 2. Firebase Config
- [ ] Verificar que `luna_config.json` está configurado corretamente
- [ ] Testar conexão com Firebase em produção

### 3. Redis (Recomendado para Rate Limiting)
- [ ] Instalar Redis no servidor
- [ ] Configurar Redis para iniciar automaticamente
- [ ] Testar conexão: `redis-cli ping`

### 4. Segurança
- [ ] Verificar que `DEBUG=false`
- [ ] Verificar CORS está configurado apenas para domínios de produção
- [ ] Configurar firewall (permitir apenas portas necessárias)
- [ ] Usar HTTPS obrigatório

---

## 🎨 Configuração do Frontend

### 1. Variáveis de Ambiente (`.env`)

Cria/atualiza o ficheiro `.env` no frontend:

```bash
# Backend API URL (PRODUÇÃO)
REACT_APP_API_URL=https://api.luna-ai.com
```

### 2. Firebase
- [ ] Verificar `src/firebase.js` está configurado corretamente
- [ ] Adicionar domínio de produção no Firebase Console:
  - Authentication → Settings → Authorized domains
  - Adicionar: `luna-ai.com`, `www.luna-ai.com`

### 3. Build de Produção
```bash
cd luna-frontend
npm run build
```
- [ ] Verificar que o build foi criado na pasta `build/`
- [ ] Testar build localmente antes de fazer deploy

---

## 🚢 Opções de Deploy

### Opção 1: Backend - Railway / Render / Fly.io (Recomendado)

**Vantagens:** Fácil, automático, HTTPS incluído

1. Conecta repositório GitHub
2. Configura variáveis de ambiente na plataforma
3. Define comando de start: `python3 app.py`
4. Deploy automático

**Variáveis a configurar:**
- `GEMINI_API_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `FRONTEND_URLS`
- `PORT` (geralmente definido pela plataforma)
- `DEBUG=false`
- `RATE_LIMIT_STORAGE` (se usar Redis)

### Opção 2: Backend - VPS (Ubuntu/Debian)

**Passos:**
1. Conectar ao servidor via SSH
2. Instalar dependências:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx redis-server
```

3. Clonar repositório
4. Criar ambiente virtual e instalar dependências
5. Configurar `.env`
6. Configurar Nginx como reverse proxy
7. Configurar SSL com Let's Encrypt (Certbot)
8. Configurar systemd service para iniciar automaticamente

### Opção 3: Frontend - Vercel (Recomendado)

**Vantagens:** Gratuito, fácil, HTTPS automático

1. Instalar Vercel CLI: `npm i -g vercel`
2. Fazer login: `vercel login`
3. Deploy: `vercel --prod`
4. Configurar variável de ambiente `REACT_APP_API_URL` no dashboard

### Opção 4: Frontend - Netlify

1. Conectar repositório
2. Build command: `npm run build`
3. Publish directory: `build`
4. Configurar variável de ambiente `REACT_APP_API_URL`

---

## ✅ Testes Antes do Lançamento

### Backend
- [ ] Testar endpoint `/health`: `curl https://api.luna-ai.com/health`
- [ ] Testar CORS (fazer requisição do frontend)
- [ ] Testar rate limiting
- [ ] Testar webhook do Stripe (usar Stripe CLI ou dashboard)

### Frontend
- [ ] Testar login/registro
- [ ] Testar chat (enviar mensagem)
- [ ] Testar pagamento (usar cartão de teste do Stripe)
- [ ] Testar histórico de conversas
- [ ] Testar em diferentes navegadores (Chrome, Firefox, Safari)
- [ ] Testar em mobile (responsividade)

### Integração
- [ ] Testar fluxo completo: Registro → Pagamento → Chat
- [ ] Verificar que mensagens são salvas no Firestore
- [ ] Verificar que subscrições são criadas no Stripe
- [ ] Testar cancelamento de subscrição

---

## 🔒 Segurança Final

- [ ] Verificar que todas as chaves de teste foram removidas
- [ ] Verificar que `DEBUG=false` no backend
- [ ] Verificar CORS está restrito apenas aos domínios de produção
- [ ] Verificar que ficheiros sensíveis (`.env`, `luna_config.json`) não estão no Git
- [ ] Configurar monitoramento de erros (ex: Sentry)
- [ ] Configurar logs de produção
- [ ] Configurar backup do Firestore (se necessário)

---

## 📊 Monitoramento e Manutenção

### Configurar Alertas
- [ ] Alertas de quota da API Gemini
- [ ] Alertas de erros do servidor
- [ ] Alertas de uso de recursos (CPU, memória)
- [ ] Alertas de pagamentos falhados no Stripe

### Logs
- [ ] Configurar sistema de logs (ex: CloudWatch, Logtail)
- [ ] Revisar logs regularmente

### Performance
- [ ] Monitorar tempo de resposta da API
- [ ] Monitorar uso de recursos
- [ ] Otimizar conforme necessário

---

## 🎯 Checklist Final

Antes de anunciar publicamente:

- [ ] Todos os testes passaram
- [ ] Domínio configurado e funcionando
- [ ] HTTPS funcionando (sem avisos)
- [ ] Pagamentos funcionando (testar com cartão real)
- [ ] Chat funcionando corretamente
- [ ] Histórico de conversas funcionando
- [ ] Autenticação funcionando
- [ ] Responsivo em mobile
- [ ] Termos de serviço e política de privacidade publicados
- [ ] Suporte ao cliente configurado (email, chat, etc.)

---

## 🆘 Em Caso de Problemas

### Backend não responde
1. Verificar logs do servidor
2. Verificar se processo está rodando
3. Verificar variáveis de ambiente
4. Verificar firewall

### Erro de CORS
1. Verificar `FRONTEND_URLS` no backend
2. Verificar que domínio do frontend está na lista
3. Verificar que está usando HTTPS

### Pagamentos não funcionam
1. Verificar chaves do Stripe (modo produção)
2. Verificar webhook está configurado corretamente
3. Verificar logs do Stripe Dashboard

### Firebase não funciona
1. Verificar `luna_config.json`
2. Verificar domínios autorizados no Firebase
3. Verificar regras de segurança do Firestore

---

## 📝 Notas Importantes

1. **Nunca commites** ficheiros `.env` ou `luna_config.json`
2. **Sempre use HTTPS** em produção
3. **Teste tudo** antes de lançar
4. **Tenha um plano de rollback** (saber como voltar atrás se algo der errado)
5. **Monitore** a aplicação nos primeiros dias após o lançamento

---

## 🎉 Pronto para Lançar!

Depois de completar todos os itens acima, a tua aplicação está pronta para o público!

**Boa sorte! 🚀**

