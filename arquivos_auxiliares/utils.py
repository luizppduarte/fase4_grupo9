# =============================================================================
# SIGIC - Utilitários de exibição e formatação
# Funções auxiliares para formatação de saída no terminal
# =============================================================================

def linha(caractere="═", tamanho=56):
    """Retorna uma linha decorativa com o caractere e tamanho especificados."""
    return caractere * tamanho


def cabecalho(titulo):
    """Exibe um cabeçalho formatado com bordas decorativas."""
    largura = 56
    print(f"\n╔{linha('═', largura)}╗")
    print(f"║{titulo:^{largura}}║")
    print(f"╚{linha('═', largura)}╝")


def subcabecalho(titulo):
    """Exibe um subcabeçalho com linhas simples."""
    largura = 56
    print(f"\n┌{linha('─', largura)}┐")
    print(f"│{titulo:^{largura}}│")
    print(f"└{linha('─', largura)}┘")


def separador():
    """Exibe um separador visual simples."""
    print(f"  {'─' * 52}")


def exibir_tabela(cabecalhos, linhas_dados, larguras=None):
    """
    Exibe uma tabela formatada no terminal.

    Parâmetros:
        cabecalhos (list): lista de strings com os nomes das colunas.
        linhas_dados (list): lista de listas, cada sublista é uma linha da tabela.
        larguras (list|None): larguras personalizadas para cada coluna.
    """
    num_colunas = len(cabecalhos)

    # Calcular larguras automáticas se não fornecidas
    if larguras is None:
        larguras = []
        for i in range(num_colunas):
            max_largura = len(str(cabecalhos[i]))
            for linha_dados in linhas_dados:
                if i < len(linha_dados):
                    max_largura = max(max_largura, len(str(linha_dados[i])))
            larguras.append(max_largura + 2)

    # Linha superior
    linha_sup = "┌" + "┬".join("─" * l for l in larguras) + "┐"
    linha_meio = "├" + "┼".join("─" * l for l in larguras) + "┤"
    linha_inf = "└" + "┴".join("─" * l for l in larguras) + "┘"

    print(linha_sup)

    # Cabeçalhos
    celulas = []
    for i, cab in enumerate(cabecalhos):
        celulas.append(f" {str(cab):<{larguras[i]-1}}")
    print("│" + "│".join(celulas) + "│")
    print(linha_meio)

    # Dados
    for linha_dados in linhas_dados:
        celulas = []
        for i in range(num_colunas):
            valor = str(linha_dados[i]) if i < len(linha_dados) else ""
            celulas.append(f" {valor:<{larguras[i]-1}}")
        print("│" + "│".join(celulas) + "│")

    print(linha_inf)


def pausar():
    """Pausa a execução aguardando o usuário pressionar Enter."""
    input("\n  Pressione Enter para continuar...")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    """
    Lê um número inteiro do usuário com validação.

    Parâmetros:
        mensagem (str): mensagem exibida ao usuário.
        minimo (int|None): valor mínimo aceito.
        maximo (int|None): valor máximo aceito.

    Retorna:
        int: valor inteiro validado.
    """
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"   Valor deve ser no mínimo {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"   Valor deve ser no máximo {maximo}.")
                continue
            return valor
        except ValueError:
            print("   Entrada inválida. Digite um número inteiro.")


def formatar_caminho(nomes_modulos, caminho, custo_total):
    """
    Formata e exibe um caminho entre módulos com custo.

    Parâmetros:
        nomes_modulos (list): lista de nomes dos módulos.
        caminho (list): lista de IDs dos módulos no caminho.
        custo_total (float): custo total do caminho.
    """
    if not caminho:
        print("   Nenhum caminho encontrado.")
        return

    partes = []
    for i, modulo_id in enumerate(caminho):
        partes.append(nomes_modulos[modulo_id])
        if i < len(caminho) - 1:
            partes.append(" → ")

    print(f"\n  Rota: {''.join(partes)}")
    print(f"  Distância total: {custo_total:.1f} metros")
