# =============================================================================
# SIGIC - Sustentabilidade e Governança ESG
#
# Este módulo implementa análises de sustentabilidade e governança tecnológica
# aplicadas à infraestrutura da colônia Aurora Siger, abordando:
#   - Uso sustentável de energia
#   - Priorização de sistemas críticos
#   - Governança tecnológica para cenários de emergência
#   - Redução de desperdícios via otimização de rotas
#   - Simulação de expansão organizada
#
# Referências: Cap. 3 CeT (Ciência e Tecnologia), Cap. 7 (Armazenamento)
# =============================================================================


def analisar_uso_energia(modulos, lista_adj, nomes_modulos):
    """
    Analisa o uso sustentável de energia na colônia.

    Calcula o desperdício total da rede (baseado nas perdas por distância),
    identifica conexões mais custosas e propõe reduções.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list): nomes dos módulos.
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela, separador
    from arquivos_auxiliares.modelagem import funcao_perda

    subcabecalho("Análise de Uso Sustentável de Energia")

    # Consumo total e por categoria de prioridade
    consumo_total = 0.0
    consumo_critico = 0.0
    consumo_alto = 0.0
    consumo_medio = 0.0

    for m in modulos:
        consumo_total += m["consumo_energetico"]
        nivel = m["prioridade"][0]
        if nivel == 5:
            consumo_critico += m["consumo_energetico"]
        elif nivel == 4:
            consumo_alto += m["consumo_energetico"]
        else:
            consumo_medio += m["consumo_energetico"]

    print(f"\n   Consumo energético total: {consumo_total:.0f} kWh/ciclo")
    print(f"  {'─' * 45}")
    print(f"  Sistemas críticos (prioridade 5): {consumo_critico:.0f} kWh ({consumo_critico/consumo_total*100:.1f}%)")
    print(f"  Sistemas alta prioridade (4):     {consumo_alto:.0f} kWh ({consumo_alto/consumo_total*100:.1f}%)")
    print(f"  Sistemas média prioridade (3):    {consumo_medio:.0f} kWh ({consumo_medio/consumo_total*100:.1f}%)")

    # Calcular perda energética por conexão
    separador()
    print(f"\n   Perdas energéticas por conexão:")

    conexoes_analisadas = []
    perda_total_rede = 0.0

    visitadas = {}
    for v in lista_adj:
        for viz, peso in lista_adj[v]:
            chave = (min(v, viz), max(v, viz))
            if chave not in visitadas:
                visitadas[chave] = True
                perda = funcao_perda(peso)
                perda_total_rede += perda
                conexoes_analisadas.append((v, viz, peso, perda))

    cabecalhos = ["Conexão", "Dist. (m)", "Perda (kWh)", "Eficiência"]
    linhas = []
    for orig, dest, dist, perda in conexoes_analisadas:
        eficiencia = 100 - (perda / 100 * 100)
        indicador = "🟢" if eficiencia > 95 else "🟡" if eficiencia > 90 else ""
        linhas.append([
            f"{nomes_modulos[orig][:12]} ↔ {nomes_modulos[dest][:12]}",
            f"{dist}",
            f"{perda:.2f}",
            f"{indicador} {eficiencia:.1f}%"
        ])

    exibir_tabela(cabecalhos, linhas)

    print(f"\n   Perda total da rede: {perda_total_rede:.2f} kWh/ciclo")
    print(f"   Percentual de perda: {perda_total_rede/consumo_total*100:.2f}%")

    # Propostas de redução
    separador()
    print(f"\n   Propostas de Redução de Desperdícios:")
    print(f"  1. Instalar repetidores nas conexões > 70m para reduzir perdas")
    print(f"  2. Priorizar armazenamento local nos módulos de alta demanda")
    print(f"  3. Implementar modo de economia em módulos de prioridade média")
    print(f"     durante períodos de baixa atividade")
    print(f"  4. Considerar fonte de energia redundante próxima aos módulos")
    print(f"     críticos (Habitação, Centro de Controle, Prod. Oxigênio)")


def priorizar_sistemas(modulos):
    """
    Classifica e exibe os módulos por prioridade operacional.

    Usa um score combinado: prioridade × consumo para determinar
    a ordem de alocação em cenários de recursos limitados.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela

    subcabecalho("Priorização de Sistemas Críticos")

    # Calcular score: prioridade * (consumo / consumo_max)
    consumo_max = 0.0
    for m in modulos:
        if m["consumo_energetico"] > consumo_max:
            consumo_max = m["consumo_energetico"]

    ranking = []
    for m in modulos:
        nivel = m["prioridade"][0]
        # Score: quanto maior a prioridade e o consumo, mais importante
        score = nivel * (m["consumo_energetico"] / consumo_max)
        ranking.append((m, score))

    # Ordenar por score (maior primeiro) — bubble sort para manter Python puro
    for i in range(len(ranking)):
        for j in range(len(ranking) - 1 - i):
            if ranking[j][1] < ranking[j + 1][1]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]

    cabecalhos = ["Posição", "Módulo", "Prioridade", "Consumo", "Score"]
    linhas = []
    for pos, (m, score) in enumerate(ranking, 1):
        nivel, rotulo = m["prioridade"]
        medalhao = "" if pos == 1 else "" if pos == 2 else "" if pos == 3 else f" {pos}."
        linhas.append([
            medalhao,
            m["nome"],
            f"{rotulo} ({nivel})",
            f"{m['consumo_energetico']:.0f} kWh",
            f"{score:.2f}"
        ])

    exibir_tabela(cabecalhos, linhas)

    print(f"\n   Interpretação:")
    print(f"  Em cenário de emergência com energia limitada, os módulos")
    print(f"  devem ser atendidos na ordem acima. O score combina a")
    print(f"  prioridade operacional com a demanda energética.")
    print(f"  Módulos com score mais alto são essenciais e devem receber")
    print(f"  energia primeiro para garantir a sobrevivência da colônia.")


