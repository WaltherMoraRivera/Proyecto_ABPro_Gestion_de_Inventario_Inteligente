"""
Pruebas unitarias para el módulo de modelos.

Este módulo contiene tests para las clases Producto e Inventario,
verificando la correcta representación vectorial y matricial.
"""

import pytest
import numpy as np
import pandas as pd
from models import Producto, Inventario


class TestProducto:
    """Pruebas para la clase Producto."""
    
    def test_crear_producto_basico(self):
        """Verifica la creación correcta de un producto."""
        producto = Producto(
            id=1,
            nombre="Test Product",
            precio=99.99,
            stock_actual=50,
            stock_minimo=10,
            stock_maximo=100,
            categoria="Test"
        )
        
        assert producto.id == 1
        assert producto.nombre == "Test Product"
        assert producto.precio == 99.99
        assert producto.stock_actual == 50
        assert producto.stock_minimo == 10
        assert producto.stock_maximo == 100
        assert producto.categoria == "Test"
    
    def test_crear_producto_con_valores_default(self):
        """Verifica los valores por defecto del producto."""
        producto = Producto(id=1, nombre="Test", precio=10.0)
        
        assert producto.stock_actual == 0
        assert producto.stock_minimo == 10
        assert producto.stock_maximo == 100
        assert producto.categoria == "General"
    
    def test_precio_negativo_lanza_error(self):
        """Verifica que un precio negativo lance ValueError."""
        with pytest.raises(ValueError, match="precio no puede ser negativo"):
            Producto(id=1, nombre="Test", precio=-10.0)
    
    def test_stock_actual_negativo_lanza_error(self):
        """Verifica que un stock negativo lance ValueError."""
        with pytest.raises(ValueError, match="stock actual no puede ser negativo"):
            Producto(id=1, nombre="Test", precio=10.0, stock_actual=-5)
    
    def test_stock_maximo_menor_que_minimo_lanza_error(self):
        """Verifica que stock_maximo < stock_minimo lance ValueError."""
        with pytest.raises(ValueError, match="stock máximo debe ser mayor"):
            Producto(
                id=1, nombre="Test", precio=10.0,
                stock_minimo=50, stock_maximo=10
            )
    
    def test_to_vector(self):
        """Verifica la conversión a representación vectorial."""
        producto = Producto(
            id=1, nombre="Test", precio=99.99,
            stock_actual=50, stock_minimo=10, stock_maximo=100
        )
        
        vector = producto.to_vector()
        
        assert isinstance(vector, np.ndarray)
        assert vector.shape == (5,)
        assert vector[0] == 1      # id
        assert vector[1] == 99.99  # precio
        assert vector[2] == 50     # stock_actual
        assert vector[3] == 10     # stock_minimo
        assert vector[4] == 100    # stock_maximo
    
    def test_from_vector(self):
        """Verifica la creación de producto desde vector."""
        vector = np.array([5, 149.99, 25, 5, 50])
        
        producto = Producto.from_vector(vector, "Test Product", "Electrónica")
        
        assert producto.id == 5
        assert producto.precio == 149.99
        assert producto.stock_actual == 25
        assert producto.stock_minimo == 5
        assert producto.stock_maximo == 50
        assert producto.nombre == "Test Product"
        assert producto.categoria == "Electrónica"
    
    def test_necesita_reabastecimiento_true(self):
        """Verifica detección de necesidad de reabastecimiento."""
        producto = Producto(
            id=1, nombre="Test", precio=10.0,
            stock_actual=5, stock_minimo=10
        )
        
        assert producto.necesita_reabastecimiento() is True
    
    def test_necesita_reabastecimiento_false(self):
        """Verifica cuando no necesita reabastecimiento."""
        producto = Producto(
            id=1, nombre="Test", precio=10.0,
            stock_actual=20, stock_minimo=10
        )
        
        assert producto.necesita_reabastecimiento() is False
    
    def test_espacio_disponible(self):
        """Verifica cálculo de espacio disponible."""
        producto = Producto(
            id=1, nombre="Test", precio=10.0,
            stock_actual=30, stock_maximo=100
        )
        
        assert producto.espacio_disponible() == 70
    
    def test_valor_en_inventario(self):
        """Verifica cálculo del valor en inventario."""
        producto = Producto(
            id=1, nombre="Test", precio=25.00,
            stock_actual=40
        )
        
        assert producto.valor_en_inventario() == 1000.00


