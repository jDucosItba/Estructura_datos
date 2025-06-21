"""
Sistema de Transporte
Trabajo Práctico - Estructura de Datos
Alumno: Joaquín Ducos
Legajo: 64.891

"""
from estructuras_datos import ListaEnlazada, Pila
from estructuras_datos import quicksort, mergesort
from leer_csv import leer_nodos, leer_conexiones, leer_solicitudes
from calculador_rutas import encontrar_rutas_principales, calcular_tiempo_segun_consigna, calcular_costo_segun_consigna, crear_itinerario_texto, hay_conexion_aerea_desde_origen, obtener_nombre_vehiculo_amigable
from excepciones import ErrorArchivoCSV, ErrorTransporte
from graficos import generar_todos_los_graficos
import time

def convertir_minutos_a_tiempo(minutos):
    horas = minutos // 60
    minutos_resto = minutos % 60
    segundos = 0
    return "{}h {}m {}s".format(horas, minutos_resto, segundos)

def mostrar_caminos_validos(soluciones):
    # Muestro solo los caminos que realmente funcionan
    print("=== Caminos Validos Encontrados ===")
    
    letras = ['A', 'B', 'C']
    for i, solucion in enumerate(soluciones):
        ruta, conexiones, tiempo_min, costo, itinerario, tipo, peso = solucion
        
        if tipo != 'Aerea' and costo is not None:
            letra = letras[i]
            nombre_vehiculo = obtener_nombre_vehiculo_amigable(tipo)
            tiempo_formateado = convertir_minutos_a_tiempo(tiempo_min)
            
            print("{}: {} - {} - ${:,} - {}".format(
                letra, nombre_vehiculo, itinerario, costo, tiempo_formateado
            ))
    
    print()

def main():
    print("=== Sistema de Transporte Simple ===")
    print()
    
    try:
        print("Leyendo datos de archivos CSV...")
        nodos = leer_nodos('archivos_ejemplo/nodos.csv')
        conexiones = leer_conexiones('archivos_ejemplo/conexiones.csv')
        solicitudes = leer_solicitudes('archivos_ejemplo/solicitudes.csv')
        
        print("Datos cargados: {} nodos, {} conexiones, {} solicitudes".format(
            len(nodos), len(conexiones), len(solicitudes)
        ))
        print()
        
        todas_las_soluciones = []
        
        for idx, solicitud in enumerate(solicitudes):
            origen = solicitud['origen']
            destino = solicitud['destino']
            peso = solicitud['peso_kg']
            
            print("=== SOLICITUD {} ===".format(idx + 1))
            print("Procesando: {} ({} kg)".format(solicitud['id_carga'], peso))
            print("Ruta: {} -> {}".format(origen, destino))
            
            # Encuentro todas las rutas principales por tipo
            print("\nBuscando rutas principales por tipo de transporte...\n")
            rutas_por_tipo = encontrar_rutas_principales(conexiones, origen, destino)
            
            if not rutas_por_tipo:
                print("\nNo se encontraron rutas posibles para esta solicitud\n")
                continue
            
            soluciones = []
            tipos_orden = ['Ferroviaria', 'Automotor', 'Fluvial', 'Aerea']
            
            for tipo in tipos_orden:
                if tipo in rutas_por_tipo:

                    ruta, conexiones_ruta = rutas_por_tipo[tipo]
                    tiempo = calcular_tiempo_segun_consigna(conexiones_ruta)
                    costo = calcular_costo_segun_consigna(conexiones_ruta, peso)
                    itinerario = crear_itinerario_texto(ruta)
                    soluciones.append((ruta, conexiones_ruta, tiempo, costo, itinerario, tipo, peso))

                elif tipo == 'Aerea':
                    if not hay_conexion_aerea_desde_origen(conexiones, origen):
                        soluciones.append(([], [], 0, 0, "", 'Aerea', peso))
            
            mostrar_caminos_validos(soluciones)
            
            soluciones_validas = []
            for sol in soluciones:
                if sol[5] != 'Aerea' and sol[3] is not None:  # Excluyo aéreo y costos None
                    soluciones_validas.append(sol)
            
            if soluciones_validas:
                for solucion in soluciones_validas:
                    todas_las_soluciones.append(solucion)
                
                mejor_tiempo = min(soluciones_validas, key=lambda x: x[2])
                nombre_mejor_tiempo = obtener_nombre_vehiculo_amigable(mejor_tiempo[5])
                print("=== KPI 1: Entrega mas Rapida ===")
                print("Ganador: {} - {} - ${:,}".format(
                    nombre_mejor_tiempo, 
                    convertir_minutos_a_tiempo(mejor_tiempo[2]),
                    mejor_tiempo[3]
                ))
                
                mejor_costo = min(soluciones_validas, key=lambda x: x[3])
                nombre_mejor_costo = obtener_nombre_vehiculo_amigable(mejor_costo[5])
                print("\n=== KPI 2: Transporte mas Economico ===")
                print("Ganador: {} - ${:,} - {}".format(
                    nombre_mejor_costo,
                    mejor_costo[3],
                    convertir_minutos_a_tiempo(mejor_costo[2])
                ))
                
            print()
        
        if todas_las_soluciones:
            print("=== Uso de Estructuras de Datos (todas las solicitudes) ===")
            
            lista_rutas = ListaEnlazada()
            for solucion in todas_las_soluciones:
                lista_rutas.insertar(solucion[4])
            print("Lista enlazada: {} rutas guardadas".format(lista_rutas.tamaño))
            
            pila_soluciones = Pila() 
            for solucion in todas_las_soluciones:
                pila_soluciones.apilar(solucion)
            print("Pila: {} elementos".format(pila_soluciones.tamaño()))
            
            costos = []
            for solucion in todas_las_soluciones:
                costos.append(solucion[3])
            
            inicio = time.perf_counter()
            costos_quick = quicksort(costos.copy())
            tiempo_quick = (time.perf_counter() - inicio) * 1000  # milisegundos
            
            inicio = time.perf_counter() 
            costos_merge = mergesort(costos.copy())
            tiempo_merge = (time.perf_counter() - inicio) * 1000  # milisegundos
            
            print("QuickSort: {:.3f}ms | MergeSort: {:.3f}ms".format(tiempo_quick, tiempo_merge))
            
            generar_todos_los_graficos(todas_las_soluciones)
            
        print("=== Analisis completado ===")
        
    except ErrorArchivoCSV as e:
        print("Error: No se pudo encontrar el archivo:", str(e))
    except ErrorTransporte as e:
        print("Error en los datos:", str(e))
    except Exception as e:
        print("Error inesperado:", str(e))

if __name__ == "__main__":
    main() 