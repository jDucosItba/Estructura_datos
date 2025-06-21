# -*- coding: utf-8 -*-
# Graficos escalables con matplotlib

import matplotlib.pyplot as plt
from calculador_rutas import obtener_nombre_vehiculo_amigable

def generar_grafico_dispersion_tiempo_distancia(soluciones_validas):
    # Grafico 1- Tiempo total vs Distancia total
    plt.figure(figsize=(10, 6))
    
    # Colores por tipo de vehiculo
    colores_vehiculos = {'Tren': 'red', 'Camion': 'blue', 'Barco': 'green', 'Avion': 'orange'}
    
    for solucion in soluciones_validas:
        ruta, conexiones_ruta, tiempo_total, costo_total, itinerario, tipo, peso = solucion
        nombre_vehiculo = obtener_nombre_vehiculo_amigable(tipo)
        
        distancia_total = 0
        for conexion in conexiones_ruta:
            distancia_total += conexion['distancia_km']
        
        # Tamaño del punto basado en el peso (peso mayor = punto más grande)
        tamaño_punto = (peso / 1000) + 20  
        
        color = colores_vehiculos.get(nombre_vehiculo, 'gray')
        plt.scatter(tiempo_total, distancia_total, 
        c=color, s=tamaño_punto, alpha=0.7, label=nombre_vehiculo)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    
    plt.xlabel('Tiempo Total (minutos)')
    plt.ylabel('Distancia Total (km)')
    plt.title('Tiempo vs Distancia (tamaño = peso)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_distancia_tiempo.png')

def generar_histograma_costos(soluciones_validas):
    # Grafico 2- Histograma de costos por tipo de vehiculo
    plt.figure(figsize=(12, 6))
    
    # Separo costos por vehiculo
    costos_por_vehiculo = {}
    for solucion in soluciones_validas:
        ruta, conexiones_ruta, tiempo_total, costo_total, itinerario, tipo, peso = solucion
        nombre_vehiculo = obtener_nombre_vehiculo_amigable(tipo)
        
        if nombre_vehiculo not in costos_por_vehiculo:
            costos_por_vehiculo[nombre_vehiculo] = []
        costos_por_vehiculo[nombre_vehiculo].append(costo_total)
    
    colores = ['red', 'blue', 'green', 'orange']
    vehiculos = list(costos_por_vehiculo.keys())
    
    for i, vehiculo in enumerate(vehiculos):
        plt.subplot(2, 2, i+1)
        costos = costos_por_vehiculo[vehiculo]
        color = colores[i % len(colores)]
        
        plt.hist(costos, bins=10, color=color, alpha=0.7, edgecolor='black')
        plt.title('Costos - {}'.format(vehiculo))
        plt.xlabel('Costo ($)')
        plt.ylabel('Cantidad de Rutas')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_costo_distancia.png')

def generar_grafico_eficiencia(soluciones_validas):
    # Grafico 3- Tiempo vs Costo (muestra la eficiencia)
    plt.figure(figsize=(10, 6))
    
    colores_vehiculos = {'Tren': 'red', 'Camion': 'blue', 'Barco': 'green', 'Avion': 'orange'}
    
    for solucion in soluciones_validas:
        ruta, conexiones_ruta, tiempo_total, costo_total, itinerario, tipo, peso = solucion
        nombre_vehiculo = obtener_nombre_vehiculo_amigable(tipo)
        
        color = colores_vehiculos.get(nombre_vehiculo, 'gray')
        plt.scatter(peso, costo_total, 
                   c=color, s=50, alpha=0.7, label=nombre_vehiculo)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    
    plt.xlabel('Peso (kg)')
    plt.ylabel('Costo ($)')
    plt.title('Peso vs Costo por Vehiculo')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_barras_simple.png')

def generar_todos_los_graficos(soluciones_validas):
    try:
        generar_grafico_dispersion_tiempo_distancia(soluciones_validas)
        generar_histograma_costos(soluciones_validas)
        generar_grafico_eficiencia(soluciones_validas)
        
        print("\nLos graficos ya están listos!")
        
    except Exception as e:
        print("Error generando graficos:", str(e))