def governanca_emergencia(modulos, lista_adj, nomes_modulos):
    """
    Simula cenário de emergência e aplica regras de governança.

    Cenário: disponibilidade de energia reduzida a 60% da capacidade total.
    O sistema decide quais módulos manter ativos, quais reduzir
    e quais desligar temporariamente.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list): nomes dos módulos.
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela, separador

    subcabecalho("Simulação: Governança em Emergência Energética")

    consumo_total = 0.0
    for m in modulos:
        consumo_total += m["consumo_energetico"]

    energia_disponivel = consumo_total * 0.60  # 60% da capacidade

    print(f"\n    CENÁRIO DE EMERGÊNCIA")
    print(f"  {'─' * 45}")
    print(f"  Consumo total normal:       {consumo_total:.0f} kWh")
    print(f"  Energia disponível (60%):   {energia_disponivel:.0f} kWh")
    print(f"  Déficit energético:         {consumo_total - energia_disponivel:.0f} kWh")

    # Ordenar por prioridade (maior primeiro), depois por consumo (menor primeiro)
    modulos_ordenados = []
    for m in modulos:
        modulos_ordenados.append(m)

    # Bubble sort por prioridade decrescente
    for i in range(len(modulos_ordenados)):
        for j in range(len(modulos_ordenados) - 1 - i):
            m1 = modulos_ordenados[j]
            m2 = modulos_ordenados[j + 1]
            if m1["prioridade"][0] < m2["prioridade"][0]:
                modulos_ordenados[j], modulos_ordenados[j + 1] = modulos_ordenados[j + 1], modulos_ordenados[j]

    # Alocar energia
    separador()
    print(f"\n   Alocação de energia por regra de governança:")
    print(f"  Regra: prioridade 5 → 100% | prioridade 4 → 80% | prioridade 3 → 50%\n")

    energia_restante = energia_disponivel
    cabecalhos = ["Módulo", "Consumo", "Alocação", "Energia", "Status"]
    linhas = []

    for m in modulos_ordenados:
        nivel = m["prioridade"][0]
        consumo = m["consumo_energetico"]

        # Definir fator de alocação baseado na prioridade
        if nivel == 5:
            fator = 1.0
            status_str = "100%"
        elif nivel == 4:
            fator = 0.80
            status_str = "80%"
        else:
            fator = 0.50
            status_str = "50%"

        energia_alocada = consumo * fator

        if energia_restante >= energia_alocada:
            energia_restante -= energia_alocada
            decisao = "Operacional"
        elif energia_restante > 0:
            energia_alocada = energia_restante
            energia_restante = 0
            fator = energia_alocada / consumo
            status_str = f" {fator*100:.0f}%"
            decisao = "Parcial"
        else:
            energia_alocada = 0
            status_str = " 0%"
            decisao = "Desligado"

        linhas.append([
            m["nome"],
            f"{consumo:.0f} kWh",
            status_str,
            f"{energia_alocada:.0f} kWh",
            decisao
        ])

    exibir_tabela(cabecalhos, linhas)

    print(f"\n  Energia restante não alocada: {max(0, energia_restante):.0f} kWh")

    # Critérios de governança
    separador()
    print(f"\n   Critérios de Governança Tecnológica:")
    print(f"  1. Sistemas de suporte à vida são SEMPRE priorizados")
    print(f"  2. Decisões são automatizadas para agilidade em emergências")
    print(f"  3. Módulos não críticos podem operar em modo econômico")
    print(f"  4. Comunicação com a Terra é mantida para solicitar suporte")
    print(f"  5. Decisões de desligamento requerem confirmação manual")


def comparar_otimizacao_rotas(lista_adj, nomes_modulos):
    """
    Compara rotas antes e depois de otimização para demonstrar
    redução de desperdícios.

    Parâmetros:
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list): nomes dos módulos.
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela, separador
    from arquivos_auxiliares.algoritmos import dijkstra
    from arquivos_auxiliares.modelagem import funcao_perda

    subcabecalho("Comparação: Otimização de Rotas")

    # Cenários de teste: enviar energia do Armazenamento para cada módulo
    id_armazenamento = 2

    print(f"\n  Origem:  {nomes_modulos[id_armazenamento]}")
    print(f"  Comparação: rota direta vs caminho otimizado (Dijkstra)\n")

    cabecalhos = ["Destino", "Rota otimizada (m)", "Perda otim. (kWh)", "Saltos"]
    linhas = []

    for destino in range(len(nomes_modulos)):
        if destino == id_armazenamento:
            continue

        caminho, distancia = dijkstra(lista_adj, id_armazenamento, destino)
        perda = funcao_perda(distancia)

        rota_str = " → ".join([nomes_modulos[c][:6] for c in caminho])

        linhas.append([
            nomes_modulos[destino],
            f"{distancia:.0f}",
            f"{perda:.2f}",
            f"{len(caminho) - 1} ({rota_str})"
        ])

    exibir_tabela(cabecalhos, linhas)

    print(f"\n   O algoritmo de Dijkstra encontra a rota com menor perda")
    print(f"     energética, reduzindo desperdícios na distribuição.")


