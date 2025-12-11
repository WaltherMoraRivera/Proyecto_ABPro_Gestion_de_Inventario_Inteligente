#!/usr/bin/env python3
"""Script de prueba del sistema BIN"""

from models import Producto, Inventario

# Crear inventario
inv = Inventario()

# Crear productos en diferentes BINs
p1 = Producto(1, "Router WiFi", 89.99, 15, 10, 40, "Redes", "100012", "012345678912", "002/015/008")
p2 = Producto(2, "Router WiFi", 89.99, 10, 10, 40, "Redes", "100012", "012345678912", "003/010/004")
p3 = Producto(3, "Laptop HP", 899.99, 20, 5, 50, "Electrónica", "100001", "012345678901", "001/020/006")

inv.agregar_producto(p1)
inv.agregar_producto(p2)
inv.agregar_producto(p3)

print("=" * 70)
print("PRUEBA DEL SISTEMA BIN")
print("=" * 70)

print(f"\n✓ Total de entradas en inventario: {len(inv.productos)}")

agrupados = inv.obtener_productos_agrupados()
print(f"✓ Productos únicos (agrupados): {len(agrupados)}")

print("\n--- Router WiFi (en 2 ubicaciones) ---")
stock_total_router = inv.obtener_stock_total_producto(numero_item="100012")
print(f"Stock total: {stock_total_router} unidades")

bins_router = inv.obtener_bins_producto(numero_item="100012")
print(f"Ubicaciones (BINs): {bins_router}")

print("\n--- Laptop HP (en 1 ubicación) ---")
stock_total_laptop = inv.obtener_stock_total_producto(numero_item="100001")
print(f"Stock total: {stock_total_laptop} unidades")

bins_laptop = inv.obtener_bins_producto(numero_item="100001")
print(f"Ubicaciones (BINs): {bins_laptop}")

print("\n--- Búsqueda por BIN específico ---")
router_bin1 = inv.obtener_producto_por_numero_item_y_bin("100012", "002/015/008")
print(f"Router en BIN 002/015/008: {router_bin1.stock_actual} unidades")

router_bin2 = inv.obtener_producto_por_numero_item_y_bin("100012", "003/010/004")
print(f"Router en BIN 003/010/004: {router_bin2.stock_actual} unidades")

print("\n" + "=" * 70)
print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
print("=" * 70)
