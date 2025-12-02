# Sistema de Gestión de Inventario Inteligente

## 📋 Descripción

Sistema de gestión de inventario desarrollado en Python que utiliza **álgebra lineal** (NumPy/Pandas) para representar productos como vectores y el inventario como matrices. Esto permite realizar cálculos eficientes de stock, entradas, salidas y alertas mediante operaciones matriciales.

## 🏗️ Estructura del Proyecto

```
Proyecto_ABPro_Gestion_de_Inventario_Inteligente/
├── main.py                    # Punto de entrada de la aplicación (consola)
├── gui.py                     # Interfaz gráfica (tkinter)
├── models/                    # Módulo de modelos (POO)
│   ├── __init__.py
│   ├── producto.py            # Clase Producto (representación vectorial)
│   └── inventario.py          # Clase Inventario (representación matricial)
├── logic/                     # Módulo de lógica de negocio
│   ├── __init__.py
│   └── operaciones_matriciales.py  # Operaciones de álgebra lineal
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   ├── test_modelos.py
│   └── test_operaciones.py
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

## 📐 Modelo Matemático

### 1. Representación Vectorial de Productos

Cada producto se representa como un **vector** de características numéricas:

```
p = [id, precio, stock_actual, stock_mínimo, stock_máximo]
```

Ejemplo:
```
Laptop HP = [1, 899.99, 15, 5, 50]
```

### 2. Representación Matricial del Inventario

El inventario completo se representa como una **matriz** de dimensión `(n × 5)`, donde `n` es el número de productos:

```
        | id₁  precio₁  stock₁  min₁  max₁ |
    I = | id₂  precio₂  stock₂  min₂  max₂ |
        | ...    ...     ...    ...   ...  |
        | idₙ  precioₙ  stockₙ  minₙ  maxₙ |
```

### 3. Operaciones de Álgebra Lineal

#### 3.1 Extracción de Vectores de Columna

- **Vector de stock**: `s = I[:, 2]` → Extrae la columna de stock actual
- **Vector de precios**: `p = I[:, 1]` → Extrae la columna de precios
- **Vector de mínimos**: `min = I[:, 3]` → Extrae la columna de stock mínimo

#### 3.2 Cálculo del Valor Total del Inventario

El valor total se calcula mediante el **producto punto** entre el vector de precios y el vector de stock:

```
V = p · s = Σ(precioᵢ × stockᵢ)
```

En código:
```python
valor_total = np.dot(precios, stock)
```

#### 3.3 Operaciones de Entrada y Salida

Las operaciones de entrada y salida se modelan como operaciones vectoriales:

- **Entrada de productos**: `s' = s + e` (donde `e` es el vector de entradas)
- **Salida de productos**: `s' = s - x` (donde `x` es el vector de salidas)

Restricciones:
- `s' ≥ 0` (no se permite stock negativo)
- `s' ≤ max` (no se excede la capacidad máxima)

#### 3.4 Sistema de Alertas

Las alertas de stock bajo se calculan mediante **comparación vectorial elemento a elemento**:

```
alertas = s < min
```

Esto genera un vector booleano donde `True` indica productos que requieren reabastecimiento.

En código:
```python
alertas = stock < minimos  # Retorna [False, True, False, ...]
productos_alerta = np.where(alertas)[0]  # Índices de productos con alerta
```

#### 3.5 Cálculo de Valores por Producto

El valor de cada producto se calcula mediante el **producto de Hadamard** (elemento a elemento):

```
valores = p ⊙ s = [precio₁×stock₁, precio₂×stock₂, ..., precioₙ×stockₙ]
```

En código:
```python
valores = precios * stock  # Producto elemento a elemento
```

## 🚀 Instalación y Uso

### Requisitos

- Python 3.8+
- NumPy
- Pandas
- pytest (para ejecutar pruebas)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/WaltherMoraRivera/Proyecto_ABPro_Gestion_de_Inventario_Inteligente.git
cd Proyecto_ABPro_Gestion_de_Inventario_Inteligente

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo (para pruebas)
pip install pytest
```

### Ejecución

```bash
# Ejecutar la aplicación con interfaz gráfica (recomendado)
python gui.py

# O ejecutar la versión de consola
python main.py
```

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Ejecutar pruebas con cobertura
pytest tests/ -v --cov=.
```

## 📊 Funcionalidades

### Interfaz Gráfica (gui.py)
1. **🖥️ Interfaz Visual Moderna**
   - Diseño intuitivo con tkinter
   - Panel de menú lateral con todas las opciones
   - Área de trabajo con scroll para visualizar datos

2. **📁 Carga de Inventario desde Excel**
   - Botón dedicado para cargar archivos .xlsx y .xls
   - Vista previa de datos importados
   - Preparado para mapeo personalizado de columnas

3. **🎯 Funcionalidades Integradas**
   - Ver todos los productos
   - Ver matriz de inventario
   - Alertas de stock bajo
   - Registrar entradas/salidas (con diálogos)
   - Estadísticas en tiempo real
   - Reportes completos (DataFrame)
   - Análisis por categoría
   - Agregar nuevos productos (formulario)

### Funcionalidades Generales

1. **Gestión de Productos**
   - Agregar/eliminar productos
   - Representación vectorial automática

2. **Control de Stock**
   - Registrar entradas de inventario
   - Registrar salidas de inventario
   - Validación de restricciones (mínimos y máximos)

3. **Sistema de Alertas**
   - Detección automática de stock bajo
   - Cálculo de cantidades de reabastecimiento sugeridas

4. **Análisis y Reportes**
   - Valor total del inventario
   - Estadísticas calculadas matricialmente
   - Análisis por categoría
   - Reportes en formato DataFrame

## 🎓 Aspectos Educativos

Este proyecto demuestra:

- **Programación Orientada a Objetos (POO)**: Clases `Producto` e `Inventario`
- **Álgebra Lineal Aplicada**: Uso de NumPy para operaciones matriciales
- **Análisis de Datos**: Uso de Pandas para reportes
- **Buenas Prácticas**: Código limpio, documentado y con pruebas unitarias
- **Patrones de Diseño**: Separación de responsabilidades (models/logic)

## 📝 Licencia

Este proyecto fue desarrollado con fines educativos para el curso de Programación Avanzada.

## 👥 Autores

Proyecto desarrollado para ABPro - Gestión de Inventario Inteligente
