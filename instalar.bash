#!/bin/bash

# Verifica se o requirements.txt existe
if [ ! -f requirements.txt ]; then
    echo "Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Instala os requisitos usando pip
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt