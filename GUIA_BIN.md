# Guía: Sistema BIN - Gestión de Múltiples Ubicaciones de Bodega

## 📦 ¿Qué es el BIN?

**BIN** (del inglés "Binary Location") es el código de ubicación física de un producto en la bodega.

- **Formato:** XXX/XXX/XXX (ejemplo: `001/020/006`)
- **Significado:** Indica la ubicación exacta dentro del almacén
- **Importante:** Un mismo producto puede estar en múltiples ubicaciones (BINs)

## 🔑 Identificación Única de Productos

### Cambio Fundamental

Antes, un producto se identificaba únicamente por:
- Número Item O Código UPC

Ahora, un producto se identifica por la **combinación**:
- **(Número Item O Código UPC) + BIN**

### Ejemplo Práctico

```
Producto: Router WiFi 6
Número Item: 100012
Código UPC: 012345678912

Ubicación 1:
  - BIN: 002/015/008
  - Stock: 15 unidades
  
Ubicación 2:
  - BIN: 003/010/004
  - Stock: 10 unidades

STOCK TOTAL: 25 unidades
```

Este producto existe en **DOS** entradas diferentes en el inventario, una por cada BIN.

## 📊 Visualización de Stock

### Stock por BIN (Individual)
Cada registro muestra el stock en **esa ubicación específica**.

### Stock Total (Consolidado)
Es la **suma** de todas las ubicaciones donde está el producto.

## 📥 Carga desde Excel

### Requisitos de Mapeo

Al cargar desde Excel, **BIN es OBLIGATORIO**:

```
Atributos Requeridos:
✓ Al menos uno: ID, Número Item, o Código UPC
✓ BIN (Obligatorio) - identifica la ubicación
```

### Ejemplo de Mapeo

```
Columna Excel          →  Atributo Producto
─────────────────────────────────────────────
ID_Producto            →  ID del Producto
Num_Item               →  Número Item
UPC                    →  Código UPC
BIN_Bodega             →  BIN (Ubicación Bodega)  ← REQUERIDO
Descripcion            →  Nombre
Cantidad_Stock         →  Stock Actual
...
```

## 🔄 Actualización vs. Creación

### Producto en MISMO BIN (Actualización)

Excel:
```
Num_Item: 100012
BIN: 002/015/008
Stock: 20  (antes era 15)
```

**Resultado:** Actualiza el stock en ese BIN de 15 → 20 unidades

### Producto en NUEVO BIN (Creación)

Excel:
```
Num_Item: 100012  (ya existe)
BIN: 004/025/010  (BIN nuevo)
Stock: 8
```

**Resultado:** Crea una nueva entrada - ahora el producto está en 3 ubicaciones

## 📋 Casos de Uso

### Caso 1: Producto en Una Sola Bodega

```
Laptop Dell XPS
- Núm Item: 100001
- BIN: 001/020/006
- Stock: 15 unidades
```

Stock Total = 15 unidades

### Caso 2: Producto en Múltiples Bodegas

```
Mouse Logitech
- Núm Item: 100002

Ubicaciones:
  BIN: 001/020/007 → 45 unidades
  BIN: 002/015/005 → 30 unidades
  BIN: 003/010/002 → 25 unidades

Stock Total = 100 unidades
```

### Caso 3: Actualización Parcial

Archivo Excel con:
```
| Num_Item | BIN         | Stock |
|----------|-------------|-------|
| 100002   | 001/020/007 | 50    |  ← Solo actualiza este BIN
```

**Resultado:**
- BIN 001/020/007: 45 → **50 unidades** (actualizado)
- BIN 002/015/005: 30 unidades (sin cambios)
- BIN 003/010/002: 25 unidades (sin cambios)

Stock Total = 105 unidades

## 🎯 Visualización en la Aplicación

### Vista Agrupada

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

## ⚙️ Funcionalidades del Sistema

### Métodos Nuevos en Inventario

```python
# Obtener stock total de un producto (todas las bodegas)
stock_total = inventario.obtener_stock_total_producto(numero_item="100012")

# Obtener diccionario {BIN: stock}
bins = inventario.obtener_bins_producto(numero_item="100012")
# Retorna: {"002/015/008": 15, "003/010/004": 10}

# Buscar producto específico en un BIN
producto = inventario.obtener_producto_por_numero_item_y_bin(
    numero_item="100012", 
    bin="002/015/008"
)

# Obtener productos agrupados
agrupados = inventario.obtener_productos_agrupados()
```

## 📝 Archivo Excel de Ejemplo

El sistema incluye productos duplicados para demostrar múltiples ubicaciones:

```
Fila 1: Router WiFi 6, BIN 002/015/008, Stock: 15
Fila 2: Router WiFi 6, BIN 003/010/004, Stock: 10
        ↑ Mismo producto, diferentes ubicaciones
```

## ⚠️ Consideraciones Importantes

### 1. BIN es Obligatorio en la Carga
No se pueden cargar productos sin especificar su ubicación.

### 2. Combinación Única
La combinación (Número Item + BIN) o (Código UPC + BIN) debe ser única.

### 3. Stock Actual vs. Stock Total
- **stock_actual**: Stock en ESE BIN específico
- **Stock Total**: Suma de todos los BINs del producto

### 4. Alertas de Stock Bajo
Se evalúan por BIN individual, no por stock total.

### 5. Valores por Defecto
Si no se especifica BIN al crear un producto manualmente, se asigna "N/D".

## 🔍 Identificación en Tres Pasos

1. **Primero:** Busca por (Número Item + BIN)
2. **Segundo:** Si no encuentra, busca por (Código UPC + BIN)
3. **Tercero:** Como respaldo, busca solo por ID (sin considerar BIN)

## 📈 Ventajas del Sistema BIN

✅ **Control preciso** de ubicaciones físicas
✅ **Distribución de stock** en múltiples almacenes
✅ **Trazabilidad** de dónde está cada unidad
✅ **Flexibilidad** para reorganizar inventario
✅ **Optimización** de picking y almacenamiento

## 🚀 Ejemplo Completo de Flujo

### 1. Carga Inicial
```
Excel:
  - Router WiFi 6, BIN: 002/015/008, Stock: 15
```

### 2. Expansión a Nueva Bodega
```
Excel:
  - Router WiFi 6, BIN: 003/010/004, Stock: 10
```

Ahora tienes 2 entradas, stock total = 25

### 3. Actualización de Stock en Una Bodega
```
Excel:
  - Router WiFi 6, BIN: 002/015/008, Stock: 20
```

Resultado:
- BIN 002/015/008: 20 unidades (actualizado)
- BIN 003/010/004: 10 unidades (sin cambios)
- Stock total = 30 unidades

### 4. Consulta en la Aplicación
Ver "📋 Ver Todos los Productos" muestra:
- Producto agrupado con stock total
- Desglose de cada BIN
