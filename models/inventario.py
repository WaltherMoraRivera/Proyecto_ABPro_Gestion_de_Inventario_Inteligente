"""
Módulo que define la clase Inventario para gestión de múltiples productos.

El inventario se representa como una matriz donde:
- Cada fila representa un producto
- Cada columna representa una característica del producto

Esta representación matricial permite realizar operaciones de álgebra lineal
para cálculos eficientes de stock, entradas, salidas y alertas.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from models.producto import Producto


class Inventario:
    """
    Clase que gestiona el inventario completo de productos.
    
    Utiliza representación matricial para operaciones eficientes:
    - Matriz de inventario: cada fila es un producto (vector)
    - Operaciones vectoriales para cálculos de stock
    - Álgebra lineal para análisis de inventario
    
    Atributos:
        productos (Dict[int, Producto]): Diccionario de productos por ID
        _matriz_cache (np.ndarray): Caché de la matriz de inventario
        _cache_valido (bool): Indica si el caché está actualizado
    """
    
    def __init__(self):
        """Inicializa un inventario vacío."""
        self.productos: Dict[int, Producto] = {}
        self._matriz_cache: Optional[np.ndarray] = None
        self._cache_valido: bool = False
        self._nombres_cache: List[str] = []
    
    def _invalidar_cache(self):
        """Invalida el caché de la matriz cuando hay cambios."""
        self._cache_valido = False
    
    def agregar_producto(self, producto: Producto) -> bool:
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            producto: Producto a agregar
        
        Returns:
            bool: True si se agregó exitosamente, False si ya existe
        """
        if producto.id in self.productos:
            return False
        
        self.productos[producto.id] = producto
        self._invalidar_cache()
        return True
    
    def eliminar_producto(self, producto_id: int) -> bool:
        """
        Elimina un producto del inventario.
        
        Args:
            producto_id: ID del producto a eliminar
        
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if producto_id not in self.productos:
            return False
        
        del self.productos[producto_id]
        self._invalidar_cache()
        return True
    
    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """
        Obtiene un producto por su ID.
        
        Args:
            producto_id: ID del producto
        
        Returns:
            Producto o None si no existe
        """
        return self.productos.get(producto_id)
    
    def obtener_matriz_inventario(self) -> np.ndarray:
        """
        Obtiene la representación matricial del inventario.
        
        La matriz tiene la forma (n_productos, 5) donde cada fila es:
        [id, precio, stock_actual, stock_minimo, stock_maximo]
        
        Returns:
            np.ndarray: Matriz de inventario
        """
        if self._cache_valido and self._matriz_cache is not None:
            return self._matriz_cache
        
        if not self.productos:
            return np.array([]).reshape(0, 5)
        
        # Construir matriz a partir de vectores de productos
        vectores = [p.to_vector() for p in self.productos.values()]
        self._matriz_cache = np.vstack(vectores)
        self._nombres_cache = [p.nombre for p in self.productos.values()]
        self._cache_valido = True
        
        return self._matriz_cache
    
    def obtener_dataframe(self) -> pd.DataFrame:
        """
        Obtiene el inventario como DataFrame de Pandas.
        
        Útil para análisis y visualización de datos.
        
        Returns:
            pd.DataFrame: Inventario en formato tabular
        """
        if not self.productos:
            return pd.DataFrame(columns=[
                'id', 'nombre', 'precio', 'stock_actual',
                'stock_minimo', 'stock_maximo', 'categoria', 'valor_inventario'
            ])
        
        datos = []
        for producto in self.productos.values():
            datos.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'stock_actual': producto.stock_actual,
                'stock_minimo': producto.stock_minimo,
                'stock_maximo': producto.stock_maximo,
                'categoria': producto.categoria,
                'valor_inventario': producto.valor_en_inventario()
            })
        
        return pd.DataFrame(datos)
    
    def cantidad_productos(self) -> int:
        """
        Retorna la cantidad de productos en el inventario.
        
        Returns:
            int: Número de productos
        """
        return len(self.productos)
    
    def listar_productos(self) -> List[Producto]:
        """
        Lista todos los productos del inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self.productos.values())
    
    def __len__(self) -> int:
        """Retorna la cantidad de productos."""
        return len(self.productos)
    
    def __iter__(self):
        """Permite iterar sobre los productos."""
        return iter(self.productos.values())
    
    def __contains__(self, producto_id: int) -> bool:
        """Verifica si un producto existe en el inventario."""
        return producto_id in self.productos
    
    def __repr__(self) -> str:
        """Representación string del inventario."""
        return f"Inventario(productos={len(self.productos)})"
