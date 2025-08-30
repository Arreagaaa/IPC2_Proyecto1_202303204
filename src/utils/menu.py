from ..logic.sistema_agricultura import SistemaAgricultura
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
        print("|1. Cargar archivo (seleccionar archivo)|")
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
            for k, v in datos.items():
                print(f"{k}: {v}")

        elif opcion == "5":
            sistema.listar_campos()
            id_campo = input("Ingrese el ID del campo a graficar: ")
            print("Tipos disponibles:")
            print("- suelo (matriz frecuencia F[n,s])")
            print("- cultivo (matriz frecuencia F[n,t])")
            print("- patron (matriz patrones Fp[n,s])")
            print("- reducida_suelo (matriz reducida Fr[n,s])")
            print("- reducida_cultivo (matriz reducida Fr[n,t])")
            tipo = input("Ingrese tipo de matriz a graficar: ")
            resultado = sistema.generar_grafica_campo(id_campo, tipo=tipo)
            if resultado:
                print(f"Gráfica generada exitosamente!")
                print("Para generar PNG ejecutar: dot -Tpng archivo.dot -o archivo.png")

        elif opcion == "6":
            print("\nMostrar matrices:")
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
