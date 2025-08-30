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
