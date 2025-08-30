from ..models.lista_enlazada import ListaEnlazada
from ..models.campo import CampoAgricola
from ..models.estacion import Estacion
from ..models.frecuencia import Frecuencia
from ..models.sensor import Sensor
from xml.dom.minidom import parse


class SistemaAgricultura:
    def __init__(self):
        self.campos = ListaEnlazada()

    def cargar_archivo(self, ruta_archivo):
        try:
            dom = parse(ruta_archivo)
            campos_xml = dom.getElementsByTagName("campo")

            for campo_xml in campos_xml:
                id_campo = campo_xml.getAttribute("id")
                nombre_campo = campo_xml.getAttribute("nombre")
                campo = CampoAgricola(id_campo, nombre_campo)

                print(f"Cargando campo: {nombre_campo} (ID: {id_campo})")

                estaciones_xml = campo_xml.getElementsByTagName('estacion')
                for estacion_xml in estaciones_xml:
                    id_est = estacion_xml.getAttribute('id')
                    nombre_est = estacion_xml.getAttribute('nombre')
                    estacion = Estacion(id_est, nombre_est)
                    campo.estaciones.insertar(estacion)

                    print(f"Creando estacion base {id_est}")

                sensores_suelo_xml = campo_xml.getElementsByTagName('sensorS')
                for sensor_xml in sensores_suelo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)

                    frecuencias_xml = sensor_xml.getElementsByTagName(
                        'frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)

                    campo.sensores_suelo.insertar(sensor)
                    print(f"Creando sensor de suelo {id_sensor}")

                sensores_cultivo_xml = campo_xml.getElementsByTagName(
                    'sensorT')
                for sensor_xml in sensores_cultivo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)

                    frecuencias_xml = sensor_xml.getElementsByTagName(
                        'frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)

                    campo.sensores_cultivo.insertar(sensor)
                    print(f"Creando sensor de cultivo {id_sensor}")

                campo.construir_matrices()
                self.campos.insertar(campo)
                print(f"Campo {nombre_campo} cargado exitosamente.\n")

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def listar_campos(self):
        print("Campos disponibles:")
        print("-"*25)
        actual = self.campos.primero

        while actual:
            campo = actual.dato
            print(f"ID: {campo.id}, Nombre: {campo.nombre}")
            actual = actual.siguiente

        def mostrar_campos(self, id_campo):
            actual = self.campos.primero

            while actual:
                campo = actual.dato
                if campo.id == id_campo:
                    campo.mostrar_matrices()
                    return

        def procesar_campos(self):
            print("Procesando campos...")
            actual = self.campos.primero
            while actual:
                campo = actual.dato
                print(f"Procesando campo {campo.id} - {campo.nombre}")
                campo.construir_matriz_patron()
                campo.reducir_patrones()
                actual = actual.siguiente
            print("Procesamiento finalizado.")

        def escribir_salida_xml(self, ruta_salida):
            from xml.dom.minidom import Document

            doc = Document()
            root = doc.createElement('salida')
            doc.appendChild(root)

            estudiante = doc.createElement('estudiante')
            estudiante.appendChild(self._crear_text_element(
                doc, 'nombre', 'Tu Nombre Aqui'))
            estudiante.appendChild(
                self._crear_text_element(doc, 'carnet', '202303204'))
            estudiante.appendChild(self._crear_text_element(
                doc, 'curso', 'Introducción a la Programación y Computación 2'))
            estudiante.appendChild(
                self._crear_text_element(doc, 'seccion', 'A'))
            estudiante.appendChild(
                self._crear_text_element(doc, 'semestre', '4'))
            estudiante.appendChild(self._crear_text_element(
                doc, 'documentacion', 'enlace_a_documentacion'))
            root.appendChild(estudiante)

            campos_node = doc.createElement('campos')
            actual = self.campos.primero
            while actual:
                campo = actual.dato
                cnode = doc.createElement('campo')
                cnode.setAttribute('id', str(campo.id))
                cnode.setAttribute('nombre', campo.nombre)

                if hasattr(campo, 'matriz_reducida_suelo') and campo.matriz_reducida_suelo:
                    mr = doc.createElement('matriz_reducida_suelo')
                    for i in range(campo.matriz_reducida_suelo.num_filas):
                        fila = doc.createElement('fila')
                        for j in range(campo.matriz_reducida_suelo.num_columnas):
                            f = campo.matriz_reducida_suelo.obtener(i, j)
                            cel = doc.createElement('celda')
                            cel.appendChild(doc.createTextNode(
                                str(f.valor if f else '0')))
                            fila.appendChild(cel)
                        mr.appendChild(fila)
                    cnode.appendChild(mr)

                if hasattr(campo, 'matriz_reducida_cultivo') and campo.matriz_reducida_cultivo:
                    mr = doc.createElement('matriz_reducida_cultivo')
                    for i in range(campo.matriz_reducida_cultivo.num_filas):
                        fila = doc.createElement('fila')
                        for j in range(campo.matriz_reducida_cultivo.num_columnas):
                            f = campo.matriz_reducida_cultivo.obtener(i, j)
                            cel = doc.createElement('celda')
                            cel.appendChild(doc.createTextNode(
                                str(f.valor if f else '0')))
                            fila.appendChild(cel)
                        mr.appendChild(fila)
                    cnode.appendChild(mr)

                campos_node.appendChild(cnode)
                actual = actual.siguiente

            root.appendChild(campos_node)

            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(doc.toprettyxml(indent='  ',
                        encoding='utf-8').decode('utf-8'))

            print(f"Archivo de salida escrito en {ruta_salida}")

        def _crear_text_element(self, doc, tag, text):
            el = doc.createElement(tag)
            el.appendChild(doc.createTextNode(text))
            return el

        def datos_estudiante(self):
            return {
                'nombre': 'Tu Nombre Aqui',
                'carnet': '202303204',
                'curso': 'Introducción a la Programación y Computación 2',
                'seccion': 'A',
                'semestre': '4',
                'documentacion': 'enlace_a_documentacion'
            }

        def generar_grafica_campo(self, id_campo, tipo='suelo'):
            actual = self.campos.primero
            while actual:
                campo = actual.dato
                if campo.id == id_campo:
                    if tipo == 'suelo' and campo.matriz_suelo:
                        return campo.matriz_suelo.generar_graphviz_tabla(f"Matriz Suelo - Campo {campo.id}", campo.estaciones, campo.sensores_suelo, f"matriz_suelo_campo_{campo.id}")
                    if tipo == 'cultivo' and campo.matriz_cultivo:
                        return campo.matriz_cultivo.generar_graphviz_tabla(f"Matriz Cultivo - Campo {campo.id}", campo.estaciones, campo.sensores_cultivo, f"matriz_cultivo_campo_{campo.id}")
                    if tipo == 'patron' and hasattr(campo, 'matriz_patron_suelo'):
                        return campo.matriz_patron_suelo.generar_graphviz_tabla(f"Matriz Patron Suelo - Campo {campo.id}", campo.estaciones, campo.sensores_suelo, f"matriz_patron_suelo_campo_{campo.id}")
                actual = actual.siguiente
            print(
                f"Campo {id_campo} no encontrado o tipo {tipo} no disponible")
            return None
