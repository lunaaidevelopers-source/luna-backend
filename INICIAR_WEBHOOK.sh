#!/bin/bash

# Script para iniciar o webhook do Stripe localmente

echo "🔔 Iniciando Stripe Webhook Listener..."
echo ""
echo "📋 Este comando vai:"
echo "   1. Criar um túnel para o teu backend local"
echo "   2. Mostrar-te o 'webhook signing secret'"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Mantém este terminal aberto enquanto testas pagamentos"
echo "   - Copia o 'whsec_...' que aparecer e envia-me"
echo "   - Pressiona Ctrl+C para parar"
echo ""
echo "🚀 A iniciar..."
echo ""

# Iniciar o listener
stripe listen --forward-to localhost:5001/api/v1/payment/webhook

