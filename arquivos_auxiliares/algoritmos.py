# =============================================================================
# SIGIC - Algoritmos de Rede
#
# Implementação dos algoritmos fundamentais para análise da rede da colônia:
#   - BFS (Busca em Largura): exploração nível a nível usando FILA
#   - DFS (Busca em Profundidade): exploração recursiva usando PILHA
#   - Dijkstra (Caminho Mínimo): rota mais eficiente com pesos não-negativos
#
# Todos os algoritmos utilizam apenas Python puro (sem bibliotecas externas),
# conforme estudado nos capítulos 3 (Grafos) e 2 (Estruturas de Dados).
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# BFS — Busca em Largura
# ─────────────────────────────────────────────────────────────────────────────

def bfs(lista_adj, vertice_inicial, nomes_modulos=None):
    """
    Executa a Busca em Largura (BFS) a partir de um vértice inicial.

    A BFS explora o grafo nível a nível, visitando primeiro todos os vizinhos
    diretos antes de avançar para vizinhos mais distantes. Utiliza uma FILA
    (lista com append/pop(0)) como estrutura auxiliar.

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        vertice_inicial (int): ID do vértice de partida.
        nomes_modulos (list|None): nomes dos módulos para exibição.

    Retorna:
        tuple: (ordem_visitacao, predecessores)
            - ordem_visitacao (list): IDs dos vértices na ordem visitada.
            - predecessores (dict): mapeamento de cada vértice ao seu predecessor.
    """
    # Estruturas de controle
    visitados = {}          # Dicionário de vértices já visitados
    fila = []               # FILA para controle da BFS (append = enfileirar, pop(0) = desenfileirar)
    ordem_visitacao = []    # Lista com a ordem de visitação
    predecessores = {}      # Para reconstrução do caminho

    # Inicializar BFS com o vértice inicial
    for v in lista_adj:
        visitados[v] = False
        predecessores[v] = None

    visitados[vertice_inicial] = True
    fila.append(vertice_inicial)

    if nomes_modulos:
        print(f"\n  ▶ Iniciando BFS a partir de: {nomes_modulos[vertice_inicial]}")
        print(f"  {'─' * 50}")

    nivel = 0
    # Mapeamento nível → vértices para exibição
    niveis = {vertice_inicial: 0}

    while len(fila) > 0:
        # Desenfileirar o primeiro elemento (FIFO)
        vertice_atual = fila.pop(0)
        ordem_visitacao.append(vertice_atual)

        if nomes_modulos:
            nome = nomes_modulos[vertice_atual]
            nivel_atual = niveis[vertice_atual]
            print(f"  {'  ' * nivel_atual}├─ Nível {nivel_atual}: {nome} (ID: {vertice_atual})")

        # Explorar vizinhos não visitados
        for vizinho, peso in lista_adj[vertice_atual]:
            if not visitados[vizinho]:
                visitados[vizinho] = True
                predecessores[vizinho] = vertice_atual
                niveis[vizinho] = niveis[vertice_atual] + 1
                fila.append(vizinho)

    if nomes_modulos:
        print(f"\n   Total de módulos visitados: {len(ordem_visitacao)}/{len(lista_adj)}")

        # Verificar conectividade
        if len(ordem_visitacao) == len(lista_adj):
            print("   A rede é CONEXA — todos os módulos são alcançáveis.")
        else:
            nao_visitados = []
            for v in lista_adj:
                if not visitados[v]:
                    nao_visitados.append(nomes_modulos[v])
            print(f"   A rede NÃO é conexa. Módulos isolados: {', '.join(nao_visitados)}")

    return ordem_visitacao, predecessores


def reconstruir_caminho_bfs(predecessores, destino):
    """
    Reconstrói o caminho da BFS do vértice inicial até o destino.

    Parâmetros:
        predecessores (dict): dicionário de predecessores da BFS.
        destino (int): ID do vértice de destino.

    Retorna:
        list: caminho do vértice inicial até o destino.
    """
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()
    return caminho


# ─────────────────────────────────────────────────────────────────────────────
# DFS — Busca em Profundidade
# ─────────────────────────────────────────────────────────────────────────────