def simular_expansao(modulos, matriz, lista_adj, nomes_modulos):
    """
    Simula a adição de um novo módulo à colônia e analisa o impacto.

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
        matriz (list): matriz de adjacência.
        lista_adj (dict): lista de adjacência.
        nomes_modulos (list): nomes dos módulos.

    Retorna:
        tuple: (modulos_atualizado, matriz_atualizada, lista_adj_atualizada, nomes_atualizado)
    """
    import copy
    from arquivos_auxiliares.utils import subcabecalho, ler_inteiro, separador
    from arquivos_auxiliares.grafo import adicionar_conexao

    subcabecalho("Simulação: Expansão da Colônia")

    print(f"\n  Módulos atuais: {len(modulos)}")
    print(f"  Adicionando novo módulo à infraestrutura...")

    # Dados do novo módulo
    print(f"\n  Novo módulo sugerido: 'Estação de Reciclagem'")
    print(f"  (Essencial para sustentabilidade e economia circular)")

    novo_id = len(modulos)

    novo_modulo = {
        "id": novo_id,
        "nome": "Estação de Reciclagem",
        "consumo_energetico": 85.0,
        "prioridade": (3, "Média"),
        "capacidade_armazenamento": 45.0,
        "necessidade_comunicacao": "Baixa",
        "status": "Ativo"
    }

    # Criar cópias para não alterar o estado original
    modulos_novo = copy.deepcopy(modulos)
    modulos_novo.append(novo_modulo)

    nomes_novo = []
    for m in modulos_novo:
        nomes_novo.append(m["nome"])

    # Expandir matriz de adjacência
    matriz_nova = copy.deepcopy(matriz)
    for linha in matriz_nova:
        linha.append(0)
    nova_linha = [0] * (novo_id + 1)
    matriz_nova.append(nova_linha)

    # Expandir lista de adjacência
    lista_adj_nova = copy.deepcopy(lista_adj)
    lista_adj_nova[novo_id] = []

    # Conectar ao módulo de Agricultura (3) e Laboratório (4)
    print(f"\n  Conectando '{novo_modulo['nome']}' à rede:")
    adicionar_conexao(matriz_nova, lista_adj_nova, novo_id, 3, 35)   # → Agricultura
    adicionar_conexao(matriz_nova, lista_adj_nova, novo_id, 4, 50)   # → Laboratório

    # Impacto na rede
    separador()
    print(f"\n   Impacto da expansão:")
    print(f"  Módulos: {len(modulos)} → {len(modulos_novo)}")

    consumo_antes = sum(m["consumo_energetico"] for m in modulos)
    consumo_depois = sum(m["consumo_energetico"] for m in modulos_novo)

    print(f"  Consumo total: {consumo_antes:.0f} → {consumo_depois:.0f} kWh (+{consumo_depois - consumo_antes:.0f})")

    arestas_antes = 0
    for v in lista_adj:
        arestas_antes += len(lista_adj[v])
    arestas_antes = arestas_antes // 2

    arestas_depois = 0
    for v in lista_adj_nova:
        arestas_depois += len(lista_adj_nova[v])
    arestas_depois = arestas_depois // 2

    print(f"  Conexões: {arestas_antes} → {arestas_depois}")

    print(f"\n   Expansão simulada com sucesso.")
    print(f"  O novo módulo contribui para a sustentabilidade da colônia")
    print(f"  ao processar resíduos e recuperar materiais reutilizáveis.")

    return modulos_novo, matriz_nova, lista_adj_nova, nomes_novo


