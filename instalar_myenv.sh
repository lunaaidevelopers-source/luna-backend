#!/bin/bash

# Script para instalar dependências no ambiente virtual myenv

cd "$(dirname "$0")"

echo "🔧 A instalar dependências no ambiente virtual 'myenv'..."
echo ""

# Ativa o ambiente virtual myenv
if [ ! -d "myenv" ]; then
    echo "❌ Ambiente virtual 'myenv' não encontrado!"
    echo "A criar ambiente virtual 'myenv'..."
    python3 -m venv myenv
fi

source myenv/bin/activate

# Atualiza pip
echo "📦 A atualizar pip..."
python3 -m pip install --upgrade pip --quiet

# Instala as dependências
echo "📦 A instalar dependências do requirements.txt..."
python3 -m pip install -r requirements.txt

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "Para iniciar o backend, executa:"
echo "  cd /Users/matildematosa/Desktop/Luna_Backend"
echo "  source myenv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Ou simplesmente:"
echo "  ./start_backend.sh"

