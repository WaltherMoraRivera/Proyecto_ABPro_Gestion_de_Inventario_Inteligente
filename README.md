# Sistema de Gestión de Inventario Inteligente

## 📋 Descripción

Sistema de gestión de inventario desarrollado en Python que utiliza **álgebra lineal** (NumPy/Pandas) para representar productos como vectores y el inventario como matrices. Esto permite realizar cálculos eficientes de stock, entradas, salidas y alertas mediante operaciones matriciales.

### 🆕 Características Avanzadas

- **Sistema BIN**: Gestión de múltiples ubicaciones de bodega por producto
- **Carga masiva desde Excel**: Mapeo personalizado de columnas con actualización inteligente
- **Stock consolidado**: Cálculo automático de stock total sumando todas las ubicaciones
- **Identificación única**: Combinación de (Número Item/UPC + BIN) para control granular
- **Visualización agrupada**: Muestra productos con desglose de stock por bodega

## 🏗️ Estructura del Proyecto

```
Proyecto_ABPro_Gestion_de_Inventario_Inteligente/
├── main.py                    # Punto de entrada de la aplicación (consola)
├── gui.py                     # Interfaz gráfica (tkinter)
├── crear_excel_ejemplo.py     # Generador de archivo Excel de ejemplo
├── test_bin.py                # Script de pruebas del sistema BIN
├── models/                    # Módulo de modelos (POO)
│   ├── __init__.py
│   ├── producto.py            # Clase Producto (representación vectorial + BIN)
│   └── inventario.py          # Clase Inventario (representación matricial)
├── logic/                     # Módulo de lógica de negocio
│   ├── __init__.py
│   └── operaciones_matriciales.py  # Operaciones de álgebra lineal
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   ├── test_modelos.py
│   └── test_operaciones.py
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
├── GUIA_CARGA_EXCEL.md       # Guía detallada de carga desde Excel
├── GUIA_BIN.md               # Guía del sistema de ubicaciones BIN
└── RESUMEN_CAMBIOS_BIN.md    # Documentación técnica de cambios
```

## 📐 Modelo Matemático

### 1. Representación Vectorial de Productos

Cada producto se representa como un **vector** de características numéricas:

```
p = [id, precio, stock_actual, stock_mínimo, stock_máximo]
```

**Atributos del Producto:**
- **ID**: Identificador numérico único
- **Número Item**: Código de 6 dígitos (identificador único)
- **Código UPC**: Código de barras universal (identificador único)
- **BIN**: Ubicación en bodega (formato: XXX/XXX/XXX)
- **Nombre**: Descripción del producto
- **Precio**: Valor unitario
- **Stock Actual**: Cantidad en **esta ubicación** (BIN) específica
- **Stock Mínimo/Máximo**: Umbrales de control
- **Categoría**: Clasificación del producto

Ejemplo:
```
Laptop HP en BIN 001/020/006 = [1, 899.990, 15, 5, 50]
Laptop HP en BIN 002/015/003 = [2, 899.990, 10, 5, 50]
Stock Total de Laptop HP = 25 unidades
```

### 2. Sistema BIN - Múltiples Ubicaciones

**Concepto clave**: Un mismo producto puede estar en múltiples ubicaciones de bodega.

- **Identificación única**: (Número Item O Código UPC) + BIN
- **Stock por BIN**: Cada entrada registra el stock en esa ubicación específica
- **Stock Total**: Suma automática de todas las ubicaciones del producto

Ejemplo:
```
Router WiFi (Núm. Item: 100012):
  - BIN 002/015/008: 15 unidades
  - BIN 003/010/004: 10 unidades
  → Stock Total: 25 unidades
```

### 2. Representación Matricial del Inventario

El inventario completo se representa como una **matriz** de dimensión `(n × 5)`, donde `n` es el número de **entradas** (productos en ubicaciones específicas):

```
        | id₁  precio₁  stock₁  min₁  max₁ |
    I = | id₂  precio₂  stock₂  min₂  max₂ |
        | ...    ...     ...    ...   ...  |
        | idₙ  precioₙ  stockₙ  minₙ  maxₙ |
```

