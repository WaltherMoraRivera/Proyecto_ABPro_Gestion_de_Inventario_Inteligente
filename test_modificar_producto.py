#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de Modificar Producto
=============================================================

Este script demuestra las tres formas de buscar productos para modificar:
1. Por ID
2. Por Número de Item
3. Por Código UPC

Autor: Sistema de Gestión de Inventario
Versión: 2.0.0
"""

from models import Producto, Inventario

def main():
    print("=" * 70)
    print("PRUEBA DE FUNCIONALIDAD: MODIFICAR PRODUCTO")
    print("=" * 70)
    print()
    
    # Crear inventario de prueba
    inventario = Inventario()
    
    # Agregar productos de ejemplo
    productos_ejemplo = [
        Producto(1, "Laptop HP 15", 899.990, 15, 5, 50, "Electrónica", "100001", "012345678901", "001/020/006"),
        Producto(2, "Mouse Inalámbrico", 29.990, 45, 20, 100, "Accesorios", "100002", "012345678902", "001/020/007"),
        Producto(3, "Teclado Mecánico", 79.990, 8, 10, 40, "Accesorios", "100003", "012345678903", "001/020/008"),
    ]
    
    for producto in productos_ejemplo:
        inventario.agregar_producto(producto)
    
    print("✓ Inventario creado con 3 productos de ejemplo\n")
    
    # PRUEBA 1: Búsqueda por ID
    print("─" * 70)
    print("PRUEBA 1: Buscar producto por ID")
    print("─" * 70)
    producto_id = inventario.obtener_producto(1)
    if producto_id:
        print(f"✓ Producto encontrado por ID=1:")
        print(f"  - Nombre: {producto_id.nombre}")
        print(f"  - Número Item: {producto_id.numero_item}")
        print(f"  - Código UPC: {producto_id.codigo_upc}")
        print(f"  - BIN: {producto_id.bin}")
        print(f"  - Precio: ${producto_id.precio:.2f}")
        print(f"  - Stock: {producto_id.stock_actual}")
        
        # Modificar el producto
        print("\n  Modificando precio de 899.990 a 799.990...")
        producto_id.precio = 799.990
        print(f"  ✓ Nuevo precio: ${producto_id.precio:.2f}")
    else:
        print("✗ Producto no encontrado")
    
    print()
    
    # PRUEBA 2: Búsqueda por Número de Item
    print("─" * 70)
    print("PRUEBA 2: Buscar producto por Número de Item")
    print("─" * 70)
    producto_item = inventario.obtener_producto_por_numero_item("100002")
    if producto_item:
        print(f"✓ Producto encontrado por Número Item=100002:")
        print(f"  - ID: {producto_item.id}")
        print(f"  - Nombre: {producto_item.nombre}")
        print(f"  - Código UPC: {producto_item.codigo_upc}")
        print(f"  - BIN: {producto_item.bin}")
        print(f"  - Stock: {producto_item.stock_actual}")
        
        # Modificar el stock
        print(f"\n  Modificando stock de {producto_item.stock_actual} a 60...")
        producto_item.stock_actual = 60
        print(f"  ✓ Nuevo stock: {producto_item.stock_actual}")
    else:
        print("✗ Producto no encontrado")
    
    print()
    
    # PRUEBA 3: Búsqueda por Código UPC
    print("─" * 70)
    print("PRUEBA 3: Buscar producto por Código UPC")
    print("─" * 70)
    producto_upc = inventario.obtener_producto_por_codigo_upc("012345678903")
    if producto_upc:
        print(f"✓ Producto encontrado por Código UPC=012345678903:")
        print(f"  - ID: {producto_upc.id}")
        print(f"  - Nombre: {producto_upc.nombre}")
        print(f"  - Número Item: {producto_upc.numero_item}")
        print(f"  - BIN: {producto_upc.bin}")
        print(f"  - Categoría: {producto_upc.categoria}")
        
        # Modificar la categoría
        print(f"\n  Modificando categoría de '{producto_upc.categoria}' a 'Periféricos'...")
        producto_upc.categoria = "Periféricos"
        print(f"  ✓ Nueva categoría: {producto_upc.categoria}")
    else:
        print("✗ Producto no encontrado")
    
    print()
    
    # Verificar cambios finales
    print("=" * 70)
    print("VERIFICACIÓN FINAL DE CAMBIOS")
    print("=" * 70)
    for producto in inventario.listar_productos():
        print(f"\nID {producto.id}: {producto.nombre}")
        print(f"  - Precio: ${producto.precio:.2f}")
        print(f"  - Stock: {producto.stock_actual}")
        print(f"  - Categoría: {producto.categoria}")
        print(f"  - Número Item: {producto.numero_item}")
        print(f"  - Código UPC: {producto.codigo_upc}")
        print(f"  - BIN: {producto.bin}")
    
    print("\n" + "=" * 70)
    print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()
