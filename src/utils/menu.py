from ..logic.sistema_agricultura import SistemaAgricultura
from ..models.lista_enlazada import ListaEnlazada
import tkinter as tk
from tkinter import filedialog


def elegir_archivo_dialogo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        filetypes=[('XML files', '*.xml'), ('All files', '*.*')])
    root.destroy()
    return archivo


def guardar_archivo_dialogo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[
                                           ('XML files', '*.xml'), ('All files', '*.*')])
    root.destroy()
    return archivo


def main():
    sistema = SistemaAgricultura()

    while True:
        print("---------------------------------------")
        print("| SISTEMA DE AGRICULTURA DE PRECISION |")
        print("---------------------------------------")
        print("|1. Cargar archivo                     |")
        print("|2. Procesar archivo                   |")
        print("|3. Escribir archivo de salida         |")
        print("|4. Mostrar datos del estudiante       |")
        print("|5. Generar gráfica                    |")
        print("|6. Mostrar matrices                   |")
        print("|7. Salir                              |")
        print("---------------------------------------")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            print("\nSeleccionar archivo XML a cargar...")
            archivo = elegir_archivo_dialogo()
            if archivo:
                sistema.cargar_archivo(archivo)
            else:
                print("No se seleccionó archivo")

        elif opcion == "2":
            print("\nProcesando archivo en memoria...")
            sistema.procesar_campos()

        elif opcion == "3":
            print("\nSeleccionar ubicación para guardar archivo de salida...")
            salida = guardar_archivo_dialogo()
            if salida:
                sistema.escribir_salida_xml(salida)
            else:
                print("No se seleccionó ruta de salida")

        elif opcion == "4":
            datos = sistema.datos_estudiante()
            print("Datos del estudiante:")
            # Convertir diccionario nativo a lista enlazada
            lista_datos = ListaEnlazada()
            for k, v in datos.items():
                lista_datos.insertar((k, v))
            
            for i in range(lista_datos.longitud):
                k, v = lista_datos.obtener(i)
                print(f"{k}: {v}")

        elif opcion == "5":
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo a graficar: ")

            print("\n" + "="*50)
            print("       SELECCIONAR TIPO DE MATRIZ")
            print("="*50)
            print("| 1. Suelo (matriz frecuencia F[n,s])      |")
            print("| 2. Cultivo (matriz frecuencia F[n,t])    |")
            print("| 3. Patrón (matriz patrones Fp[n,s])      |")
            print("| 4. Reducida Suelo (matriz Fr[n,s])       |")
            print("| 5. Reducida Cultivo (matriz Fr[n,t])     |")
            print("="*50)

            tipo_opcion = input("Seleccione el tipo de matriz (1-5): ")

            tipos_matriz = {
                "1": "suelo",
                "2": "cultivo",
                "3": "patron",
                "4": "reducida_suelo",
                "5": "reducida_cultivo"
            }

            if tipo_opcion in tipos_matriz:
                tipo = tipos_matriz[tipo_opcion]
                print(
                    f"\n Generando gráfica tipo '{tipo}' para campo {id_campo}...")
                resultado = sistema.generar_grafica_campo(id_campo, tipo=tipo)
                if resultado:
                    print(f"¡Gráfica generada exitosamente!")
                    print(f"Archivo: {resultado}")
                    print(
                        "Para generar PNG ejecutar: dot -Tpng archivo.dot -o archivo.png")
                else:
                    print("Error al generar la gráfica")
            else:
                print("Opción no válida. Debe seleccionar un número del 1 al 5.")

        elif opcion == "6":
            print("\n" + "="*50)
            print("         MOSTRAR MATRICES DE CAMPO")
            print("="*50)
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo: ")
            sistema.mostrar_campos(id_campo)

        elif opcion == "7":
            print("Ejecucion Finalizada...")
            break

        else:
            print("Opcion no valida")


if __name__ == "__main__":
    main()
