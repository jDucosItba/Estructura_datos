def leer_nodos(archivo):
    nodos = []
    with open(archivo, 'r') as f:
        lineas = f.readlines()
        # Salto la primera linea que son los titulos
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea:  #Si no está vacía la línea
                nodos.append(linea)
    return nodos

def leer_conexiones(archivo):
    conexiones = []
    with open(archivo, 'r') as f:
        lineas = f.readlines()
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea: 
                partes = linea.split(',')
                conexion = {
                    'origen': partes[0],
                    'destino': partes[1],
                    'tipo': partes[2],
                    'distancia_km': int(partes[3])
                }
                if len(partes) > 4 and partes[4]:
                    conexion['restriccion'] = partes[4]
                    if len(partes) > 5 and partes[5]:
                        # Convierto el valor segun el tipo
                        valor = partes[5]
                        if valor.replace('.', '').isdigit():
                            conexion['valor_restriccion'] = float(valor)
                        else:
                            conexion['valor_restriccion'] = valor
                conexiones.append(conexion)
    return conexiones

def leer_solicitudes(archivo):
    solicitudes = []
    with open(archivo, 'r') as f:
        lineas = f.readlines()
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea: 
                partes = linea.split(',')
                solicitud = {
                    'id_carga': partes[0],
                    'peso_kg': int(partes[1]),
                    'origen': partes[2],
                    'destino': partes[3]
                }
                solicitudes.append(solicitud)
    return solicitudes

