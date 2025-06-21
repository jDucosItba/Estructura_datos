def obtener_caracteristicas_vehiculos():
    # Todos los datos son en kg, $(pesos), km/h, km.
    return {
        'Ferroviaria': {
            'velocidad': 100, 
            'capacidad': 150000, 
            'costo_fijo': 100, 
            'costo_por_km_corto': 20, 
            'costo_por_km_largo': 15, 
            'costo_por_kg': 3 
        },
        'Automotor': {
            'velocidad': 80, 
            'capacidad': 30000, 
            'costo_fijo': 30, 
            'costo_por_km': 5, 
            'costo_por_kg_liviano': 1, 
            'costo_por_kg_pesado': 2 
        },
        'Fluvial': {
            'velocidad': 40, 
            'capacidad': 100000, 
            'costo_fijo_fluvial': 500, 
            'costo_fijo_maritimo': 1500, 
            'costo_por_km': 15, 
            'costo_por_kg': 2 
        },
        'Aerea': {
            'velocidad_normal': 600, 
            'velocidad_mal_tiempo': 400, 
            'capacidad': 5000, 
            'costo_fijo': 750, 
            'costo_por_km': 40, 
            'costo_por_kg': 10 
        }
    }

def obtener_nombres_vehiculos():
    return {
        'Ferroviaria': 'Tren',
        'Automotor': 'Camion',
        'Fluvial': 'Barco',
        'Aerea': 'Avion'
    }

def calcular_cantidad_vehiculos_necesarios(peso_carga, capacidad_vehiculo):
    cantidad_vehiculos = peso_carga // capacidad_vehiculo
    if peso_carga % capacidad_vehiculo > 0:
        cantidad_vehiculos += 1
    return int(cantidad_vehiculos)

def calcular_velocidad_real(tipo_vehiculo, conexion):
    vehiculos = obtener_caracteristicas_vehiculos()
    
    if tipo_vehiculo not in vehiculos:
        return 80
    
    vehiculo = vehiculos[tipo_vehiculo]
    
    if tipo_vehiculo == 'Ferroviaria':
        velocidad_base = vehiculo['velocidad']

        if (conexion.get('restriccion') == 'velocidad_max' and conexion.get('valor_restriccion')):

            velocidad_maxima = float(conexion['valor_restriccion'])
            return min(velocidad_base, velocidad_maxima)
        
        return velocidad_base
    
    elif tipo_vehiculo == 'Aerea':

        if (conexion.get('restriccion') == 'prob_mal_tiempo' and conexion.get('valor_restriccion')):
            prob_mal_tiempo = float(conexion['valor_restriccion'])

            if prob_mal_tiempo > 0:
                return vehiculo['velocidad_mal_tiempo']
            
        return vehiculo['velocidad_normal']
    
    else:
        return vehiculo['velocidad']

def puede_usar_conexion(tipo_vehiculo, conexion, peso_carga):
    # Chequeamos si un vehiculo puede usar una conexion
    vehiculos = obtener_caracteristicas_vehiculos()
    
    if tipo_vehiculo not in vehiculos:
        return False
    
    if tipo_vehiculo == 'Automotor':

        if (conexion.get('restriccion') == 'peso_max' and conexion.get('valor_restriccion')):
            peso_max_conexion = float(conexion['valor_restriccion'])

            if peso_carga > peso_max_conexion:
                return False
    
    return True

def calcular_costo_tramo(tipo_vehiculo, conexion, peso_carga):
    vehiculos = obtener_caracteristicas_vehiculos()
    
    if tipo_vehiculo not in vehiculos:
        return 0
    
    vehiculo = vehiculos[tipo_vehiculo]
    distancia = conexion['distancia_km']
    
    cantidad_vehiculos = calcular_cantidad_vehiculos_necesarios(peso_carga, vehiculo['capacidad'])
    
    if tipo_vehiculo == 'Fluvial':
        if (conexion.get('restriccion') == 'tipo' and conexion.get('valor_restriccion') == 'maritimo'):
            costo_fijo = vehiculo['costo_fijo_maritimo'] * cantidad_vehiculos

        else:
            costo_fijo = vehiculo['costo_fijo_fluvial'] * cantidad_vehiculos
    else:
        costo_fijo = vehiculo['costo_fijo'] * cantidad_vehiculos
    
    # Costo por distancia (por cada km recorrido)
    if tipo_vehiculo == 'Ferroviaria':

        if distancia < 200:
            costo_por_km = vehiculo['costo_por_km_corto']

        else:
            costo_por_km = vehiculo['costo_por_km_largo']
        costo_distancia = costo_por_km * distancia * cantidad_vehiculos

    else:
        costo_distancia = vehiculo['costo_por_km'] * distancia * cantidad_vehiculos
    
    return costo_fijo + costo_distancia

def calcular_costo_por_carga(tipo_vehiculo, peso_carga):
    # Calcula el costo por carga (una sola vez para todo el viaje también)
    vehiculos = obtener_caracteristicas_vehiculos()
    
    if tipo_vehiculo not in vehiculos:
        return 0
    
    vehiculo = vehiculos[tipo_vehiculo]
    
    if tipo_vehiculo == 'Automotor':
        # Costo diferente segun peso
        if peso_carga < 15000:
            return vehiculo['costo_por_kg_liviano'] * peso_carga
        else:
            return vehiculo['costo_por_kg_pesado'] * peso_carga
    else:
        return vehiculo['costo_por_kg'] * peso_carga 