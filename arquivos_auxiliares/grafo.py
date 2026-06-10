# =============================================================================
# SIGIC - Estrutura de Grafo da Rede da Colônia
#
# A infraestrutura da colônia é representada como um GRAFO NÃO-DIRECIONADO
# PONDERADO, onde:
#   - Vértices = módulos da colônia (0 a 7)
#   - Arestas = conexões entre módulos com peso (distância em metros)
#
# Representações implementadas:
#   - Matriz de adjacência: LISTA DE LISTAS (acesso O(1) para verificar adjacência)
#   - Lista de adjacência: DICIONÁRIO DE LISTAS (eficiente para percorrer vizinhos)
#
# A dupla representação permite comparar trade-offs de memória e desempenho
# conforme estudado no Cap. 3 (Grafos e Algoritmos de Rede).
# =============================================================================

import copy



def criar_matriz_adjacencia(num_vertices, conexoes):
    """
    Cria a MATRIZ DE ADJACÊNCIA da rede da colônia.

    A matriz é uma lista de listas (num_vertices x num_vertices), onde
    matriz[i][j] contém o peso da aresta entre os vértices i e j,
    ou 0 se não há conexão direta.

    Parâmetros:
        num_vertices (int): número total de vértices (módulos).
        conexoes (list): lista de tuplas (origem, destino, peso).

    Retorna:
        list: matriz de adjacência (lista de listas).
    """
    # Inicializar matriz com zeros (sem conexão)
    matriz = []
    for i in range(num_vertices):
        linha = []
        for j in range(num_vertices):
            linha.append(0)
        matriz.append(linha)

    # Preencher com os pesos das conexões (grafo não-direcionado: simétrico)
    for origem, destino, peso in conexoes:
        matriz[origem][destino] = peso
        matriz[destino][origem] = peso

    return matriz


def criar_lista_adjacencia(num_vertices, conexoes):
    """
    Cria a LISTA DE ADJACÊNCIA da rede da colônia.

    A lista de adjacência é um dicionário onde cada chave é um vértice
    e o valor é uma lista de tuplas (vizinho, peso).

    Parâmetros:
        num_vertices (int): número total de vértices (módulos).
        conexoes (list): lista de tuplas (origem, destino, peso).

    Retorna:
        dict: dicionário de listas de adjacência.
    """
    lista_adj = {}
    for i in range(num_vertices):
        lista_adj[i] = []

    # Adicionar conexões bidirecionais
    for origem, destino, peso in conexoes:
        lista_adj[origem].append((destino, peso))
        lista_adj[destino].append((origem, peso))

    return lista_adj


def criar_grafo(num_vertices, conexoes):
    """
    Cria e retorna o grafo completo da rede da colônia em ambas as representações.

    Parâmetros:
        num_vertices (int): número de módulos.
        conexoes (list): lista de tuplas (origem, destino, peso) representando cada aresta.

    Retorna:
        tuple: (matriz_adjacencia, lista_adjacencia, conexoes)
    """
    matriz = criar_matriz_adjacencia(num_vertices, conexoes)
    lista_adj = criar_lista_adjacencia(num_vertices, conexoes)
    return matriz, lista_adj, conexoes


def exibir_matriz_adjacencia(matriz, nomes_modulos):
    """
    Exibe a matriz de adjacência formatada no terminal.

    Parâmetros:
        matriz (list): matriz de adjacência (lista de listas).
        nomes_modulos (list): lista de nomes dos módulos para rotulação.
    """
    from arquivos_auxiliares.utils import subcabecalho

    subcabecalho("Matriz de Adjacência")

    num = len(matriz)

    # Abreviações dos módulos para caber no terminal
    abreviacoes = []
    for nome in nomes_modulos:
        partes = nome.split()
        if len(partes) >= 2:
            abreviacoes.append((partes[0][:3] + partes[1][:3]).upper())
        else:
            abreviacoes.append(nome[:6].upper())

    # Cabeçalho da matriz
    print(f"\n  {'':>8}", end="")
    for abrev in abreviacoes:
        print(f"{abrev:>8}", end="")
    print()

    print(f"  {'':>8}", end="")
    for _ in range(num):
        print(f"{'───────':>8}", end="")
    print()

    # Linhas da matriz
    for i in range(num):
        print(f"  {abreviacoes[i]:>7}│", end="")
        for j in range(num):
            valor = matriz[i][j]
            if valor == 0:
                print(f"{'·':>7} ", end="")
            else:
                print(f"{valor:>7} ", end="")
        print()

    print(f"\n  Legenda: · = sem conexão | valores = distância (metros)")


