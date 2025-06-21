from vehiculos import (calcular_velocidad_real, puede_usar_conexion, 
                      calcular_costo_tramo, calcular_costo_por_carga, 
                      obtener_nombres_vehiculos, obtener_caracteristicas_vehiculos)

def encontrar_rutas_principales(conexiones, origen, destino):
    rutas_por_tipo = {}
    
    # Primero busco conexiones directas
    for conexion in conexiones:
        if conexion['origen'] == origen and conexion['destino'] == destino:
            tipo = conexion['tipo']
            ruta = [origen, destino]
            conexiones_ruta = [conexion]
            rutas_por_tipo[tipo] = (ruta, conexiones_ruta)
    
    # Si no encuentro directas, busco rutas con una parada intermedia
    if not rutas_por_tipo:
        ciudades_intermedias = set()
        for conexion in conexiones:
            if conexion['origen'] == origen:
                ciudades_intermedias.add(conexion['destino'])
        
        # Para cada ciudad intermedia, verifico si hay conexion al destino
        for ciudad_intermedia in ciudades_intermedias:
            conexiones_tramo1 = []
            for conexion in conexiones:
                if conexion['origen'] == origen and conexion['destino'] == ciudad_intermedia:
                    conexiones_tramo1.append(conexion)
            
            conexiones_tramo2 = []
            for conexion in conexiones:
                if conexion['origen'] == ciudad_intermedia and conexion['destino'] == destino:
                    conexiones_tramo2.append(conexion)
            
            # Combino por tipo de transporte
            for conn1 in conexiones_tramo1:
                for conn2 in conexiones_tramo2:
                    if conn1['tipo'] == conn2['tipo']:  # Mismo tipo de transporte
                        tipo = conn1['tipo']
                        ruta = [origen, ciudad_intermedia, destino]
                        conexiones_ruta = [conn1, conn2]
                        rutas_por_tipo[tipo] = (ruta, conexiones_ruta)
    
    return rutas_por_tipo

def calcular_tiempo_segun_consigna(conexiones_ruta):
    if not conexiones_ruta:
        return 0
    
    tiempo_total_minutos = 0
    
    for conexion in conexiones_ruta:
        tipo_vehiculo = conexion['tipo']
        velocidad_real = calcular_velocidad_real(tipo_vehiculo, conexion)
        
        tiempo_horas = conexion['distancia_km'] / velocidad_real
        tiempo_minutos = tiempo_horas * 60
        tiempo_total_minutos += tiempo_minutos
    
    return int(tiempo_total_minutos)

def calcular_costo_segun_consigna(conexiones_ruta, peso_carga):
    if not conexiones_ruta:
        return 0
    
    tipo_transporte = conexiones_ruta[0]['tipo']
    
    for conexion in conexiones_ruta:
        if not puede_usar_conexion(tipo_transporte, conexion, peso_carga):
            return None  # La ruta no es valida
    
    costo_total = 0
    for conexion in conexiones_ruta:
        costo_tramo = calcular_costo_tramo(tipo_transporte, conexion, peso_carga)
        costo_total += costo_tramo
    
    # Costo por carga (una sola vez para todo el viaje)
    costo_carga = calcular_costo_por_carga(tipo_transporte, peso_carga)
    costo_total += costo_carga
    
    return int(costo_total)

def crear_itinerario_texto(ruta):
    return " - ".join(ruta)

def hay_conexion_aerea_desde_origen(conexiones, origen):
    # Verifico si hay conexiones aereas desde el origen
    for conexion in conexiones:
        if conexion['origen'] == origen and conexion['tipo'] == 'Aerea':
            return True
    return False

def obtener_nombre_vehiculo_amigable(tipo):
    nombres = obtener_nombres_vehiculos()
    return nombres.get(tipo, tipo)

def calcular_datos_acumulados_solucion(ruta, conexiones_ruta, peso_carga):
    if not conexiones_ruta:
        return [], [], [], []
    
    distancias_acum = [0]  
    tiempos_acum = [0]    
    costos_acum = [0]      
    nombres_tramos = ['Inicio']
    
    tipo_transporte = conexiones_ruta[0]['tipo']
    
    distancia_total = 0
    tiempo_total = 0
    costo_total = 0
    
    for i, conexion in enumerate(conexiones_ruta):
        distancia_total += conexion['distancia_km']
        distancias_acum.append(distancia_total)
        
        velocidad_real = calcular_velocidad_real(tipo_transporte, conexion)
        tiempo_tramo_horas = conexion['distancia_km'] / velocidad_real
        tiempo_tramo_min = tiempo_tramo_horas * 60
        tiempo_total += tiempo_tramo_min
        tiempos_acum.append(tiempo_total)
        
        costo_tramo = calcular_costo_tramo(tipo_transporte, conexion, peso_carga)
        costo_total += costo_tramo
        costos_acum.append(costo_total)
        
        nombres_tramos.append("{} -> {}".format(conexion['origen'], conexion['destino']))
    
    # Agrego costo por carga al final (solo una vez)
    costo_carga = calcular_costo_por_carga(tipo_transporte, peso_carga)
    
    for i in range(1, len(costos_acum)):
        costos_acum[i] += costo_carga
    
    return distancias_acum, tiempos_acum, costos_acum, nombres_tramos 