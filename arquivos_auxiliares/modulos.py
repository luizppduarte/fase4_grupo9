# =============================================================================
# SIGIC - Definição dos Módulos da Colônia Aurora Siger
#
# Cada módulo é representado como um DICIONÁRIO (acesso por chave-valor).
# A coleção de módulos é armazenada em uma LISTA (acesso por índice).
# A prioridade de cada módulo é uma TUPLA imutável (nível, rótulo).
#
# Justificativa das estruturas:
#   - Dicionário: permite acesso direto a atributos por nome (ex: modulo["consumo_energetico"])
#   - Lista: mantém ordem e permite iteração indexada sobre todos os módulos
#   - Tupla: garante imutabilidade da prioridade operacional (dado fixo de projeto)
# =============================================================================



def obter_nomes(modulos):
    """
    Retorna uma lista com os nomes de todos os módulos.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.

    Retorna:
        list: lista de strings com os nomes.
    """
    nomes = []
    for modulo in modulos:
        nomes.append(modulo["nome"])
    return nomes


def exibir_modulo(modulo):
    """
    Exibe as informações detalhadas de um módulo no terminal.

    Parâmetros:
        modulo (dict): dicionário com os dados do módulo.
    """
    nivel_prioridade, rotulo_prioridade = modulo["prioridade"]
    print(f"\n  {modulo['nome']} (ID: {modulo['id']})")
    print(f"  {'─' * 40}")
    print(f"  Consumo energético:      {modulo['consumo_energetico']:.1f} kWh")
    print(f"  Prioridade:              {rotulo_prioridade} (nível {nivel_prioridade}/5)")
    print(f"  Capacidade armazenam.:   {modulo['capacidade_armazenamento']:.1f} kWh")
    print(f"  Necessidade comunicação: {modulo['necessidade_comunicacao']}")
    print(f"  Status operacional:      {modulo['status']}")


def exibir_todos_modulos(modulos):
    """
    Exibe um resumo de todos os módulos em formato de tabela.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
    """
    from arquivos_auxiliares.utils import exibir_tabela, subcabecalho

    subcabecalho("Módulos da Colônia Aurora Siger")

    cabecalhos = ["ID", "Módulo", "Consumo", "Prioridade", "Status"]
    linhas = []
    for m in modulos:
        nivel, rotulo = m["prioridade"]
        linhas.append([
            m["id"],
            m["nome"],
            f"{m['consumo_energetico']:.0f} kWh",
            f"{rotulo} ({nivel})",
            m["status"]
        ])

    exibir_tabela(cabecalhos, linhas)

    # Resumo
    consumo_total = 0.0
    for m in modulos:
        consumo_total += m["consumo_energetico"]
    print(f"\n   Consumo total da colônia: {consumo_total:.1f} kWh")


def alterar_status(modulos, modulo_id, novo_status):
    """
    Altera o status operacional de um módulo.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
        modulo_id (int): ID do módulo a ser alterado.
        novo_status (str): novo status ('Ativo', 'Manutenção' ou 'Alerta').

    Retorna:
        bool: True se alterado com sucesso, False caso contrário.
    """
    status_validos = ("Ativo", "Manutenção", "Alerta")
    if novo_status not in status_validos:
        print(f"   Status inválido. Valores aceitos: {status_validos}")
        return False

    for modulo in modulos:
        if modulo["id"] == modulo_id:
            modulo["status"] = novo_status
            print(f"   Status de '{modulo['nome']}' alterado para '{novo_status}'.")
            return True

    print(f"   Módulo com ID {modulo_id} não encontrado.")
    return False
