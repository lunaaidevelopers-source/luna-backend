# 📤 Como Enviar Código para GitHub e Fazer Deploy

## 🎯 Objetivo
Enviar o código para o GitHub para depois fazer deploy no Render e Vercel.

---

## 📋 Passo 1: Criar Conta/Repositórios no GitHub

1. **Criar conta no GitHub** (se ainda não tiver):
   - Ir para [github.com](https://github.com)
   - Sign up (é gratuito)

2. **Criar 2 repositórios novos:**
   - `luna-backend` (para o backend)
   - `luna-frontend` (para o frontend)
   
   **Como criar:**
   - Clicar no "+" no canto superior direito
   - "New repository"
   - Nome: `luna-backend` (ou `luna-frontend`)
   - **NÃO** marcar "Initialize with README" (já temos código)
   - Clicar "Create repository"
   - Repetir para o segundo repositório

---

## 🔧 Passo 2: Preparar Backend para GitHub

Abre o terminal e executa:

```bash
cd /Users/matildematosa/Desktop/Luna_Backend

# Inicializar git
git init

# Adicionar todos os ficheiros (exceto os que estão no .gitignore)
git add .

# Fazer primeiro commit
git commit -m "Initial commit - Luna Backend"

# Adicionar repositório remoto (substitui TUA_CONTA pelo teu username do GitHub)
git remote add origin https://github.com/TUA_CONTA/luna-backend.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** Substitui `TUA_CONTA` pelo teu username do GitHub!

---

## 🎨 Passo 3: Preparar Frontend para GitHub

O frontend já tem git, só precisa fazer commit e push:

```bash
cd /Users/matildematosa/Desktop/luna-frontend

# Adicionar todas as mudanças
git add .

# Fazer commit
git commit -m "Initial commit - Luna Frontend"

# Adicionar repositório remoto (substitui TUA_CONTA pelo teu username)
git remote add origin https://github.com/TUA_CONTA/luna-frontend.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** Substitui `TUA_CONTA` pelo teu username do GitHub!

---

## 🚀 Passo 4: Deploy no Render (Backend)

Agora que o código está no GitHub:

1. **Ir para Render:**
   - [dashboard.render.com](https://dashboard.render.com)
   - Clicar "New" → "Web Service"

2. **Conectar GitHub:**
   - Clicar "GitHub"
   - Autorizar Render
   - Selecionar repositório `luna-backend`

3. **Configurar:**
   - **Name:** `luna-backend`
   - **Region:** Escolher mais próximo
   - **Branch:** `main`
   - **Root Directory:** (deixar vazio)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** (deixar vazio - o Render detecta o Procfile automaticamente)
     - OU usar: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

4. **Variáveis de Ambiente:**
   - Clicar "Advanced" → "Add Environment Variable"
   - Adicionar cada uma:
     ```
     GEMINI_API_KEY=sua_chave
     STRIPE_SECRET_KEY=sk_test_...
     STRIPE_PUBLISHABLE_KEY=pk_test_...
     STRIPE_WEBHOOK_SECRET=whsec_...
     FRONTEND_URLS=https://luna-ai.vercel.app
     DEBUG=false
     RATE_LIMIT_STORAGE=memory://
     ```

5. **Deploy:**
   - Clicar "Create Web Service"
   - Aguardar deploy (5-10 minutos)
   - Copiar URL gerada

---

## 🎨 Passo 5: Deploy no Vercel (Frontend)

1. **Ir para Vercel:**
   - [vercel.com](https://vercel.com)
   - Sign up com GitHub

2. **Importar Projeto:**
   - "Add New" → "Project"
   - Selecionar repositório `luna-frontend`

3. **Configurar:**
   - **Framework Preset:** Create React App
   - **Root Directory:** (deixar vazio)
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

4. **Variáveis de Ambiente:**
   - Adicionar: `REACT_APP_API_URL`
   - Valor: URL do backend do Render (ex: `https://luna-backend.onrender.com`)

5. **Deploy:**
   - Clicar "Deploy"
   - Aguardar (2-5 minutos)
   - Copiar URL gerada

---

## ✅ Verificar

1. **Backend:**
   - Testar: `https://sua-url.onrender.com/health`
   - Deve retornar: `{"status":"ok","service":"Luna Backend"}`

2. **Frontend:**
   - Abrir URL do Vercel
   - Deve carregar a aplicação

3. **Atualizar variáveis:**
   - No Vercel, atualizar `REACT_APP_API_URL` com a URL real do backend
   - No Render, atualizar `FRONTEND_URLS` com a URL real do frontend

---

## 🆘 Problemas Comuns

### Erro ao fazer push
- Verificar que criaste o repositório no GitHub primeiro
- Verificar que o username está correto na URL

### Erro de autenticação GitHub
- Pode precisar de token de acesso pessoal
- GitHub → Settings → Developer settings → Personal access tokens

### Build falha no Render
- Verificar logs no Render
- Verificar que `requirements.txt` está correto

---

## 📝 Notas

- **Nunca commites** ficheiros `.env` ou `luna_config.json` (já estão no .gitignore)
- **Mantém secrets seguros** - usa variáveis de ambiente nas plataformas
- **Testa localmente** antes de fazer deploy



