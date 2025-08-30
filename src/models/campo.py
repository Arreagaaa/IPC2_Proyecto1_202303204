from .lista_enlazada import ListaEnlazada
from .matriz import Matriz


class CampoAgricola:
    def __init__(self, id_campo, nombre):
        self.id = id_campo
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_suelo = ListaEnlazada()
        self.sensores_cultivo = ListaEnlazada()
        self.matriz_suelo = None
        self.matriz_cultivo = None

    def construir_matrices(self):
        num_estaciones = self.estaciones.longitud
        num_sensores_suelo = self.sensores_suelo.longitud
        num_sensores_cultivo = self.sensores_cultivo.longitud

        self.matriz_suelo = Matriz(num_estaciones, num_sensores_suelo)
        self.matriz_cultivo = Matriz(num_estaciones, num_sensores_cultivo)

        for num_columna in range(num_sensores_suelo):
            sensor = self.sensores_suelo.obtener(num_columna)
            if not sensor:
                continue
            actual_frecuencia = sensor.frecuencias.primero

            while actual_frecuencia:
                frecuencia = actual_frecuencia.dato
                num_fila = self.estaciones.buscar_indice(
                    frecuencia.id_estacion)
                if num_fila != -1:
                    self.matriz_suelo.establecer(
                        num_fila, num_columna, frecuencia)
                actual_frecuencia = actual_frecuencia.siguiente

        for num_columna in range(num_sensores_cultivo):
            sensor = self.sensores_cultivo.obtener(num_columna)
            if not sensor:
                continue
            actual_frecuencia = sensor.frecuencias.primero

            while actual_frecuencia:
                frecuencia = actual_frecuencia.dato
                num_fila = self.estaciones.buscar_indice(
                    frecuencia.id_estacion)
                if num_fila != -1:
                    self.matriz_cultivo.establecer(
                        num_fila, num_columna, frecuencia)
                actual_frecuencia = actual_frecuencia.siguiente

    def mostrar_matrices(self):
        if self.matriz_suelo:
            titulo_suelo = f"Matriz de Suelo - Campo {self.id}"
            self.matriz_suelo.mostrar(
                titulo_suelo, self.estaciones, self.sensores_suelo)

        if self.matriz_cultivo:
            titulo_cultivo = f"Matriz de Cultivo - Campo {self.id}"
            self.matriz_cultivo.mostrar(
                titulo_cultivo, self.estaciones, self.sensores_cultivo)

    def visualizar_matrices_graphviz(self):
        if self.matriz_suelo:
            print("Estoy generando visualización de matriz de suelo...")
            self.matriz_suelo.generar_graphviz_tabla(
                f"Matriz Suelo - Campo {self.id}",
                self.estaciones,
                self.sensores_suelo,
                f"matriz_suelo_campo_{self.id}"
            )

        if self.matriz_cultivo:
            print("Estoy generando visualización de matriz de cultivo...")
            self.matriz_cultivo.generar_graphviz_tabla(
                f"Matriz Cultivo - Campo {self.id}",
                self.estaciones,
                self.sensores_cultivo,
                f"matriz_cultivo_campo_{self.id}"
            )

    def construir_matriz_patron(self):
        if self.matriz_suelo:
            patron = Matriz(self.matriz_suelo.num_filas,
                            self.matriz_suelo.num_columnas)
            for i in range(self.matriz_suelo.num_filas):
                for j in range(self.matriz_suelo.num_columnas):
                    freq = self.matriz_suelo.obtener(i, j)
                    val = "1" if freq and str(freq.valor).strip() not in [
                        "", "0"] else "0"
                    patron.establecer(i, j, type(freq)(
                        freq.id_estacion, val) if freq else None)
            self.matriz_patron_suelo = patron

        if self.matriz_cultivo:
            patron = Matriz(self.matriz_cultivo.num_filas,
                            self.matriz_cultivo.num_columnas)
            for i in range(self.matriz_cultivo.num_filas):
                for j in range(self.matriz_cultivo.num_columnas):
                    freq = self.matriz_cultivo.obtener(i, j)
                    val = "1" if freq and str(freq.valor).strip() not in [
                        "", "0"] else "0"
                    patron.establecer(i, j, type(freq)(
                        freq.id_estacion, val) if freq else None)
            self.matriz_patron_cultivo = patron

    def reducir_patrones(self):
        def reducir(m_patron, headers_fila, matriz_original):
            grupos_idx = {}
            filas_keys = []
            for i in range(m_patron.num_filas):
                row = [str(m_patron.obtener(i, j).valor) if m_patron.obtener(
                    i, j) else "0" for j in range(m_patron.num_columnas)]
                key = ",".join(row)
                if key in grupos_idx:
                    grupos_idx[key].append(i)
                else:
                    grupos_idx[key] = [i]
                    filas_keys.append(key)

            m_red = Matriz(len(filas_keys), m_patron.num_columnas)
            grupos_nombres = {}
            for r_idx, key in enumerate(filas_keys):
                fila_indices = grupos_idx[key]
                nombres = []
                for j in range(m_patron.num_columnas):
                    suma = 0
                    any_val = False
                    for orig_row in fila_indices:
                        cell = matriz_original.obtener(orig_row, j)
                        if cell and str(cell.valor).strip() not in ["", "0"]:
                            try:
                                suma += float(cell.valor)
                                any_val = True
                            except Exception:
                                pass
                    src = matriz_original.obtener(0, j)
                    freq_cls = type(src) if src else None
                    if freq_cls:
                        val_str = str(int(suma)) if any_val else "0"
                        m_red.establecer(r_idx, j, freq_cls("", val_str))
                nombres = [headers_fila.obtener(
                    idx).nombre for idx in fila_indices]
                grupos_nombres[key] = {
                    'indices': fila_indices, 'nombres': nombres}

            return m_red, grupos_nombres

        if hasattr(self, 'matriz_patron_suelo') and self.matriz_patron_suelo:
            m_red, grupos = reducir(
                self.matriz_patron_suelo, self.estaciones, self.matriz_suelo)
            self.matriz_reducida_suelo = m_red
            self.grupos_suelo = grupos

        if hasattr(self, 'matriz_patron_cultivo') and self.matriz_patron_cultivo:
            m_red, grupos = reducir(
                self.matriz_patron_cultivo, self.estaciones, self.matriz_cultivo)
            self.matriz_reducida_cultivo = m_red
            self.grupos_cultivo = grupos
