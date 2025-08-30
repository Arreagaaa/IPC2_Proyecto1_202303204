from .lista_enlazada import ListaEnlazada
from .frecuencia import Frecuencia


class Matriz:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = ListaEnlazada()

        for i in range(num_filas):
            fila = ListaEnlazada()
            for j in range(num_columnas):
                frecuencia = Frecuencia("", 0)
                fila.insertar(frecuencia)
            self.matriz.insertar(fila)

    def establecer(self, num_fila, num_columna, frecuencia):
        fila = self.matriz.obtener(num_fila)
        if fila:
            fila.establecer(num_columna, frecuencia)

    def obtener(self, num_fila, num_columna):
        fila = self.matriz.obtener(num_fila)
        if fila:
            return fila.obtener(num_columna)
        return None

    def mostrar(self, titulo, headers_fila, headers_columna):
        print(f"\n{titulo}")
        print("-" * 61)

        header_row = ["Estacion\\Sensor"]
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            header_row.append(str(sensor.id if sensor else ""))
        print("\t".join(header_row))

        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            row_vals = [str(estacion.id if estacion else "")]
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                row_vals.append(str(frecuencia.valor if frecuencia else "0"))
            print("\t".join(row_vals))

    def generar_graphviz_tabla(self, titulo, headers_fila, headers_columna, nombre_archivo="matriz_tabla"):
        import graphviz

        def esc(s):
            return str(s).replace('"', '\\"')

        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor.id if sensor else "")}</b></td>'

        filas_html = ""
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion.id if estacion else "")}</b></td>'
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                valor = esc(frecuencia.valor if frecuencia else "0")
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
