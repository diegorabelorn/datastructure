# Análise Comparativa de Algoritmos de Caminho Mínimo: Dijkstra Clássico vs. Otimizado (Tempo e Carbono)

## Sumário

Este repositório documenta um estudo de caso focado na análise de desempenho e eficiência energética (pegada de carbono) de três diferentes implementações do Algoritmo de Dijkstra para a resolução do problema de Caminho Mínimo de Fonte Única (SSSP) em grafos ponderados.

O objetivo principal é comparar a complexidade teórica com a performance empírica, demonstrando o impacto da otimização algorítmica (uso de estruturas de dados eficientes, como o Min-Heap) no consumo de recursos computacionais.

---

## 1. Implementações Avaliadas

O estudo avaliou três abordagens distintas, que representam diferentes níveis de complexidade e otimização:

| Algoritmo | Complexidade Teórica (Tempo) | Estrutura de Dados |
| :--- | :--- | :--- |
| **Dijkstra Clássico** | $O(V^2 + E)$ | Busca Linear (Vetores/Listas) |
| **Dijkstra Otimizado** | $O((V + E) \log V)$ | Implementação Manual de Min-Heap |
| **NetworkX (Referência)** | $O((V + E) \log V)$ | Heap de Prioridade otimizado (Referência da biblioteca) |

> **Legenda:** $V$ = Número de Vértices (Nós); $E$ = Número de Arestas.

---

## 2. Metodologia do Experimento

Para garantir a robustez estatística e a validade dos resultados, foi aplicada a seguinte metodologia:

### 2.1. Geração de Grafos

* **Tamanhos (V):** O experimento foi executado em grafos com diferentes números de nós: **V = [100, 500, 1000, 5000, 10000]**.
* **Modelo:** Os grafos foram gerados utilizando o modelo aleatório de Erdős–Rényi (G(n, p)) através da biblioteca `networkx`, garantindo que fossem **conectados e ponderados** (pesos inteiros entre 1 e 10).
* **Arestas:** O grafo é tratado como **não-direcionado** na estrutura de lista de adjacência, refletindo a simetria de caminhos (arestas bidirecionais).

### 2.2. Robustez Estatística e Reprodutibilidade

* **Repetições:** Para cada tamanho de grafo ($V$), o experimento foi repetido **15 vezes**.
* **Amostragem:** Em cada repetição, foram selecionados **5 nós iniciais aleatórios** para o cálculo do caminho mínimo (totalizando $15 \times 5 = 75$ execuções por tamanho de grafo).
* **Seeds Fixas:** Foi utilizada uma semente fixa (`random.seed(42)` e `np.random.seed(42)`) para garantir que os grafos gerados e os nós amostrados fossem **idênticos** em todas as execuções, assegurando a reprodutibilidade.

### 2.3. Métricas de Avaliação

* **Tempo de Execução:** Medido em segundos (`time.time()`).
* **Pegada de Carbono ($\text{CO}_2\text{e}$):** Calculada em quilogramas de dióxido de carbono equivalente ($\text{kg}$ $\text{CO}_2\text{e}$) utilizando a biblioteca **`codecarbon`**.
* **Estatísticas:** Média, Desvio Padrão (DP) e Intervalos de Confiança (IC de 95%) para o Tempo e o $\text{CO}_2\text{e}$.

---

## 3. Estrutura do Repositório (Arquivos Gerados)

Este repositório contém o código-fonte Python e os seguintes arquivos de dados gerados:

### 3.1. Código Fonte

* `dijkstra.ipybn`.

### 3.2. Arquivos de Dados CSV

Os arquivos CSV contêm os resultados brutos e agregados do experimento.

| Nome do Arquivo | Tipo de Tabela | Conteúdo |
| :--- | :--- | :--- |
| `detalhe_[algoritmo]_V[size].csv` | Tabela Detalhada | Resultados brutos das 15 Repetições (Média de 5 execuções) para um $V$ específico. |
| `resumo_classic.csv` | Tabela Resumo | Estatísticas (Média, DP) do **Dijkstra Clássico** para todos os $V$. |
| `resumo_miniheap.csv` | Tabela Resumo | Estatísticas (Média, DP) do **Dijkstra Mini-Heap** para todos os $V$. |
| `resumo_networkx.csv` | Tabela Resumo | Estatísticas (Média, DP) do **NetworkX** para todos os $V$. |
| **`tabela_consolidada_final.csv`** | **Tabela Comparativa** | **Estatísticas de todos os 3 algoritmos, prontas para análise.** |

### 3.3. Gráficos

* `comparacao_tempo_dijkstra_linear.png`
* `comparacao_co2_dijkstra_linear.png`

---

## 4. Conclusões Chave (Baseadas na Análise Gráfica)

A análise dos resultados, especialmente nos gráficos, demonstra claramente a importância da complexidade algorítmica:

1.  **Tempo de Execução:** O Dijkstra Clássico $(O(V^2))$ exibe um crescimento quase vertical, tornando-se inutilizável para $V \ge 5000$. O aumento de 100 vezes em $V$ (de 100 para 10000) resultou em um tempo de execução que saltou de $1.088\text{ ms}$ para $9.834$ segundos. Este comportamento é uma evidência empírica direta da sua natureza quadrática, limitando seu uso a grafos muito pequenos. 
Por outro lado, tanto o Mini-Heap quanto o NetworkX mantiveram os tempos de execução em uma faixa gerenciável, mesmo para $V=10000$. O Mini-Heap customizado finalizou em $0.579$ segundos, enquanto o NetworkX em $1.175$ segundos.

2.  **Eficiência Energética:** A pegada de carbono ($\text{CO}_2\text{e}$) espelha diretamente o tempo de execução. O custo computacional desnecessário do algoritmo $O(V^2)$, passando de $\sim 2.0 \times 10^{-8} \text{ kg}$ para $\sim 9.1 \times 10^{-5} \text{ kg}$ de $\text{CO}_2\text{e}$ em $V=10000$, se traduz em um consumo de energia e emissão de carbono exponencialmente maior em comparação com as soluções otimizadas. m $V=10000$, a solução Clássica exige $\sim 17$ vezes mais $\text{CO}_2\text{e}$ do que a solução Mini-Heap, demonstrando que a escolha do algoritmo tem um impacto mensurável na eficiência energética e na sustentabilidade do processamento de grandes volumes de dados.

3.  **Referência:** A implementação do NetworkX prova ser a mais rápida, devido às otimizações de baixo nível, mas a implementação do Mini-Heap demonstra que o ganho de complexidade pode ser alcançado com estruturas de dados customizadas em Python.

---

**Desenvolvido por:** Diego Rabelo

**Publicação:** https://open.substack.com/pub/diegorabelos/p/do-classico-ao-sustentavel-desvendando?r=1lh0a7&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true
