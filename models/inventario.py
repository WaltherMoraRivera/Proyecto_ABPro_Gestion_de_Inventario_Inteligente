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
        """Invalida el caché de la matriz cuando hay cambios (uso interno)."""
        self._cache_valido = False
    
    def notificar_cambio_stock(self):
        """
        Notifica que hubo un cambio en el stock de productos.
        
        Debe llamarse después de modificar el stock de un producto
        para mantener la coherencia del caché de la matriz.
        """
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
    
    def obtener_producto_por_numero_item(self, numero_item: str) -> Optional[Producto]:
        """
        Obtiene un producto por su número de item.
        
        NOTA: Si hay múltiples productos con el mismo numero_item en diferentes BINs,
        retorna el primero encontrado. Use obtener_producto_por_numero_item_y_bin()
        para especificar el BIN.
        
        Args:
            numero_item: Número de item del producto
        
        Returns:
            Producto o None si no existe
        """
        for producto in self.productos.values():
            if producto.numero_item == numero_item and numero_item != "N/D":
                return producto
        return None
    
    def obtener_producto_por_codigo_upc(self, codigo_upc: str) -> Optional[Producto]:
        """
        Obtiene un producto por su código UPC.
        
        NOTA: Si hay múltiples productos con el mismo codigo_upc en diferentes BINs,
        retorna el primero encontrado. Use obtener_producto_por_codigo_upc_y_bin()
        para especificar el BIN.
        
        Args:
            codigo_upc: Código UPC del producto
        
        Returns:
            Producto o None si no existe
        """
        for producto in self.productos.values():
            if producto.codigo_upc == codigo_upc and codigo_upc != "N/D":
                return producto
        return None
    
    def obtener_producto_por_numero_item_y_bin(self, numero_item: str, bin: str) -> Optional[Producto]:
        """
        Obtiene un producto por su número de item Y ubicación de bodega (BIN).
        
        Esta es la forma correcta de identificar un producto único considerando
        que puede estar en múltiples ubicaciones de bodega.
        
        Args:
            numero_item: Número de item del producto
            bin: Código de ubicación en bodega
        
        Returns:
            Producto o None si no existe
        """
        for producto in self.productos.values():
            if (producto.numero_item == numero_item and numero_item != "N/D" and
                producto.bin == bin and bin != "N/D"):
                return producto
        return None
    
    def obtener_producto_por_codigo_upc_y_bin(self, codigo_upc: str, bin: str) -> Optional[Producto]:
        """
        Obtiene un producto por su código UPC Y ubicación de bodega (BIN).
        
        Esta es la forma correcta de identificar un producto único considerando
        que puede estar en múltiples ubicaciones de bodega.
        
        Args:
            codigo_upc: Código UPC del producto
            bin: Código de ubicación en bodega
        
        Returns:
            Producto o None si no existe
        """
        for producto in self.productos.values():
            if (producto.codigo_upc == codigo_upc and codigo_upc != "N/D" and
                producto.bin == bin and bin != "N/D"):
                return producto
        return None
    
    def obtener_stock_total_producto(self, numero_item: str = None, codigo_upc: str = None) -> int:
        """
        Calcula el stock total de un producto sumando todas sus ubicaciones de bodega.
        
        Args:
            numero_item: Número de item del producto
            codigo_upc: Código UPC del producto (alternativo si no hay numero_item)
        
        Returns:
            int: Stock total en todas las bodegas
        """
        total = 0
        for producto in self.productos.values():
            if numero_item and numero_item != "N/D":
                if producto.numero_item == numero_item:
                    total += producto.stock_actual
            elif codigo_upc and codigo_upc != "N/D":
                if producto.codigo_upc == codigo_upc:
                    total += producto.stock_actual
        return total
    
    def obtener_bins_producto(self, numero_item: str = None, codigo_upc: str = None) -> Dict[str, int]:
        """
        Obtiene un diccionario de todas las ubicaciones de bodega (BINs) y sus stocks
        para un producto específico.
        
        Args:
            numero_item: Número de item del producto
            codigo_upc: Código UPC del producto (alternativo si no hay numero_item)
        
        Returns:
            Dict[str, int]: Diccionario {BIN: stock}
        """
        bins = {}
        for producto in self.productos.values():
            if numero_item and numero_item != "N/D":
                if producto.numero_item == numero_item:
                    bins[producto.bin] = producto.stock_actual
            elif codigo_upc and codigo_upc != "N/D":
                if producto.codigo_upc == codigo_upc:
                    bins[producto.bin] = producto.stock_actual
        return bins
    
    def obtener_productos_agrupados(self) -> Dict[str, List[Producto]]:
        """
        Agrupa productos por numero_item o codigo_upc, mostrando todas sus ubicaciones.
        
        Returns:
            Dict[str, List[Producto]]: Diccionario {identificador: [productos en diferentes BINs]}
        """
        agrupados = {}
        for producto in self.productos.values():
            # Usar numero_item como clave principal, o codigo_upc si no hay numero_item
            clave = producto.numero_item if producto.numero_item != "N/D" else producto.codigo_upc
            
            if clave == "N/D":
                # Si no tiene identificador válido, usar el ID
                clave = f"ID_{producto.id}"
            
            if clave not in agrupados:
                agrupados[clave] = []
            agrupados[clave].append(producto)
        
        return agrupados
    
    def actualizar_o_agregar_producto(self, producto_nuevo: Producto) -> Tuple[bool, str, Optional[Producto]]:
        """
        Actualiza un producto existente o agrega uno nuevo basándose en numero_item/codigo_upc Y BIN.
        
        IMPORTANTE: La combinación de (numero_item o codigo_upc) + BIN determina
        la unicidad del producto en el inventario.
        
        Args:
            producto_nuevo: Producto a actualizar o agregar
        
        Returns:
            Tuple[bool, str, Optional[Producto]]: (éxito, mensaje, producto_existente)
        """
        # Buscar producto existente por (numero_item o codigo_upc) Y BIN
        producto_existente = None
        
        if producto_nuevo.numero_item != "N/D" and producto_nuevo.bin != "N/D":
            producto_existente = self.obtener_producto_por_numero_item_y_bin(
                producto_nuevo.numero_item, producto_nuevo.bin
            )
        
        if not producto_existente and producto_nuevo.codigo_upc != "N/D" and producto_nuevo.bin != "N/D":
            producto_existente = self.obtener_producto_por_codigo_upc_y_bin(
                producto_nuevo.codigo_upc, producto_nuevo.bin
            )
        
        if producto_existente:
            # Producto existe en ese BIN, retornar para actualización
            return (True, "Producto encontrado en este BIN para actualización", producto_existente)
        else:
            # Producto no existe en ese BIN, agregar nuevo
            if self.agregar_producto(producto_nuevo):
                return (True, "Producto nuevo agregado en este BIN", None)
            else:
                return (False, "Error al agregar producto", None)
    
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
                'id', 'numero_item', 'codigo_upc', 'bin', 'nombre', 'precio', 'stock_actual',
                'stock_minimo', 'stock_maximo', 'categoria', 'valor_inventario'
            ])
        
        datos = []
        for producto in self.productos.values():
            datos.append({
                'id': producto.id,
                'numero_item': producto.numero_item,
                'codigo_upc': producto.codigo_upc,
                'bin': producto.bin,
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
