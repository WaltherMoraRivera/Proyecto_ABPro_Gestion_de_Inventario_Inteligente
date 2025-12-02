"""
Pruebas unitarias para el módulo de operaciones matriciales.

Este módulo verifica el correcto funcionamiento de las operaciones
de álgebra lineal utilizadas para gestión de inventario.
"""

import pytest
import numpy as np
import pandas as pd
from models import Producto, Inventario
from logic import OperacionesMatriciales


class TestOperacionesMatriciales:
    """Pruebas para la clase OperacionesMatriciales."""
    
    @pytest.fixture
    def inventario_con_productos(self):
        """Fixture que crea un inventario con productos de prueba."""
        inventario = Inventario()
        inventario.agregar_producto(
            Producto(1, "Producto A", 100.0, 20, 10, 50, "Cat1")
        )
        inventario.agregar_producto(
            Producto(2, "Producto B", 50.0, 5, 10, 30, "Cat1")  # Stock bajo
        )
        inventario.agregar_producto(
            Producto(3, "Producto C", 75.0, 25, 15, 40, "Cat2")
        )
        return inventario
    
    @pytest.fixture
    def operaciones(self, inventario_con_productos):
        """Fixture que crea las operaciones matriciales."""
        return OperacionesMatriciales(inventario_con_productos)
    
    # =========================================================================
    # Tests de vectores
    # =========================================================================
    
    def test_obtener_vector_stock(self, operaciones):
        """Verifica extracción del vector de stock."""
        vector = operaciones.obtener_vector_stock()
        
        assert isinstance(vector, np.ndarray)
        assert len(vector) == 3
        np.testing.assert_array_equal(vector, [20, 5, 25])
    
    def test_obtener_vector_precios(self, operaciones):
        """Verifica extracción del vector de precios."""
        vector = operaciones.obtener_vector_precios()
        
        assert isinstance(vector, np.ndarray)
        assert len(vector) == 3
        np.testing.assert_array_equal(vector, [100.0, 50.0, 75.0])
    
    def test_obtener_vector_minimos(self, operaciones):
        """Verifica extracción del vector de mínimos."""
        vector = operaciones.obtener_vector_minimos()
        
        np.testing.assert_array_equal(vector, [10, 10, 15])
    
    def test_obtener_vector_maximos(self, operaciones):
        """Verifica extracción del vector de máximos."""
        vector = operaciones.obtener_vector_maximos()
        
        np.testing.assert_array_equal(vector, [50, 30, 40])
    
    def test_vectores_inventario_vacio(self):
        """Verifica vectores con inventario vacío."""
        inventario = Inventario()
        ops = OperacionesMatriciales(inventario)
        
        assert ops.obtener_vector_stock().size == 0
        assert ops.obtener_vector_precios().size == 0
    
    # =========================================================================
    # Tests de cálculos de valor
    # =========================================================================
    
    def test_calcular_valor_total_inventario(self, operaciones):
        """
        Verifica cálculo del valor total usando producto punto.
        
        V = p · s = 100*20 + 50*5 + 75*25 = 2000 + 250 + 1875 = 4125
        """
        valor = operaciones.calcular_valor_total_inventario()
        
        assert valor == 4125.0
    
    def test_calcular_vector_valores(self, operaciones):
        """Verifica cálculo vectorizado de valores por producto."""
        valores = operaciones.calcular_vector_valores()
        
        # precio * stock para cada producto
        esperado = np.array([2000.0, 250.0, 1875.0])
        np.testing.assert_array_equal(valores, esperado)
    
    def test_valor_total_inventario_vacio(self):
        """Verifica valor total con inventario vacío."""
        inventario = Inventario()
        ops = OperacionesMatriciales(inventario)
        
        assert ops.calcular_valor_total_inventario() == 0.0
    
    # =========================================================================
    # Tests de alertas
    # =========================================================================
    
    def test_calcular_alertas_stock_bajo(self, operaciones):
        """
        Verifica cálculo vectorizado de alertas.
        
        Producto B tiene stock=5, min=10, entonces alerta=True
        """
        alertas = operaciones.calcular_alertas_stock_bajo()
        
        assert isinstance(alertas, np.ndarray)
        assert alertas.dtype == bool
        # Solo Producto B tiene stock bajo (5 < 10)
        np.testing.assert_array_equal(alertas, [False, True, False])
    
    def test_obtener_productos_alerta(self, operaciones):
        """Verifica obtención de productos con alerta."""
        productos = operaciones.obtener_productos_alerta()
        
        assert len(productos) == 1
        assert productos[0].nombre == "Producto B"
    
    def test_calcular_espacio_disponible(self, operaciones):
        """
        Verifica cálculo del espacio disponible.
        
        d = max - stock = [50-20, 30-5, 40-25] = [30, 25, 15]
        """
        espacio = operaciones.calcular_espacio_disponible()
        
        np.testing.assert_array_equal(espacio, [30, 25, 15])
    
    def test_calcular_cantidad_reabastecimiento(self, operaciones):
        """Verifica cálculo de sugerencia de reabastecimiento."""
        sugerencia = operaciones.calcular_cantidad_reabastecimiento()
        
        # Solo Producto B necesita reabastecimiento
        # punto_optimo = (10 + 30) / 2 = 20
        # cantidad = 20 - 5 = 15
        assert sugerencia[0] == 0   # Producto A no necesita
        assert sugerencia[1] == 15  # Producto B necesita 15
        assert sugerencia[2] == 0   # Producto C no necesita
    
    # =========================================================================
    # Tests de entradas
    # =========================================================================
    
    def test_registrar_entrada_exitosa(self, inventario_con_productos):
        """Verifica registro exitoso de entrada."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_entrada(1, 10)
        
        assert exito is True
        assert "Entrada registrada" in mensaje
        assert inventario_con_productos.obtener_producto(1).stock_actual == 30
    
    def test_registrar_entrada_excede_maximo(self, inventario_con_productos):
        """Verifica que no se exceda el stock máximo."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_entrada(1, 100)
        
        assert exito is False
        assert "espacio" in mensaje.lower()
    
    def test_registrar_entrada_cantidad_negativa(self, inventario_con_productos):
        """Verifica rechazo de cantidad negativa."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_entrada(1, -5)
        
        assert exito is False
        assert "positiva" in mensaje.lower()
    
    def test_registrar_entrada_producto_inexistente(self, inventario_con_productos):
        """Verifica rechazo de producto inexistente."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_entrada(999, 10)
        
        assert exito is False
        assert "no encontrado" in mensaje.lower()
    
    def test_registrar_entradas_batch(self, inventario_con_productos):
        """Verifica registro de múltiples entradas."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        entradas = {1: 5, 2: 10, 3: 5}
        exitosas, mensajes = ops.registrar_entradas_batch(entradas)
        
        assert exitosas == 3
        assert len(mensajes) == 3
    
    # =========================================================================
    # Tests de salidas
    # =========================================================================
    
    def test_registrar_salida_exitosa(self, inventario_con_productos):
        """Verifica registro exitoso de salida."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_salida(1, 5)
        
        assert exito is True
        assert "Salida registrada" in mensaje
        assert inventario_con_productos.obtener_producto(1).stock_actual == 15
    
    def test_registrar_salida_stock_insuficiente(self, inventario_con_productos):
        """Verifica rechazo por stock insuficiente."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_salida(2, 10)  # Stock es 5
        
        assert exito is False
        assert "insuficiente" in mensaje.lower()
    
    def test_registrar_salida_cantidad_negativa(self, inventario_con_productos):
        """Verifica rechazo de cantidad negativa."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        exito, mensaje = ops.registrar_salida(1, -5)
        
        assert exito is False
        assert "positiva" in mensaje.lower()
    
    def test_registrar_salidas_batch(self, inventario_con_productos):
        """Verifica registro de múltiples salidas."""
        ops = OperacionesMatriciales(inventario_con_productos)
        
        salidas = {1: 5, 3: 10}
        exitosas, mensajes = ops.registrar_salidas_batch(salidas)
        
        assert exitosas == 2
        assert len(mensajes) == 2
    
    # =========================================================================
    # Tests de estadísticas y reportes
    # =========================================================================
    
    def test_calcular_estadisticas(self, operaciones):
        """Verifica cálculo de estadísticas completas."""
        stats = operaciones.calcular_estadisticas()
        
        assert stats['total_productos'] == 3
        assert stats['total_unidades'] == 50  # 20 + 5 + 25
        assert stats['valor_total'] == 4125.0
        assert stats['productos_alerta'] == 1
        assert 'porcentaje_alerta' in stats
        assert 'stock_promedio' in stats
    
    def test_generar_reporte_dataframe(self, operaciones):
        """Verifica generación de reporte como DataFrame."""
        df = operaciones.generar_reporte_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert 'alerta_stock' in df.columns
        assert 'espacio_disponible' in df.columns
        assert 'sugerencia_reabastecimiento' in df.columns
        assert 'porcentaje_ocupacion' in df.columns
    
    def test_analisis_por_categoria(self, operaciones):
        """Verifica análisis agrupado por categoría."""
        df = operaciones.analisis_por_categoria()
        
        assert isinstance(df, pd.DataFrame)
        assert 'Cat1' in df.index
        assert 'Cat2' in df.index
        assert 'cantidad_productos' in df.columns
        assert 'total_unidades' in df.columns
        assert 'valor_total' in df.columns
    
    def test_estadisticas_inventario_vacio(self):
        """Verifica estadísticas con inventario vacío."""
        inventario = Inventario()
        ops = OperacionesMatriciales(inventario)
        
        stats = ops.calcular_estadisticas()
        
        assert stats['total_productos'] == 0
        assert stats['total_unidades'] == 0
        assert stats['valor_total'] == 0.0
