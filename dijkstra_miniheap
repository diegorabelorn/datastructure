# DIJKSTRA COM MINI-HEAP
# PARTE 4 - CLASSE E FUNÇÕES

import networkx as nx
import random
import time
import math
from codecarbon import EmissionsTracker
import sys
import pandas as pd
import numpy as np
from scipy import stats # Importação para o cálculo do IC

# Aumenta o limite de recursão
sys.setrecursionlimit(2000)

# =================================================================
# CONFIGURAÇÃO GERAL
# =================================================================

GRAPH_SIZES = [100, 500, 1000, 5000, 10000] 
NUM_REPETITIONS = 15         
NODES_PER_EXPERIMENT = 5     
PROBABILITY = 0.02           
CONFIDENCE_LEVEL = 0.95 # Nível de confiança desejado
FIXED_SEED = 42 # Semente fixa para reprodutibilidade

class MinHeap:
    # (O código da sua classe MinHeap: __init__, isEmpty, buildHeap, siftDown, siftUp, remove, swap, update deve ser inserido aqui)
    # NOTE: O código da classe MinHeap e seus métodos não foram incluídos aqui para brevidade, 
    # mas eles devem estar definidos no ambiente de execução.
    # Assumimos que a classe MinHeap está corretamente definida acima deste bloco.

    def __init__(self, array):
        self.vertexMap = {idx: idx for idx in range(len(array))}
        self.heap = self.buildHeap(array)

    def isEmpty(self):
        return len(self.heap) == 0

    def buildHeap(self, array):
        firstParentIdx = (len(array) - 2) // 2
        for currentIdx in reversed(range(firstParentIdx + 1)):
            self.siftDown(currentIdx, len(array) - 1, array)
        return array

    def siftDown(self, currentIdx, endIdx, heap):
        childOneIdx = currentIdx * 2 + 1
        while childOneIdx <= endIdx:
            childTwoIdx = currentIdx * 2 + 2 if currentIdx * 2 + 2 <= endIdx else -1
            if childTwoIdx != -1 and heap[childTwoIdx][1] < heap[childOneIdx][1]:
                idxToSwap = childTwoIdx
            else:
                idxToSwap = childOneIdx
            if heap[idxToSwap][1] < heap[currentIdx][1]:
                self.swap(currentIdx, idxToSwap, heap)
                currentIdx = idxToSwap
                childOneIdx = currentIdx * 2 + 1
            else:
                return

    def siftUp(self, currentIdx, heap):
        parentIdx = (currentIdx - 1) // 2
        while currentIdx > 0 and heap[currentIdx][1] < heap[parentIdx][1]:
            self.swap(currentIdx, parentIdx, heap)
            currentIdx = parentIdx
            parentIdx = (currentIdx - 1) // 2

    def remove(self):
        if self.isEmpty():
            return None

        self.swap(0, len(self.heap) - 1, self.heap)
        vertex, distance = self.heap.pop()
        self.vertexMap.pop(vertex)
        self.siftDown(0, len(self.heap) - 1, self.heap)
        return vertex, distance

    def swap(self, i, j, heap):
        self.vertexMap[heap[i][0]] = j
        self.vertexMap[heap[j][0]] = i
        heap[i], heap[j] = heap[j], heap[i]

    def update(self, vertex, value):
        self.heap[self.vertexMap[vertex]] = (vertex, value)
        self.siftUp(self.vertexMap[vertex], self.heap)

def dijkstrasAlgorithm(start, edges):
    """Implementação do Dijkstra Otimizado O((V+E)logV)."""
    numberOfVertices = len(edges)
    minDistances = [float("inf") for _ in range(numberOfVertices)]
    minDistances[start] = 0

    minDistancesHeap = MinHeap([(idx, float("inf")) for idx in range(numberOfVertices)])
    minDistancesHeap.update(start, 0)

    while not minDistancesHeap.isEmpty():
        vertex, currentMinDistance = minDistancesHeap.remove()

        if currentMinDistance == float("inf"):
            break

        for edge in edges[vertex]:
            destination, distanceToDestination = edge
            newPathDistance = currentMinDistance + distanceToDestination
            currentDestinationDistance = minDistances[destination]

            if newPathDistance < currentDestinationDistance:
                minDistances[destination] = newPathDistance
                minDistancesHeap.update(destination, newPathDistance)
    
    return list(map(lambda x: -1 if x == float("inf") else x, minDistances))

# PARTE 5 -  Configuração e impressão  

# =================================================================
# CONFIGURAÇÃO E EXECUÇÃO DO EXPERIMENTO
# =================================================================

summary_results_miniheap = pd.DataFrame(columns=[
    'V', 'Média Tempo (s)', 'DP Tempo (s)', 'Média CO2e (kg)', 'DP CO2e (kg)'
])

print("Iniciando a avaliação do Dijkstra Otimizado (O((V+E)logV)) com coleta de estatísticas...")
print("========================================================================================")

