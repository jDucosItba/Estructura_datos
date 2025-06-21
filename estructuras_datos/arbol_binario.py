class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(valor)

            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        else:

            if nodo.derecho is None:
                nodo.derecho = NodoArbol(valor)

            else:
                self._insertar_recursivo(nodo.derecho, valor)
    
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        
        if nodo.valor == valor:
            return True
        
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)
    
    def recorrer_en_orden(self):
        resultado = []

        self._en_orden_recursivo(self.raiz, resultado)
        return resultado
    
    def _en_orden_recursivo(self, nodo, resultado):
        if nodo:
            self._en_orden_recursivo(nodo.izquierdo, resultado)

            resultado.append(nodo.valor)
            self._en_orden_recursivo(nodo.derecho, resultado)
