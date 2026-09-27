# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:08:58 2026

@author: Grupo 5
"""

# -*- coding: utf-8 -*-
"""
BIBLIOTECA DE GESTION DE VEHICULOS Y TIEMPOS DE TRANSPORTE
"""

VEHICULOS = [
    {"tipo": "Bicicleta", "velocidad_kmh": 15.0},
    {"tipo": "Moto",      "velocidad_kmh": 40.0},
    {"tipo": "Auto",      "velocidad_kmh": 30.0}
]

def calcular_tiempo_viaje(distancia_km, velocidad_kmh):
    #Función que calcula la duración de un viaje en minutos basándose en la distancia y la velocidad de traslado.
    #Divide los kilómetros entre la velocidad para obtener las horas, convierte el resultado a minutos y lo devuelve 
    #redondeado a dos decimales, asegurando además que no ocurra un error si la velocidad es cero o menor.
    if velocidad_kmh <= 0:
        return 0.0
    horas = distancia_km / velocidad_kmh
    minutos = horas * 60.0
    return round(minutos, 2)

def evaluar_vehiculos_para_distancia(distancia_km):
    #Esta función genera un reporte comparativo del tiempo de viaje para diferentes medios de transporte ante una distancia dada. 
    resultados = []
    for v in VEHICULOS:
        t_min = calcular_tiempo_viaje(distancia_km, v["velocidad_kmh"])
        resultados.append({
            "vehiculo": v["tipo"],
            "velocidad_kmh": v["velocidad_kmh"],
            "tiempo_minutos": t_min
        })
    return resultados