def exibir_lista_adjacencia(lista_adj, nomes_modulos):
    """
    Exibe a lista de adjacência formatada no terminal.

    Parâmetros:
        lista_adj (dict): dicionário da lista de adjacência.
        nomes_modulos (list): lista de nomes dos módulos.
    """
    from arquivos_auxiliares.utils import subcabecalho

    subcabecalho("Lista de Adjacência")

    for vertice in lista_adj:
        vizinhos_str = []
        for vizinho, peso in lista_adj[vertice]:
            vizinhos_str.append(f"{nomes_modulos[vizinho]} ({peso}m)")

        print(f"\n  {nomes_modulos[vertice]}:")
        for viz in vizinhos_str:
            print(f"     └─ {viz}")


def exibir_rede_visual(nomes_modulos, conexoes):
    """
    Exibe um diagrama visual simplificado da rede no terminal.

    Parâmetros:
        nomes_modulos (list): lista de nomes dos módulos.
        conexoes (list): lista de tuplas (origem, destino, peso).
    """
    from arquivos_auxiliares.utils import subcabecalho

    subcabecalho("Rede da Colônia Aurora Siger")

    print("""
      Habitação ──────(50m)──────  Centro de Controle
      │  ╲                              │            ╲
    (30m) (65m)                       (60m)          (80m)
      │      ╲                          │               ╲
      Sup.  ╲                   Armazenamento    Comunicação
     Médico    ╲                   │        ╲            │
      │         ╲                (55m)     (40m)       (70m)
    (75m)        ╲                 │          ╲          │
      │           ╲                Agric. ────  Prod. O₂
      Laboratório  ──(45m)──── ╱
         Científico
    """)

    print(f"  Total de módulos: {len(nomes_modulos)}")
    print(f"  Total de conexões: {len(conexoes)}")

    custo_total = 0
    for _, _, peso in conexoes:
        custo_total += peso
    print(f"  Soma das distâncias: {custo_total} metros")


def obter_vizinhos(lista_adj, vertice):
    """
    Retorna a lista de vizinhos de um vértice com seus pesos.

    Parâmetros:
        lista_adj (dict): dicionário da lista de adjacência.
        vertice (int): ID do vértice.

    Retorna:
        list: lista de tuplas (vizinho_id, peso).
    """
    if vertice in lista_adj:
        return lista_adj[vertice]
    return []


def adicionar_conexao(matriz, lista_adj, origem, destino, peso):
    """
    Adiciona uma nova conexão ao grafo (ambas as representações).

    Parâmetros:
        matriz (list): matriz de adjacência.
        lista_adj (dict): lista de adjacência.
        origem (int): ID do módulo de origem.
        destino (int): ID do módulo de destino.
        peso (int|float): peso da conexão (distância em metros).
    """
    # Verificar se a conexão já existe
    if matriz[origem][destino] != 0:
        print(f"   Conexão entre {origem} e {destino} já existe (peso: {matriz[origem][destino]}).")
        return

    # Atualizar matriz de adjacência
    matriz[origem][destino] = peso
    matriz[destino][origem] = peso

    # Atualizar lista de adjacência
    lista_adj[origem].append((destino, peso))
    lista_adj[destino].append((origem, peso))

    print(f"   Conexão adicionada: {origem} ↔ {destino} (peso: {peso}m)")


def remover_conexao(matriz, lista_adj, origem, destino):
    """
    Remove uma conexão do grafo (ambas as representações).

    Parâmetros:
        matriz (list): matriz de adjacência.
        lista_adj (dict): lista de adjacência.
        origem (int): ID do módulo de origem.
        destino (int): ID do módulo de destino.
    """
    if matriz[origem][destino] == 0:
        print(f"   Conexão entre {origem} e {destino} não existe.")
        return

    # Remover da matriz
    matriz[origem][destino] = 0
    matriz[destino][origem] = 0

    # Remover da lista de adjacência
    lista_adj[origem] = [(v, p) for v, p in lista_adj[origem] if v != destino]
    lista_adj[destino] = [(v, p) for v, p in lista_adj[destino] if v != origem]

    print(f"   Conexão removida: {origem} ↔ {destino}")