for V in GRAPH_SIZES:
    
    # Fixa as sementes
    random.seed(FIXED_SEED)
    np.random.seed(FIXED_SEED)
    
    print(f"\n[Fase de Grafo V={V}]")
    
    temp_prob = PROBABILITY 
    
    # Geração do Grafo Conectado e Ponderado
    G = None
    while True:
        G = nx.gnp_random_graph(n=V, p=temp_prob, seed=FIXED_SEED) 
        if nx.is_connected(G):
            break
        temp_prob += 0.01 
        if temp_prob > 0.1:
            print(f"Aviso: Não foi possível garantir conectividade para V={V} com p<0.1.")
            break

    # Adiciona pesos e converte para lista de adjacência
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(1, 10) 

    edges_list = [[] for _ in range(V)]
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1) 
        edges_list[u].append([v, weight])
        if not G.is_directed():
             edges_list[v].append([u, weight])

    E = G.number_of_edges()
    print(f"Grafo gerado: V={V}, E={E}.")
    
    table_data = []

    # LOOP SECUNDÁRIO: REPETE O EXPERIMENTO 15 VEZES
    for rep_num in range(1, NUM_REPETITIONS + 1):
        
        print(f"  -> Repetição {rep_num}/{NUM_REPETITIONS} (V={V}) em andamento...", end='\r')
        
        # Seleção de 5 novos nós aleatórios (usa a semente fixa)
        random_starts = random.sample(range(V), min(V, NODES_PER_EXPERIMENT))
        
        total_time = 0
        total_emissions = 0

        # LOOP INTERNO: EXECUTA DIJKSTRA PARA CADA UM DOS 5 NÓS
        for start_node in random_starts:
            
            tracker = EmissionsTracker(output_dir=".", save_to_file=False, log_level="error")
            tracker.start()
            start_time = time.time()
            
            # CHAMA A FUNÇÃO DIJKSTRA OTIMIZADA
            _ = dijkstrasAlgorithm(start_node, edges_list)
            
            end_time = time.time()
            emissions = tracker.stop()
            
            total_time += (end_time - start_time)
            total_emissions += emissions if emissions is not None else 0
            
        # Cálculo da Média da Repetição (dividido por 5)
        avg_time = total_time / NODES_PER_EXPERIMENT
        avg_co2e = total_emissions / NODES_PER_EXPERIMENT

        table_data.append({
            'Nº Repetição': rep_num,
            'Nós Usados': str(sorted(random_starts)),
            'Tempo (s)': avg_time,
            'CO2e (kg)': avg_co2e
        })
    
    print(" " * 80, end='\r') 

    # =================================================================
    # CÁLCULO DAS ESTATÍSTICAS E IMPRESSÃO
    # =================================================================
    
    df_detail = pd.DataFrame(table_data)
    time_samples = df_detail['Tempo (s)'].values
    co2e_samples = df_detail['CO2e (kg)'].values
    n = len(time_samples)

    if n > 1:
        mean_time = np.mean(time_samples)
        std_time = np.std(time_samples, ddof=1) 
        mean_co2e = np.mean(co2e_samples)
        std_co2e = np.std(co2e_samples, ddof=1)
        
        # Adiciona as estatísticas agregadas ao DataFrame resumo
        summary_results_miniheap.loc[len(summary_results_miniheap)] = [V, mean_time, std_time, mean_co2e, std_co2e]

        # Cálculo do IC 95%
        df_t = n - 1 
        t_critical = stats.t.ppf(1 - (1 - CONFIDENCE_LEVEL) / 2, df_t)
        me_time = t_critical * (std_time / np.sqrt(n))
        me_co2e = t_critical * (std_co2e / np.sqrt(n))
        ic_time_str = f"[{mean_time - me_time:.6f} s, {mean_time + me_time:.6f} s]"
        ic_co2e_str = f"[{mean_co2e - me_co2e:.10f} kg, {mean_co2e + me_co2e:.10f} kg]"
        
    else:
        ic_time_str = "N/A"
        ic_co2e_str = "N/A"

    # Impressão da Tabela Detalhada e IC
    print("\n" + "="*70)
    print(f"TABELA DE ROBUSTEZ ESTATÍSTICA: DIJKSTRA O((V+E)logV) | V = {V} NÓS")
    print("=======================================================================")

    print(f"Média Geral (Tempo) das 15 repetições: {mean_time:.6f} s")
    print(f"Desvio Padrão (Tempo): {std_time:.9f} s")
    print(f"Intervalo de Confiança 95% (Tempo): {ic_time_str}")
    
    print(f"\nMédia Geral (CO₂e) das 15 repetições: {mean_co2e:.10f} kg")
    print(f"Desvio Padrão (CO₂e): {std_co2e:.12f} kg")
    print(f"Intervalo de Confiança 95% (CO₂e): {ic_co2e_str}")
    print("-" * 70)

    df_detail['Tempo (s)'] = df_detail['Tempo (s)'].map('{:.6f}'.format)
    df_detail['CO2e (kg)'] = df_detail['CO2e (kg)'].map('{:.10f}'.format)
    print(df_detail.to_markdown(index=False))
    print("\n" + "="*70 + "\n")

# PARTE 6 - Tabela Resumo

# Adicionado: Conversão forçada para float para evitar o ValueError
for col in ['Média Tempo (s)', 'DP Tempo (s)', 'Média CO2e (kg)', 'DP CO2e (kg)']:
    try:
        summary_results_miniheap[col] = summary_results_miniheap[col].astype(float)
    except ValueError:
        pass

# Aplicar a formatação (o .map deve funcionar após a garantia da tipagem)
summary_results_miniheap['Média Tempo (s)'] = summary_results_miniheap['Média Tempo (s)'].map('{:.6f}'.format)
summary_results_miniheap['DP Tempo (s)'] = summary_results_miniheap['DP Tempo (s)'].map('{:.9f}'.format)
summary_results_miniheap['Média CO2e (kg)'] = summary_results_miniheap['Média CO2e (kg)'].map('{:.10f}'.format)
summary_results_miniheap['DP CO2e (kg)'] = summary_results_miniheap['DP CO2e (kg)'].map('{:.12f}'.format)

# Imprime a tabela
print(summary_results_miniheap.to_markdown(index=False))
