#!/bin/bash

# Script para limpar e recriar o ambiente virtual myenv do zero

cd "$(dirname "$0")"

echo "🧹 A limpar ambiente virtual 'myenv' antigo..."
rm -rf myenv

echo "✨ A criar novo ambiente virtual 'myenv' limpo..."
python3 -m venv myenv

echo "📦 A ativar ambiente virtual..."
source myenv/bin/activate

echo "📦 A atualizar pip..."
python3 -m pip install --upgrade pip --quiet

echo "📦 A instalar todas as dependências..."
python3 -m pip install -r requirements.txt

echo ""
echo "✅ Ambiente virtual 'myenv' recriado e dependências instaladas!"
echo ""
echo "Para iniciar o backend, executa:"
echo "  cd /Users/matildematosa/Desktop/Luna_Backend"
echo "  source myenv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Ou simplesmente:"
echo "  ./start_backend.sh"

