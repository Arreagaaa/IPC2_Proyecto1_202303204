from ..models.lista_enlazada import ListaEnlazada
from ..models.campo import CampoAgricola
from ..models.estacion import Estacion
from ..models.frecuencia import Frecuencia
from ..models.sensor import Sensor
from xml.dom.minidom import parse, Document


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
                    print(f"Creando estación base {id_est}")

                sensores_suelo_xml = campo_xml.getElementsByTagName('sensorS')
                for sensor_xml in sensores_suelo_xml:
                    id_sensor = sensor_xml.getAttribute('id')
                    nombre_sensor = sensor_xml.getAttribute('nombre')
                    sensor = Sensor(id_sensor, nombre_sensor)
                    frecuencias_xml = sensor_xml.getElementsByTagName(
                        'frecuencia')
                    for freq_xml in frecuencias_xml:
                        id_estacion = freq_xml.getAttribute('idEstacion')
                        valor = freq_xml.firstChild.data.strip() if freq_xml.firstChild else '0'
                        frecuencia = Frecuencia(id_estacion, int(valor))
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
                        valor = freq_xml.firstChild.data.strip() if freq_xml.firstChild else '0'
                        frecuencia = Frecuencia(id_estacion, int(valor))
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
            actual = actual.siguiente
        print(f"Campo {id_campo} no encontrado.")

    def procesar_campos(self):
        print("Procesando campos...")
        actual = self.campos.primero
        while actual:
            campo = actual.dato
            print(f"Procesando campo {campo.id} - {campo.nombre}")
            campo.construir_matriz_patron()
            campo.reducir_patrones()
            print(
                f"Campo {campo.id} procesado - Estaciones reducidas generadas")
            actual = actual.siguiente
        print("Procesamiento finalizado.")

    def escribir_salida_xml(self, ruta_salida):
        doc = Document()
        root = doc.createElement('camposAgricolas')
        doc.appendChild(root)

        actual = self.campos.primero
        while actual:
            campo = actual.dato
            cnode = doc.createElement('campo')
            cnode.setAttribute('id', str(campo.id))
            cnode.setAttribute('nombre', campo.nombre)

            grupos = None
            if hasattr(campo, 'grupos_estaciones') and campo.grupos_estaciones:
                grupos = campo.grupos_estaciones
            elif hasattr(campo, 'grupos_suelo') and campo.grupos_suelo:
                grupos = campo.grupos_suelo
            elif hasattr(campo, 'grupos_cultivo') and campo.grupos_cultivo:
                grupos = campo.grupos_cultivo

            if grupos:
                est_red = doc.createElement('estacionesBaseReducidas')
                for key, info in grupos.items():
                    nombres = info.get('nombres', [])
                    indices = info.get('indices', [])
                    rep_id = ''
                    if indices:
                        est_obj = campo.estaciones.obtener(indices[0])
                        rep_id = est_obj.id if est_obj else ''
                    e = doc.createElement('estacion')
                    if rep_id:
                        e.setAttribute('id', rep_id)
                    e.setAttribute('nombre', ', '.join(nombres))
                    est_red.appendChild(e)
                cnode.appendChild(est_red)

                if hasattr(campo, 'matriz_reducida_suelo') and campo.matriz_reducida_suelo:
                    sensores_node = doc.createElement('sensoresSuelo')
                    m = campo.matriz_reducida_suelo
                    for j in range(m.num_columnas):
                        sensor_obj = campo.sensores_suelo.obtener(j)
                        s_node = doc.createElement('sensorS')
                        if sensor_obj:
                            s_node.setAttribute('id', sensor_obj.id)
                            s_node.setAttribute('nombre', sensor_obj.nombre)
                        for row_idx, (key, info) in enumerate(grupos.items()):
                            indices = info.get('indices', [])
                            rep_id = campo.estaciones.obtener(
                                indices[0]).id if indices else ''
                            val_cell = m.obtener(row_idx, j)
                            valor = None
                            if val_cell and hasattr(val_cell, 'valor'):
                                try:
                                    val_num = int(val_cell.valor) if isinstance(
                                        val_cell.valor, str) else val_cell.valor
                                    if val_num > 0:
                                        valor = str(val_num)
                                except:
                                    pass
                            if valor:
                                f_el = doc.createElement('frecuencia')
                                if rep_id:
                                    f_el.setAttribute('idEstacion', rep_id)
                                f_el.appendChild(doc.createTextNode(valor))
                                s_node.appendChild(f_el)
                        sensores_node.appendChild(s_node)
                    cnode.appendChild(sensores_node)

                if hasattr(campo, 'matriz_reducida_cultivo') and campo.matriz_reducida_cultivo:
                    sensores_node = doc.createElement('sensoresCultivo')
                    m = campo.matriz_reducida_cultivo
                    for j in range(m.num_columnas):
                        sensor_obj = campo.sensores_cultivo.obtener(j)
                        s_node = doc.createElement('sensorT')
                        if sensor_obj:
                            s_node.setAttribute('id', sensor_obj.id)
                            s_node.setAttribute('nombre', sensor_obj.nombre)
                        for row_idx, (key, info) in enumerate(grupos.items()):
                            indices = info.get('indices', [])
                            rep_id = campo.estaciones.obtener(
                                indices[0]).id if indices else ''
                            val_cell = m.obtener(row_idx, j)
                            valor = None
                            if val_cell and hasattr(val_cell, 'valor'):
                                try:
                                    val_num = int(val_cell.valor) if isinstance(
                                        val_cell.valor, str) else val_cell.valor
                                    if val_num > 0:
                                        valor = str(val_num)
                                except:
                                    pass
                            if valor:
                                f_el = doc.createElement('frecuencia')
                                if rep_id:
                                    f_el.setAttribute('idEstacion', rep_id)
                                f_el.appendChild(doc.createTextNode(valor))
                                s_node.appendChild(f_el)
                        sensores_node.appendChild(s_node)
                    cnode.appendChild(sensores_node)

            else:
                estaciones_base = doc.createElement('estacionesBase')
                for i in range(campo.estaciones.tamanio()):
                    est = campo.estaciones.obtener(i)
                    e = doc.createElement('estacion')
                    e.setAttribute('id', str(est.id))
                    e.setAttribute('nombre', est.nombre)
                    estaciones_base.appendChild(e)
                cnode.appendChild(estaciones_base)

                sensores_node = doc.createElement('sensoresSuelo')
                for si in range(campo.sensores_suelo.tamanio()):
                    sensor_obj = campo.sensores_suelo.obtener(si)
                    s_node = doc.createElement('sensorS')
                    if sensor_obj:
                        s_node.setAttribute('id', sensor_obj.id)
                        s_node.setAttribute('nombre', sensor_obj.nombre)
                        actual_f = sensor_obj.frecuencias.primero
                        while actual_f:
                            f = actual_f.dato
                            f_el = doc.createElement('frecuencia')
                            f_el.setAttribute('idEstacion', f.id_estacion)
                            f_el.appendChild(doc.createTextNode(str(f.valor)))
                            s_node.appendChild(f_el)
                            actual_f = actual_f.siguiente
                    sensores_node.appendChild(s_node)
                cnode.appendChild(sensores_node)

                sensores_node = doc.createElement('sensoresCultivo')
                for si in range(campo.sensores_cultivo.tamanio()):
                    sensor_obj = campo.sensores_cultivo.obtener(si)
                    s_node = doc.createElement('sensorT')
                    if sensor_obj:
                        s_node.setAttribute('id', sensor_obj.id)
                        s_node.setAttribute('nombre', sensor_obj.nombre)
                        actual_f = sensor_obj.frecuencias.primero
                        while actual_f:
                            f = actual_f.dato
                            f_el = doc.createElement('frecuencia')
                            f_el.setAttribute('idEstacion', f.id_estacion)
                            f_el.appendChild(doc.createTextNode(str(f.valor)))
                            s_node.appendChild(f_el)
                            actual_f = actual_f.siguiente
                    sensores_node.appendChild(s_node)
                cnode.appendChild(sensores_node)

            root.appendChild(cnode)
            actual = actual.siguiente

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent='  ',
                    encoding='utf-8').decode('utf-8'))

        print(f"Archivo de salida escrito en {ruta_salida}")

    def datos_estudiante(self):
        return {
            'nombre': 'Christian Javier Rivas Arreaga',
            'carnet': '202303204',
            'curso': 'Introducción a la Programación y Computación 2',
            'seccion': 'C',
            'semestre': '4to. Semestre',
            'documentacion': 'https://github.com/Arreagaaa/IPC2_Proyecto1_202303204'
        }

    def generar_grafica_campo(self, id_campo, tipo='suelo'):
        actual = self.campos.primero
        while actual:
            campo = actual.dato
            if campo.id == id_campo:
                if tipo == 'suelo' and campo.matriz_suelo:
                    return campo.matriz_suelo.generar_graphviz_tabla(f"Matriz Frecuencia F[n,s] - Campo {campo.id}", campo.estaciones, campo.sensores_suelo, f"matriz_suelo_campo_{campo.id}")
                elif tipo == 'cultivo' and campo.matriz_cultivo:
                    return campo.matriz_cultivo.generar_graphviz_tabla(f"Matriz Frecuencia F[n,t] - Campo {campo.id}", campo.estaciones, campo.sensores_cultivo, f"matriz_cultivo_campo_{campo.id}")
                elif tipo == 'patron' and hasattr(campo, 'matriz_patron_suelo'):
                    return campo.matriz_patron_suelo.generar_graphviz_tabla(f"Matriz Patrones Fp[n,s] - Campo {campo.id}", campo.estaciones, campo.sensores_suelo, f"matriz_patron_suelo_campo_{campo.id}")
                elif tipo == 'reducida_suelo' and hasattr(campo, 'matriz_reducida_suelo'):
                    return campo.matriz_reducida_suelo.generar_graphviz_tabla(f"Matriz Reducida Fr[n,s] - Campo {campo.id}", campo.estaciones, campo.sensores_suelo, f"matriz_reducida_suelo_campo_{campo.id}")
                elif tipo == 'reducida_cultivo' and hasattr(campo, 'matriz_reducida_cultivo'):
                    return campo.matriz_reducida_cultivo.generar_graphviz_tabla(f"Matriz Reducida Fr[n,t] - Campo {campo.id}", campo.estaciones, campo.sensores_cultivo, f"matriz_reducida_cultivo_campo_{campo.id}")
                else:
                    print(
                        f"Tipo de gráfica '{tipo}' no disponible para el campo {id_campo}")
                    print(
                        "Tipos válidos: suelo, cultivo, patron, reducida_suelo, reducida_cultivo")
                    return None
            actual = actual.siguiente
        print(f"Campo {id_campo} no encontrado")
        return None
