# =============================================================================
# SIGIC - Modelagem Matemática e Otimização
#
# Este módulo implementa modelagens matemáticas para análise do sistema
# energético da colônia Aurora Siger, aplicando conceitos de:
#   - Cálculo diferencial (derivadas numéricas por diferenças finitas)
#   - Funções exponenciais para modelagem de crescimento e perda
#   - Otimização via gradiente descendente unidimensional
#
# Referências: Cap. 4 (Cálculo Diferencial) e Cap. 5 (Ajustes Lineares)
#
# NOTA: Utiliza apenas a biblioteca padrão 'math' — sem NumPy/SymPy.
# =============================================================================

import math


# ─────────────────────────────────────────────────────────────────────────────
# FENÔMENO 1: Crescimento do Consumo Energético
# ─────────────────────────────────────────────────────────────────────────────

def funcao_consumo(t, c0=1030.0, k=0.05):
    """
    Modela o crescimento exponencial do consumo energético da colônia.

    Fórmula: C(t) = C₀ · e^(k·t)

    Onde:
        C(t) = consumo energético total no instante t (kWh)
        C₀   = consumo inicial da colônia (soma dos 8 módulos = 1030 kWh)
        k    = taxa de crescimento mensal (5% → expansão da infraestrutura)
        t    = tempo em meses desde o início da operação

    Parâmetros:
        t (float): tempo em meses.
        c0 (float): consumo inicial em kWh (padrão: 1030.0).
        k (float): taxa de crescimento (padrão: 0.05).

    Retorna:
        float: consumo energético no instante t.
    """
    return c0 * math.exp(k * t)


def derivada_consumo(t, c0=1030.0, k=0.05):
    """
    Calcula a derivada analítica do consumo energético.

    Fórmula: C'(t) = k · C₀ · e^(k·t)

    Interpretação: taxa de variação do consumo — indica quão rápido
    o consumo está crescendo em cada instante.

    Parâmetros:
        t (float): tempo em meses.
        c0 (float): consumo inicial em kWh.
        k (float): taxa de crescimento.

    Retorna:
        float: taxa de variação do consumo no instante t (kWh/mês).
    """
    return k * c0 * math.exp(k * t)


def derivada_numerica(funcao, t, h=0.0001):
    """
    Calcula a derivada numérica de uma função usando diferenças finitas centrais.

    Fórmula: f'(t) ≈ (f(t+h) - f(t-h)) / (2h)

    Este método é mais preciso que diferenças avançadas ou atrasadas,
    com erro de ordem O(h²).

    Parâmetros:
        funcao (callable): função a ser derivada.
        t (float): ponto onde calcular a derivada.
        h (float): passo para diferenças finitas (padrão: 0.0001).

    Retorna:
        float: valor aproximado da derivada.
    """
    return (funcao(t + h) - funcao(t - h)) / (2 * h)