**Importante**: Cada fila representa un producto en un BIN específico. Un mismo producto en diferentes BINs aparece en múltiples filas.

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
- NumPy (>=1.21.0)
- Pandas (>=1.3.0)
- openpyxl (>=3.0.0) - Para lectura/escritura de Excel
- tkinter (incluido con Python)
- pytest (para ejecutar pruebas)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/WaltherMoraRivera/Proyecto_ABPro_Gestion_de_Inventario_Inteligente.git
cd Proyecto_ABPro_Gestion_de_Inventario_Inteligente

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

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

# Generar archivo Excel de ejemplo con datos de prueba (incluye sistema BIN)
python crear_excel_ejemplo.py

# Ejecutar pruebas del sistema BIN
python test_bin.py
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

2. **📁 Gestión de Datos (Carga, Exportación y Purga)**
   
   **Cargar Excel:**
   - Botón dedicado para cargar archivos .xlsx y .xls
   - **Mapeo personalizado de columnas**: Selecciona qué columnas del Excel corresponden a cada atributo
   - **Opción "No cargar datos"**: Permite carga parcial de información
   - **Actualización inteligente**: 
     - Si el producto existe (mismo Núm. Item/UPC + BIN) → Actualiza datos
     - Si el producto no existe → Crea nuevo registro
   - **BIN obligatorio**: Identifica la ubicación de bodega del producto
   - Vista previa de datos importados
   - Reporte de operaciones realizadas (agregados/actualizados/errores)
   
   **💾 Exportar Base de Datos:**
   - Exporta todos los productos actuales a un archivo Excel
   - Incluye todas las columnas: ID, Número Item, Código UPC, BIN, Nombre, Precio, Stock (Actual/Mín/Máx), Categoría
   - Formato compatible con "Cargar Excel" para restaurar datos en nuevas sesiones
   - Permite guardar el trabajo realizado y continuar en otra sesión
   - Ideal para respaldos y transferencia de datos
   
   **🗑️ Purgar Base de Datos:**
   - Elimina TODOS los productos del inventario actual
   - **Doble confirmación de seguridad**:
     1. Diálogo de advertencia con cantidad de productos a eliminar
     2. Requiere escribir "purgar" para confirmar la acción
   - Acción permanente e irreversible
   - Útil para limpiar datos de prueba antes de cargar datos reales
   - Recomendación: Exportar antes de purgar
   - Ideal para respaldos y transferencia de datos

3. **🎯 Funcionalidades Integradas**
   - **Ver todos los productos** (agrupados con stock total y desglose por BIN)
   - Ver matriz de inventario
   - Alertas de stock bajo
   - Registrar entradas/salidas (con diálogos)
   - Estadísticas en tiempo real
   - Reportes completos (DataFrame con columna BIN)
   - Análisis por categoría
   - Agregar nuevos productos (formulario con campo BIN)
   - **✏️ Modificar productos existentes**:
     - Búsqueda por ID, Número de Item o Código UPC
     - Visualización de todos los atributos actuales
     - Edición de uno o múltiples campos simultáneamente
     - Campos pre-llenados con valores actuales
     - Validación automática de datos

### Sistema BIN - Gestión de Ubicaciones

**Características:**
- Productos en múltiples ubicaciones de bodega
- Control individual de stock por BIN
- Cálculo automático de stock total
- Identificación única: (Número Item/UPC) + BIN
- Visualización agrupada por producto con desglose

**Métodos disponibles:**
```python
# Obtener stock total de un producto (todas las bodegas)
inventario.obtener_stock_total_producto(numero_item="100012")

# Obtener diccionario {BIN: stock}
inventario.obtener_bins_producto(numero_item="100012")

# Buscar producto en BIN específico
inventario.obtener_producto_por_numero_item_y_bin("100012", "002/015/008")

# Agrupar productos por item
inventario.obtener_productos_agrupados()
```

### Funcionalidades Generales

