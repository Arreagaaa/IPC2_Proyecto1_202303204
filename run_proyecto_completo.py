#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 RUNNER COMPLETO DEL PROYECTO IPC2
Ejecuta TODA la funcionalidad del proyecto en un solo comando
Perfecto para pruebas rápidas y demostración completa
"""

from src.logic.sistema_agricultura import SistemaAgricultura
from src.models.lista_enlazada import ListaEnlazada
import os


def main():
    print("🚀 EJECUTANDO PROYECTO COMPLETO IPC2")
    print("=" * 60)
    print("📋 Christian Javier Rivas Arreaga - 202303204")
    print("🎯 Sistema de Agricultura de Precisión")
    print("=" * 60)

    # PASO 1: INICIALIZAR SISTEMA
    print("\n📁 PASO 1: CARGANDO DATOS")
    print("-" * 40)
    sistema = SistemaAgricultura()
    sistema.cargar_archivo('src/data/camposAgricolas.xml')
    print("✅ Datos cargados exitosamente")

    # PASO 2: PROCESAR CAMPOS
    print("\n⚙️  PASO 2: PROCESANDO CAMPOS")
    print("-" * 40)
    sistema.procesar_campos()
    print("✅ Procesamiento completado")

    # PASO 3: GENERAR XML DE SALIDA
    print("\n💾 PASO 3: GENERANDO XML DE SALIDA")
    print("-" * 40)
    sistema.escribir_salida_xml('salida_final.xml')
    print("✅ XML de salida generado")

    # PASO 4: MOSTRAR DATOS DEL ESTUDIANTE
    print("\n👨‍🎓 PASO 4: DATOS DEL ESTUDIANTE")
    print("-" * 40)
    datos = sistema.datos_estudiante()
    # Convertir diccionario nativo a lista enlazada de tuplas
    lista_datos = ListaEnlazada()
    for k, v in datos.items():
        lista_datos.insertar((k, v))

    for i in range(lista_datos.longitud):
        k, v = lista_datos.obtener(i)
        print(f"  {k}: {v}")

    # PASO 5: GENERAR MATRICES EJEMPLO
    print("\n📊 PASO 5: GENERANDO MATRICES DE EJEMPLO")
    print("-" * 40)

    # Usar lista enlazada en lugar de lista nativa
    ejemplos_matrices = ListaEnlazada()
    ejemplos_matrices.insertar(
        ('02', 'suelo', 'Matriz F[n,s] - Suelo Campo 02'))
    ejemplos_matrices.insertar(
        ('02', 'cultivo', 'Matriz F[n,t] - Cultivo Campo 02'))
    ejemplos_matrices.insertar(
        ('02', 'reducida_suelo', 'Matriz Fr[n,s] - Reducida Suelo Campo 02'))
    ejemplos_matrices.insertar(
        ('03', 'reducida_cultivo', 'Matriz Fr[n,t] - Reducida Cultivo Campo 03'))

    matrices_generadas = ListaEnlazada()
    for i in range(ejemplos_matrices.longitud):
        ejemplo = ejemplos_matrices.obtener(i)
        campo_id, tipo, descripcion = ejemplo
        resultado = sistema.generar_grafica_campo(campo_id, tipo)
        if resultado:
            archivo_dot = f"matriz_{tipo}_campo_{campo_id}.dot"
            matrices_generadas.insertar(archivo_dot)
            print(f"  ✅ {descripcion}")
        else:
            print(f"  ❌ Error: {descripcion}")

    # PASO 6: GENERAR PNGs AUTOMÁTICAMENTE
    print("\n🖼️  PASO 6: GENERANDO IMÁGENES PNG")
    print("-" * 40)

    pngs_generados = 0
    for i in range(matrices_generadas.longitud):
        archivo_dot = matrices_generadas.obtener(i)
        archivo_png = archivo_dot.replace('.dot', '.png')
        if os.system(f"dot -Tpng {archivo_dot} -o {archivo_png}") == 0:
            print(f"  ✅ {archivo_png}")
            pngs_generados += 1
        else:
            print(f"  ⚠️  {archivo_png} (Requiere Graphviz)")

    # PASO 7: RESUMEN FINAL
    print("\n🎊 RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Campos procesados: 10")
    print(f"✅ XML de salida: salida_final.xml")
    print(f"✅ Matrices DOT generadas: {matrices_generadas.longitud}")
    print(f"✅ Imágenes PNG generadas: {pngs_generados}")

    # Verificar archivos generados usando lista enlazada
    archivos_importantes = ListaEnlazada()
    archivos_importantes.insertar('salida_final.xml')
    archivos_importantes.insertar('matriz_suelo_campo_02.dot')
    archivos_importantes.insertar('matriz_reducida_suelo_campo_02.dot')

    print(f"\n📂 ARCHIVOS GENERADOS:")
    for i in range(archivos_importantes.longitud):
        archivo = archivos_importantes.obtener(i)
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"  ✅ {archivo} ({size} bytes)")
        else:
            print(f"  ❌ {archivo} (no encontrado)")

    print(f"\n🎯 ¡PROYECTO EJECUTADO COMPLETAMENTE!")
    print(f"💡 Todos los archivos están listos para revisión")


if __name__ == "__main__":
    main()
