# 🔧 Erro: Port Timeout no Render

## ❌ Problema

O erro mostra:
```
Timed out - Port scan timeout reached, no open ports detected on 0.0.0.0
Detected open ports on localhost -- did you mean to bind one of these to 0.0.0.0?
```

Isso significa que o servidor não está escutando na porta correta ou não iniciou.

## 🔍 Possíveis Causas

1. **Servidor não iniciou** - Erro na inicialização antes do bind
2. **Firebase não configurado** - Pode estar causando erro fatal
3. **Procfile não detectado** - Render pode estar usando comando errado
4. **Gunicorn não instalado** - Dependência faltando

## ✅ Soluções

### 1. Verificar se o Procfile está correto

O Procfile deve estar na **raiz** do projeto e conter:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info
```

### 2. Verificar Start Command no Render

No Render Dashboard:
- Vá em **Settings** → **Build & Deploy**
- **Start Command** deve estar **VAZIO** (para usar o Procfile)
- OU usar: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 3. Verificar Variáveis de Ambiente

Certifique-se de que estas estão configuradas:
- ✅ `FIREBASE_CREDENTIALS_JSON` - JSON completo do Firebase
- ✅ `GEMINI_API_KEY` - Chave da API Gemini
- ✅ `PORT` - Deixar vazio (Render define automaticamente)

### 4. Verificar Logs

Nos logs do Render, procure por:
- ✅ `Starting gunicorn...` - Indica que o gunicorn iniciou
- ❌ `ModuleNotFoundError` - Dependência faltando
- ❌ `Firebase could not be initialized` - Firebase não configurado
- ❌ `Exited with status 1` - Erro fatal

### 5. Testar Localmente com Gunicorn

Para testar se funciona:
```bash
cd /Users/matildematosa/Desktop/Luna_Backend
source venv_new/bin/activate  # ou venv/bin/activate
pip install gunicorn
export PORT=5001
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Se funcionar localmente, o problema está na configuração do Render.

## 🚀 Checklist

- [ ] Procfile existe na raiz do projeto
- [ ] Procfile tem o comando correto com `--bind 0.0.0.0:$PORT`
- [ ] Start Command no Render está vazio (ou correto)
- [ ] `gunicorn` está no `requirements.txt`
- [ ] `FIREBASE_CREDENTIALS_JSON` está configurado
- [ ] `GEMINI_API_KEY` está configurado
- [ ] Logs mostram que o gunicorn iniciou
- [ ] Não há erros fatais nos logs

## 🔍 Debug

Se ainda não funcionar, adicione no início do `app.py`:
```python
import sys
print(f"Python: {sys.version}")
print(f"PORT: {os.getenv('PORT', 'NOT SET')}")
print(f"Firebase configured: {db is not None}")
```

Isso ajudará a ver o que está acontecendo nos logs.


