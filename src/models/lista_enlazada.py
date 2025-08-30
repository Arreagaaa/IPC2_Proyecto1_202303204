from .nodo import Nodo


class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.longitud = 0

    def agregar(self, dato):
        nodo = Nodo(dato)
        if not self.primero:
            self.primero = nodo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo
        self.longitud += 1

    def insertar(self, dato):
        return self.agregar(dato)

    def tamanio(self):
        return self.longitud

    def establecer(self, indice, dato):
        if indice < 0 or indice >= self.longitud:
            return False
        actual = self.primero
        for i in range(indice):
            actual = actual.siguiente
        actual.dato = dato
        return True

    def obtener(self, indice):
        if indice < 0 or indice >= self.longitud:
            return None
        actual = self.primero
        for i in range(indice):
            actual = actual.siguiente

        return actual.dato

    def buscar_indice(self, id_buscar):
        actual = self.primero
        indice = 0
        while actual:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_buscar:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1
