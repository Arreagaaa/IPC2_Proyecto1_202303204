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

    def generar_graphviz_tabla(self, titulo, headers_fila, headers_columna, nombre_archivo="matriz_tabla"):
        import graphviz

        def esc(s):
            return str(s).replace('"', '\\"')
        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor.id)}</b></td>'

        filas_html = ""
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion.id)}</b></td>'
        for j in range(self.num_columnas):
            frecuencia = self.obtener(i, j)
            valor = esc(frecuencia.valor)
            bg = "#ffffff" if valor == "0" else "#ffd6d6"
            filas_html += f'<td border="1" bgcolor="{bg}">{valor}</td>'
        filas_html += '</tr>'

        tabla = f'''
          <<table BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <tr><td>
          <table BORDER="1" CELLBORDER="1" CELLSPACING="0">
          <tr>{th_cols}</tr>
              {filas_html}
          </table>
          </td></tr>
          </table>>
        '''

        dot = graphviz.Digraph(comment=str(titulo))
        dot.attr(rankdir='LR')
        dot.node('matriz_tabla', label=tabla, shape='plain')

        dot.node('titulo', label=str(titulo), shape='box',
                 style='filled', fillcolor='lightgreen')
        dot.edge('titulo', 'matriz_tabla', style='invis')

        with open(f'{nombre_archivo}.dot', 'w', encoding='utf-8') as f:
            f.write(dot.source)

        print(f"Archivo DOT generado: {nombre_archivo}.dot")
        print(
            f"Para generar PNG: dot -Tpng {nombre_archivo}.dot -o {nombre_archivo}.png")
        return dot.source
