# 🔧 Como Configurar Firebase no Render

## ❌ Problema Atual

O erro mostra que o Render não encontra o arquivo `luna_config.json`:
```
FileNotFoundError: luna_config.json
```

Isso acontece porque o arquivo está no `.gitignore` (por segurança) e não é enviado para o GitHub.

## ✅ Solução: Usar Variável de Ambiente

### Passo 1: Obter o Conteúdo do luna_config.json

No seu computador, execute:
```bash
cd /Users/matildematosa/Desktop/Luna_Backend
cat luna_config.json
```

Copie TODO o conteúdo JSON (desde `{` até `}`).

### Passo 2: Configurar no Render

1. **Ir para o Render Dashboard:**
   - Acesse: https://dashboard.render.com
   - Vá para o serviço `luna-backend`
   - Clique em **"Environment"** no menu lateral

2. **Adicionar Variável de Ambiente:**
   - Clique em **"Add Environment Variable"**
   - **Key:** `FIREBASE_CREDENTIALS_JSON`
   - **Value:** Cole o conteúdo COMPLETO do `luna_config.json` (todo o JSON)
   
   ⚠️ **IMPORTANTE:** 
   - Cole o JSON completo em uma única linha
   - Ou use aspas simples ao redor: `'{"type":"service_account",...}'`
   - Não quebre linhas

3. **Exemplo de como deve ficar:**
   ```
   FIREBASE_CREDENTIALS_JSON={"type":"service_account","project_id":"lunaai-backend","private_key_id":"cc1b2da64dea8382e67239fea1a8d3faf9b593f8","private_key":"-----BEGIN PRIVATE KEY-----\n..."}
   ```

### Passo 3: Verificar Outras Variáveis

Certifique-se de que estas variáveis também estão configuradas:

- ✅ `GEMINI_API_KEY` - Sua chave da API Gemini
- ✅ `FIREBASE_CREDENTIALS_JSON` - Conteúdo do luna_config.json
- ✅ `FRONTEND_URLS` - URLs do frontend (ex: `https://luna-ai.vercel.app`)
- ⚠️ `STRIPE_SECRET_KEY` - (Opcional, se usar pagamentos)
- ⚠️ `STRIPE_PUBLISHABLE_KEY` - (Opcional)
- ⚠️ `STRIPE_WEBHOOK_SECRET` - (Opcional)

### Passo 4: Fazer Deploy

1. Após adicionar a variável, o Render vai fazer deploy automático
2. Ou clique em **"Manual Deploy"** → **"Deploy latest commit"**
3. Aguarde o deploy completar
4. Verifique os logs - deve aparecer: `✅ Firebase initialized from environment variable`

## 🔍 Verificar se Funcionou

Após o deploy, teste:
```bash
curl https://luna-backend-zvwc.onrender.com/health
```

Deve retornar:
```json
{"status":"ok","service":"Luna Backend"}
```

## 🆘 Se Ainda Não Funcionar

1. **Verificar os logs no Render:**
   - Vá em "Logs" no menu lateral
   - Procure por mensagens de erro do Firebase

2. **Verificar formato do JSON:**
   - O JSON deve estar em uma única linha
   - Não deve ter quebras de linha
   - Deve começar com `{` e terminar com `}`

3. **Testar localmente com variável de ambiente:**
   ```bash
   export FIREBASE_CREDENTIALS_JSON='{"type":"service_account",...}'
   python3 app.py
   ```

## 📝 Alternativa: Upload do Arquivo

Se preferir usar o arquivo (menos seguro):

1. No Render, vá em "Settings" → "Build & Deploy"
2. Adicione no "Build Command":
   ```bash
   pip install -r requirements.txt && echo '{"type":"service_account",...}' > luna_config.json
   ```
   
   (Substitua `{...}` pelo conteúdo real do JSON)

Mas **NÃO RECOMENDADO** - usar variável de ambiente é mais seguro!


