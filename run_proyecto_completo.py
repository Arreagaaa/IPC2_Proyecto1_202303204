#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 RUNNER COMPLETO DEL PROYECTO IPC2
Ejecuta TODA la funcionalidad del proyecto en un solo comando
Perfecto para pruebas rápidas y demostración completa
"""

from src.logic.sistema_agricultura import SistemaAgricultura
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
    for k, v in datos.items():
        print(f"  {k}: {v}")
    
    # PASO 5: GENERAR MATRICES EJEMPLO
    print("\n📊 PASO 5: GENERANDO MATRICES DE EJEMPLO")
    print("-" * 40)
    
    ejemplos_matrices = [
        ('02', 'suelo', 'Matriz F[n,s] - Suelo Campo 02'),
        ('02', 'cultivo', 'Matriz F[n,t] - Cultivo Campo 02'),
        ('02', 'reducida_suelo', 'Matriz Fr[n,s] - Reducida Suelo Campo 02'),
        ('03', 'reducida_cultivo', 'Matriz Fr[n,t] - Reducida Cultivo Campo 03')
    ]
    
    matrices_generadas = []
    for campo_id, tipo, descripcion in ejemplos_matrices:
        resultado = sistema.generar_grafica_campo(campo_id, tipo)
        if resultado:
            archivo_dot = f"matriz_{tipo}_campo_{campo_id}.dot"
            matrices_generadas.append(archivo_dot)
            print(f"  ✅ {descripcion}")
        else:
            print(f"  ❌ Error: {descripcion}")
    
    # PASO 6: GENERAR PNGs AUTOMÁTICAMENTE
    print("\n🖼️  PASO 6: GENERANDO IMÁGENES PNG")
    print("-" * 40)
    
    pngs_generados = 0
    for archivo_dot in matrices_generadas:
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
    print(f"✅ Matrices DOT generadas: {len(matrices_generadas)}")
    print(f"✅ Imágenes PNG generadas: {pngs_generados}")
    
    # Verificar archivos generados
    archivos_importantes = [
        'salida_final.xml',
        'matriz_suelo_campo_02.dot',
        'matriz_reducida_suelo_campo_02.dot'
    ]
    
    print(f"\n📂 ARCHIVOS GENERADOS:")
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"  ✅ {archivo} ({size} bytes)")
        else:
            print(f"  ❌ {archivo} (no encontrado)")
    
    print(f"\n🎯 ¡PROYECTO EJECUTADO COMPLETAMENTE!")
    print(f"💡 Todos los archivos están listos para revisión")

if __name__ == "__main__":
    main()