def dfs(lista_adj, vertice_inicial, nomes_modulos=None):
    """
    Executa a Busca em Profundidade (DFS) a partir de um vértice inicial.

    A DFS explora o grafo avançando o mais fundo possível antes de retroceder.
    Esta implementação usa uma PILHA explícita (lista com append/pop())
    em vez de recursão, para maior clareza e controle.

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        vertice_inicial (int): ID do vértice de partida.
        nomes_modulos (list|None): nomes dos módulos para exibição.

    Retorna:
        tuple: (ordem_visitacao, arestas_arvore)
            - ordem_visitacao (list): IDs dos vértices na ordem visitada.
            - arestas_arvore (list): lista de tuplas (pai, filho) da árvore DFS.
    """
    visitados = {}
    pilha = []              # PILHA para controle da DFS (append = empilhar, pop() = desempilhar)
    ordem_visitacao = []
    arestas_arvore = []     # Arestas da árvore de busca
    predecessor = {}

    for v in lista_adj:
        visitados[v] = False
        predecessor[v] = None

    pilha.append(vertice_inicial)

    if nomes_modulos:
        print(f"\n  ▶ Iniciando DFS a partir de: {nomes_modulos[vertice_inicial]}")
        print(f"  {'─' * 50}")

    profundidade_mapa = {vertice_inicial: 0}

    while len(pilha) > 0:
        # Desempilhar o topo (LIFO)
        vertice_atual = pilha.pop()

        if visitados[vertice_atual]:
            continue

        visitados[vertice_atual] = True
        ordem_visitacao.append(vertice_atual)

        if nomes_modulos:
            prof = profundidade_mapa.get(vertice_atual, 0)
            nome = nomes_modulos[vertice_atual]
            print(f"  {'  ' * prof}├─ Prof. {prof}: {nome} (ID: {vertice_atual})")

        if predecessor[vertice_atual] is not None:
            arestas_arvore.append((predecessor[vertice_atual], vertice_atual))

        # Empilhar vizinhos não visitados (ordem reversa para manter ordem natural)
        vizinhos_ordenados = []
        for vizinho, peso in lista_adj[vertice_atual]:
            vizinhos_ordenados.append((vizinho, peso))

        # Reverter para que o primeiro vizinho seja processado primeiro
        vizinhos_ordenados.reverse()

        for vizinho, peso in vizinhos_ordenados:
            if not visitados[vizinho]:
                pilha.append(vizinho)
                if vizinho not in profundidade_mapa:
                    profundidade_mapa[vizinho] = profundidade_mapa.get(vertice_atual, 0) + 1
                    predecessor[vizinho] = vertice_atual

    if nomes_modulos:
        print(f"\n   Total de módulos visitados: {len(ordem_visitacao)}/{len(lista_adj)}")

    return ordem_visitacao, arestas_arvore


def dfs_detectar_ciclos(lista_adj, nomes_modulos=None):
    """
    Utiliza DFS para detectar ciclos no grafo.

    Um ciclo é detectado quando, durante a DFS, encontramos uma aresta
    que leva a um vértice já visitado (aresta de retorno).

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list|None): nomes dos módulos.

    Retorna:
        list: lista de arestas de retorno (ciclos detectados).
    """
    visitados = {}
    predecessor = {}
    arestas_retorno = []

    for v in lista_adj:
        visitados[v] = False

    def _dfs_recursiva(v, pai):
        """Função auxiliar recursiva para detecção de ciclos."""
        visitados[v] = True
        predecessor[v] = pai

        for vizinho, peso in lista_adj[v]:
            if not visitados[vizinho]:
                _dfs_recursiva(vizinho, v)
            elif vizinho != pai:
                # Aresta de retorno encontrada → ciclo detectado
                arestas_retorno.append((v, vizinho))

    # Executar DFS em todos os componentes
    for v in lista_adj:
        if not visitados[v]:
            _dfs_recursiva(v, -1)

    if nomes_modulos:
        if len(arestas_retorno) > 0:
            print(f"\n   Ciclos detectados na rede ({len(arestas_retorno)} arestas de retorno):")
            for orig, dest in arestas_retorno:
                print(f"     └─ {nomes_modulos[orig]} ↔ {nomes_modulos[dest]}")
        else:
            print("\n   Nenhum ciclo detectado — a rede é uma árvore.")

    return arestas_retorno


# ─────────────────────────────────────────────────────────────────────────────
# DIJKSTRA — Caminho Mínimo
# ─────────────────────────────────────────────────────────────────────────────

