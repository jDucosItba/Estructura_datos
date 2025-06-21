class ErrorTransporte(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
    
    def __str__(self):
        return "Error: {}".format(self.mensaje)

class ErrorCarga(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje

class ErrorRuta(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje

class ErrorRutaNoEncontrada(ErrorTransporte):
    def __init__(self, origen, destino):
        mensaje = "No se encontro ruta de {} a {}".format(origen, destino)
        super().__init__(mensaje)

class ErrorCapacidadInsuficiente(ErrorTransporte):
    def __init__(self, peso_carga, capacidad_vehiculo):
        mensaje = "Carga de {}kg excede capacidad de {}kg".format(peso_carga, capacidad_vehiculo)
        super().__init__(mensaje)

class ErrorNodoInexistente(ErrorTransporte):
    def __init__(self, nombre_nodo):
        mensaje = "El nodo '{}' no existe".format(nombre_nodo)
        super().__init__(mensaje)

class ErrorArchivoCSV(ErrorTransporte):
    def __init__(self, archivo, problema):
        mensaje = "Error en archivo {}: {}".format(archivo, problema)
        super().__init__(mensaje)


 