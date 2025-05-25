#!/bin/bash

# Caminho para o script Python
SCRIPT="gerador_de_cartelas.py"

# Verifica se o script existe
if [ ! -f "$SCRIPT" ]; then
    echo "Arquivo $SCRIPT não encontrado!"
    exit 1
fi

# Executa o script Python
python3 "$SCRIPT"