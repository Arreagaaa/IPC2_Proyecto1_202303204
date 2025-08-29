from lista_enlazada import ListaEnlazada
from frecuencia import Frecuencia


class Matriz:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = ListaEnlazada()

        for i in range(num_filas):
            fila = ListaEnlazada()
            for j in range(num_columnas):
                frecuencia = Frecuencia("", 0)
                fila.agregar(frecuencia)
            self.matriz.agregar(fila)

    def establecer(self, num_fila, num_columna, frecuencia):
        fila = self.matriz.obtener(num_fila)
        if fila:
            columna = fila.primero
            for i in range(num_columna):
                if columna:
                    columna = columna.siguiente
            if columna:
                columna.dato = frecuencia

    def obtener(self, num_fila, num_columna):
        fila = self.matriz.obtener(num_fila)
        if fila:
            return fila.obtener(num_columna)
        return None

    def mostrar(self, titulo, headers_fila, headers_columna):
        print(f"\n{titulo}")
        print("-"*61)

        print("Estacion\\Sensor", end="\t")
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            print(f"{sensor.id}", end="\t")
        print()

        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            print(f"{estacion.id}", end="\t")
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                print(f"{frecuencia.valor}", end="\t")
        print()
