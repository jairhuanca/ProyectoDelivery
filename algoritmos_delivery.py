
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:47:56 2026

@author: Grupo 5
"""
"""
BIBLIOTECA DE ALGORITMOS Y HERRAMIENTAS DE OPTIMIZACIÓN DE RUTAS
"""
import math
import itertools
from vehiculos_metodos import calcular_tiempo_viaje

#  MATRIZ Y TSP POR COORDENADAS
def calcular_matriz_distancias(puntos):
    #Esta función calcula la distancia en línea recta entre todos los pares de puntos de una lista.
    n = len(puntos)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = puntos[i]["x"] - puntos[j]["x"]
                dy = puntos[i]["y"] - puntos[j]["y"]
                matriz[i][j] = round(math.sqrt(dx**2 + dy**2), 2)
    return matriz

def resolver_fuerza_bruta(matriz):
    n = len(matriz)
    if n <= 1:
        return [0], 0.0
        
    nodos_intermedios = list(range(1, n))
    mejor_distancia = float('inf')
    mejor_ruta = []
    
    for perm in itertools.permutations(nodos_intermedios):
        ruta_actual = [0] + list(perm) + [0]
        distancia_actual = sum(matriz[ruta_actual[k]][ruta_actual[k+1]] for k in range(len(ruta_actual)-1))
            
        if distancia_actual < mejor_distancia:
            mejor_distancia = distancia_actual
            mejor_ruta = ruta_actual
            
    return mejor_ruta, round(mejor_distancia, 2)

def resolver_greedy(matriz):
    n = len(matriz)
    if n <= 1:
        return [0], 0.0
        
    visitados = [False] * n
    ruta = [0]
    visitados[0] = True
    distancia_total = 0.0
    actual = 0
    
    for _ in range(n - 1):
        siguiente = -1
        menor_distancia = float('inf')
        
        for i in range(n):
            if not visitados[i] and matriz[actual][i] < menor_distancia:
                menor_distancia = matriz[actual][i]
                siguiente = i
                
        if siguiente != -1:
            ruta.append(siguiente)
            visitados[siguiente] = True
            distancia_total += menor_distancia
            actual = siguiente
        
    distancia_total += matriz[actual][0]
    ruta.append(0)
    
    return ruta, round(distancia_total, 2)


#  CÁLCULO DE RUTA Y TIEMPO PUNTO A PUNTO
def calcular_entrega_directa(origen, destino, km, vehiculo_nombre):
    velocidades = {"Bicicleta": 15.0, "Moto": 40.0, "Auto": 30.0}
    vel = velocidades.get(vehiculo_nombre, 30.0)
    
    # En lugar de km / vel * 60:
    tiempo_minutos = calcular_tiempo_viaje(km, vel)
    
    return {
        "origen": origen,
        "destino": destino,
        "kilometros": km,
        "vehiculo": vehiculo_nombre,
        "velocidad_kmh": vel,
        "tiempo_minutos": tiempo_minutos
    }
