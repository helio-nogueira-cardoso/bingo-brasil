import random
import re
import os
from bs4 import BeautifulSoup

# Função para ler cartelas do arquivo HTML
def ler_cartelas_html(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    tabelas = soup.find_all('table')
    cartelas = []
    ids = []

    # Ler apenas as tabelas de cartelas (ignorando a tabela da regra)
    for tabela in tabelas[1:]:
        linhas = tabela.find_all('tr')
        id_cartela = linhas[0].get_text(strip=True)
        ids.append(id_cartela)

        numeros = {letra: [] for letra in "BINGO"}

        for linha in linhas[2:]:  # Ignora cabeçalho e ID
            celulas = linha.find_all('td')
            for idx, letra in enumerate("BINGO"):
                valor = celulas[idx].get_text(strip=True)
                if valor.upper() == "FREE":
                    numeros[letra].append("FREE")
                else:
                    numeros[letra].append(int(valor))

        cartelas.append((id_cartela, numeros))

    # Agrupar cartelas por página (4 por página)
    paginas = [cartelas[i:i + 4] for i in range(0, len(cartelas), 4)]
    return paginas

# Função para verificar se uma cartela venceu
def cartela_venceu(cartela, bolas_sorteadas):
    _, numeros = cartela
    for letra, valores in numeros.items():
        for valor in valores:
            if valor != "FREE" and valor not in bolas_sorteadas:
                return False
    return True

# Função para verificar se uma página venceu (todas as 4 cartelas completas)
def pagina_venceu(pagina, bolas_sorteadas):
    return all(cartela_venceu(cartela, bolas_sorteadas) for cartela in pagina)

# --- Início do programa ---

print("🎱 Bem-vindo ao Bingo CLI 🎱\n")

arquivo = input("Digite o nome do arquivo .html com as cartelas: ").strip()
while not os.path.exists(arquivo):
    print("Arquivo não encontrado. Tente novamente.")
    arquivo = input("Digite o nome do arquivo .html com as cartelas: ").strip()

# Ler cartelas
paginas = ler_cartelas_html(arquivo)
print(f"\n✅ {len(paginas)} páginas de cartelas carregadas com sucesso.\n")

# Cadastro dos jogadores
jogadores = []
while True:
    nome = input("Nome do jogador (ou ENTER para encerrar cadastro): ").strip()
    if nome == "":
        break
    valor_por_pagina = float(input(f"Valor pago por página para {nome} (R$): "))
    qtd_paginas = int(input(f"Número de páginas compradas por {nome}: "))

    jogadores.append({
        "nome": nome,
        "valor_por_pagina": valor_por_pagina,
        "qtd_paginas": qtd_paginas,
        "paginas": []
    })

# Distribuir páginas para jogadores
paginas_disponiveis = paginas.copy()
random.shuffle(paginas_disponiveis)

for jogador in jogadores:
    for _ in range(jogador["qtd_paginas"]):
        if paginas_disponiveis:
            jogador["paginas"].append(paginas_disponiveis.pop())

# Valores de premiação
x = float(input("\nDigite a porcentagem do prêmio para o vencedor (ex.: 70 para 70%): ")) / 100
instituicao = input("Nome da instituição que receberá a doação: ")

# Valor total arrecadado
valor_total = sum(j["valor_por_pagina"] * j["qtd_paginas"] for j in jogadores)
print(f"\n💰 Valor total arrecadado: R$ {valor_total:.2f}")

# Iniciar o jogo
print("\n🎰 Iniciando o sorteio das bolinhas...\n")
bolas = [f"{letra}{num}" for letra, intervalo in zip("BINGO", [(1,15),(16,30),(31,45),(46,60),(61,75)])
         for num in range(intervalo[0], intervalo[1]+1)]
random.shuffle(bolas)

bolas_sorteadas = []
vencedor = None

for bola in bolas:
    bolas_sorteadas.append(int(re.findall(r'\d+', bola)[0]))
    print(f"🟢 Bola sorteada: {bola}")
    input("Pressione ENTER para continuar...")

    for jogador in jogadores:
        for pagina in jogador["paginas"]:
            if pagina_venceu(pagina, bolas_sorteadas):
                vencedor = jogador
                break
        if vencedor:
            break
    if vencedor:
        break

# Resultado
if vencedor:
    premio = valor_total * x
    doacao = valor_total * (1 - x)

    print("\n🎉 Temos um vencedor! 🎉")
    print(f"🏆 {vencedor['nome']} venceu com uma página de cartelas completa!")
    print(f"💰 Prêmio: R$ {premio:.2f}")
    print(f"🙏 Doação para {instituicao}: R$ {doacao:.2f}")
else:
    print("\n❌ Nenhum vencedor. O jogo terminou sem ganhadores.")

print("\n🔚 Fim do jogo.")
