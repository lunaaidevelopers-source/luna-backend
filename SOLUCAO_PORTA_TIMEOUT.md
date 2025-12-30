# 🔧 Solução: Port Timeout no Render

## ❌ Erro Atual

```
Timed out - Port scan timeout reached, no open ports detected on 0.0.0.0
```

## ✅ Solução Passo a Passo

### 1. Verificar Procfile na Raiz

Certifique-se de que o `Procfile` está na **raiz** do projeto (mesmo nível que `app.py`):

```
Luna_Backend/
├── Procfile          ← DEVE ESTAR AQUI
├── app.py
├── requirements.txt
└── ...
```

Conteúdo do Procfile:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info
```

### 2. Verificar Configuração no Render

No Render Dashboard:

1. Vá em **Settings** → **Build & Deploy**
2. Verifique o **Start Command**:
   - ✅ Deve estar **VAZIO** (para usar o Procfile automaticamente)
   - ❌ NÃO deve ter `python3 app.py`
   - ❌ NÃO deve ter outro comando

3. Se o Start Command não estiver vazio:
   - Apague o conteúdo
   - Salve
   - Faça um novo deploy

### 3. Verificar Variáveis de Ambiente

No Render → **Environment**, certifique-se de ter:

- ✅ `FIREBASE_CREDENTIALS_JSON` - JSON completo do Firebase
- ✅ `GEMINI_API_KEY` - Sua chave da API
- ⚠️ `PORT` - **NÃO configurar** (Render define automaticamente)

### 4. Verificar requirements.txt

Certifique-se de que `gunicorn` está no `requirements.txt`:

```txt
gunicorn==21.2.0
```

### 5. Fazer Commit e Push

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
git add Procfile requirements.txt app.py
git commit -m "Fix: Configurar Procfile para Render"
git push
```

### 6. Verificar Logs Após Deploy

Nos logs do Render, procure por:

✅ **Sucesso:**
```
Starting gunicorn...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:XXXX
```

❌ **Erro:**
```
ModuleNotFoundError: No module named 'gunicorn'
```
→ Solução: Adicionar `gunicorn==21.2.0` ao requirements.txt

❌ **Erro:**
```
Firebase could not be initialized
```
→ Solução: Configurar `FIREBASE_CREDENTIALS_JSON`

### 7. Se Ainda Não Funcionar

**Opção A: Start Command Manual**

No Render → Settings → Build & Deploy:
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

**Opção B: Verificar se Procfile está no Git**

```bash
git ls-files | grep Procfile
```

Se não aparecer, adicione:
```bash
git add Procfile
git commit -m "Add Procfile"
git push
```

## 🔍 Debug

Se ainda não funcionar, adicione no início do `app.py` (já adicionado):
```python
import sys
print(f"Python: {sys.version}")
print(f"PORT env: {os.getenv('PORT', 'NOT SET')}")
```

Isso aparecerá nos logs e ajudará a diagnosticar.

## ✅ Checklist Final

- [ ] Procfile existe na raiz do projeto
- [ ] Procfile está commitado no Git
- [ ] Start Command no Render está **VAZIO**
- [ ] `gunicorn==21.2.0` está no requirements.txt
- [ ] `FIREBASE_CREDENTIALS_JSON` está configurado
- [ ] `GEMINI_API_KEY` está configurado
- [ ] Logs mostram "Starting gunicorn..."
- [ ] Logs mostram "Listening at: http://0.0.0.0:XXXX"


