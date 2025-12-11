# Guía de Uso: Carga de Inventario desde Excel

## 📋 Descripción de la Funcionalidad

Esta funcionalidad permite cargar productos al inventario desde archivos Excel, con la posibilidad de:
- Mapear columnas del Excel a atributos de productos
- Actualizar productos existentes o agregar nuevos
- Carga parcial de datos (algunos atributos pueden omitirse)

## 🆕 Nuevos Atributos de Producto

La clase `Producto` ahora incluye:
- **ID del Producto** (int): Identificador numérico único
- **Número Item** (str): Número de 6 dígitos, identificador único
- **Código UPC** (str): Código UPC, identificador único
- **Nombre** (str): Nombre descriptivo
- **Precio** (float): Precio unitario
- **Stock Actual** (int): Cantidad en inventario
- **Stock Mínimo** (int): Umbral de alerta
- **Stock Máximo** (int): Capacidad máxima
- **Categoría** (str): Clasificación del producto

## 🔍 Identificación de Productos

El sistema utiliza tres posibles identificadores únicos para detectar si un producto ya existe:
1. **Número Item** (prioritario)
2. **Código UPC** (alternativo)
3. **ID del Producto** (respaldo)

## 📥 Proceso de Carga desde Excel

### Paso 1: Preparar el Archivo Excel

Crea un archivo Excel (.xlsx o .xls) con tus datos de inventario. Las columnas pueden tener cualquier nombre, por ejemplo:

```
| ID_Producto | Num_Item | UPC          | Descripcion    | Precio_Unitario | Cantidad_Stock | ... |
|-------------|----------|--------------|----------------|-----------------|----------------|-----|
| 11          | 100011   | 012345678911 | Laptop Dell    | 899.99          | 10             | ... |
| 12          | 100012   | 012345678912 | Mouse Logitech | 29.99           | 50             | ... |
```

### Paso 2: Cargar el Archivo

1. Abre la aplicación GUI: `python gui.py`
2. Haz clic en el botón **"📁 Cargar Excel"** en la esquina superior derecha
3. Selecciona tu archivo Excel

### Paso 3: Mapear Columnas

Se abrirá un diálogo de "Mapeo de Columnas" donde debes:

1. **Seleccionar qué columna del Excel corresponde a cada atributo:**
   - Para cada atributo (ID, Número Item, Código UPC, etc.)
   - Selecciona la columna correspondiente del Excel
   - O selecciona "No cargar datos" si no quieres cargar ese atributo

2. **Requisito mínimo:**
   - Al menos UNO de estos identificadores debe ser mapeado:
     - ID del Producto
     - Número Item
     - Código UPC

3. **Ejemplo de mapeo:**
   ```
   Atributo del Producto       →  Columna del Excel
   ─────────────────────────────────────────────────
   ID del Producto          *   →  ID_Producto
   Número Item (6 dígitos)  *   →  Num_Item
   Código UPC              *   →  UPC
   Nombre                      →  Descripcion
   Precio                      →  Precio_Unitario
   Stock Actual                →  Cantidad_Stock
   Stock Mínimo                →  Stock_Min
   Stock Máximo                →  Stock_Max
   Categoría                   →  Cat
   ```

### Paso 4: Confirmar la Carga

Haz clic en **"Cargar Datos"** para procesar el archivo.

## 🔄 Actualización vs. Creación

### Producto Existente (Actualización)

Si el sistema encuentra un producto con el mismo **Número Item** o **Código UPC**:

1. **Atributos mapeados:** Se actualizan con los valores del Excel
2. **Atributos con "No cargar datos":** Se mantienen los valores previos
3. Ejemplo:
   - Producto existente: `Laptop Dell` con precio $899.99
   - Excel solo mapea: Nombre y Stock Actual
   - Resultado: Se actualiza nombre y stock, el precio se mantiene en $899.99

### Producto Nuevo (Creación)

Si el producto NO existe en el inventario:

1. **Atributos mapeados:** Usan los valores del Excel
2. **Atributos con "No cargar datos":** Se establecen como "N/D" (Not Data)
3. Valores por defecto numéricos:
   - Precio: 0.0
   - Stock Actual: 0
   - Stock Mínimo: 10
   - Stock Máximo: 100

## 📝 Ejemplo Práctico

### Archivo Excel: `inventario_ejemplo.xlsx`

```
| ID_Producto | Num_Item | UPC          | Descripcion      | Precio_Unitario | Cantidad_Stock |
|-------------|----------|--------------|------------------|-----------------|----------------|
| 11          | 100011   | 012345678911 | Impresora HP     | 299.99          | 8              |
| 2           | 100002   | 012345678902 | Mouse Actualizado| 34.99           | 60             |
```

### Mapeo Configurado:
- ID del Producto → ID_Producto
- Número Item → Num_Item  
- Código UPC → UPC
- Nombre → Descripcion
- Precio → Precio_Unitario
- Stock Actual → Cantidad_Stock
- Stock Mínimo → No cargar datos
- Stock Máximo → No cargar datos
- Categoría → No cargar datos

### Resultado:
1. **Producto ID=11** (nuevo):
   - Se crea con: ID=11, numero_item=100011, UPC=012345678911
   - Nombre: "Impresora HP", Precio: 299.99, Stock: 8
   - Stock Mín/Máx: 10/100 (valores por defecto)
   - Categoría: "N/D"

2. **Producto numero_item=100002** (existente, era "Mouse Inalámbrico"):
   - Se actualiza: Nombre → "Mouse Actualizado", Precio → 34.99, Stock → 60
   - Stock Mín/Máx y Categoría: Se mantienen los valores previos (20/100, "Accesorios")

## ⚠️ Notas Importantes

1. **Identificadores Únicos:**
   - Número Item y Código UPC son únicos en todo el inventario
   - No se permite duplicación de estos valores (excepto "N/D")

2. **Validación de Datos:**
   - Los valores numéricos deben ser válidos
   - Stock mínimo ≤ Stock máximo
   - Precios no negativos

3. **Manejo de Errores:**
   - Si una fila tiene errores, se reporta pero continúa con las demás
   - Se muestra un resumen al final: productos agregados, actualizados y errores

4. **Formato de Número Item:**
   - Aunque se recomienda 6 dígitos, el sistema acepta cualquier formato de texto
   - Usa formato consistente en tu inventario

## 🚀 Genera tu Archivo de Prueba

El proyecto incluye un script para generar un Excel de ejemplo:

```bash
python crear_excel_ejemplo.py
```

Este crea `inventario_ejemplo.xlsx` con datos de prueba que puedes usar inmediatamente.

## 📊 Visualización de Resultados

Después de cargar el archivo:
- Se muestra un resumen con productos agregados/actualizados
- Usa "📋 Ver Todos los Productos" para ver el inventario actualizado
- Usa "📈 Reporte Completo" para ver todos los detalles en formato tabla

## 🎯 Casos de Uso

### Caso 1: Carga Inicial Completa
Mapea todas las columnas para crear el inventario desde cero.

### Caso 2: Actualización de Precios
Mapea solo ID/Número Item/UPC y Precio para actualizar precios masivamente.

### Caso 3: Ajuste de Stock
Mapea solo identificadores y Stock Actual para actualizar cantidades.

### Caso 4: Carga Parcial con Mezcla
Combina productos nuevos y actualizaciones en un solo archivo.
