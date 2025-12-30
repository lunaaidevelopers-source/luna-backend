#!/bin/bash

# Script para obter o JSON do Firebase formatado para colar no Render

cd "$(dirname "$0")"

if [ ! -f "luna_config.json" ]; then
    echo "❌ Arquivo luna_config.json não encontrado!"
    exit 1
fi

echo "📋 Copie o valor abaixo e cole no Render como FIREBASE_CREDENTIALS_JSON:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import json
with open('luna_config.json', 'r') as f:
    data = json.load(f)
    print(json.dumps(data))
"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Cole este valor no Render → Environment → FIREBASE_CREDENTIALS_JSON"


