#!/usr/bin/env python3
"""
Script para crear un archivo Excel de ejemplo para probar la carga de inventario.

Genera un archivo Excel con datos de ejemplo que puede ser utilizado
para probar la funcionalidad de mapeo de columnas.
"""

import pandas as pd

# Datos de ejemplo para el inventario
datos_ejemplo = {
    'ID_Producto': [11, 12, 13, 14, 15, 16],
    'Num_Item': ['100011', '100012', '100012', '100013', '100014', '100015'],
    'UPC': ['012345678911', '012345678912', '012345678912', '012345678913', '012345678914', '012345678915'],
    'BIN_Bodega': ['001/020/015', '002/015/008', '003/010/004', '001/020/016', '002/015/009', '001/020/017'],
    'Descripcion': [
        'Impresora Láser HP',
        'Router WiFi 6',
        'Router WiFi 6',
        'Switch Gigabit 8 puertos',
        'Disco Externo 2TB',
        'Adaptador USB-C'
    ],
    'Precio_Unitario': [299.99, 89.99, 89.99, 45.99, 79.99, 19.99],
    'Cantidad_Stock': [8, 15, 10, 20, 12, 50],
    'Stock_Min': [5, 10, 10, 15, 8, 30],
    'Stock_Max': [25, 40, 40, 60, 35, 150],
    'Cat': ['Impresoras', 'Redes', 'Redes', 'Redes', 'Almacenamiento', 'Accesorios']
}

# Crear DataFrame
df = pd.DataFrame(datos_ejemplo)

# Guardar a Excel
archivo_salida = 'inventario_ejemplo.xlsx'
df.to_excel(archivo_salida, index=False)

print(f"✓ Archivo Excel creado: {archivo_salida}")
print(f"\nColumnas del archivo:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nFilas: {len(df)}")
print("\nVista previa:")
print(df.to_string())
