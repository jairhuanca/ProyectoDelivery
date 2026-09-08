# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:09:26 2026

@author: jairh
"""

# -*- coding: utf-8 -*-
"""
BIBLIOTECA DE ALGORITMOS DE ORDENAMIENTO Y CAMBIO VORAZ
"""

def burbuja_rutas(lista_rutas, clave="kilometros"):
    lista = list(lista_rutas)
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][clave] > lista[j + 1][clave]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def quicksort_rutas(lista_rutas, clave="kilometros"):
    if len(lista_rutas) <= 1:
        return lista_rutas
    
    pivote = lista_rutas[len(lista_rutas) // 2][clave]
    menores = [x for x in lista_rutas if x[clave] < pivote]
    iguales = [x for x in lista_rutas if x[clave] == pivote]
    mayores = [x for x in lista_rutas if x[clave] > pivote]
    
    return quicksort_rutas(menores, clave) + iguales + quicksort_rutas(mayores, clave)

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