import random
from datetime import datetime

# Função para gerar uma única cartela
def gerar_cartela_bingo(id_num):
    cartela = {
        "B": random.sample(range(1, 16), 5),
        "I": random.sample(range(16, 31), 5),
        "N": random.sample(range(31, 46), 5),
        "G": random.sample(range(46, 61), 5),
        "O": random.sample(range(61, 76), 5),
    }
    cartela["N"][2] = "FREE"  # Espaço livre no centro
    return (f"ID-{id_num:03d}", cartela)

# Solicitar parâmetros ao usuário
num_cartelas = int(input("Número total de cartelas a gerar: "))
cartelas_por_pagina = int(input("Número de cartelas por página: "))
nome_arquivo = input("Nome do arquivo .html de saída (ex.: cartelas.html): ")

# Gerar cartelas
cartelas = [gerar_cartela_bingo(i + 1) for i in range(num_cartelas)]

# Começar HTML
html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Cartelas de Bingo</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        padding: 20px;
    }}
    h1, h2 {{
        text-align: center;
    }}
    table {{
        border-collapse: collapse;
        margin: 10px;
        display: inline-block;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-radius: 8px;
        overflow: hidden;
    }}
    th, td {{
        border: 1px solid #ccc;
        padding: 12px;
        text-align: center;
    }}
    th {{
        background-color: #0077b6;
        color: white;
    }}
    .page {{
        page-break-after: always;
        text-align: center;
    }}
</style>
</head>
<body>

<h1>Cartelas de Bingo Americano</h1>
<p style="text-align:center;">Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>

<h2>Tabela do Bingo Americano</h2>
<table style="margin:auto;">
  <tr><th>Letra</th><th>Intervalo</th><th>Termo Fonético</th></tr>
  <tr><td><b>B</b></td><td>1 - 15</td><td>Bravo</td></tr>
  <tr><td><b>I</b></td><td>16 - 30</td><td>Índia</td></tr>
  <tr><td><b>N</b></td><td>31 - 45</td><td>November</td></tr>
  <tr><td><b>G</b></td><td>46 - 60</td><td>Golf</td></tr>
  <tr><td><b>O</b></td><td>61 - 75</td><td>Oscar</td></tr>
</table>
"""

# Gerar páginas
for i in range(0, len(cartelas), cartelas_por_pagina):
    html += '<div class="page">\n'
    grupo = cartelas[i:i + cartelas_por_pagina]

    for id_cartela, numeros in grupo:
        html += f'<table>\n'
        html += f'<tr><td colspan="5"><b>{id_cartela}</b></td></tr>\n'
        html += '<tr>' + ''.join(f'<th>{letra}</th>' for letra in "BINGO") + '</tr>\n'

        for linha in range(5):
            html += '<tr>'
            for letra in "BINGO":
                valor = numeros[letra][linha]
                html += f'<td>{valor}</td>'
            html += '</tr>\n'
        html += '</table>\n'

    html += '</div>\n'

# Fechar HTML
html += """
</body>
</html>
"""

# Salvar arquivo
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Arquivo '{nome_arquivo}' gerado com sucesso no diretório atual!")
