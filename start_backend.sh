#!/bin/bash

# Script para iniciar o backend Luna

cd "$(dirname "$0")"

# Ativa o ambiente virtual (tenta venv_new primeiro, depois venv, depois myenv)
if [ -d "venv_new" ]; then
    source venv_new/bin/activate
    echo "✅ A usar ambiente virtual 'venv_new'"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ A usar ambiente virtual 'venv'"
elif [ -d "myenv" ]; then
    source myenv/bin/activate
    echo "✅ A usar ambiente virtual 'myenv'"
    # Verifica se Flask está instalado
    if ! python3 -c "import flask" 2>/dev/null; then
        echo "⚠️  Flask não encontrado no myenv!"
        echo "A instalar dependências..."
        python3 -m pip install --upgrade pip --quiet
        python3 -m pip install -r requirements.txt
    fi
else
    echo "❌ Nenhum ambiente virtual encontrado!"
    echo "Executa primeiro: ./install_dependencies.sh ou ./instalar_myenv.sh"
    exit 1
fi

# Inicia o servidor Flask
echo "🚀 A iniciar o servidor Flask na porta 5001..."
python3 app.py

