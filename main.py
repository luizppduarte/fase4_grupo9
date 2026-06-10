# =============================================================================
# SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia
# Arquivo Principal de Execução
# =============================================================================

import sys
import os

# Adiciona o diretório atual ao sys.path para garantir que os imports funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from arquivos_auxiliares.modulos import obter_nomes, exibir_todos_modulos, exibir_modulo, alterar_status
from arquivos_auxiliares.grafo import criar_grafo, exibir_matriz_adjacencia, exibir_lista_adjacencia, exibir_rede_visual
from arquivos_auxiliares.algoritmos import bfs, dfs, dijkstra, detectar_pontos_criticos, analisar_eficiencia_rede
from arquivos_auxiliares.modelagem import analisar_consumo_energetico, analisar_perda_energetica
from arquivos_auxiliares.sustentabilidade import relatorio_esg_completo, simular_expansao
from arquivos_auxiliares.utils import cabecalho, subcabecalho, separador, pausar, ler_inteiro


def exibir_menu():
    """Exibe o menu principal do SIGIC."""
    cabecalho("SIGIC - Aurora Siger")
    print("  1. Visualizar rede da colônia")
    print("  2. Consultar módulos")
    print("  3. Exibir matriz de adjacência")
    print("  4. Exibir lista de adjacência")
    print("  5. Executar BFS (Busca em Largura)")
    print("  6. Executar DFS (Busca em Profundidade)")
    print("  7. Calcular caminho mínimo (Dijkstra)")
    print("  8. Detectar conexões críticas")
    print("  9. Analisar eficiência da rede")
    print(" 10. Modelagem matemática - Consumo energético")
    print(" 11. Modelagem matemática - Perda energética")
    print(" 12. Simulação: Emergência energética")
    print(" 13. Análise de sustentabilidade e ESG")
    print(" 14. Simular expansão da colônia")
    print("  0. Sair")
    print(f"╚{'═'*56}╝")


def principal():
    """Função principal que gerencia o loop do menu e estado do sistema."""
    
    # Inicialização do estado do sistema via CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    df_modulos = pd.read_csv(os.path.join(base_dir, "data", "modulos.csv"))
    modulos = []
    for _, row in df_modulos.iterrows():
        modulos.append({
            "id": int(row["id"]),
            "nome": str(row["nome"]),
            "consumo_energetico": float(row["consumo_energetico"]),
            "prioridade": (int(row["prioridade_nivel"]), str(row["prioridade_rotulo"])),
            "capacidade_armazenamento": float(row["capacidade_armazenamento"]),
            "necessidade_comunicacao": str(row["necessidade_comunicacao"]),
            "status": str(row["status"])
        })
        
    df_conexoes = pd.read_csv(os.path.join(base_dir, "data", "conexoes.csv"))
    conexoes_iniciais = []
    for _, row in df_conexoes.iterrows():
        conexoes_iniciais.append((int(row["origem"]), int(row["destino"]), int(row["distancia"])))

    nomes_modulos = obter_nomes(modulos)
    matriz, lista_adj, conexoes = criar_grafo(len(modulos), conexoes_iniciais)
    
    while True:
        # Limpar terminal (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        exibir_menu()
        opcao = ler_inteiro("\n  Escolha uma opção: ", 0, 14)
        
        # Limpar terminal após escolha para exibir resultado limpo
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if opcao == 0:
            cabecalho("Encerrando SIGIC")
            print("\n  Desconectando dos sistemas da Aurora Siger...")
            print("  Operação finalizada com sucesso.\n")
            break
            
        elif opcao == 1:
            exibir_rede_visual(nomes_modulos, conexoes)
            
        elif opcao == 2:
            exibir_todos_modulos(modulos)
            print("\n  Opções:")
            print("  1. Ver detalhes de um módulo específico")
            print("  2. Alterar status operacional")
            print("  0. Voltar")
            
            sub_op = ler_inteiro("\n  Escolha: ", 0, 2)
            if sub_op == 1:
                idx = ler_inteiro("  ID do módulo: ", 0, len(modulos)-1)
                exibir_modulo(modulos[idx])
            elif sub_op == 2:
                idx = ler_inteiro("  ID do módulo: ", 0, len(modulos)-1)
                print("  Status: 1=Ativo, 2=Manutenção, 3=Alerta")
                st_op = ler_inteiro("  Novo status: ", 1, 3)
                status_map = {1: "Ativo", 2: "Manutenção", 3: "Alerta"}
                alterar_status(modulos, idx, status_map[st_op])
                
        elif opcao == 3:
            exibir_matriz_adjacencia(matriz, nomes_modulos)
            
        elif opcao == 4:
            exibir_lista_adjacencia(lista_adj, nomes_modulos)
            
        elif opcao == 5:
            subcabecalho("Busca em Largura (BFS)")
            exibir_todos_modulos(modulos)
            origem = ler_inteiro("\n  ID do módulo de origem: ", 0, len(modulos)-1)
            bfs(lista_adj, origem, nomes_modulos)
            
        elif opcao == 6:
            subcabecalho("Busca em Profundidade (DFS)")
            exibir_todos_modulos(modulos)
            origem = ler_inteiro("\n  ID do módulo de origem: ", 0, len(modulos)-1)
            dfs(lista_adj, origem, nomes_modulos)
            
        elif opcao == 7:
            subcabecalho("Cálculo de Caminho Mínimo (Dijkstra)")
            exibir_todos_modulos(modulos)
            origem = ler_inteiro("\n  ID do módulo de origem: ", 0, len(modulos)-1)
            destino = ler_inteiro("  ID do módulo de destino: ", 0, len(modulos)-1)
            dijkstra(lista_adj, origem, destino, nomes_modulos)
            
        elif opcao == 8:
            detectar_pontos_criticos(lista_adj, nomes_modulos)
            
        elif opcao == 9:
            analisar_eficiencia_rede(lista_adj, nomes_modulos)
            
        elif opcao == 10:
            analisar_consumo_energetico()
            
        elif opcao == 11:
            analisar_perda_energetica()
            
        elif opcao == 12:
            from arquivos_auxiliares.sustentabilidade import governanca_emergencia
            governanca_emergencia(modulos, lista_adj, nomes_modulos)
            
        elif opcao == 13:
            relatorio_esg_completo(modulos, lista_adj, nomes_modulos)
            
        elif opcao == 14:
            modulos, matriz, lista_adj, nomes_modulos = simular_expansao(
                modulos, matriz, lista_adj, nomes_modulos
            )
            
            # Recriar conexões baseado na nova lista adjacente para exibir visualmente
            conexoes = []
            visitadas = set()
            for u in lista_adj:
                for v, peso in lista_adj[u]:
                    edge = tuple(sorted([u, v]))
                    if edge not in visitadas:
                        visitadas.add(edge)
                        conexoes.append((u, v, peso))
            
            print("\n  A rede e os módulos foram atualizados nesta sessão.")
            print("  As novas análises e algoritmos incluirão o novo módulo.")
            
        pausar()


if __name__ == "__main__":
    try:
        principal()
    except KeyboardInterrupt:
        print("\n\n  Execução interrompida pelo usuário.")
        sys.exit(0)
