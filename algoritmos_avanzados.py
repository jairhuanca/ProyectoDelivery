# -*- coding: utf-8 -*-
"""
MÓDULO DE ALGORITMOS AVANZADOS Y ESTRATEGIAS ESPECIALIZADAS
Incluye: Búsqueda con descarte rápido (Backtracking), Optimización con memoria (Programación Dinámica),
Simulación de tráfico con imprevistos (Monte Carlo) y Cálculo en varios procesadores (Paralelismo).
"""

import math
import random
import time
from concurrent.futures import ProcessPoolExecutor

# ==============================================================================
# 1. BACKTRACKING CON PODA (Búsqueda paso a paso descartando rutas malas)
# ==============================================================================
def resolver_backtracking(matriz):
    """
    Encuentra la ruta más corta probando diferentes caminos de entrega (Backtracking).
    Si a mitad de un camino la distancia ya supera a la mejor ruta que teníamos guardada, se
    cancela ese camino de inmediato para ahorrar tiempo (Poda).
    """
    n = len(matriz)
    if n <= 1:
        return [0], 0.0

    visitados = [False] * n
    visitados[0] = True
    mejor_distancia = [float('inf')]
    mejor_ruta = [[]]

    def _backtrack(actual, visitados_count, dist_acumulada, ruta_actual):
        # PODA: Si el costo acumulado ya supera la mejor distancia registrada, no continuamos
        if dist_acumulada >= mejor_distancia[0]:
            return

        # CASO BASE: Si visitamos todos los nodos, retornamos al origen (nodo 0)
        if visitados_count == n:
            dist_total = dist_acumulada + matriz[actual][0]
            if dist_total < mejor_distancia[0]:
                mejor_distancia[0] = dist_total
                mejor_ruta[0] = list(ruta_actual) + [0]
            return

        # PASO RECURSIVO: Probar todos los vecinos no visitados
        for siguiente in range(n):
            if not visitados[siguiente]:
                visitados[siguiente] = True
                ruta_actual.append(siguiente)

                _backtrack(siguiente, visitados_count + 1, dist_acumulada + matriz[actual][siguiente], ruta_actual)

                # BACKTRACK: Deshacer la selección para evaluar la siguiente posibilidad
                ruta_actual.pop()
                visitados[siguiente] = False

    _backtrack(0, 1, 0.0, [0])
    return mejor_ruta[0], round(mejor_distancia[0], 2)


# ==============================================================================
# 2. PROGRAMACIÓN DINÁMICA (Optimización guardando resultados en memoria)
# ==============================================================================
def resolver_programacion_dinamica(matriz):
    """
    Resuelve el problema de rutas guardando en memoria los caminos ya calculados para no repetirlos.
    Usa una técnica eficiente para saber qué clientes ya fueron visitados y reduce enormemente
    el tiempo de cómputo frente a la Fuerza Bruta.
    """
    n = len(matriz)
    if n <= 1:
        return [0], 0.0

    memo = {}

    def _held_karp(mask, pos):
        # Caso base: Todos los nodos han sido visitados (todos los bits en 1)
        if mask == (1 << n) - 1:
            return matriz[pos][0], [pos, 0]

        estado = (mask, pos)
        if estado in memo:
            return memo[estado]

        ans = float('inf')
        mejor_camino = []

        for nxt in range(n):
            # Si el nodo 'nxt' no ha sido visitado
            if not (mask & (1 << nxt)):
                nuevo_costo, camino = _held_karp(mask | (1 << nxt), nxt)
                costo_total = matriz[pos][nxt] + nuevo_costo
                if costo_total < ans:
                    ans = costo_total
                    mejor_camino = [pos] + camino

        memo[estado] = (ans, mejor_camino)
        return memo[estado]

    dist_minima, ruta = _held_karp(1, 0)
    return ruta, round(dist_minima, 2)


# ==============================================================================
# 3. ALGORITMO PROBABILISTA (Simulación de tráfico con imprevistos)
# ==============================================================================
def simular_trafico_monte_carlo(distancia_base_km, velocidad_base_kmh=30.0, num_simulaciones=5000):
    """
    Simula miles de viajes probando diferentes niveles de tráfico aleatorio (hora punta, imprevistos).
    Permite calcular el tiempo promedio de entrega, así como el mejor y el peor escenario posible.
    """
    if distancia_base_km <= 0:
        return {"tiempo_promedio_min": 0.0, "tiempo_mejor_caso_min": 0.0, "tiempo_peor_caso_min": 0.0}

    tiempos_simulados = []

    for _ in range(num_simulaciones):
        # Factor probabilista de tráfico (simula hora punta o imprevistos entre 0.8x y 1.6x)
        factor_congestion = random.uniform(0.8, 1.6)
        vel_efectiva = velocidad_base_kmh / factor_congestion
        tiempo_min = (distancia_base_km / vel_efectiva) * 60.0
        tiempos_simulados.append(tiempo_min)

    tiempo_promedio = sum(tiempos_simulados) / num_simulaciones
    
    return {
        "tiempo_promedio_min": round(tiempo_promedio, 2),
        "tiempo_mejor_caso_min": round(min(tiempos_simulados), 2),
        "tiempo_peor_caso_min": round(max(tiempos_simulados), 2)
    }


# ==============================================================================
# 4. EVALUACIÓN EN PARALELO (Probar varios caminos al mismo tiempo)
# ==============================================================================
def _evaluar_subruta_worker(args):
    """
    Función auxiliar para evaluar una permutación específica en un proceso hijo.
    """
    matriz, perm = args
    ruta_actual = [0] + list(perm) + [0]
    distancia = sum(matriz[ruta_actual[k]][ruta_actual[k+1]] for k in range(len(ruta_actual)-1))
    return distancia, ruta_actual

def resolver_tsp_paralelo(matriz):
    """
   Divide la tarea entre todos los 'núcleos' del procesador para probar varios caminos 
   a la vez en lugar de hacerlo uno por uno.
    """
    import itertools
    n = len(matriz)
    if n <= 1:
        return [0], 0.0

    nodos_intermedios = list(range(1, n))
    permutaciones = list(itertools.permutations(nodos_intermedios))
    tareas = [(matriz, p) for p in permutaciones]

    # Distribución en paralelo usando múltiples núcleos
    with ProcessPoolExecutor() as executor:
        resultados = list(executor.map(_evaluar_subruta_worker, tareas))

    # Selección del mejor resultado calculado
    dist_min, ruta_min = min(resultados, key=lambda x: x[0])
    return ruta_min, round(dist_min, 2)
