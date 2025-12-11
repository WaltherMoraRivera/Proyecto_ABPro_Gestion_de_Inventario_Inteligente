"""
Módulo que define la clase Producto para el sistema de inventario.

Un producto se representa matemáticamente como un vector de características:
[id, precio, stock_actual, stock_minimo, stock_maximo]

Este enfoque vectorial permite realizar operaciones matriciales eficientes
para análisis y cálculos de inventario.
"""

import numpy as np
from typing import Optional


class Producto:
    """
    Clase que representa un producto en el sistema de inventario.
    
    Cada producto se modela como un vector de características que permite
    realizar operaciones de álgebra lineal para cálculos eficientes.
    
    IMPORTANTE: Un producto puede estar en múltiples ubicaciones de bodega (BINs).
    Cada combinación de (numero_item/codigo_upc + BIN) representa una entrada
    única que indica cuánto stock hay en esa bodega específica.
    
    Atributos:
        id (int): Identificador único del producto
        numero_item (str): Número de item (6 dígitos, identificador único)
        codigo_upc (str): Código UPC (identificador único)
        bin (str): Código de ubicación en bodega (formato: XXX/XXX/XXX)
        nombre (str): Nombre descriptivo del producto
        precio (float): Precio unitario del producto
        stock_actual (int): Cantidad en esta ubicación específica (BIN)
        stock_minimo (int): Stock mínimo antes de generar alerta
        stock_maximo (int): Capacidad máxima de almacenamiento
        categoria (str): Categoría del producto
    
    Representación Vectorial:
        El producto se puede representar como un vector numérico:
        v = [id, precio, stock_actual, stock_minimo, stock_maximo]
    """
    
    def __init__(
        self,
        id: int,
        nombre: str,
        precio: float,
        stock_actual: int = 0,
        stock_minimo: int = 10,
        stock_maximo: int = 100,
        categoria: str = "General",
        numero_item: str = "N/D",
        codigo_upc: str = "N/D",
        bin: str = "N/D"
    ):
        """
        Inicializa un nuevo producto.
        
        Args:
            id: Identificador único del producto
            nombre: Nombre descriptivo del producto
            precio: Precio unitario (debe ser positivo)
            stock_actual: Cantidad en esta ubicación de bodega (BIN)
            stock_minimo: Umbral mínimo para alertas
            stock_maximo: Capacidad máxima de almacenamiento
            categoria: Categoría de clasificación
            numero_item: Número de item (6 dígitos, identificador único)
            codigo_upc: Código UPC (identificador único)
            bin: Código de ubicación en bodega (formato: XXX/XXX/XXX)
        
        Raises:
            ValueError: Si el precio es negativo o los stocks son inválidos
        """
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if stock_actual < 0:
            raise ValueError("El stock actual no puede ser negativo")
        if stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
        if stock_maximo < stock_minimo:
            raise ValueError("El stock máximo debe ser mayor o igual al mínimo")
        
        self.id = id
        self.numero_item = numero_item
        self.codigo_upc = codigo_upc
        self.bin = bin
        self.nombre = nombre
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.categoria = categoria
    
    def to_vector(self) -> np.ndarray:
        """
        Convierte el producto a su representación vectorial.
        
        Esta representación permite realizar operaciones matriciales
        eficientes cuando se trabaja con múltiples productos.
        
        Returns:
            np.ndarray: Vector [id, precio, stock_actual, stock_minimo, stock_maximo]
        """
        return np.array([
            self.id,
            self.precio,
            self.stock_actual,
            self.stock_minimo,
            self.stock_maximo
        ], dtype=np.float64)
    
    @classmethod
    def from_vector(
        cls,
        vector: np.ndarray,
        nombre: str,
        categoria: str = "General"
    ) -> 'Producto':
        """
        Crea un producto a partir de su representación vectorial.
        
        Args:
            vector: Array [id, precio, stock_actual, stock_minimo, stock_maximo]
            nombre: Nombre del producto
            categoria: Categoría del producto
        
        Returns:
            Producto: Nueva instancia de producto
        """
        return cls(
            id=int(vector[0]),
            nombre=nombre,
            precio=float(vector[1]),
            stock_actual=int(vector[2]),
            stock_minimo=int(vector[3]),
            stock_maximo=int(vector[4]),
            categoria=categoria
        )
    
    def necesita_reabastecimiento(self) -> bool:
        """
        Verifica si el producto necesita reabastecimiento.
        
        El reabastecimiento es necesario cuando el stock actual
        está por debajo del stock mínimo establecido.
        
        Returns:
            bool: True si el stock está por debajo del mínimo
        """
        return self.stock_actual < self.stock_minimo
    
    def espacio_disponible(self) -> int:
        """
        Calcula el espacio disponible para almacenar más unidades.
        
        Returns:
            int: Unidades adicionales que se pueden almacenar
        """
        return max(0, self.stock_maximo - self.stock_actual)
    
    def valor_en_inventario(self) -> float:
        """
        Calcula el valor monetario del stock actual.
        
        Returns:
            float: Valor total del producto en inventario
        """
        return self.precio * self.stock_actual
    
    def __repr__(self) -> str:
        """Representación string del producto."""
        return (
            f"Producto(id={self.id}, nombre='{self.nombre}', "
            f"precio={self.precio:.2f}, stock={self.stock_actual})"
        )
    
    def __str__(self) -> str:
        """Representación legible del producto."""
        estado = "⚠️ BAJO STOCK" if self.necesita_reabastecimiento() else "✓ OK"
        return (
            f"{self.nombre} (ID: {self.id})\n"
            f"  Número Item: {self.numero_item}\n"
            f"  Código UPC: {self.codigo_upc}\n"
            f"  BIN (Bodega): {self.bin}\n"
            f"  Precio: ${self.precio:.2f}\n"
            f"  Stock en este BIN: {self.stock_actual}/{self.stock_maximo} [{estado}]\n"
            f"  Categoría: {self.categoria}"
        )