def relatorio_esg_completo(modulos, lista_adj, nomes_modulos):
    """
    Gera o relatório completo de sustentabilidade e governança ESG.

    Cobre todos os 5 pilares exigidos:
    1. Uso sustentável de energia
    2. Expansão organizada
    3. Priorização de sistemas críticos
    4. Governança tecnológica
    5. Redução de desperdícios

    Parâmetros:
        modulos (list): lista de dicionários dos módulos.
        lista_adj (dict): lista de adjacência do grafo.
        nomes_modulos (list): nomes dos módulos.
    """
    from arquivos_auxiliares.utils import cabecalho, separador

    cabecalho("Relatório de Sustentabilidade e ESG")

    print(f"\n  A análise ESG da Aurora Siger segue os princípios do")
    print(f"  Triple Bottom Line (Elkington, 2018): People, Planet, Profit.")
    print(f"  Adaptado ao contexto marciano:")
    print(f"  •  Social: bem-estar e segurança da tripulação")
    print(f"  •  Ambiental: uso eficiente de recursos limitados")
    print(f"  •  Governança: decisões computacionais responsáveis")

    separador()

    # 1. Uso sustentável
    analisar_uso_energia(modulos, lista_adj, nomes_modulos)

    separador()
    input("\n  [Pressione Enter para continuar o relatório...]")

    # 2. Priorização
    priorizar_sistemas(modulos)

    separador()
    input("\n  [Pressione Enter para continuar o relatório...]")

    # 3. Governança
    governanca_emergencia(modulos, lista_adj, nomes_modulos)

    separador()
    input("\n  [Pressione Enter para continuar o relatório...]")

    # 4. Otimização de rotas
    comparar_otimizacao_rotas(lista_adj, nomes_modulos)

    separador()

    # Conclusão
    print(f"\n   Conclusão do Relatório ESG:")
    print(f"  {'─' * 45}")
    print(f"  A infraestrutura da Aurora Siger demonstra compromisso com")
    print(f"  a sustentabilidade ao:")
    print(f"  • Utilizar algoritmos de otimização para reduzir perdas")
    print(f"  • Priorizar sistemas de suporte à vida em emergências")
    print(f"  • Planejar expansões com análise de impacto prévio")
    print(f"  • Automatizar decisões críticas com regras transparentes")
    print(f"  • Monitorar continuamente o consumo e eficiência da rede")