class TestInventario:
    """Pruebas para la clase Inventario."""
    
    def test_crear_inventario_vacio(self):
        """Verifica creación de inventario vacío."""
        inventario = Inventario()
        
        assert len(inventario) == 0
        assert inventario.cantidad_productos() == 0
    
    def test_agregar_producto(self):
        """Verifica agregar un producto al inventario."""
        inventario = Inventario()
        producto = Producto(id=1, nombre="Test", precio=10.0)
        
        resultado = inventario.agregar_producto(producto)
        
        assert resultado is True
        assert len(inventario) == 1
        assert 1 in inventario
    
    def test_agregar_producto_duplicado(self):
        """Verifica que no se pueda agregar producto duplicado."""
        inventario = Inventario()
        producto1 = Producto(id=1, nombre="Test 1", precio=10.0)
        producto2 = Producto(id=1, nombre="Test 2", precio=20.0)
        
        inventario.agregar_producto(producto1)
        resultado = inventario.agregar_producto(producto2)
        
        assert resultado is False
        assert len(inventario) == 1
    
    def test_eliminar_producto(self):
        """Verifica eliminar un producto del inventario."""
        inventario = Inventario()
        producto = Producto(id=1, nombre="Test", precio=10.0)
        inventario.agregar_producto(producto)
        
        resultado = inventario.eliminar_producto(1)
        
        assert resultado is True
        assert len(inventario) == 0
        assert 1 not in inventario
    
    def test_eliminar_producto_inexistente(self):
        """Verifica eliminar producto que no existe."""
        inventario = Inventario()
        
        resultado = inventario.eliminar_producto(999)
        
        assert resultado is False
    
    def test_obtener_producto(self):
        """Verifica obtener un producto por ID."""
        inventario = Inventario()
        producto = Producto(id=1, nombre="Test", precio=10.0)
        inventario.agregar_producto(producto)
        
        obtenido = inventario.obtener_producto(1)
        
        assert obtenido is not None
        assert obtenido.nombre == "Test"
    
    def test_obtener_producto_inexistente(self):
        """Verifica obtener producto que no existe."""
        inventario = Inventario()
        
        obtenido = inventario.obtener_producto(999)
        
        assert obtenido is None
    
    def test_obtener_matriz_inventario(self):
        """Verifica la representación matricial del inventario."""
        inventario = Inventario()
        inventario.agregar_producto(
            Producto(1, "P1", 10.0, 20, 5, 50)
        )
        inventario.agregar_producto(
            Producto(2, "P2", 25.0, 30, 10, 100)
        )
        
        matriz = inventario.obtener_matriz_inventario()
        
        assert isinstance(matriz, np.ndarray)
        assert matriz.shape == (2, 5)
        
        # Primera fila: producto 1
        assert matriz[0, 0] == 1   # id
        assert matriz[0, 1] == 10  # precio
        assert matriz[0, 2] == 20  # stock
        
        # Segunda fila: producto 2
        assert matriz[1, 0] == 2   # id
        assert matriz[1, 1] == 25  # precio
        assert matriz[1, 2] == 30  # stock
    
    def test_obtener_matriz_inventario_vacio(self):
        """Verifica matriz de inventario vacío."""
        inventario = Inventario()
        
        matriz = inventario.obtener_matriz_inventario()
        
        assert matriz.shape == (0, 5)
    
    def test_obtener_dataframe(self):
        """Verifica obtener inventario como DataFrame."""
        inventario = Inventario()
        inventario.agregar_producto(
            Producto(1, "Test", 10.0, 20, 5, 50, "Cat1")
        )
        
        df = inventario.obtener_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert 'id' in df.columns
        assert 'nombre' in df.columns
        assert 'precio' in df.columns
        assert 'valor_inventario' in df.columns
    
    def test_iterar_productos(self):
        """Verifica que se puede iterar sobre productos."""
        inventario = Inventario()
        inventario.agregar_producto(Producto(1, "P1", 10.0))
        inventario.agregar_producto(Producto(2, "P2", 20.0))
        
        productos = list(inventario)
        
        assert len(productos) == 2
