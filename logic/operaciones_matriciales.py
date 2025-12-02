"""
Módulo de operaciones matriciales para gestión de inventario.

Este módulo implementa la lógica de negocio utilizando álgebra lineal
(NumPy/Pandas) para representar y manipular el inventario de manera eficiente.

Modelo Matemático:
==================

1. REPRESENTACIÓN MATRICIAL DEL INVENTARIO
   
   El inventario se representa como una matriz I de dimensión (n x 5):
   
   I = | id₁  precio₁  stock₁  min₁  max₁ |
       | id₂  precio₂  stock₂  min₂  max₂ |
       | ...  ...      ...     ...   ...  |
       | idₙ  precioₙ  stockₙ  minₙ  maxₙ |
   
   Donde cada fila es un vector producto: p = [id, precio, stock, min, max]

2. VECTOR DE STOCK
   
   Se extrae como la columna 2 de la matriz:
   s = I[:, 2] = [stock₁, stock₂, ..., stockₙ]ᵀ

3. OPERACIONES DE ENTRADA/SALIDA
   
   - Entrada: s' = s + e  (donde e es el vector de entradas)
   - Salida:  s' = s - x  (donde x es el vector de salidas)
   
   Estas operaciones se validan para mantener: 0 ≤ s' ≤ max

4. ALERTAS DE STOCK
   
   Vector de alertas: a = s < min (comparación elemento a elemento)
   Productos con alerta: {i : aᵢ = True}

5. VALOR TOTAL DEL INVENTARIO
   
   V = pᵀ · s = Σ(precioᵢ × stockᵢ)
   
   Donde p es el vector de precios y s el vector de stock.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from models.inventario import Inventario
from models.producto import Producto


class OperacionesMatriciales:
    """
    Clase que implementa operaciones de álgebra lineal para gestión de inventario.
    
    Utiliza NumPy para operaciones matriciales eficientes y Pandas para
    análisis y presentación de datos.
    
    Índices de columnas en la matriz de inventario:
        - COL_ID (0): Identificador del producto
        - COL_PRECIO (1): Precio unitario
        - COL_STOCK (2): Stock actual
        - COL_MIN (3): Stock mínimo
        - COL_MAX (4): Stock máximo
    """
    
    # Constantes para índices de columnas
    COL_ID = 0
    COL_PRECIO = 1
    COL_STOCK = 2
    COL_MIN = 3
    COL_MAX = 4
    
    def __init__(self, inventario: Inventario):
        """
        Inicializa el módulo de operaciones con un inventario.
        
        Args:
            inventario: Instancia de Inventario a gestionar
        """
        self.inventario = inventario
    
    # =========================================================================
    # OPERACIONES DE CONSULTA (LECTURA)
    # =========================================================================
    
    def obtener_vector_stock(self) -> np.ndarray:
        """
        Extrae el vector de stock actual de la matriz de inventario.
        
        Operación matricial: s = I[:, COL_STOCK]
        
        Returns:
            np.ndarray: Vector de stock actual de cada producto
        """
        matriz = self.inventario.obtener_matriz_inventario()
        if matriz.size == 0:
            return np.array([])
        return matriz[:, self.COL_STOCK]
    
    def obtener_vector_precios(self) -> np.ndarray:
        """
        Extrae el vector de precios de la matriz de inventario.
        
        Operación matricial: p = I[:, COL_PRECIO]
        
        Returns:
            np.ndarray: Vector de precios de cada producto
        """
        matriz = self.inventario.obtener_matriz_inventario()
        if matriz.size == 0:
            return np.array([])
        return matriz[:, self.COL_PRECIO]
    
    def obtener_vector_minimos(self) -> np.ndarray:
        """
        Extrae el vector de stock mínimo de la matriz.
        
        Returns:
            np.ndarray: Vector de stock mínimo de cada producto
        """
        matriz = self.inventario.obtener_matriz_inventario()
        if matriz.size == 0:
            return np.array([])
        return matriz[:, self.COL_MIN]
    
    def obtener_vector_maximos(self) -> np.ndarray:
        """
        Extrae el vector de stock máximo de la matriz.
        
        Returns:
            np.ndarray: Vector de stock máximo de cada producto
        """
        matriz = self.inventario.obtener_matriz_inventario()
        if matriz.size == 0:
            return np.array([])
        return matriz[:, self.COL_MAX]
    
    def calcular_valor_total_inventario(self) -> float:
        """
        Calcula el valor monetario total del inventario.
        
        Operación matricial: V = pᵀ · s (producto punto)
        
        Donde:
            - p: vector de precios
            - s: vector de stock
        
        Returns:
            float: Valor total del inventario
        """
        precios = self.obtener_vector_precios()
        stock = self.obtener_vector_stock()
        
        if precios.size == 0:
            return 0.0
        
        # Producto punto: suma de (precio × cantidad)
        return float(np.dot(precios, stock))
    
    def calcular_vector_valores(self) -> np.ndarray:
        """
        Calcula el vector de valores (precio × stock) para cada producto.
        
        Operación matricial: v = p ⊙ s (producto elemento a elemento)
        
        Returns:
            np.ndarray: Vector de valores de cada producto
        """
        precios = self.obtener_vector_precios()
        stock = self.obtener_vector_stock()
        
        if precios.size == 0:
            return np.array([])
        
        # Producto de Hadamard (elemento a elemento)
        return precios * stock
    
    # =========================================================================
    # OPERACIONES DE ALERTAS
    # =========================================================================
    
    def calcular_alertas_stock_bajo(self) -> np.ndarray:
        """
        Genera un vector booleano de alertas de stock bajo.
        
        Operación matricial: a = s < min (comparación elemento a elemento)
        
        Returns:
            np.ndarray: Vector booleano (True = stock bajo)
        """
        stock = self.obtener_vector_stock()
        minimos = self.obtener_vector_minimos()
        
        if stock.size == 0:
            return np.array([], dtype=bool)
        
        return stock < minimos
    
    def obtener_productos_alerta(self) -> List[Producto]:
        """
        Obtiene la lista de productos que necesitan reabastecimiento.
        
        Utiliza el vector de alertas para filtrar productos eficientemente.
        
        Returns:
            List[Producto]: Productos con stock bajo
        """
        alertas = self.calcular_alertas_stock_bajo()
        
        if alertas.size == 0:
            return []
        
        productos_lista = self.inventario.listar_productos()
        
        # Usar el vector de alertas como máscara booleana
        return [p for p, alerta in zip(productos_lista, alertas) if alerta]
    
    def calcular_espacio_disponible(self) -> np.ndarray:
        """
        Calcula el espacio disponible para cada producto.
        
        Operación matricial: d = max - s
        
        Returns:
            np.ndarray: Vector de espacio disponible
        """
        stock = self.obtener_vector_stock()
        maximos = self.obtener_vector_maximos()
        
        if stock.size == 0:
            return np.array([])
        
        # Asegurar que no hay valores negativos
        return np.maximum(0, maximos - stock)
    
    def calcular_cantidad_reabastecimiento(self) -> np.ndarray:
        """
        Calcula la cantidad sugerida de reabastecimiento.
        
        Para productos con stock bajo, sugiere llenar hasta el punto medio
        entre el mínimo y el máximo.
        
        Operación: r = max(0, (min + max)/2 - stock) si stock < min, 0 en otro caso
        
        Returns:
            np.ndarray: Vector de cantidades sugeridas
        """
        stock = self.obtener_vector_stock()
        minimos = self.obtener_vector_minimos()
        maximos = self.obtener_vector_maximos()
        
        if stock.size == 0:
            return np.array([])
        
        # Punto óptimo: promedio entre mínimo y máximo
        punto_optimo = (minimos + maximos) / 2
        
        # Cantidad a pedir solo si stock < mínimo
        alertas = stock < minimos
        cantidad = np.where(alertas, punto_optimo - stock, 0)
        
        return np.maximum(0, cantidad).astype(int)
    
    # =========================================================================
    # OPERACIONES DE ENTRADA (COMPRAS/RECEPCIÓN)
    # =========================================================================
    
    def registrar_entrada(
        self,
        producto_id: int,
        cantidad: int
    ) -> Tuple[bool, str]:
        """
        Registra una entrada de inventario para un producto.
        
        Operación: stock_nuevo = stock_actual + cantidad
        Restricción: stock_nuevo ≤ stock_maximo
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a ingresar (debe ser positiva)
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if cantidad <= 0:
            return False, "La cantidad debe ser positiva"
        
        producto = self.inventario.obtener_producto(producto_id)
        if producto is None:
            return False, f"Producto con ID {producto_id} no encontrado"
        
        espacio = producto.espacio_disponible()
        if cantidad > espacio:
            return False, (
                f"No hay suficiente espacio. "
                f"Espacio disponible: {espacio}, Cantidad solicitada: {cantidad}"
            )
        
        # Actualizar stock
        producto.stock_actual += cantidad
        self.inventario._invalidar_cache()
        
        return True, f"Entrada registrada: {cantidad} unidades de '{producto.nombre}'"
    
    def registrar_entradas_batch(
        self,
        vector_entradas: Dict[int, int]
    ) -> Tuple[int, List[str]]:
        """
        Registra múltiples entradas de inventario.
        
        Operación matricial: s' = s + e
        
        Args:
            vector_entradas: Diccionario {producto_id: cantidad}
        
        Returns:
            Tuple[int, List[str]]: (cantidad exitosa, lista de mensajes)
        """
        exitosas = 0
        mensajes = []
        
        for producto_id, cantidad in vector_entradas.items():
            exito, mensaje = self.registrar_entrada(producto_id, cantidad)
            mensajes.append(mensaje)
            if exito:
                exitosas += 1
        
        return exitosas, mensajes
    
    # =========================================================================
    # OPERACIONES DE SALIDA (VENTAS/DESPACHO)
    # =========================================================================
    
    def registrar_salida(
        self,
        producto_id: int,
        cantidad: int
    ) -> Tuple[bool, str]:
        """
        Registra una salida de inventario para un producto.
        
        Operación: stock_nuevo = stock_actual - cantidad
        Restricción: stock_nuevo ≥ 0
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a retirar (debe ser positiva)
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if cantidad <= 0:
            return False, "La cantidad debe ser positiva"
        
        producto = self.inventario.obtener_producto(producto_id)
        if producto is None:
            return False, f"Producto con ID {producto_id} no encontrado"
        
        if cantidad > producto.stock_actual:
            return False, (
                f"Stock insuficiente. "
                f"Disponible: {producto.stock_actual}, Solicitado: {cantidad}"
            )
        
        # Actualizar stock
        producto.stock_actual -= cantidad
        self.inventario._invalidar_cache()
        
        return True, f"Salida registrada: {cantidad} unidades de '{producto.nombre}'"
    
    def registrar_salidas_batch(
        self,
        vector_salidas: Dict[int, int]
    ) -> Tuple[int, List[str]]:
        """
        Registra múltiples salidas de inventario.
        
        Operación matricial: s' = s - x
        
        Args:
            vector_salidas: Diccionario {producto_id: cantidad}
        
        Returns:
            Tuple[int, List[str]]: (cantidad exitosa, lista de mensajes)
        """
        exitosas = 0
        mensajes = []
        
        for producto_id, cantidad in vector_salidas.items():
            exito, mensaje = self.registrar_salida(producto_id, cantidad)
            mensajes.append(mensaje)
            if exito:
                exitosas += 1
        
        return exitosas, mensajes
    
    # =========================================================================
    # ESTADÍSTICAS Y ANÁLISIS
    # =========================================================================
    
    def calcular_estadisticas(self) -> Dict[str, float]:
        """
        Calcula estadísticas descriptivas del inventario usando operaciones
        de álgebra lineal.
        
        Returns:
            Dict con estadísticas del inventario
        """
        stock = self.obtener_vector_stock()
        precios = self.obtener_vector_precios()
        valores = self.calcular_vector_valores()
        alertas = self.calcular_alertas_stock_bajo()
        
        if stock.size == 0:
            return {
                'total_productos': 0,
                'total_unidades': 0,
                'valor_total': 0.0,
                'productos_alerta': 0,
                'porcentaje_alerta': 0.0,
                'stock_promedio': 0.0,
                'precio_promedio': 0.0,
                'valor_promedio': 0.0
            }
        
        total_productos = len(stock)
        
        return {
            'total_productos': total_productos,
            'total_unidades': int(np.sum(stock)),
            'valor_total': float(np.sum(valores)),
            'productos_alerta': int(np.sum(alertas)),
            'porcentaje_alerta': float(np.mean(alertas) * 100),
            'stock_promedio': float(np.mean(stock)),
            'precio_promedio': float(np.mean(precios)),
            'valor_promedio': float(np.mean(valores))
        }
    
    def generar_reporte_dataframe(self) -> pd.DataFrame:
        """
        Genera un reporte completo del inventario como DataFrame.
        
        Incluye información calculada mediante operaciones vectoriales.
        
        Returns:
            pd.DataFrame: Reporte detallado del inventario
        """
        df = self.inventario.obtener_dataframe()
        
        if df.empty:
            return df
        
        # Agregar columnas calculadas vectorialmente
        alertas = self.calcular_alertas_stock_bajo()
        espacio = self.calcular_espacio_disponible()
        reabastecimiento = self.calcular_cantidad_reabastecimiento()
        
        df['alerta_stock'] = alertas
        df['espacio_disponible'] = espacio
        df['sugerencia_reabastecimiento'] = reabastecimiento
        
        # Calcular porcentaje de ocupación
        if 'stock_actual' in df.columns and 'stock_maximo' in df.columns:
            df['porcentaje_ocupacion'] = (
                df['stock_actual'] / df['stock_maximo'] * 100
            ).round(2)
        
        return df
    
    def analisis_por_categoria(self) -> pd.DataFrame:
        """
        Realiza análisis de inventario agrupado por categoría.
        
        Utiliza operaciones de agregación de Pandas sobre datos vectorizados.
        
        Returns:
            pd.DataFrame: Análisis por categoría
        """
        df = self.inventario.obtener_dataframe()
        
        if df.empty:
            return pd.DataFrame()
        
        # Agregación por categoría usando operaciones vectoriales
        return df.groupby('categoria').agg({
            'id': 'count',
            'stock_actual': 'sum',
            'valor_inventario': 'sum',
            'precio': 'mean'
        }).rename(columns={
            'id': 'cantidad_productos',
            'stock_actual': 'total_unidades',
            'valor_inventario': 'valor_total',
            'precio': 'precio_promedio'
        }).round(2)
