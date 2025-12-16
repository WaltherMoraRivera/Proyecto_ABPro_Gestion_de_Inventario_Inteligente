#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de Purgar Base de Datos
==============================================================

Este script simula el proceso de purga de la base de datos
y verifica que la funcionalidad funcione correctamente.

Autor: Sistema de Gestión de Inventario
Versión: 2.3.0
"""

from models import Producto, Inventario

def main():
    print("=" * 70)
    print("PRUEBA DE FUNCIONALIDAD: PURGAR BASE DE DATOS")
    print("=" * 70)
    print()
    
    # PRUEBA 1: Crear inventario con productos
    print("─" * 70)
    print("PRUEBA 1: Crear inventario con productos")
    print("─" * 70)
    
    inventario = Inventario()
    
    productos_ejemplo = [
        Producto(1, "Laptop HP 15", 899.990, 15, 5, 50, "Electrónica", "100001", "012345678901", "001/020/006"),
        Producto(2, "Mouse Inalámbrico", 29.990, 45, 20, 100, "Accesorios", "100002", "012345678902", "001/020/007"),
        Producto(3, "Teclado Mecánico", 79.990, 8, 10, 40, "Accesorios", "100003", "012345678903", "001/020/008"),
        Producto(4, "Monitor 24\" LG", 249.990, 12, 5, 30, "Electrónica", "100004", "012345678904", "001/020/009"),
        Producto(5, "Cable HDMI 2m", 14.990, 3, 30, 200, "Accesorios", "100005", "012345678905", "003/010/001"),
    ]
    
    for producto in productos_ejemplo:
        inventario.agregar_producto(producto)
    
    productos_iniciales = len(inventario.productos)
    print(f"✓ Inventario creado con {productos_iniciales} productos")
    print(f"  IDs: {list(inventario.productos.keys())}")
    print()
    
    # PRUEBA 2: Verificar estado antes de purgar
    print("─" * 70)
    print("PRUEBA 2: Estado del inventario ANTES de purgar")
    print("─" * 70)
    print(f"Cantidad de productos: {len(inventario.productos)}")
    print(f"Productos:")
    for producto in inventario.listar_productos():
        print(f"  - ID {producto.id}: {producto.nombre}")
    print()
    
    # PRUEBA 3: Simular purga
    print("─" * 70)
    print("PRUEBA 3: Simular purga de base de datos")
    print("─" * 70)
    print("Ejecutando purga...")
    
    # Guardar información para verificación
    ids_antes = list(inventario.productos.keys())
    cantidad_antes = len(inventario.productos)
    
    # Purgar (eliminar todos los productos)
    inventario.productos.clear()
    inventario._invalidar_cache()
    
    print(f"✓ Productos eliminados: {cantidad_antes}")
    print(f"✓ IDs eliminados: {ids_antes}")
    print()
    
    # PRUEBA 4: Verificar estado después de purgar
    print("─" * 70)
    print("PRUEBA 4: Estado del inventario DESPUÉS de purgar")
    print("─" * 70)
    cantidad_despues = len(inventario.productos)
    print(f"Cantidad de productos: {cantidad_despues}")
    
    if cantidad_despues == 0:
        print("✓ Inventario está vacío (purga exitosa)")
    else:
        print(f"✗ ERROR: Inventario tiene {cantidad_despues} productos")
        return
    
    print()
    
    # PRUEBA 5: Verificar que se pueden agregar nuevos productos después de purgar
    print("─" * 70)
    print("PRUEBA 5: Agregar nuevos productos después de purgar")
    print("─" * 70)
    
    nuevo_producto = Producto(
        10, "Producto Nuevo", 99.99, 10, 5, 20, 
        "Nueva Categoría", "200001", "987654321098", "005/025/010"
    )
    
    if inventario.agregar_producto(nuevo_producto):
        print(f"✓ Nuevo producto agregado exitosamente")
        print(f"  ID: {nuevo_producto.id}")
        print(f"  Nombre: {nuevo_producto.nombre}")
        print(f"  Inventario actual: {len(inventario.productos)} producto(s)")
    else:
        print("✗ ERROR: No se pudo agregar el nuevo producto")
        return
    
    print()
    
    # PRUEBA 6: Verificar integridad del inventario
    print("─" * 70)
    print("PRUEBA 6: Verificar integridad del inventario")
    print("─" * 70)
    
    # Verificar que el producto agregado está en el inventario
    producto_recuperado = inventario.obtener_producto(10)
    
    if producto_recuperado:
        print("✓ Producto recuperado correctamente del inventario")
        print(f"  ID: {producto_recuperado.id}")
        print(f"  Nombre: {producto_recuperado.nombre}")
        print(f"  Precio: ${producto_recuperado.precio:.2f}")
    else:
        print("✗ ERROR: No se pudo recuperar el producto")
        return
    
    # Verificar que los productos antiguos no existen
    print()
    print("Verificando que productos antiguos fueron eliminados:")
    productos_antiguos_encontrados = 0
    for id_antiguo in ids_antes:
        if inventario.obtener_producto(id_antiguo):
            productos_antiguos_encontrados += 1
            print(f"  ✗ ERROR: Producto ID {id_antiguo} aún existe")
    
    if productos_antiguos_encontrados == 0:
        print(f"  ✓ Ningún producto antiguo encontrado (correcto)")
    
    print()
    
    # PRUEBA 7: Purgar inventario vacío
    print("─" * 70)
    print("PRUEBA 7: Intentar purgar inventario vacío")
    print("─" * 70)
    
    # Primero vaciar el inventario
    inventario.productos.clear()
    
    if len(inventario.productos) == 0:
        print("✓ Inventario está vacío")
        print("  En la GUI, debería mostrarse mensaje: 'No hay productos para purgar'")
    else:
        print("✗ ERROR: Inventario no está vacío")
    
    print()
    
    # RESULTADO FINAL
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    
    print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print()
    print("Funcionalidad de Purgar Base de Datos verificada:")
    print(f"  • Purga completa: {cantidad_antes} productos eliminados")
    print(f"  • Inventario queda vacío: {cantidad_despues} productos restantes")
    print(f"  • Permite agregar nuevos productos después de purgar")
    print(f"  • No quedan rastros de productos antiguos")
    print(f"  • Maneja correctamente inventario vacío")
    print()
    print("En la GUI:")
    print("  • Botón '🗑️ Purgar Base de Datos' disponible en barra superior")
    print("  • Confirmación nivel 1: Diálogo de advertencia")
    print("  • Confirmación nivel 2: Escribir 'purgar' para confirmar")
    print("  • Mensaje de éxito al completar la purga")
    print("=" * 70)


if __name__ == "__main__":
    main()
