!pip install codecarbon networkx
# DIJKSTRA CLÁSSICO
# PARTE 1

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
# Implementação do Dijkstra Clássico (O(V^2 + E) Time)
# =================================================================

def getVertexWithMinDistance(distances, visited):
    """Função auxiliar O(V) para encontrar o nó não visitado com a menor distância conhecida."""
    currentMinDistance = float("inf")
    vertex = -1
    for vertexIdx, distance in enumerate(distances):
        if vertexIdx in visited:
            continue
        if distance <= currentMinDistance:
            vertex = vertexIdx
            currentMinDistance = distance
    return vertex, currentMinDistance

def dijkstrasAlgorithmClassic(start, edges):
    """Implementação do Dijkstra Clássico O(V^2)."""
    numberOfVertices = len(edges)
    minDistances = [float("inf") for _ in range(numberOfVertices)]
    minDistances[start] = 0
    visited = set()

    while len(visited) != numberOfVertices:
        vertex, currentMinDistance = getVertexWithMinDistance(minDistances, visited)
        if currentMinDistance == float("inf"):
            break
        visited.add(vertex)

        for edge in edges[vertex]:
            destination, distanceToDestination = edge
            if destination in visited:
                continue
            newPathDistance = currentMinDistance + distanceToDestination
            if newPathDistance < minDistances[destination]:
                minDistances[destination] = newPathDistance
    
    return [x if x != float("inf") else -1 for x in minDistances]

#PARTE 2 - Configuração e impressão       

# =================================================================
# CONFIGURAÇÃO DO EXPERIMENTO
# =================================================================

GRAPH_SIZES = [100, 500, 1000, 5000, 10000] 
NUM_REPETITIONS = 15         
NODES_PER_EXPERIMENT = 5     
PROBABILITY = 0.02           
CONFIDENCE_LEVEL = 0.95 # Nível de confiança desejado
FIXED_SEED = 42 # Semente fixa para reprodutibilidade

# Inicializa o DataFrame que armazenará as estatísticas finais por V
summary_results_classic = pd.DataFrame(columns=[
    'V', 'Média Tempo (s)', 'DP Tempo (s)', 'Média CO2e (kg)', 'DP CO2e (kg)'
])

# =================================================================
# LOOP PRINCIPAL: Itera sobre os tamanhos de grafo (V)
# =================================================================

print("Iniciando a avaliação do Dijkstra Clássico (O(V^2)) com Intervalos de Confiança...")
print("===================================================================================")

