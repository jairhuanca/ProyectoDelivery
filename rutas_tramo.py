# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:10:12 2026

@author: Grupo 5
"""
"""
GESTION DE TRAMOS, ORDENAMIENTO Y CAMBIO VORAZ
"""

def crear_tramo(origen, destino, kilometros):
    #Esta función crea y organiza los datos de un tramo de viaje en un formato estructurado de diccionario. 
    #Recibe un punto de partida, un destino y la distancia, asegura que los kilómetros se registren como un número decimal y 
    #agrupa toda la información en un solo objeto fácil de usar.
    return {
        "origen": origen,
        "destino": destino,
        "kilometros": float(kilometros)
    }

def calcular_distancia_total(lista_rutas):
    #Calcula la distancia total acumulada de un viaje sumando los kilómetros de cada uno de sus tramos. 
    #Recorre una lista de rutas para extraer el valor de los kilómetros de cada sección y devuelve la suma de todo el recorrido.
    return sum(tramo["kilometros"] for tramo in lista_rutas)

def ordenamiento_burbuja_tramos(lista_rutas, clave="kilometros"):
    #Esta función ordena una lista de rutas de menor a mayor comparando y acomodando los elementos de forma consecutiva.
    #Utiliza el algoritmo de ordenamiento burbuja (Bubble Sort), el cual revisa la lista repetidamente para intercambiar 
    #las posiciones de las rutas contiguas si están en el orden incorrecto según la característica elegida (como los kilómetros).

    lista = list(lista_rutas)
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][clave] > lista[j + 1][clave]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def ordenamiento_quicksort_tramos(lista_rutas, clave="kilometros"):
    #Esta función calcula el tiempo de viaje estimado para realizar un envío directo entre dos puntos según 
    #el tipo de transporte utilizado. A partir del vehículo seleccionado, determina su velocidad promedio, 
    #calcula la duración del trayecto en minutos y devuelve un resumen detallado con los datos del viaje.
    
    if len(lista_rutas) <= 1:
        return lista_rutas
    
    pivote = lista_rutas[len(lista_rutas) // 2][clave]
    menores = [x for x in lista_rutas if x[clave] < pivote]
    iguales = [x for x in lista_rutas if x[clave] == pivote]
    mayores = [x for x in lista_rutas if x[clave] > pivote]
    
    return ordenamiento_quicksort_tramos(menores, clave) + iguales + ordenamiento_quicksort_tramos(mayores, clave)

def cambio_monedas_delivery(denominaciones, monto):
    #Función que calcula la menor cantidad de monedas necesarias para dar un vuelto.
    #Utiliza un enfoque voraz que consiste en repartir primero las monedas de mayor valor hasta cubrir el total, 
    #devolviendo el desglose de las monedas utilizadas y el saldo restante que no se pudo simplificar.

    denominaciones_ord = sorted(denominaciones, reverse=True)
    resultado = []
    monto_restante = monto
    
    for moneda in denominaciones_ord:
        cantidad = monto_restante // moneda
        monto_restante = monto_restante % moneda
        if cantidad > 0:
            resultado.append({"denominacion": moneda, "cantidad": cantidad})
            
    return resultado, monto_restante