1. **Gestión de Productos**
   - Agregar/eliminar productos
   - **Modificar productos existentes** (búsqueda por ID/Item/UPC)
   - Representación vectorial automática
   - Soporte para múltiples ubicaciones (BINs)
   - Identificadores únicos: ID, Número Item, Código UPC

2. **Control de Stock**
   - Registrar entradas de inventario
   - Registrar salidas de inventario
   - Validación de restricciones (mínimos y máximos)
   - Stock por ubicación y stock total consolidado

3. **Sistema de Alertas**
   - Detección automática de stock bajo (por BIN)
   - Cálculo de cantidades de reabastecimiento sugeridas

4. **Análisis y Reportes**
   - Valor total del inventario
   - Estadísticas calculadas matricialmente
   - Análisis por categoría
   - Reportes en formato DataFrame (incluye BIN)
   - Agrupación de productos con múltiples ubicaciones

## 🎓 Aspectos Educativos

Este proyecto demuestra:

- **Programación Orientada a Objetos (POO)**: Clases `Producto` e `Inventario` bien estructuradas
- **Álgebra Lineal Aplicada**: Uso de NumPy para operaciones matriciales eficientes
- **Análisis de Datos**: Uso de Pandas para reportes y manipulación de datos
- **Interfaces Gráficas**: Desarrollo de GUI con tkinter
- **Manejo de Archivos Excel**: Lectura/escritura con openpyxl y pandas
- **Buenas Prácticas**: Código limpio, documentado y con pruebas unitarias
- **Patrones de Diseño**: Separación de responsabilidades (models/logic/ui)
- **Gestión de Inventario Real**: Sistema BIN para múltiples ubicaciones de bodega
- **Validación de Datos**: Manejo robusto de errores y validaciones

## 📚 Documentación Adicional

📖 **[ÍNDICE COMPLETO DE DOCUMENTACIÓN](INDICE_DOCUMENTACION.md)** - Guía de navegación de toda la documentación

- **[GUIA_CARGA_EXCEL.md](GUIA_CARGA_EXCEL.md)**: Guía completa sobre cómo cargar inventario desde Excel
  - Proceso de mapeo de columnas
  - Actualización vs. creación de productos
  - Casos de uso y ejemplos

- **[GUIA_BIN.md](GUIA_BIN.md)**: Guía del sistema de ubicaciones BIN
  - Concepto de BIN y múltiples ubicaciones
  - Identificación única de productos
  - Cálculo de stock total
  - Ejemplos prácticos

- **[RESUMEN_CAMBIOS_BIN.md](RESUMEN_CAMBIOS_BIN.md)**: Documentación técnica de la implementación del sistema BIN

- **[CHANGELOG.md](CHANGELOG.md)**: Registro de cambios y versiones del proyecto

## 🚀 Inicio Rápido

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generar datos de ejemplo:**
   ```bash
   python crear_excel_ejemplo.py
   ```
   Esto crea `inventario_ejemplo.xlsx` con productos de prueba incluyendo ejemplos de múltiples ubicaciones.

3. **Ejecutar la aplicación:**
   ```bash
   python gui.py
   ```

4. **Cargar el Excel:**
   - Click en "📁 Cargar Excel"
   - Seleccionar `inventario_ejemplo.xlsx`
   - Mapear columnas (BIN es obligatorio)
   - Ver resultados en "📋 Ver Todos los Productos"

## 💡 Ejemplo de Visualización

```
═══════════════════════════════════════════════════════════
📦 Router WiFi 6 (Núm. Item: 100012)
   UPC: 012345678912 | Precio: $89.99
   Categoría: Redes
   📊 STOCK TOTAL: 25 unidades

   Desglose por Bodega (BIN):
     ✓ BIN 002/015/008: 15 unidades (ID: 12, Min: 10, Max: 40)
     ✓ BIN 003/010/004: 10 unidades (ID: 13, Min: 10, Max: 40)
───────────────────────────────────────────────────────────
```

## 📝 Licencia

Este proyecto fue desarrollado con fines educativos para el curso de Programación Avanzada.

## 👥 Autores

Proyecto desarrollado para ABPro - Gestión de Inventario Inteligente
