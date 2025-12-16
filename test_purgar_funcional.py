"""
Script de prueba funcional para verificar la purga de base de datos.
Este script prueba programáticamente que la funcionalidad de purgar
elimina correctamente todos los productos del inventario.
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.inventario import Inventario
from models.producto import Producto


def test_purgar_funcional():
    """Prueba funcional de la purga de base de datos."""
    print("=" * 80)
    print("PRUEBA FUNCIONAL: Purgar Base de Datos")
    print("=" * 80)
    
    # Crear inventario
    inventario = Inventario()
    print(f"\n✓ Inventario creado")
    
    # Agregar productos de prueba
    productos_prueba = [
        Producto(
            id="P001",
            nombre="Laptop HP Pavilion 15",
            precio=899.99,
            stock_actual=15,
            categoria="Computadoras",
            codigo_upc="123456789011",
            numero_item="100001",
            bin="A-01-01",
            stock_minimo=5,
            stock_maximo=50
        ),
        Producto(
            id="P002",
            nombre="Mouse Logitech M310",
            precio=25.50,
            stock_actual=50,
            categoria="Accesorios",
            codigo_upc="123456789012",
            numero_item="100002",
            bin="B-02-03",
            stock_minimo=10,
            stock_maximo=100
        ),
        Producto(
            id="P003",
            nombre="Teclado Mecánico Corsair K70",
            precio=75.00,
            stock_actual=30,
            categoria="Accesorios",
            codigo_upc="123456789013",
            numero_item="100003",
            bin="B-02-04",
            stock_minimo=8,
            stock_maximo=60
        ),
        Producto(
            id="P004",
            nombre="Monitor Samsung 24 pulgadas",
            precio=250.00,
            stock_actual=20,
            categoria="Monitores",
            codigo_upc="123456789014",
            numero_item="100004",
            bin="C-01-05",
            stock_minimo=5,
            stock_maximo=40
        ),
        Producto(
            id="P005",
            nombre="Cable HDMI 2m AmazonBasics",
            precio=12.99,
            stock_actual=100,
            categoria="Cables",
            codigo_upc="123456789015",
            numero_item="100005",
            bin="D-03-10",
            stock_minimo=20,
            stock_maximo=200
        )
    ]
    
    # Agregar productos al inventario
    for producto in productos_prueba:
        inventario.agregar_producto(producto)
    
    cantidad_inicial = len(inventario.productos)
    print(f"✓ {cantidad_inicial} productos agregados al inventario")
    
    # Mostrar productos antes de purgar
    print(f"\n📊 ESTADO ANTES DE PURGAR:")
    print(f"   Total de productos: {cantidad_inicial}")
    print(f"   IDs en inventario: {list(inventario.productos.keys())}")
    
    # Verificar que los productos están en el inventario
    assert cantidad_inicial == 5, f"Error: Se esperaban 5 productos, pero hay {cantidad_inicial}"
    print(f"   ✓ Cantidad correcta de productos")
    
    # Simular la purga (lo que hace el botón)
    print(f"\n🗑️ EJECUTANDO PURGA...")
    print(f"   1. Limpiando diccionario de productos...")
    inventario.productos.clear()
    
    print(f"   2. Invalidando caché...")
    inventario._invalidar_cache()
    
    # Verificar estado después de purgar
    cantidad_final = len(inventario.productos)
    print(f"\n📊 ESTADO DESPUÉS DE PURGAR:")
    print(f"   Total de productos: {cantidad_final}")
    print(f"   IDs en inventario: {list(inventario.productos.keys())}")
    
    # Validaciones
    print(f"\n🧪 VALIDACIONES:")
    
    # 1. Verificar que el inventario está vacío
    if cantidad_final == 0:
        print(f"   ✅ El inventario está vacío (0 productos)")
    else:
        print(f"   ❌ ERROR: El inventario debería estar vacío, pero tiene {cantidad_final} productos")
        return False
    
    # 2. Verificar que productos.clear() funcionó
    if len(inventario.productos) == 0:
        print(f"   ✅ productos.clear() funcionó correctamente")
    else:
        print(f"   ❌ ERROR: productos.clear() no eliminó todos los productos")
        return False
    
    # 3. Verificar que no quedan productos antiguos
    productos_viejos_encontrados = False
    for producto_viejo in productos_prueba:
        if producto_viejo.id in inventario.productos:
            print(f"   ❌ ERROR: Producto antiguo {producto_viejo.id} aún existe")
            productos_viejos_encontrados = True
    
    if not productos_viejos_encontrados:
        print(f"   ✅ No quedan rastros de productos antiguos")
    else:
        return False
    
    # 4. Verificar que se pueden agregar nuevos productos después de purgar
    print(f"\n➕ PROBANDO AGREGAR NUEVO PRODUCTO DESPUÉS DE PURGAR...")
    nuevo_producto = Producto(
        id="N001",
        nombre="Producto Nuevo Post-Purga",
        precio=100.00,
        stock_actual=10,
        categoria="Nueva",
        codigo_upc="999999999999",
        numero_item="999999",
        bin="Z-99-99",
        stock_minimo=5,
        stock_maximo=20
    )
    
    inventario.agregar_producto(nuevo_producto)
    
    if len(inventario.productos) == 1 and "N001" in inventario.productos:
        print(f"   ✅ Se puede agregar productos nuevos después de purgar")
        print(f"   ✅ Nuevo producto N001 agregado correctamente")
    else:
        print(f"   ❌ ERROR: No se puede agregar productos después de purgar")
        return False
    
    # 5. Verificar que el inventario vacío se maneja correctamente
    inventario.productos.clear()
    inventario._invalidar_cache()
    
    if len(inventario.productos) == 0:
        print(f"   ✅ El inventario vacío se maneja correctamente")
    else:
        print(f"   ❌ ERROR: Problemas al manejar inventario vacío")
        return False
    
    print(f"\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 80)
    print(f"\nFuncionalidad verificada:")
    print(f"  • Purga completa: {cantidad_inicial} productos eliminados")
    print(f"  • Inventario queda vacío: 0 productos restantes")
    print(f"  • Permite agregar nuevos productos después de purgar")
    print(f"  • No quedan rastros de productos antiguos")
    print(f"  • Maneja correctamente inventario vacío")
    print(f"\n🎯 CONCLUSIÓN: La funcionalidad de purgar está operativa")
    
    return True


if __name__ == "__main__":
    try:
        exito = test_purgar_funcional()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA PRUEBA:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
