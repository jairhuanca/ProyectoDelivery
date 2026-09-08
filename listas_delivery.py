
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:38:58 2026

@author: jairh
"""

"""
PROGRAMA PRINCIPAL DE OPTIMIZACIÓN DE RUTAS DE DELIVERY
"""
import time

# Importaciones desde ambos módulos creados
from algoritmos_delivery import (
    calcular_matriz_distancias,
    resolver_fuerza_bruta,
    resolver_greedy,
    evaluar_tiempos_vehiculos,
    calcular_entrega_directa
)

from rutas_tramo import (
    crear_tramo,
    calcular_distancia_total,
    ordenamiento_burbuja_tramos,
    ordenamiento_quicksort_tramos,
    cambio_monedas_delivery
)

# Variables globales iniciales
PUNTOS_INICIALES = [
    {"id": 0, "nombre": "Almacen Central",            "x": 0.0, "y": 0.0},
    {"id": 1, "nombre": "Cliente A - San Isidro",     "x": 3.0, "y": 4.0},
    {"id": 2, "nombre": "Cliente B - Miraflores",     "x": 6.0, "y": 1.0},
    {"id": 3, "nombre": "Cliente C - Santiago Surco", "x": 7.0, "y": 5.0},
    {"id": 4, "nombre": "Cliente D - San Borja",      "x": 2.0, "y": 8.0},
]

TRAMOS_DIRECTOS = [
    crear_tramo("Almacen Central", "San Isidro", 5.0),
    crear_tramo("San Isidro",      "Miraflores", 3.6),
    crear_tramo("Miraflores",      "Surco",      6.2),
    crear_tramo("Surco",           "San Borja",  5.8)
]

puntos_delivery = list(PUNTOS_INICIALES)
tramos_kilometros = list(TRAMOS_DIRECTOS)
matriz_distancias = calcular_matriz_distancias(puntos_delivery)

# Variables globales para el Explorador de Variables de Spyder
ruta_fb = []
dist_fb = 0.0
t_fb = 0.0

ruta_gr = []
dist_gr = 0.0
t_gr = 0.0

tramos_ordenados = []
evaluacion_vehiculos = []
desglose_vuelto = []
denominaciones_monedas = [100, 50, 20, 10, 5, 2, 1]
ultima_cotizacion_delivery = {}

def formatear_ruta(indices):
    return " -> ".join([puntos_delivery[i]['nombre'] for i in indices])

def agregar_punto():
    global puntos_delivery, matriz_distancias
    print("\n--- AGREGAR NUEVO PUNTO POR COORDENADAS ---")
    nombre = input("Ingrese el nombre del punto/cliente: ").strip()
    try:
        coord_x = float(input("Ingrese la coordenada X (en km): "))
        coord_y = float(input("Ingrese la coordenada Y (en km): "))
        nuevo_id = len(puntos_delivery)
        puntos_delivery.append({"id": nuevo_id, "nombre": nombre, "x": coord_x, "y": coord_y})
        matriz_distancias = calcular_matriz_distancias(puntos_delivery)
        print(f"Punto '{nombre}' registrado correctamente.")
    except ValueError:
        print("Error: Ingrese valores numericos validos.")

def agregar_tramo_kilometros():
    global tramos_kilometros
    print("\n--- AGREGAR TRAMO POR KILOMETRAJE DIRECTO ---")
    origen = input("Punto de Origen: ").strip()
    destino = input("Punto de Destino: ").strip()
    try:
        km = float(input("Distancia en kilometros: "))
        nuevo_tramo = crear_tramo(origen, destino, km)
        tramos_kilometros.append(nuevo_tramo)
        print(f"Tramo {origen} -> {destino} ({km} km) agregado.")
    except ValueError:
        print("Error: Ingrese un kilometraje valido.")

def cotizar_envio_punto_a_punto():
    global ultima_cotizacion_delivery
    print("\n--- COTIZADOR DE ENTREGA DIRECTA (PUNTO A PUNTO) ---")
    origen = input("Ingrese Punto de Inicio (Origen): ").strip()
    destino = input("Ingrese Punto de Llegada (Destino): ").strip()
    
    try:
        km = float(input("Ingrese la distancia en kilometros: "))
        if km <= 0:
            print("Error: La distancia debe ser mayor a 0.")
            return
            
        print("\nSeleccione el Medio de Transporte:")
        print("1. Bicicleta (15 km/h)")
        print("2. Moto (40 km/h)")
        print("3. Auto (30 km/h)")
        op_v = input("Seleccione una opcion (1-3): ").strip()
        
        vehiculos_map = {"1": "Bicicleta", "2": "Moto", "3": "Auto"}
        v_seleccionado = vehiculos_map.get(op_v, "Moto")
        
        ultima_cotizacion_delivery = calcular_entrega_directa(origen, destino, km, v_seleccionado)
        
        print("\n============================================================")
        print("            RESUMEN DE RUTA Y TIEMPO ESTIMADO")
        print("============================================================")
        print(f"  RUTA MARCADA   : {origen} ===> {destino}")
        print(f"  DISTANCIA      : {km:.2f} km")
        print(f"  TRANSPORTE     : {ultima_cotizacion_delivery['vehiculo']} ({ultima_cotizacion_delivery['velocidad_kmh']} km/h)")
        print(f"  TIEMPO ESTIMADO: {ultima_cotizacion_delivery['tiempo_minutos']} minutos")
        print("============================================================")
        
    except ValueError:
        print("Error: Ingrese un numero valido para la distancia.")

def menu():
    global puntos_delivery, tramos_kilometros, matriz_distancias
    global ruta_fb, dist_fb, t_fb
    global ruta_gr, dist_gr, t_gr
    global tramos_ordenados, evaluacion_vehiculos, desglose_vuelto

    while True:
        matriz_distancias = calcular_matriz_distancias(puntos_delivery)
        
        print("\n============================================================")
        print("      SISTEMA INTEGRADO DE OPTIMIZACIÓN Y DELIVERIES")
        print("============================================================")
        print("1. Listar puntos de entrega")
        print("2. Agregar nuevo punto de entrega")
        print("3. Mostrar Matriz de Distancias Euclidianas")
        print("4. Ejecutar TSP - Fuerza Bruta vs Greedy")
        print("5. Registrar y Ordenar tramos por kilometraje")
        print("6. Evaluar tiempo por vehiculo en tramos registrados")
        print("7. Calculadora de Vueltos/Cambio de Pago")
        print("8. Calcular entrega directa punto a punto")
        print("9. Restablecer datos predeterminados")
        print("10. Salir")
        print("============================================================")
        
        opcion = input("Selecciona una opcion (1-10): ").strip()
        
        if opcion == "1":
            print(f"\nPuntos cargados ({len(puntos_delivery)} nodos):")
            for p in puntos_delivery:
                print(f"   [{p['id']}] {p['nombre']} -> X={p['x']}, Y={p['y']}")
                
        elif opcion == "2":
            agregar_punto()
            
        elif opcion == "3":
            print("\nMatriz de Distancias Euclidianas (km):")
            print("     " + "".join([f"[{i}]".rjust(10) for i in range(len(puntos_delivery))]))
            for idx, fila in enumerate(matriz_distancias):
                valores = "".join([f"{val:.2f}".rjust(10) for val in fila])
                print(f"[{idx}] {valores}")
                
        elif opcion == "4":
            inicio = time.perf_counter()
            ruta_fb, dist_fb = resolver_fuerza_bruta(matriz_distancias)
            t_fb = time.perf_counter() - inicio
            
            inicio = time.perf_counter()
            ruta_gr, dist_gr = resolver_greedy(matriz_distancias)
            t_gr = time.perf_counter() - inicio
            
            print(f"\n--- FUERZA BRUTA ---")
            print(f"Ruta: {formatear_ruta(ruta_fb)} | Distancia: {dist_fb:.2f} km | Tiempo: {t_fb:.6f} s")
            
            print(f"\n--- GREEDY (VORAZ) ---")
            print(f"Ruta: {formatear_ruta(ruta_gr)} | Distancia: {dist_gr:.2f} km | Tiempo: {t_gr:.6f} s")
            
        elif opcion == "5":
            print("\n1. Agregar tramo directo en kilometros")
            print("2. Ordenar tramos actuales de menor a mayor distancia")
            sub_op = input("Seleccione sub-opcion: ").strip()
            if sub_op == "1":
                agregar_tramo_kilometros()
            elif sub_op == "2":
                inicio = time.perf_counter()
                tramos_burbuja = ordenamiento_burbuja_tramos(tramos_kilometros)
                t_burbuja = time.perf_counter() - inicio
                
                inicio = time.perf_counter()
                tramos_ordenados = ordenamiento_quicksort_tramos(tramos_kilometros)
                t_quicksort = time.perf_counter() - inicio
                
                print("\nTramos ordenados por distancia (QuickSort):")
                for t in tramos_ordenados:
                    print(f"   {t['origen']} -> {t['destino']}: {t['kilometros']:.2f} km")
                print(f"\nTiempo Burbuja: {t_burbuja:.6f} s | Tiempo QuickSort: {t_quicksort:.6f} s")
                
        elif opcion == "6":
            distancia_total = calcular_distancia_total(tramos_kilometros)
            evaluacion_vehiculos = evaluar_tiempos_vehiculos(distancia_total)
            print(f"\n--- TIEMPOS PARA RECORRER {distancia_total:.2f} KM TOTALES ---")
            for ev in evaluacion_vehiculos:
                print(f"   Vehiculo: {ev['vehiculo']:<10} | Vel: {ev['velocidad_kmh']} km/h | Tiempo: {ev['tiempo_minutos']} min")
            rapido = min(evaluacion_vehiculos, key=lambda x: x['tiempo_minutos'])
            print(f"\nEl vehiculo mas rapido es: {rapido['vehiculo']}")
            
        elif opcion == "7":
            try:
                pago = float(input("\nMonto entregado por el cliente: "))
                costo = float(input("Costo del pedido: "))
                vuelto = int(pago - costo)
                if vuelto < 0:
                    print("El monto ingresado es menor al costo.")
                else:
                    desglose_vuelto, sobrante = cambio_monedas_delivery(denominaciones_monedas, vuelto)
                    print(f"\nVuelto total: {vuelto}")
                    for d in desglose_vuelto:
                        print(f"   Denominacion: {d['denominacion']} -> Cantidad: {d['cantidad']}")
            except ValueError:
                print("Error: Ingrese un monto valido.")
                
        elif opcion == "8":
            cotizar_envio_punto_a_punto()

        elif opcion == "9":
            puntos_delivery = list(PUNTOS_INICIALES)
            tramos_kilometros = list(TRAMOS_DIRECTOS)
            print("\nDatos restablecidos.")
            
        elif opcion == "10":
            print("\nPrograma finalizado.")
            break

if __name__ == "__main__":
    menu()