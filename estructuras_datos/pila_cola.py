class Pila:
    def __init__(self):
        self.elementos = []
    
    def apilar(self, elemento):
        self.elementos.append(elemento)
    
    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()
    
    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def tamaño(self):
        return len(self.elementos)

 