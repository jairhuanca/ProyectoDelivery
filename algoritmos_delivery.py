
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:47:56 2026

@author: jairh
"""
"""
BIBLIOTECA DE ALGORITMOS Y HERRAMIENTAS DE OPTIMIZACIÓN DE RUTAS
"""
import math
import itertools

#  MATRIZ Y TSP POR COORDENADAS
def calcular_matriz_distancias(puntos):
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


# TIEMPOS POR VEHÍCULO
VEHICULOS_DISPONIBLES = [
    {"tipo": "Bicicleta", "velocidad_kmh": 15.0},
    {"tipo": "Moto",      "velocidad_kmh": 40.0},
    {"tipo": "Auto",      "velocidad_kmh": 30.0}
]

def evaluar_tiempos_vehiculos(distancia_km):
    resultados = []
    for v in VEHICULOS_DISPONIBLES:
        tiempo_horas = distancia_km / v["velocidad_kmh"]
        tiempo_minutos = tiempo_horas * 60.0
        resultados.append({
            "vehiculo": v["tipo"],
            "velocidad_kmh": v["velocidad_kmh"],
            "tiempo_minutos": round(tiempo_minutos, 2)
        })
    return resultados


# ORDENAMIENTO DE TRAMOS POR KILOMETRAJE
def ordenamiento_burbuja_tramos(lista_tramos):
    lista = list(lista_tramos)
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["kilometros"] > lista[j + 1]["kilometros"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def ordenamiento_quicksort_tramos(lista_tramos):
    if len(lista_tramos) <= 1:
        return lista_tramos
    pivote = lista_tramos[len(lista_tramos) // 2]["kilometros"]
    menores = [x for x in lista_tramos if x["kilometros"] < pivote]
    iguales = [x for x in lista_tramos if x["kilometros"] == pivote]
    mayores = [x for x in lista_tramos if x["kilometros"] > pivote]
    return ordenamiento_quicksort_tramos(menores) + iguales + ordenamiento_quicksort_tramos(mayores)


#  CAMBIO DE MONEDA  PARA VUELTOS DE DELIVERY
def cambio_monedas_delivery(denominaciones, monto):
    denominaciones_ord = sorted(denominaciones, reverse=True)
    resultado = []
    monto_restante = monto
    for moneda in denominaciones_ord:
        cantidad = monto_restante // moneda
        monto_restante = monto_restante % moneda
        if cantidad > 0:
            resultado.append({"denominacion": moneda, "cantidad": cantidad})
    return resultado, monto_restante

#  CÁLCULO DE RUTA Y TIEMPO PUNTO A PUNTO
def calcular_entrega_directa(origen, destino, km, vehiculo_nombre):
    velocidades = {
        "Bicicleta": 15.0,
        "Moto": 40.0,
        "Auto": 30.0
    }
    
    vel = velocidades.get(vehiculo_nombre, 30.0)
    tiempo_horas = km / vel
    tiempo_minutos = tiempo_horas * 60.0
    
    return {
        "origen": origen,
        "destino": destino,
        "kilometros": km,
        "vehiculo": vehiculo_nombre,
        "velocidad_kmh": vel,
        "tiempo_minutos": round(tiempo_minutos, 2)
    }