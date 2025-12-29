#!/bin/bash

# Script para iniciar o backend Luna

cd "$(dirname "$0")"

# Encontrar e usar o Python do ambiente virtual (sem precisar ativar)
PYTHON_CMD=""

if [ -d "venv_new" ] && [ -f "venv_new/bin/python3" ]; then
    PYTHON_CMD="venv_new/bin/python3"
    echo "✅ A usar ambiente virtual 'venv_new'"
elif [ -d "venv" ] && [ -f "venv/bin/python3" ]; then
    PYTHON_CMD="venv/bin/python3"
    echo "✅ A usar ambiente virtual 'venv'"
elif [ -d "myenv" ] && [ -f "myenv/bin/python3" ]; then
    PYTHON_CMD="myenv/bin/python3"
    echo "✅ A usar ambiente virtual 'myenv'"
    # Verifica se Flask está instalado
    if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
        echo "⚠️  Flask não encontrado no myenv!"
        echo "A instalar dependências..."
        $PYTHON_CMD -m pip install --upgrade pip --quiet
        $PYTHON_CMD -m pip install -r requirements.txt
    fi
else
    echo "❌ Nenhum ambiente virtual encontrado!"
    echo "Executa primeiro: ./install_dependencies.sh ou ./instalar_myenv.sh"
    exit 1
fi

# Verifica se Flask está instalado
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask não encontrado! A instalar dependências..."
    $PYTHON_CMD -m pip install --upgrade pip --quiet
    $PYTHON_CMD -m pip install -r requirements.txt
fi

# Inicia o servidor Flask
echo "🚀 A iniciar o servidor Flask na porta 5001..."
$PYTHON_CMD app.py

