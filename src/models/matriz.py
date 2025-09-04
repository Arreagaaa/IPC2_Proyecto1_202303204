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
        def esc(s):
            return str(s).replace('"', '\\"').replace('<', '&lt;').replace('>', '&gt;')

        encabezados_col = ""
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            sensor_id = esc(sensor.id if sensor else f"S{j+1}")
            encabezados_col += f'<td bgcolor="#4CAF50"><font color="white"><b>{sensor_id}</b></font></td>'

        filas_datos = ""
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            estacion_id = esc(estacion.id if estacion else f"E{i+1}")

            filas_datos += f'<tr><td bgcolor="#2196F3"><font color="white"><b>{estacion_id}</b></font></td>'

            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                valor = str(frecuencia.valor if frecuencia else "0")

                if valor == "0":
                    color_fondo = "#FFEBEE"
                else:
                    val_num = int(valor) if valor.isdigit() else 0
                    if val_num > 2000:
                        color_fondo = "#C8E6C9"
                    elif val_num > 1000:
                        color_fondo = "#E8F5E8"
                    else:
                        color_fondo = "#F3E5F5"

                filas_datos += f'<td bgcolor="{color_fondo}"><b>{valor}</b></td>'
            filas_datos += '</tr>'

        tabla_html = f'''<
        <table border="2" cellspacing="0" cellpadding="6">
            <tr>
                <td bgcolor="#FF9800"><font color="white"><b>Est\\Sens</b></font></td>
                {encabezados_col}
            </tr>
            {filas_datos}
        </table>
        >'''

        contenido_dot = f'''// {titulo}
digraph matriz {{
    rankdir=TB;
    node [shape=plaintext];
    graph [bgcolor=white];
    
    // Título con mejor formato
    titulo [label="{esc(titulo)}" 
            shape=box
            style=filled 
            fillcolor="#E3F2FD"
            fontsize=14 
            fontweight=bold
            color="#1976D2"];
    
    // Matriz con tabla HTML
    matriz [label={tabla_html}];
    
    // Layout
    titulo -> matriz [style=invis weight=10];
    
    // Configuración global
    graph [splines=false, pad=0.5];
}}'''

        with open(f'{nombre_archivo}.dot', 'w', encoding='utf-8') as f:
            f.write(contenido_dot)

        print(f"Archivo DOT generado: {nombre_archivo}.dot")
        print(
            f"Para generar PNG: dot -Tpng {nombre_archivo}.dot -o {nombre_archivo}.png")
        print(
            f"Matriz {self.num_filas}x{self.num_columnas} creada exitosamente")
        return contenido_dot