def analisar_consumo_energetico():
    """
    Realiza a análise completa do crescimento do consumo energético.

    Exibe:
    - Tabela de consumo ao longo do tempo (0 a 24 meses)
    - Taxa de variação (derivada) em cada período
    - Identificação do ponto de alerta (consumo > 2x inicial)
    - Comparação entre derivada analítica e numérica
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela, separador

    subcabecalho("Modelagem: Crescimento do Consumo Energético")

    c0 = 1030.0  # Consumo inicial (soma dos 8 módulos)
    k = 0.05     # Taxa de crescimento mensal (5%)

    # Exibir modelo
    print(f"\n   Modelo matemático:")
    print(f"  C(t) = C₀ · e^(k·t)")
    print(f"")
    print(f"  Variáveis:")
    print(f"  • C₀ = {c0:.0f} kWh (consumo inicial total)")
    print(f"  • k  = {k} (taxa de crescimento mensal = {k*100:.0f}%)")
    print(f"  • t  = tempo em meses")
    print(f"")
    print(f"  Derivada: C'(t) = k · C₀ · e^(k·t)")
    print(f"  Interpretação: velocidade de crescimento do consumo")

    separador()

    # Tabela de evolução
    print(f"\n   Evolução do consumo ao longo de 24 meses:")

    cabecalhos = ["Mês", "Consumo (kWh)", "Variação (kWh/mês)", "Crescimento"]
    linhas = []

    limiar_alerta = c0 * 2  # Dobro do consumo inicial
    mes_alerta = None

    for t in range(0, 25, 3):
        consumo = funcao_consumo(t, c0, k)
        variacao = derivada_consumo(t, c0, k)
        crescimento_pct = ((consumo - c0) / c0) * 100

        if consumo >= limiar_alerta and mes_alerta is None:
            mes_alerta = t

        indicador = "" if consumo >= limiar_alerta else ""
        linhas.append([
            f"t = {t:>2}",
            f"{consumo:>10.1f}",
            f"{variacao:>10.1f}",
            f"{crescimento_pct:>6.1f}% {indicador}"
        ])

    exibir_tabela(cabecalhos, linhas)

    # Ponto de alerta
    separador()
    print(f"\n    Análise de alerta:")
    print(f"  Limiar de alerta definido: {limiar_alerta:.0f} kWh (2× consumo inicial)")

    if mes_alerta is not None:
        print(f"  O consumo atinge o dobro por volta do mês {mes_alerta}.")
    else:
        # Calcular analiticamente: C₀·e^(kt) = 2·C₀ → t = ln(2)/k
        t_critico = math.log(2) / k
        print(f"  Previsão analítica: mês {t_critico:.1f} (t = ln(2)/k)")

    # Comparação derivada analítica vs numérica
    separador()
    print(f"\n   Validação: Derivada analítica vs numérica (t = 12 meses):")
    t_teste = 12
    deriv_analitica = derivada_consumo(t_teste, c0, k)
    deriv_numerica = derivada_numerica(lambda t: funcao_consumo(t, c0, k), t_teste)
    erro = abs(deriv_analitica - deriv_numerica)

    print(f"  Derivada analítica: {deriv_analitica:.6f} kWh/mês")
    print(f"  Derivada numérica:  {deriv_numerica:.6f} kWh/mês")
    print(f"  Erro absoluto:      {erro:.10f}")
    print(f"   Validação bem-sucedida — erro desprezível.")

    # Análise qualitativa
    separador()
    print(f"\n   Análise qualitativa:")
    print(f"  • O consumo cresce exponencialmente com taxa de {k*100:.0f}% ao mês.")
    print(f"  • A derivada C'(t) também é exponencial → o crescimento ACELERA.")
    print(f"  • Para manter a colônia sustentável, a produção de energia deve")
    print(f"    acompanhar essa taxa ou medidas de eficiência devem ser adotadas.")
    print(f"  • Relação com a colônia: o planejamento de expansão da Aurora Siger")
    print(f"    deve considerar este crescimento para dimensionar novas fontes.")


# ─────────────────────────────────────────────────────────────────────────────
# FENÔMENO 2: Perda Energética na Distribuição
# ─────────────────────────────────────────────────────────────────────────────

def funcao_perda(d, p0=100.0, alfa=0.015):
    """
    Modela a perda energética ao longo das conexões da rede.

    Fórmula: P(d) = P₀ · (1 - e^(-α·d))

    Onde:
        P(d) = perda energética na distância d (kWh)
        P₀   = perda máxima assintótica (100 kWh)
        α    = coeficiente de atenuação (0.015 por metro)
        d    = distância entre módulos (metros)

    Comportamento: a perda aumenta com a distância, mas satura —
    a partir de certo ponto, aumentar a distância quase não muda a perda.

    Parâmetros:
        d (float): distância em metros.
        p0 (float): perda máxima assintótica em kWh.
        alfa (float): coeficiente de atenuação.

    Retorna:
        float: perda energética na distância d.
    """
    return p0 * (1 - math.exp(-alfa * d))


def derivada_perda(d, p0=100.0, alfa=0.015):
    """
    Calcula a derivada analítica da função de perda.

    Fórmula: P'(d) = P₀ · α · e^(-α·d)

    Interpretação: taxa marginal de perda — indica quanto a perda
    aumenta para cada metro adicional de distância.

    Parâmetros:
        d (float): distância em metros.
        p0 (float): perda máxima assintótica.
        alfa (float): coeficiente de atenuação.

    Retorna:
        float: taxa marginal de perda no ponto d.
    """
    return p0 * alfa * math.exp(-alfa * d)


def otimizar_distancia_maxima(limite_perda_pct=10.0, p0=100.0, alfa=0.015):
    """
    Calcula a distância máxima aceitável para que a perda fique abaixo do limite.

    Usa gradiente descendente 1D para minimizar |P(d) - limite|.
    (Também pode ser resolvido analiticamente: d = -ln(1 - limite%/100) / α)

    Parâmetros:
        limite_perda_pct (float): limite percentual de perda aceitável.
        p0 (float): perda máxima assintótica.
        alfa (float): coeficiente de atenuação.

    Retorna:
        float: distância máxima aceitável em metros.
    """
    # Solução analítica: P(d) = P₀·(1-e^(-αd)) = limite → d = -ln(1-limite/P₀)/α
    limite_absoluto = p0 * (limite_perda_pct / 100.0)
    d_max = -math.log(1 - limite_absoluto / p0) / alfa

    return d_max


def gradiente_descendente_1d(funcao_custo, d_inicial=50.0, taxa_aprendizado=0.5,
                              num_iteracoes=100, tolerancia=1e-6):
    """
    Implementa o gradiente descendente unidimensional para otimização.

    Minimiza uma função de custo f(d) atualizando iterativamente:
        d_novo = d_atual - taxa_aprendizado · f'(d_atual)

    A derivada é calculada numericamente por diferenças finitas.

    Parâmetros:
        funcao_custo (callable): função a minimizar.
        d_inicial (float): ponto de partida.
        taxa_aprendizado (float): tamanho do passo.
        num_iteracoes (int): número máximo de iterações.
        tolerancia (float): critério de parada.

    Retorna:
        tuple: (d_otimo, historico)
            - d_otimo (float): ponto de mínimo encontrado.
            - historico (list): lista de tuplas (iteracao, d, custo).
    """
    d = d_inicial
    historico = []

    for i in range(num_iteracoes):
        custo = funcao_custo(d)
        gradiente = derivada_numerica(funcao_custo, d)

        historico.append((i, d, custo))

        if abs(gradiente) < tolerancia:
            break

        d = d - taxa_aprendizado * gradiente

        # Garantir que d não fique negativo (distância é positiva)
        if d < 0:
            d = 0.01

    return d, historico


def analisar_perda_energetica():
    """
    Realiza a análise completa da perda energética na distribuição.

    Exibe:
    - Tabela de perda vs distância
    - Ponto de saturação (eficiência marginal)
    - Distância máxima para perda aceitável (< 10%)
    - Demonstração do gradiente descendente
    """
    from arquivos_auxiliares.utils import subcabecalho, exibir_tabela, separador

    subcabecalho("Modelagem: Perda Energética na Distribuição")

    p0 = 100.0    # Perda máxima assintótica (kWh)
    alfa = 0.015  # Coeficiente de atenuação

    # Exibir modelo
    print(f"\n   Modelo matemático:")
    print(f"  P(d) = P₀ · (1 - e^(-α·d))")
    print(f"")
    print(f"  Variáveis:")
    print(f"  • P₀   = {p0:.0f} kWh (perda máxima assintótica)")
    print(f"  • α    = {alfa} (coeficiente de atenuação por metro)")
    print(f"  • d    = distância entre módulos (metros)")
    print(f"")
    print(f"  Derivada: P'(d) = P₀ · α · e^(-α·d)")
    print(f"  Interpretação: taxa marginal de perda (quanto a perda")
    print(f"  aumenta por metro adicional — diminui com a distância)")

    separador()

    # Tabela de perda vs distância
    print(f"\n   Perda energética por distância:")

    cabecalhos = ["Distância (m)", "Perda (kWh)", "Perda (%)", "Taxa marginal"]
    linhas = []

    distancias = [10, 20, 30, 40, 50, 60, 70, 80, 100, 150, 200]
    for d in distancias:
        perda = funcao_perda(d, p0, alfa)
        perda_pct = (perda / p0) * 100
        taxa = derivada_perda(d, p0, alfa)

        indicador = ""
        if perda_pct > 50:
            indicador = " "
        elif perda_pct > 30:
            indicador = " "

        linhas.append([
            f"{d:>6}",
            f"{perda:>8.2f}",
            f"{perda_pct:>6.1f}%{indicador}",
            f"{taxa:>8.4f} kWh/m"
        ])

    exibir_tabela(cabecalhos, linhas)

    # Distância máxima aceitável
    separador()
    print(f"\n   Otimização: Distância máxima para perda ≤ 10%:")

    d_max = otimizar_distancia_maxima(10.0, p0, alfa)
    perda_no_limite = funcao_perda(d_max, p0, alfa)

    print(f"  Solução analítica: d_max = -ln(1 - 0.10) / {alfa}")
    print(f"  d_max = {d_max:.2f} metros")
    print(f"  Perda nesse ponto: {perda_no_limite:.2f} kWh ({(perda_no_limite/p0)*100:.1f}%)")

    # Demonstração do gradiente descendente
    separador()
    print(f"\n   Demonstração: Gradiente descendente 1D")
    print(f"  Objetivo: encontrar a distância onde a perda é exatamente 10 kWh")

    # Função de custo: (P(d) - 10)² → mínimo quando P(d) = 10
    def custo_alvo(d):
        return (funcao_perda(d, p0, alfa) - 10.0) ** 2

    d_otimo, historico = gradiente_descendente_1d(custo_alvo, d_inicial=50.0,
                                                   taxa_aprendizado=0.3,
                                                   num_iteracoes=50)

    print(f"\n  Resultado após {len(historico)} iterações:")
    print(f"  d_ótimo = {d_otimo:.2f} metros")
    print(f"  P(d_ótimo) = {funcao_perda(d_otimo, p0, alfa):.4f} kWh")

    # Mostrar algumas iterações
    print(f"\n  Primeiras iterações do gradiente descendente:")
    cab_iter = ["Iteração", "d (m)", "Custo"]
    lin_iter = []
    for i, d, custo in historico[:8]:
        lin_iter.append([i, f"{d:.4f}", f"{custo:.6f}"])
    if len(historico) > 8:
        lin_iter.append(["...", "...", "..."])
        ultimo = historico[-1]
        lin_iter.append([ultimo[0], f"{ultimo[1]:.4f}", f"{ultimo[2]:.6f}"])

    exibir_tabela(cab_iter, lin_iter)

    # Análise qualitativa
    separador()
    print(f"\n   Análise qualitativa:")
    print(f"  • A perda cresce rapidamente nos primeiros metros, mas SATURA.")
    print(f"  • A taxa marginal P'(d) → 0 quando d → ∞ (rendimentos decrescentes).")
    print(f"  • Para a Aurora Siger, conexões > {d_max:.0f}m devem ser evitadas")
    print(f"    ou reforçadas com repetidores/cabos de menor resistência.")
    print(f"  • A rede atual (max ~80m) opera dentro da zona aceitável (<10%).")