for V in GRAPH_SIZES:

    # REQUISITO ATENDIDO: Fixa as sementes antes de cada tamanho de grafo
    random.seed(FIXED_SEED)
    np.random.seed(FIXED_SEED)
    # A geração de grafo NetworkX também usará o estado do random.seed

    print(f"\n[Fase de Grafo V={V}]")
    
    temp_prob = PROBABILITY 
    
    # 1. Geração do Grafo ponderados e conectados com networkx
    G = None
    while True:
        random_seed = int(V * time.time()) 
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

    # =================================================================
    # LOOP SECUNDÁRIO: REPETE O EXPERIMENTO 15 VEZES (Gera 15 linhas)
    # =================================================================

    # 2. Escolhe 5 nós aleatórios e chama a função dijkstrasAlgorithmClassic para calcular o caminho mínimo
    # 3. Repete o experimento 15 vezes (trocando os 5 nós a cada repetição)

    for rep_num in range(1, NUM_REPETITIONS + 1):
        
        print(f"  -> Repetição {rep_num}/{NUM_REPETITIONS} (V={V}) em andamento...", end='\r')

       
        random_starts = random.sample(range(V), min(V, NODES_PER_EXPERIMENT))
        
        total_time = 0
        total_emissions = 0

        # =================================================================
        # LOOP INTERNO: EXECUTA DIJKSTRA PARA CADA UM DOS 5 NÓS
        # =================================================================
        for start_node in random_starts:

            # 4. Medição do tempo(s) e CO2   
            tracker = EmissionsTracker(output_dir=".", save_to_file=False, log_level="error")
            tracker.start()
            start_time = time.time()
            
            _ = dijkstrasAlgorithmClassic(start_node, edges_list)
            
            end_time = time.time()
            emissions = tracker.stop()
            
            total_time += (end_time - start_time)
            total_emissions += emissions if emissions is not None else 0
            
        # Cálculo da Média da Repetição (dividido por 5)
        avg_time = total_time / NODES_PER_EXPERIMENT
        avg_co2e = total_emissions / NODES_PER_EXPERIMENT

        # Adiciona a linha à tabela DESTE V
        table_data.append({
            'Nº Repetição': rep_num,
            'Nós Usados': str(sorted(random_starts)),
            'Tempo (s)': avg_time,
            'CO2e (kg)': avg_co2e
        })
    
    print(" " * 80, end='\r') # Limpa a linha de progresso

    
    # 5. CÁLCULO DOS INTERVALOS DE CONFIANÇA (IC 95%)
    df = pd.DataFrame(table_data)
    
    # Extrai as 15 amostras de cada repetição
    time_samples = df['Tempo (s)'].values
    co2e_samples = df['CO2e (kg)'].values
    n = len(time_samples)

    if n > 1:
        # Estatísticas: Média Geral e Desvio Padrão Amostral (ddof=1)
        mean_time = np.mean(time_samples)
        std_time = np.std(time_samples, ddof=1) 
        mean_co2e = np.mean(co2e_samples)
        std_co2e = np.std(co2e_samples, ddof=1)
        
        # Valor crítico t de Student para 95% de confiança e n-1 graus de liberdade
        df_t = n - 1 
        t_critical = stats.t.ppf(1 - (1 - CONFIDENCE_LEVEL) / 2, df_t)
        
        # Margem de Erro (ME = t * (s / sqrt(n)))
        me_time = t_critical * (std_time / np.sqrt(n))
        me_co2e = t_critical * (std_co2e / np.sqrt(n))
        
        # Intervalo de Confiança (IC = Média +/- ME)
        ic_time_str = f"[{mean_time - me_time:.6f} s, {mean_time + me_time:.6f} s]"
        ic_co2e_str = f"[{mean_co2e - me_co2e:.10f} kg, {mean_co2e + me_co2e:.10f} kg]"
        
       # Adiciona as estatísticas agregadas ao DataFrame resumo
        summary_results_classic.loc[len(summary_results_classic)] = [
          V,
          mean_time,
          std_time,
          mean_co2e,
          std_co2e
        ]

    else:
        # Caso de erro (não deveria ocorrer com n=15)
        mean_time, mean_co2e = 0, 0
        ic_time_str = "N/A (amostra muito pequena)"
        ic_co2e_str = "N/A (amostra muito pequena)"
    
    # =================================================================
    # RESULTADO: Impressão da Tabela e do IC
    # =================================================================

    print("\n" + "="*70)
    print(f"TABELA DE ROBUSTEZ ESTATÍSTICA: DIJKSTRA O(V²) | V = {V} NÓS")
    print("Média do Tempo e CO₂ de 5 execuções aleatórias por repetição.")
    print("="*70)

    # Imprime os Intervalos de Confiança
    print(f"- Média Geral (Tempo) das 15 repetições: {mean_time:.6f} s")
    print(f"Desvio Padrão (Tempo): {std_time:.9f} s")
    print(f"Intervalo de Confiança 95% (Tempo): {ic_time_str}")
    print(f"\n- Média Geral (CO₂e) das 15 repetições: {mean_co2e:.10f} kg")
    print(f"Desvio Padrão (CO₂e): {std_co2e:.9f} kg")
    print(f"Intervalo de Confiança 95% (CO₂e): {ic_co2e_str}")
    print("-" * 70)


    # Formata a tabela para impressão
    df['Tempo (s)'] = df['Tempo (s)'].map('{:.6f}'.format)
    df['CO2e (kg)'] = df['CO2e (kg)'].map('{:.10f}'.format)

    print(df.to_markdown(index=False))
    print("\n" + "="*70 + "\n") # Separador entre tabelas

# PARTE 3 - Tabela Resumo
          
# Formata o DataFrame de resumo
# Adicionado: Conversão forçada para float para evitar o ValueError em ambientes de notebook
for col in ['Média Tempo (s)', 'DP Tempo (s)', 'Média CO2e (kg)', 'DP CO2e (kg)']:
    try:
        summary_results_classic[col] = summary_results_classic[col].astype(float)
    except ValueError:
        # Ignora se já for string ou se o erro for outro.
        pass

summary_results_classic['Média Tempo (s)'] = summary_results_classic['Média Tempo (s)'].map('{:.6f}'.format)
summary_results_classic['DP Tempo (s)'] = summary_results_classic['DP Tempo (s)'].map('{:.9f}'.format)
summary_results_classic['Média CO2e (kg)'] = summary_results_classic['Média CO2e (kg)'].map('{:.10f}'.format)
summary_results_classic['DP CO2e (kg)'] = summary_results_classic['DP CO2e (kg)'].map('{:.12f}'.format)

print(summary_results_classic.to_markdown(index=False))
