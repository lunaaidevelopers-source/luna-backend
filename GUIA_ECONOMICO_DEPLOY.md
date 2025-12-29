# 💰 Guia Económico de Deploy - Luna AI

## 🎯 Opções Mais Económicas (Gratuitas ou Muito Baratas)

### 1. Domínio 🌐

#### Opções Gratuitas (Limitadas)
- **Freenom** (.tk, .ml, .ga, .cf) - Gratuito, mas não recomendado para produção
- **No-IP** - Domínios dinâmicos gratuitos

#### Opções Baratas (Recomendado)
- **Namecheap** - ~$10-15/ano (.com)
- **Cloudflare Registrar** - Preço de custo (~$8-10/ano para .com)
- **Google Domains** - ~$12/ano (.com)
- **Porkbun** - ~$9/ano (.com)

**💡 Dica:** Começa sem domínio próprio usando subdomínios gratuitos das plataformas de hosting.

---

## 🖥️ Backend - Opções Gratuitas/Económicas

### Opção 1: **Render** (Recomendado - GRATUITO) ⭐

**Vantagens:**
- ✅ Plano gratuito disponível
- ✅ HTTPS automático
- ✅ Deploy automático do GitHub
- ✅ Variáveis de ambiente fáceis
- ✅ 750 horas grátis/mês (suficiente para 24/7)

