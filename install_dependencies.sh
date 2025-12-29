#!/bin/bash

# Script para instalar dependências do backend Luna

cd "$(dirname "$0")"

echo "🔧 A instalar dependências do backend..."

# Remove ambientes virtuais antigos se necessário e cria um novo limpo
echo "🧹 A criar novo ambiente virtual limpo..."
rm -rf venv_new 2>/dev/null
python3 -m venv venv_new
source venv_new/bin/activate

# Atualiza pip
echo "📦 A atualizar pip..."
python3 -m pip install --upgrade pip --quiet

# Instala as dependências
echo "📦 A instalar Flask e outras dependências..."
python3 -m pip install flask flask-cors python-dotenv google-genai firebase-admin

echo ""
echo "✅ Dependências instaladas com sucesso no venv_new!"
echo ""
echo "Para iniciar o backend, executa:"
echo "  cd /Users/matildematosa/Desktop/Luna_Backend"
echo "  source venv_new/bin/activate"
echo "  python3 app.py"