def dijkstra(lista_adj, origem, destino, nomes_modulos=None):
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho mínimo.

    Encontra a rota mais eficiente (menor distância total) entre dois módulos
    da colônia. Utiliza uma fila de prioridade simples implementada com lista
    (sem heapq), conforme restrição de usar apenas Python puro.

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        origem (int): ID do módulo de origem.
        destino (int): ID do módulo de destino.
        nomes_modulos (list|None): nomes dos módulos para exibição.

    Retorna:
        tuple: (caminho, distancia_total)
            - caminho (list): lista de IDs dos módulos no caminho mínimo.
            - distancia_total (float): distância total do caminho.
    """
    # Inicializar distâncias com "infinito" e predecessores
    distancias = {}
    predecessores = {}
    visitados = {}

    for v in lista_adj:
        distancias[v] = float('inf')
        predecessores[v] = None
        visitados[v] = False

    distancias[origem] = 0

    if nomes_modulos:
        print(f"\n  ▶ Dijkstra: {nomes_modulos[origem]} → {nomes_modulos[destino]}")
        print(f"  {'─' * 50}")

    # Processar vértices
    for _ in range(len(lista_adj)):
        # Encontrar o vértice não visitado com menor distância
        # (fila de prioridade simples — busca linear)
        vertice_atual = None
        menor_distancia = float('inf')

        for v in lista_adj:
            if not visitados[v] and distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        # Se não há mais vértices alcançáveis, encerrar
        if vertice_atual is None:
            break

        visitados[vertice_atual] = True

        if nomes_modulos:
            nome = nomes_modulos[vertice_atual]
            print(f"  Processando: {nome} (distância acumulada: {distancias[vertice_atual]}m)")

        # Se chegamos ao destino, podemos parar
        if vertice_atual == destino:
            break

        # Relaxar arestas dos vizinhos
        for vizinho, peso in lista_adj[vertice_atual]:
            if not visitados[vizinho]:
                nova_distancia = distancias[vertice_atual] + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = vertice_atual

    # Reconstruir o caminho
    caminho = []
    atual = destino

    if distancias[destino] == float('inf'):
        if nomes_modulos:
            print(f"\n   Não há caminho entre {nomes_modulos[origem]} e {nomes_modulos[destino]}.")
        return [], float('inf')

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()

    # Exibir resultado detalhado
    if nomes_modulos:
        print(f"\n   Caminho mínimo encontrado!")
        print(f"  {'─' * 50}")

        # Exibir rota passo a passo
        for i in range(len(caminho)):
            nome = nomes_modulos[caminho[i]]
            if i < len(caminho) - 1:
                # Calcular distância deste trecho
                proximo = caminho[i + 1]
                for viz, peso in lista_adj[caminho[i]]:
                    if viz == proximo:
                        print(f"  {nome}")
                        print(f"     │  ({peso}m)")
                        break
            else:
                print(f"  {nome}")

        print(f"\n   Distância total: {distancias[destino]} metros")

    return caminho, distancias[destino]


def dijkstra_todos_destinos(lista_adj, origem, nomes_modulos=None):
    """
    Executa Dijkstra de um vértice para TODOS os outros (single-source).

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        origem (int): ID do módulo de origem.
        nomes_modulos (list|None): nomes dos módulos para exibição.

    Retorna:
        dict: dicionário com distâncias mínimas para cada vértice.
    """
    distancias = {}
    visitados = {}

    for v in lista_adj:
        distancias[v] = float('inf')
        visitados[v] = False

    distancias[origem] = 0

    for _ in range(len(lista_adj)):
        vertice_atual = None
        menor_distancia = float('inf')

        for v in lista_adj:
            if not visitados[v] and distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        if vertice_atual is None:
            break

        visitados[vertice_atual] = True

        for vizinho, peso in lista_adj[vertice_atual]:
            if not visitados[vizinho]:
                nova_distancia = distancias[vertice_atual] + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia

    if nomes_modulos:
        from arquivos_auxiliares.utils import exibir_tabela, subcabecalho

        subcabecalho(f"Distâncias a partir de: {nomes_modulos[origem]}")

        cabecalhos = ["Destino", "Distância (m)", "Alcançável"]
        linhas = []
        for v in lista_adj:
            if v != origem:
                dist = distancias[v]
                alcancavel = " Sim" if dist < float('inf') else " Não"
                dist_str = f"{dist:.0f}" if dist < float('inf') else "∞"
                linhas.append([nomes_modulos[v], dist_str, alcancavel])

        exibir_tabela(cabecalhos, linhas)

    return distancias


# ─────────────────────────────────────────────────────────────────────────────
# ANÁLISE DE REDE
# ─────────────────────────────────────────────────────────────────────────────

def detectar_pontos_criticos(lista_adj, nomes_modulos=None):
    """
    Identifica pontos de articulação (conexões críticas) na rede.

    Um ponto de articulação é um vértice cuja remoção desconecta o grafo.
    Esses são módulos críticos que, se falharem, podem isolar partes da colônia.

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list|None): nomes dos módulos.

    Retorna:
        list: lista de IDs dos pontos de articulação.
    """
    pontos_articulacao = []
    num_vertices = len(lista_adj)

    # Para cada vértice, remover e verificar se o grafo continua conexo
    for vertice_removido in lista_adj:
        # Criar cópia da lista de adjacência sem o vértice removido
        lista_adj_temp = {}
        for v in lista_adj:
            if v != vertice_removido:
                vizinhos_filtrados = []
                for viz, peso in lista_adj[v]:
                    if viz != vertice_removido:
                        vizinhos_filtrados.append((viz, peso))
                lista_adj_temp[v] = vizinhos_filtrados

        # Verificar conectividade via BFS no grafo reduzido
        if len(lista_adj_temp) == 0:
            continue

        # Escolher um vértice inicial para BFS
        vertice_inicio = None
        for v in lista_adj_temp:
            vertice_inicio = v
            break

        visitados_temp = {}
        for v in lista_adj_temp:
            visitados_temp[v] = False

        fila = [vertice_inicio]
        visitados_temp[vertice_inicio] = True
        contagem = 1

        while len(fila) > 0:
            atual = fila.pop(0)
            for viz, peso in lista_adj_temp[atual]:
                if not visitados_temp[viz]:
                    visitados_temp[viz] = True
                    fila.append(viz)
                    contagem += 1

        # Se nem todos os vértices foram alcançados, é ponto de articulação
        if contagem < len(lista_adj_temp):
            pontos_articulacao.append(vertice_removido)

    if nomes_modulos:
        from arquivos_auxiliares.utils import subcabecalho

        subcabecalho("Pontos Críticos da Rede")

        if len(pontos_articulacao) > 0:
            print(f"\n   {len(pontos_articulacao)} ponto(s) de articulação encontrado(s):")
            print(f"  (Módulos cuja falha DESCONECTARIA a rede)\n")
            for pa in pontos_articulacao:
                print(f"   {nomes_modulos[pa]} (ID: {pa})")
                # Mostrar quais módulos ficariam isolados
                vizinhos = []
                for viz, peso in lista_adj[pa]:
                    vizinhos.append(nomes_modulos[viz])
                print(f"     Conexões afetadas: {', '.join(vizinhos)}")
        else:
            print("\n   Nenhum ponto de articulação encontrado.")
            print("    A rede é robusta — nenhum módulo isolado ao remover um único vértice.")

    return pontos_articulacao


def analisar_eficiencia_rede(lista_adj, nomes_modulos=None):
    """
    Calcula e exibe métricas de eficiência da rede.

    Métricas calculadas:
    - Grau de cada vértice e grau médio
    - Densidade do grafo
    - Diâmetro (maior menor caminho)

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list|None): nomes dos módulos.

    Retorna:
        dict: dicionário com as métricas calculadas.
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela

    num_vertices = len(lista_adj)

    # Calcular grau de cada vértice
    graus = {}
    total_arestas = 0
    for v in lista_adj:
        graus[v] = len(lista_adj[v])
        total_arestas += graus[v]

    total_arestas = total_arestas // 2  # Cada aresta é contada duas vezes
    grau_medio = sum(graus.values()) / num_vertices if num_vertices > 0 else 0

    # Calcular densidade: 2*E / (V*(V-1))
    max_arestas = num_vertices * (num_vertices - 1) / 2
    densidade = total_arestas / max_arestas if max_arestas > 0 else 0

    # Calcular diâmetro (maior menor caminho entre quaisquer dois vértices)
    diametro = 0
    for v in lista_adj:
        distancias = dijkstra_todos_destinos(lista_adj, v)
        for d in distancias.values():
            if d < float('inf') and d > diametro:
                diametro = d

    metricas = {
        "num_vertices": num_vertices,
        "num_arestas": total_arestas,
        "grau_medio": grau_medio,
        "densidade": densidade,
        "diametro": diametro
    }

    if nomes_modulos:
        subcabecalho("Métricas de Eficiência da Rede")

        # Tabela de graus
        cabecalhos_grau = ["Módulo", "Grau", "Conectividade"]
        linhas_grau = []
        for v in lista_adj:
            g = graus[v]
            if g >= 3:
                nivel = "Alta"
            elif g >= 2:
                nivel = "Média"
            else:
                nivel = "Baixa"
            linhas_grau.append([nomes_modulos[v], g, nivel])

        exibir_tabela(cabecalhos_grau, linhas_grau)

        print(f"\n   Resumo da Rede:")
        print(f"  {'─' * 40}")
        print(f"  Vértices (módulos):  {num_vertices}")
        print(f"  Arestas (conexões):  {total_arestas}")
        print(f"  Grau médio:          {grau_medio:.2f}")
        print(f"  Densidade:           {densidade:.2%}")
        print(f"  Diâmetro:            {diametro} metros")

        # Interpretação
        print(f"\n   Interpretação:")
        if densidade > 0.5:
            print("  • Rede DENSA — alta redundância de caminhos.")
        elif densidade > 0.25:
            print("  • Rede MODERADA — equilíbrio entre conectividade e custo.")
        else:
            print("  • Rede ESPARSA — pode ser vulnerável a falhas.")

    return metricas