**Limitações do plano gratuito:**
- ⚠️ Servidor "dorme" após 15min de inatividade (primeira requisição pode demorar)
- ⚠️ 512MB RAM
- ⚠️ Sem Redis incluído (pode usar memory://)

**Como fazer:**
1. Criar conta em [render.com](https://render.com)
2. Conectar repositório GitHub
3. Criar novo "Web Service"
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 app.py`
5. Adicionar variáveis de ambiente
6. Deploy!

**Custo:** **GRATUITO** (ou $7/mês para plano sem sleep)

---

### Opção 2: **Railway** (GRATUITO com limites)

**Vantagens:**
- ✅ $5 crédito grátis/mês
- ✅ Deploy automático
- ✅ HTTPS automático
- ✅ Muito fácil de usar

**Limitações:**
- ⚠️ Crédito pode acabar rápido se uso for alto
- ⚠️ Após crédito, precisa pagar

**Custo:** **GRATUITO** (até $5/mês) ou ~$5-20/mês

---

### Opção 3: **Fly.io** (GRATUITO)

**Vantagens:**
- ✅ Plano gratuito generoso
- ✅ Múltiplas regiões
- ✅ Muito rápido

**Limitações:**
- ⚠️ Configuração um pouco mais complexa
- ⚠️ Pode precisar de Dockerfile

**Custo:** **GRATUITO** (até certo limite de uso)

---

### Opção 4: **PythonAnywhere** (GRATUITO)

**Vantagens:**
- ✅ Específico para Python
- ✅ Fácil de configurar
- ✅ Plano gratuito disponível

**Limitações:**
- ⚠️ Domínio: `tudousuario.pythonanywhere.com`
- ⚠️ Limitado a 1 app web
- ⚠️ Requisições externas limitadas

**Custo:** **GRATUITO** (ou $5/mês para domínio próprio)

---

### Opção 5: **Heroku** (Pago, mas tem trial)

**Vantagens:**
- ✅ Muito popular e confiável
- ✅ Fácil de usar
- ✅ Boa documentação

**Limitações:**
- ❌ Não tem mais plano gratuito
- 💰 Custo: ~$7/mês (Eco Dyno)

**Custo:** **~$7/mês**

---

### ⭐ RECOMENDAÇÃO: **Render** (Gratuito)

Para começar, usa **Render** no plano gratuito. É suficiente para começar e depois podes fazer upgrade se necessário.

---

## 🎨 Frontend - Opções Gratuitas/Económicas

### Opção 1: **Vercel** (Recomendado - GRATUITO) ⭐

**Vantagens:**
- ✅ Plano gratuito generoso
- ✅ HTTPS automático
- ✅ Deploy automático do GitHub
- ✅ CDN global (muito rápido)
- ✅ Domínio gratuito: `tudousuario.vercel.app`
- ✅ Domínio próprio fácil de configurar

**Limitações:**
- ⚠️ Nenhuma relevante para começar

**Como fazer:**
1. Criar conta em [vercel.com](https://vercel.com)
2. Conectar repositório GitHub
3. Configurar:
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`
4. Adicionar variável de ambiente: `REACT_APP_API_URL`
5. Deploy!

**Custo:** **GRATUITO** (suficiente para a maioria dos casos)

---

### Opção 2: **Netlify** (GRATUITO)

**Vantagens:**
- ✅ Plano gratuito generoso
- ✅ HTTPS automático
- ✅ Deploy automático
- ✅ Domínio gratuito: `tudousuario.netlify.app`
- ✅ Formulários gratuitos (se precisar)

**Limitações:**
- ⚠️ Nenhuma relevante

**Custo:** **GRATUITO**

---

### Opção 3: **Cloudflare Pages** (GRATUITO)

**Vantagens:**
- ✅ Gratuito ilimitado
- ✅ CDN global
- ✅ Muito rápido
- ✅ Integração com Cloudflare

**Custo:** **GRATUITO**

---

### ⭐ RECOMENDAÇÃO: **Vercel** (Gratuito)

**Vercel** é a melhor opção: fácil, rápida e gratuita.

---

## 💾 Banco de Dados / Redis (Opcional)

### Para Rate Limiting

**Opção 1: Não usar Redis (Gratuito)**
- Usar `RATE_LIMIT_STORAGE=memory://` no backend
- ⚠️ Limitação: rate limiting não funciona entre múltiplas instâncias
- ✅ OK para começar com 1 servidor

**Opção 2: Upstash Redis (Gratuito)**
- 10,000 comandos/dia grátis
- Perfeito para rate limiting
- Fácil de configurar

**Custo:** **GRATUITO** (ou $0.20/100k comandos)

---

## 📊 Comparação de Custos

### Cenário 1: Totalmente Gratuito (Recomendado para começar)

| Serviço | Opção | Custo |
|---------|-------|-------|
| Domínio | Subdomínio gratuito | **$0** |
| Backend | Render (gratuito) | **$0** |
| Frontend | Vercel (gratuito) | **$0** |
| Redis | Memory (sem Redis) | **$0** |
| **TOTAL** | | **$0/mês** |

**URLs:**
- Frontend: `luna-ai.vercel.app`
- Backend: `luna-backend.onrender.com`

---

### Cenário 2: Com Domínio Próprio (Mais Profissional)

| Serviço | Opção | Custo |
|---------|-------|-------|
| Domínio | Namecheap/Cloudflare | **~$10/ano** |
| Backend | Render (gratuito) | **$0** |
| Frontend | Vercel (gratuito) | **$0** |
| Redis | Upstash (gratuito) | **$0** |
| **TOTAL** | | **~$0.83/mês** |

**URLs:**
- Frontend: `www.luna-ai.com`
- Backend: `api.luna-ai.com`

---

### Cenário 3: Sem Limitações (Quando crescer)

| Serviço | Opção | Custo |
|---------|-------|-------|
| Domínio | Namecheap | **~$10/ano** |
| Backend | Render ($7/mês sem sleep) | **$7/mês** |
| Frontend | Vercel (gratuito) | **$0** |
| Redis | Upstash (gratuito) | **$0** |
| **TOTAL** | | **~$7.83/mês** |

---

## 🚀 Plano de Ação Recomendado

### Fase 1: Começar Gratuitamente (Agora)

1. **Backend no Render:**
   - Criar conta Render
   - Deploy do backend
   - URL: `luna-backend.onrender.com`

2. **Frontend no Vercel:**
   - Criar conta Vercel
   - Deploy do frontend
   - URL: `luna-ai.vercel.app`

3. **Configurar:**
   - Frontend `.env`: `REACT_APP_API_URL=https://luna-backend.onrender.com`
   - Backend `.env`: `FRONTEND_URLS=https://luna-ai.vercel.app`

**Custo: $0/mês**

---

### Fase 2: Adicionar Domínio (Quando estiver funcionando)

1. Comprar domínio (~$10/ano)
2. Configurar DNS:
   - `www.luna-ai.com` → Vercel
   - `api.luna-ai.com` → Render
3. Atualizar variáveis de ambiente

**Custo: ~$0.83/mês**

---

### Fase 3: Upgrade (Se necessário)

1. Render sem sleep: $7/mês (se servidor dormir for problema)
2. Upstash Redis: $0 (gratuito é suficiente)

**Custo: ~$7.83/mês**

---

## 📝 Passo a Passo Detalhado

### Deploy Backend no Render

1. **Preparar código:**
   ```bash
   # Garantir que requirements.txt está atualizado
   cd Luna_Backend
   pip freeze > requirements.txt
   ```

2. **Criar conta Render:**
   - Ir para [render.com](https://render.com)
   - Sign up com GitHub

3. **Criar Web Service:**
   - New → Web Service
   - Conectar repositório GitHub
   - Selecionar branch `main` ou `master`

4. **Configurar:**
   - **Name:** `luna-backend`
   - **Region:** Escolher mais próximo (ex: Frankfurt)
   - **Branch:** `main`
   - **Root Directory:** (deixar vazio)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** (deixar vazio - o Render detecta o Procfile automaticamente)
     - OU usar: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

5. **Variáveis de Ambiente:**
   - `GEMINI_API_KEY` = (sua chave)
   - `STRIPE_SECRET_KEY` = (sua chave)
   - `STRIPE_PUBLISHABLE_KEY` = (sua chave)
   - `STRIPE_WEBHOOK_SECRET` = (sua chave)
   - `FRONTEND_URLS` = `https://luna-ai.vercel.app`
   - `PORT` = `5001` (ou deixar vazio, Render define automaticamente)
   - `DEBUG` = `false`
   - `RATE_LIMIT_STORAGE` = `memory://`

6. **Deploy!**
   - Clicar em "Create Web Service"
   - Aguardar deploy (5-10 minutos)
   - Copiar URL: `https://luna-backend.onrender.com`

---

### Deploy Frontend no Vercel

1. **Preparar código:**
   ```bash
   cd luna-frontend
   npm run build  # Testar build localmente
   ```

2. **Criar conta Vercel:**
   - Ir para [vercel.com](https://vercel.com)
   - Sign up com GitHub

3. **Importar Projeto:**
   - Add New → Project
   - Importar repositório GitHub
   - Selecionar `luna-frontend`

4. **Configurar:**
   - **Framework Preset:** Create React App
   - **Root Directory:** `./` (deixar vazio)
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   - **Install Command:** `npm install`

5. **Variáveis de Ambiente:**
   - `REACT_APP_API_URL` = `https://luna-backend.onrender.com`

6. **Deploy!**
   - Clicar em "Deploy"
   - Aguardar (2-5 minutos)
   - Copiar URL: `https://luna-ai.vercel.app`

---

## 🔧 Configurar Domínio Próprio (Opcional)

### No Vercel (Frontend)

1. Ir para Project Settings → Domains
2. Adicionar domínio: `www.luna-ai.com`
3. Copiar registros DNS mostrados
4. Configurar no registrador de domínio:
   - Tipo: `CNAME`
   - Nome: `www`
   - Valor: `cname.vercel-dns.com`

### No Render (Backend)

1. Ir para Web Service → Settings → Custom Domain
2. Adicionar domínio: `api.luna-ai.com`
3. Copiar registros DNS
4. Configurar no registrador:
   - Tipo: `CNAME`
   - Nome: `api`
   - Valor: (valor fornecido pelo Render)

---

## ✅ Checklist Final

- [ ] Backend deployado no Render
- [ ] Frontend deployado no Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Testar frontend acessa backend
- [ ] Testar login/registro
- [ ] Testar chat
- [ ] (Opcional) Domínio próprio configurado
- [ ] (Opcional) HTTPS verificado

---

## 🆘 Troubleshooting

### Backend "dorme" no Render
- **Problema:** Primeira requisição demora ~30s
- **Solução:** Upgrade para plano pago ($7/mês) ou usar serviço de "ping" gratuito (ex: UptimeRobot)

### Erro de CORS
- Verificar `FRONTEND_URLS` no backend inclui URL do frontend
- Verificar que está usando HTTPS (não HTTP)

### Build falha
- Verificar logs no Render/Vercel
- Testar build localmente primeiro
- Verificar todas as dependências estão no `requirements.txt` ou `package.json`

---

## 💡 Dicas Finais

1. **Começa gratuito** - Testa tudo antes de gastar dinheiro
2. **Monitora uso** - Acompanha métricas nas plataformas
3. **Backup** - Mantém código no GitHub
4. **Documenta** - Anota todas as configurações
5. **Testa** - Testa tudo antes de anunciar

**Boa sorte com o deploy! 🚀**



