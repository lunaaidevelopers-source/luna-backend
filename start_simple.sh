#!/bin/bash

# Script simples para iniciar o backend - usa Python do venv diretamente

cd "$(dirname "$0")"

# Tenta encontrar o Python do venv
if [ -f "venv_new/bin/python3" ]; then
    echo "✅ Usando venv_new"
    venv_new/bin/python3 app.py
elif [ -f "venv/bin/python3" ]; then
    echo "✅ Usando venv"
    venv/bin/python3 app.py
elif [ -f "myenv/bin/python3" ]; then
    echo "✅ Usando myenv"
    myenv/bin/python3 app.py
else
    echo "❌ Nenhum ambiente virtual encontrado!"
    echo "Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

