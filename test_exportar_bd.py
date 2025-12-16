#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de Exportar Base de Datos
================================================================

Este script demuestra cómo se exportan los productos a un archivo Excel
y verifica que el formato sea compatible con la carga posterior.

Autor: Sistema de Gestión de Inventario
Versión: 2.1.0
"""

import pandas as pd
from models import Producto, Inventario
import os

def main():
    print("=" * 70)
    print("PRUEBA DE FUNCIONALIDAD: EXPORTAR BASE DE DATOS")
    print("=" * 70)
    print()
    
    # Crear inventario de prueba
    inventario = Inventario()
    
    # Agregar productos de ejemplo (simulando datos de una sesión de trabajo)
    productos_ejemplo = [
        Producto(1, "Laptop HP 15", 899.990, 15, 5, 50, "Electrónica", "100001", "012345678901", "001/020/006"),
        Producto(2, "Laptop HP 15", 899.990, 10, 5, 50, "Electrónica", "100001", "012345678901", "002/015/003"),
        Producto(3, "Mouse Inalámbrico", 29.990, 45, 20, 100, "Accesorios", "100002", "012345678902", "001/020/007"),
        Producto(4, "Teclado Mecánico", 79.990, 8, 10, 40, "Accesorios", "100003", "012345678903", "001/020/008"),
        Producto(5, "Monitor 24\" LG", 249.990, 12, 5, 30, "Electrónica", "100004", "012345678904", "001/020/009"),
    ]
    
    for producto in productos_ejemplo:
        inventario.agregar_producto(producto)
    
    print(f"✓ Inventario creado con {len(productos_ejemplo)} productos\n")
    
    # PRUEBA 1: Exportar datos a Excel
    print("─" * 70)
    print("PRUEBA 1: Exportar datos a Excel")
    print("─" * 70)
    
    archivo_exportado = "inventario_prueba_exportacion.xlsx"
    
    try:
        # Crear lista de diccionarios con todos los productos
        datos_productos = []
        
        for producto in inventario.listar_productos():
            datos_productos.append({
                'ID': producto.id,
                'Numero_Item': producto.numero_item,
                'Codigo_UPC': producto.codigo_upc,
                'BIN_Bodega': producto.bin,
                'Nombre': producto.nombre,
                'Precio': producto.precio,
                'Stock_Actual': producto.stock_actual,
                'Stock_Minimo': producto.stock_minimo,
                'Stock_Maximo': producto.stock_maximo,
                'Categoria': producto.categoria
            })
        
        # Crear DataFrame
        df = pd.DataFrame(datos_productos)
        
        # Exportar a Excel
        df.to_excel(archivo_exportado, index=False, sheet_name='Inventario')
        
        print(f"✓ Archivo exportado: {archivo_exportado}")
        print(f"✓ Productos exportados: {len(datos_productos)}")
        print(f"✓ Columnas exportadas: {', '.join(df.columns.tolist())}")
        
    except Exception as e:
        print(f"✗ Error al exportar: {str(e)}")
        return
    
    print()
    
    # PRUEBA 2: Verificar que el archivo se creó correctamente
    print("─" * 70)
    print("PRUEBA 2: Verificar archivo exportado")
    print("─" * 70)
    
    if os.path.exists(archivo_exportado):
        print(f"✓ Archivo existe: {archivo_exportado}")
        
        # Leer el archivo para verificar contenido
        df_verificacion = pd.read_excel(archivo_exportado)
        
        print(f"✓ Filas leídas: {len(df_verificacion)}")
        print(f"✓ Columnas leídas: {len(df_verificacion.columns)}")
        print()
        
        # Mostrar primeras filas
        print("Primeras 3 filas del archivo exportado:")
        print("─" * 70)
        print(df_verificacion.head(3).to_string())
        print()
        
    else:
        print(f"✗ Archivo no existe: {archivo_exportado}")
        return
    
    # PRUEBA 3: Verificar compatibilidad con carga
    print("─" * 70)
    print("PRUEBA 3: Verificar compatibilidad con función 'Cargar Excel'")
    print("─" * 70)
    
    # Verificar que todas las columnas necesarias existen
    columnas_requeridas = [
        'ID', 'Numero_Item', 'Codigo_UPC', 'BIN_Bodega', 
        'Nombre', 'Precio', 'Stock_Actual', 'Stock_Minimo', 
        'Stock_Maximo', 'Categoria'
    ]
    
    columnas_archivo = df_verificacion.columns.tolist()
    
    todas_presentes = all(col in columnas_archivo for col in columnas_requeridas)
    
    if todas_presentes:
        print("✓ Todas las columnas requeridas están presentes")
        for col in columnas_requeridas:
            print(f"  ✓ {col}")
    else:
        print("✗ Faltan columnas requeridas")
        for col in columnas_requeridas:
            if col not in columnas_archivo:
                print(f"  ✗ {col} - FALTANTE")
    
    print()
    
    # PRUEBA 4: Simular carga del archivo exportado
    print("─" * 70)
    print("PRUEBA 4: Simular carga del archivo exportado")
    print("─" * 70)
    
    inventario_nuevo = Inventario()
    productos_cargados = 0
    
    for idx, fila in df_verificacion.iterrows():
        try:
            producto = Producto(
                id=int(fila['ID']),
                nombre=str(fila['Nombre']),
                precio=float(fila['Precio']),
                stock_actual=int(fila['Stock_Actual']),
                stock_minimo=int(fila['Stock_Minimo']),
                stock_maximo=int(fila['Stock_Maximo']),
                categoria=str(fila['Categoria']),
                numero_item=str(fila['Numero_Item']),
                codigo_upc=str(fila['Codigo_UPC']),
                bin=str(fila['BIN_Bodega'])
            )
            
            if inventario_nuevo.agregar_producto(producto):
                productos_cargados += 1
        
        except Exception as e:
            print(f"✗ Error al cargar producto en fila {idx}: {str(e)}")
    
    print(f"✓ Productos cargados exitosamente: {productos_cargados}/{len(df_verificacion)}")
    
    if productos_cargados == len(df_verificacion):
        print("✓ Todos los productos se cargaron correctamente")
    else:
        print(f"⚠ Solo se cargaron {productos_cargados} de {len(df_verificacion)} productos")
    
    print()
    
    # RESULTADO FINAL
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    
    if todas_presentes and productos_cargados == len(df_verificacion):
        print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print()
        print("El archivo exportado:")
        print(f"  • Contiene todas las columnas necesarias")
        print(f"  • Es compatible con la función 'Cargar Excel'")
        print(f"  • Puede ser usado para restaurar datos en una nueva sesión")
        print()
        print(f"Archivo generado: {archivo_exportado}")
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
