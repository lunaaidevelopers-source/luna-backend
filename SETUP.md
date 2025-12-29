# 🚀 Setup Rápido - Luna Backend

## 1. Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 3. Configurar Variáveis de Ambiente

Cria `.env` na raiz:
```bash
GEMINI_API_KEY=sua_chave_aqui
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URLS=http://localhost:3000
PORT=5001
DEBUG=true
```

## 4. Configurar Firebase

Coloca `luna_config.json` na raiz do projeto (obtém do Firebase Console).

## 5. Iniciar

```bash
python3 app.py
```

Ou:
```bash
./start_backend.sh
```

---

## 🔔 Webhook Stripe (Desenvolvimento)

Usa Stripe CLI:
```bash
stripe listen --forward-to localhost:5001/api/v1/payment/webhook
```

Copia o `whsec_...` que aparece e adiciona ao `.env`.

---

## 📝 Notas

- Ver `README.md` para documentação completa
- Para produção, muda `DEBUG=false` e configura `FRONTEND_URLS` com domínios reais

