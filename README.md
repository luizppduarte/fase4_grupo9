# SIGIC – Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia

## Integrantes

Julia Guimarães - RM572241
Samirah Pinotti Deranian - RM573375
Luiz Pedro Pereira Duarte – RM568970
Isaac Aurélio de Freitas Castro - RM571175

Curso: Ciência da Computação

Instituição: FIAP

---

# Sobre o Projeto

O SIGIC (Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia) foi desenvolvido para representar computacionalmente a infraestrutura da colônia marciana Aurora Siger.

O sistema utiliza conceitos de Grafos, Estruturas de Dados, Algoritmos de Busca, Caminhos Mínimos, Modelagem Matemática e Sustentabilidade ESG para monitorar e otimizar o funcionamento dos módulos da colônia.

A proposta é simular um ambiente inteligente capaz de:

- Organizar os módulos da colônia;
- Controlar o consumo energético;
- Identificar rotas eficientes para distribuição de recursos;
- Simular situações operacionais;
- Avaliar riscos de falhas na infraestrutura;
- Aplicar princípios de sustentabilidade e governança.

---

# Objetivos

O sistema foi desenvolvido com os seguintes objetivos:

- Representar a infraestrutura da colônia através de grafos;
- Aplicar algoritmos de redes estudados em aula;
- Demonstrar o uso de estruturas de dados em Python;
- Modelar matematicamente fenômenos relacionados ao consumo energético;
- Avaliar a eficiência operacional da colônia;
- Propor estratégias sustentáveis para expansão da infraestrutura.

---

# Conceitos Aplicados

## Grafos

A infraestrutura da colônia é representada por um grafo.

Cada módulo da base corresponde a um vértice.

As conexões entre módulos são representadas por arestas ponderadas.

Os pesos representam:

- Distância;
- Tempo de comunicação;
- Custo energético.

---

## BFS (Busca em Largura)

Utilizada para:

- Explorar a rede por níveis;
- Verificar conectividade;
- Descobrir módulos acessíveis.

---

## DFS (Busca em Profundidade)

Utilizada para:

- Percorrer toda a infraestrutura;
- Identificar componentes conectados;
- Detectar possíveis ciclos.

---

## Algoritmo de Dijkstra

Aplicado para:

- Encontrar o caminho mínimo entre módulos;
- Reduzir custos de distribuição;
- Melhorar a eficiência operacional.

Exemplo:

Armazenamento de Energia → Centro Médico

O sistema calcula automaticamente a melhor rota para envio de energia.

---

# Estruturas de Dados Utilizadas

## Dicionários

Armazenam informações dos módulos:

```python
{
    "Centro Médico": {
        "consumo": 150,
        "prioridade": 5
    }
}
```

## Listas

Utilizadas para:

- Conexões dos módulos;
- Resultados dos algoritmos;
- Percursos BFS e DFS.

## Matrizes

Representam:

- Matriz de adjacência;
- Custos entre módulos.

## Tuplas

Utilizadas para armazenar:

- Pares origem-destino;
- Conexões imutáveis.

---

# Módulos da Colônia

O sistema considera os seguintes módulos:

- Habitação;
- Centro de Controle;
- Armazenamento de Energia;
- Agricultura;
- Laboratório Científico;
- Comunicação;
- Centro Médico;
- Produção de Oxigênio.

Cada módulo possui:

- Consumo energético;
- Prioridade operacional;
- Capacidade de armazenamento;
- Distância dos demais módulos;
- Status operacional.

---

# Estrutura da Rede

A rede da Aurora Siger é composta por conexões entre todos os módulos essenciais.

O objetivo é garantir:

- Comunicação eficiente;
- Distribuição energética equilibrada;
- Tolerância a falhas;
- Continuidade operacional.

---

# Funcionalidades do Sistema

## 1. Visualizar Rede

Exibe todos os módulos da colônia e suas conexões.

## 2. Consultar Módulos

Mostra:

- Nome;
- Consumo energético;
- Prioridade;
- Status operacional.

## 3. Matriz de Adjacência

Apresenta a representação matricial da rede.

## 4. Lista de Adjacência

Exibe os vizinhos de cada módulo.

## 5. BFS

Executa busca em largura.

## 6. DFS

Executa busca em profundidade.

## 7. Dijkstra

Calcula o menor caminho entre módulos.

## 8. Detecção de Conexões Críticas

Identifica pontos vulneráveis da infraestrutura.

## 9. Análise da Rede

Calcula métricas como:

- Grau médio;
- Densidade;
- Conectividade.

## 10. Simulação de Emergência

Executa cenários de escassez energética.

## 11. Simulação de Expansão

Adiciona novos módulos à colônia.

---

# Modelagem Matemática

Foi utilizada modelagem matemática para representar o crescimento do consumo energético.

Função utilizada:

f(t) = C₀ · e^(kt)

Onde:

- C₀ = consumo inicial;
- k = taxa de crescimento;
- t = tempo.

Essa modelagem permite prever o aumento da demanda energética da infraestrutura.

---

# Sustentabilidade e ESG

O projeto incorpora conceitos ESG (Environmental, Social and Governance).

## Ambiental

- Redução de desperdícios energéticos;
- Uso eficiente dos recursos.

## Social

- Priorização dos módulos essenciais;
- Garantia da sobrevivência da tripulação.

## Governança

- Tomada de decisão baseada em critérios objetivos;
- Monitoramento contínuo da infraestrutura.

---

# Estrutura do Repositório

```
SIGIC/
│
├── main.py
├── modulos.py
├── grafo.py
├── algoritmos.py
├── modelagem.py
├── sustentabilidade.py
│
├── data/
│   ├── modulos.csv
│   └── conexoes.csv
│
├── imagens/
│   └── arquitetura.png
│
└── README.md
```

---

# Requisitos

Python 3.10 ou superior

Bibliotecas:

```bash
pip install pandas
```

---

# Como Executar

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/SIGIC.git
```

Entre na pasta:

```bash
cd SIGIC
```

Execute:

```bash
python main.py
```

---

# Exemplo de Uso

Entrada:

```text
Escolha um módulo:
Centro Médico
```

Saída:

```text
Melhor rota encontrada:
Armazenamento de Energia
→ Centro de Controle
→ Centro Médico

Distância total: 45 metros
```

---

# Resultados Obtidos

O sistema demonstrou ser capaz de:

- Representar a infraestrutura da colônia;
- Aplicar algoritmos de redes;
- Simular cenários operacionais;
- Identificar rotas eficientes;
- Apoiar decisões relacionadas ao gerenciamento energético.

---

# Conclusão

O SIGIC permitiu aplicar de forma prática os conceitos estudados durante a fase, integrando Grafos, Estruturas de Dados, Algoritmos de Redes, Modelagem Matemática e Sustentabilidade.

A solução proposta demonstra como técnicas computacionais podem auxiliar na gestão inteligente de infraestruturas complexas, contribuindo para a eficiência operacional e para a sustentabilidade da colônia Aurora Siger.

---

# Referências

- Material didático FIAP.
- Algoritmo de Dijkstra.
- Conceitos de BFS e DFS.
- Documentação Python.
- Conceitos ESG.
