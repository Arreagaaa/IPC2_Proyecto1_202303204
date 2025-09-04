from .lista_enlazada import ListaEnlazada
from .matriz import Matriz
from .par_clave_valor import ParClaveValor


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
            # Usar listas enlazadas en lugar de diccionarios nativos
            grupos_idx = ListaEnlazada()  # Lista de ParClaveValor
            filas_keys = ListaEnlazada()  # Lista de claves

            for i in range(m_patron.num_filas):
                # Crear la clave de la fila como string
                elementos_fila = ListaEnlazada()
                for j in range(m_patron.num_columnas):
                    valor = m_patron.obtener(i, j)
                    elementos_fila.insertar(str(valor.valor) if valor else "0")

                # Crear clave concatenando con comas
                key = ""
                for k in range(elementos_fila.longitud):
                    key += elementos_fila.obtener(k)
                    if k < elementos_fila.longitud - 1:
                        key += ","

                # Buscar si la clave ya existe
                encontrado = False
                for g in range(grupos_idx.longitud):
                    par = grupos_idx.obtener(g)
                    if par.clave == key:
                        # La clave existe, agregar índice a la lista de índices
                        par.valor.insertar(i)
                        encontrado = True
                        break

                if not encontrado:
                    # Nueva clave, crear nueva lista de índices
                    nueva_lista_indices = ListaEnlazada()
                    nueva_lista_indices.insertar(i)
                    nuevo_par = ParClaveValor(key, nueva_lista_indices)
                    grupos_idx.insertar(nuevo_par)
                    filas_keys.insertar(key)

            # Crear matriz reducida
            m_red = Matriz(filas_keys.longitud, m_patron.num_columnas)
            grupos_nombres = ListaEnlazada()  # Lista de ParClaveValor para nombres

            for r_idx in range(filas_keys.longitud):
                key = filas_keys.obtener(r_idx)

                # Buscar la lista de índices para esta clave
                fila_indices = None
                for g in range(grupos_idx.longitud):
                    par = grupos_idx.obtener(g)
                    if par.clave == key:
                        fila_indices = par.valor
                        break

                if not fila_indices:
                    continue

                # Procesar cada columna
                for j in range(m_patron.num_columnas):
                    suma = 0
                    any_val = False
                    for idx_pos in range(fila_indices.longitud):
                        orig_row = fila_indices.obtener(idx_pos)
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

                # Recopilar nombres de estaciones
                nombres = ListaEnlazada()
                for idx_pos in range(fila_indices.longitud):
                    orig_idx = fila_indices.obtener(idx_pos)
                    estacion = headers_fila.obtener(orig_idx)
                    if estacion:
                        nombres.insertar(estacion.nombre)

                # Crear información del grupo usando ParClaveValor
                info_indices = ParClaveValor('indices', fila_indices)
                info_nombres = ParClaveValor('nombres', nombres)

                # Crear lista de información para este grupo
                info_grupo = ListaEnlazada()
                info_grupo.insertar(info_indices)
                info_grupo.insertar(info_nombres)

                grupo_completo = ParClaveValor(key, info_grupo)
                grupos_nombres.insertar(grupo_completo)

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
