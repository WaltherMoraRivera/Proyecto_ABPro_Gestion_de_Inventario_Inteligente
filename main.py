#!/usr/bin/env python3
"""
Sistema de Gestión de Inventario Inteligente
=============================================

Aplicación principal que demuestra el uso del sistema de gestión de inventario
utilizando álgebra lineal (NumPy/Pandas) para operaciones eficientes.

Este programa proporciona una interfaz de consola para:
- Gestionar productos en el inventario
- Registrar entradas y salidas de stock
- Generar alertas de stock bajo
- Calcular estadísticas mediante operaciones matriciales

Uso:
    python main.py

Autor: Sistema de Gestión de Inventario
Versión: 1.0.0
"""

import sys
import numpy as np
import pandas as pd
from typing import Optional

from models import Producto, Inventario
from logic import OperacionesMatriciales


class SistemaInventario:
    """
    Clase principal que coordina la interfaz del sistema de inventario.
    
    Proporciona una interfaz de consola interactiva para gestionar
    el inventario utilizando operaciones de álgebra lineal.
    """
    
    def __init__(self):
        """Inicializa el sistema de inventario."""
        self.inventario = Inventario()
        self.operaciones = OperacionesMatriciales(self.inventario)
        self._cargar_datos_ejemplo()
    
    def _cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para demostración."""
        productos_ejemplo = [
            Producto(1, "Laptop HP 15", 899.99, 15, 5, 50, "Electrónica"),
            Producto(2, "Mouse Inalámbrico", 29.99, 45, 20, 100, "Accesorios"),
            Producto(3, "Teclado Mecánico", 79.99, 8, 10, 40, "Accesorios"),
            Producto(4, "Monitor 24\" LG", 249.99, 12, 5, 30, "Electrónica"),
            Producto(5, "Cable HDMI 2m", 14.99, 3, 30, 200, "Accesorios"),
            Producto(6, "Disco SSD 500GB", 69.99, 25, 15, 60, "Almacenamiento"),
            Producto(7, "Memoria USB 64GB", 12.99, 50, 25, 150, "Almacenamiento"),
            Producto(8, "Webcam HD", 49.99, 18, 10, 40, "Accesorios"),
            Producto(9, "Audífonos Bluetooth", 59.99, 22, 15, 50, "Audio"),
            Producto(10, "Cargador Universal", 24.99, 30, 20, 80, "Accesorios"),
        ]
        
        for producto in productos_ejemplo:
            self.inventario.agregar_producto(producto)
    
    def mostrar_menu(self):
        """Muestra el menú principal del sistema."""
        print("\n" + "=" * 60)
        print("   SISTEMA DE GESTIÓN DE INVENTARIO INTELIGENTE")
        print("=" * 60)
        print("\n  MENÚ PRINCIPAL:")
        print("  ─" * 30)
        print("  1. Ver todos los productos")
        print("  2. Ver matriz de inventario")
        print("  3. Ver productos con alerta de stock bajo")
        print("  4. Registrar entrada de productos")
        print("  5. Registrar salida de productos")
        print("  6. Ver estadísticas del inventario")
        print("  7. Ver reporte completo (DataFrame)")
        print("  8. Análisis por categoría")
        print("  9. Agregar nuevo producto")
        print("  0. Salir")
        print("  ─" * 30)
    
    def ver_productos(self):
        """Muestra todos los productos del inventario."""
        print("\n" + "─" * 50)
        print("   LISTA DE PRODUCTOS")
        print("─" * 50)
        
        if not self.inventario.productos:
            print("No hay productos en el inventario.")
            return
        
        for producto in self.inventario:
            print(f"\n{producto}")
    
    def ver_matriz_inventario(self):
        """Muestra la representación matricial del inventario."""
        print("\n" + "─" * 50)
        print("   MATRIZ DE INVENTARIO")
        print("─" * 50)
        
        matriz = self.inventario.obtener_matriz_inventario()
        
        if matriz.size == 0:
            print("No hay productos en el inventario.")
            return
        
        print("\nRepresentación matricial I (n × 5):")
        print("Columnas: [ID, Precio, Stock, Mínimo, Máximo]")
        print()
        
        # Mostrar matriz formateada
        encabezados = ["ID", "Precio", "Stock", "Mínimo", "Máximo"]
        print(f"{'':>4} | " + " | ".join(f"{h:>10}" for h in encabezados))
        print("─" * 65)
        
        for i, fila in enumerate(matriz):
            print(f"{i:>4} | " + " | ".join(f"{v:>10.2f}" for v in fila))
        
        print(f"\nDimensiones de la matriz: {matriz.shape}")
        print(f"Tipo de datos: {matriz.dtype}")
    
    def ver_alertas(self):
        """Muestra los productos que necesitan reabastecimiento."""
        print("\n" + "─" * 50)
        print("   ALERTAS DE STOCK BAJO")
        print("─" * 50)
        
        # Obtener vector de alertas
        vector_alertas = self.operaciones.calcular_alertas_stock_bajo()
        productos_alerta = self.operaciones.obtener_productos_alerta()
        sugerencias = self.operaciones.calcular_cantidad_reabastecimiento()
        
        print(f"\nVector de alertas (booleano): {vector_alertas}")
        print(f"Total de alertas: {np.sum(vector_alertas)}")
        
        if not productos_alerta:
            print("\n✓ Todos los productos tienen stock suficiente.")
            return
        
        print("\n⚠️  PRODUCTOS QUE REQUIEREN REABASTECIMIENTO:")
        print("─" * 50)
        
        productos_lista = self.inventario.listar_productos()
        for i, producto in enumerate(productos_lista):
            if vector_alertas[i]:
                print(f"\n• {producto.nombre} (ID: {producto.id})")
                print(f"  Stock actual: {producto.stock_actual}")
                print(f"  Stock mínimo: {producto.stock_minimo}")
                print(f"  Sugerencia de compra: {sugerencias[i]} unidades")
    
    def registrar_entrada(self):
        """Registra una entrada de productos al inventario."""
        print("\n" + "─" * 50)
        print("   REGISTRAR ENTRADA DE PRODUCTOS")
        print("─" * 50)
        
        try:
            producto_id = int(input("\nIngrese el ID del producto: "))
            cantidad = int(input("Ingrese la cantidad a ingresar: "))
            
            exito, mensaje = self.operaciones.registrar_entrada(producto_id, cantidad)
            
            if exito:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ Error: {mensaje}")
                
        except ValueError:
            print("\n✗ Error: Ingrese valores numéricos válidos.")
    
    def registrar_salida(self):
        """Registra una salida de productos del inventario."""
        print("\n" + "─" * 50)
        print("   REGISTRAR SALIDA DE PRODUCTOS")
        print("─" * 50)
        
        try:
            producto_id = int(input("\nIngrese el ID del producto: "))
            cantidad = int(input("Ingrese la cantidad a retirar: "))
            
            exito, mensaje = self.operaciones.registrar_salida(producto_id, cantidad)
            
            if exito:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ Error: {mensaje}")
                
        except ValueError:
            print("\n✗ Error: Ingrese valores numéricos válidos.")
    
    def ver_estadisticas(self):
        """Muestra estadísticas del inventario calculadas matricialmente."""
        print("\n" + "─" * 50)
        print("   ESTADÍSTICAS DEL INVENTARIO")
        print("─" * 50)
        
        stats = self.operaciones.calcular_estadisticas()
        
        print("\n📊 MÉTRICAS CALCULADAS MEDIANTE ÁLGEBRA LINEAL:")
        print()
        print(f"  Total de productos:        {stats['total_productos']}")
        print(f"  Total de unidades:         {stats['total_unidades']}")
        print(f"  Valor total:               ${stats['valor_total']:,.2f}")
        print(f"  Productos con alerta:      {stats['productos_alerta']}")
        print(f"  Porcentaje con alerta:     {stats['porcentaje_alerta']:.1f}%")
        print(f"  Stock promedio:            {stats['stock_promedio']:.1f} unidades")
        print(f"  Precio promedio:           ${stats['precio_promedio']:.2f}")
        print(f"  Valor promedio por prod.:  ${stats['valor_promedio']:.2f}")
        
        print("\n📐 VECTORES EXTRAÍDOS DE LA MATRIZ:")
        print()
        print(f"  Vector de stock:   {self.operaciones.obtener_vector_stock()}")
        print(f"  Vector de precios: {self.operaciones.obtener_vector_precios()}")
        print(f"  Vector de valores: {self.operaciones.calcular_vector_valores()}")
    
    def ver_reporte_dataframe(self):
        """Muestra el reporte completo como DataFrame de Pandas."""
        print("\n" + "─" * 50)
        print("   REPORTE COMPLETO (DataFrame)")
        print("─" * 50)
        
        df = self.operaciones.generar_reporte_dataframe()
        
        if df.empty:
            print("\nNo hay datos para mostrar.")
            return
        
        # Configurar pandas para mostrar todas las columnas
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 20)
        
        print("\n")
        print(df.to_string(index=False))
    
    def ver_analisis_categoria(self):
        """Muestra el análisis agrupado por categoría."""
        print("\n" + "─" * 50)
        print("   ANÁLISIS POR CATEGORÍA")
        print("─" * 50)
        
        df = self.operaciones.analisis_por_categoria()
        
        if df.empty:
            print("\nNo hay datos para mostrar.")
            return
        
        print("\n")
        print(df.to_string())
    
    def agregar_producto(self):
        """Agrega un nuevo producto al inventario."""
        print("\n" + "─" * 50)
        print("   AGREGAR NUEVO PRODUCTO")
        print("─" * 50)
        
        try:
            producto_id = int(input("\nIngrese el ID del producto: "))
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio: "))
            stock = int(input("Ingrese el stock inicial: "))
            minimo = int(input("Ingrese el stock mínimo: "))
            maximo = int(input("Ingrese el stock máximo: "))
            categoria = input("Ingrese la categoría: ")
            
            producto = Producto(
                producto_id, nombre, precio, stock, minimo, maximo, categoria
            )
            
            if self.inventario.agregar_producto(producto):
                print(f"\n✓ Producto '{nombre}' agregado exitosamente.")
            else:
                print(f"\n✗ Error: Ya existe un producto con ID {producto_id}.")
                
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def ejecutar(self):
        """Ejecuta el bucle principal del sistema."""
        print("\n🚀 Iniciando Sistema de Gestión de Inventario...")
        print("   Usando NumPy y Pandas para operaciones matriciales.")
        
        while True:
            self.mostrar_menu()
            
            try:
                opcion = input("\n  Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.ver_productos()
                elif opcion == "2":
                    self.ver_matriz_inventario()
                elif opcion == "3":
                    self.ver_alertas()
                elif opcion == "4":
                    self.registrar_entrada()
                elif opcion == "5":
                    self.registrar_salida()
                elif opcion == "6":
                    self.ver_estadisticas()
                elif opcion == "7":
                    self.ver_reporte_dataframe()
                elif opcion == "8":
                    self.ver_analisis_categoria()
                elif opcion == "9":
                    self.agregar_producto()
                elif opcion == "0":
                    print("\n¡Hasta luego! 👋")
                    break
                else:
                    print("\n✗ Opción no válida. Intente de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n¡Programa interrumpido!")
                break


def main():
    """Función principal de entrada."""
    sistema = SistemaInventario()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
