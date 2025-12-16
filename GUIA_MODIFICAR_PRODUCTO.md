# Guía de Uso: Modificar Producto

## Descripción General

La funcionalidad **"Modificar Producto"** permite buscar y editar cualquier atributo de un producto existente en el inventario. Esta característica está disponible desde el menú principal de la aplicación GUI.

## Acceso a la Funcionalidad

1. Ejecutar la aplicación: `python gui.py`
2. En el menú lateral, seleccionar **✏️ Modificar Producto**

## Proceso de Modificación

### Paso 1: Buscar el Producto

Al seleccionar "Modificar Producto", aparecerá un diálogo que permite buscar el producto mediante tres métodos:

#### Opciones de Búsqueda:
- **Por ID**: Identificador único numérico del producto
- **Por Número de Item**: Código de 6 dígitos del item
- **Por Código UPC**: Código de barras universal del producto

**Ejemplo:**
```
Buscar por: ○ ID  ○ Número Item  ○ Código UPC
Valor: [         ]
```

### Paso 2: Visualizar Datos Actuales

Una vez encontrado el producto, se mostrará un cuadro con **todos los datos actuales**:

```
╔══════════════════════════════════════╗
║         Datos Actuales               ║
╚══════════════════════════════════════╝

ID: 1
Número Item: 100001
Código UPC: 012345678901
BIN: 001/020/006
Nombre: Laptop HP 15
Precio: $899.99
Stock Actual: 15
Stock Mínimo: 5
Stock Máximo: 50
Categoría: Electrónica
```

### Paso 3: Modificar Atributos

Todos los campos estarán **pre-llenados** con los valores actuales del producto:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **ID del Producto** | Identificador único | 1 |
| **Número Item** | Código de 6 dígitos | 100001 |
| **Código UPC** | Código de barras | 012345678901 |
| **BIN** | Ubicación en bodega | 001/020/006 |
| **Nombre** | Nombre del producto | Laptop HP 15 |
| **Precio** | Precio unitario | 899.99 |
| **Stock Actual** | Cantidad disponible | 15 |
| **Stock Mínimo** | Stock mínimo permitido | 5 |
| **Stock Máximo** | Stock máximo permitido | 50 |
| **Categoría** | Categoría del producto | Electrónica |

**💡 Importante:**
- Los campos están pre-llenados con los valores actuales
- **Puede modificar uno o varios campos**
- Los campos que no modifique mantendrán su valor original
- No es necesario llenar todos los campos, solo los que desee cambiar

### Paso 4: Guardar Cambios

1. Modificar los campos deseados
2. Click en **💾 Guardar Cambios**
3. El sistema validará los datos:
   - ID debe ser número entero
   - Precio debe ser número decimal
   - Stock, Mínimo y Máximo deben ser enteros
   - Stock no puede ser negativo
4. Si la validación es exitosa, se guardarán los cambios
5. La vista de productos se actualizará automáticamente

## Características Especiales

### 🔒 Validaciones Implementadas

1. **Validación de ID único**: Si cambia el ID, el sistema verificará que no exista otro producto con ese ID
2. **Validación de tipos de datos**: Asegura que cada campo tenga el tipo de dato correcto
3. **Validación de stock**: No permite valores negativos
4. **Búsqueda flexible**: Puede buscar por cualquiera de los tres identificadores

### 🔄 Cambio de ID

Si modifica el ID del producto:
- El sistema elimina el producto con el ID antiguo
- Crea una nueva entrada con el ID nuevo
- Mantiene todos los demás atributos
- Valida que el nuevo ID no esté en uso

### ⚠️ Consideraciones Importantes

1. **BIN y Productos Duplicados**: Si un producto existe en múltiples ubicaciones (BINs diferentes), la búsqueda por Número de Item o Código UPC retornará el **primer producto encontrado**. Para especificar la ubicación exacta, use el ID único.

2. **Actualización de Caché**: El sistema invalida automáticamente el caché de la matriz de inventario al modificar un producto.

3. **Cancelación**: En cualquier momento puede presionar "Cancelar" para cerrar el diálogo sin guardar cambios.

## Ejemplos de Uso

### Ejemplo 1: Cambiar Precio

1. Buscar producto por ID: `1`
2. Modificar campo "Precio": `799.99`
3. Guardar cambios
4. ✓ Precio actualizado de $899.99 a $799.99

### Ejemplo 2: Actualizar Stock

1. Buscar producto por Número Item: `100002`
2. Modificar campo "Stock Actual": `60`
3. Guardar cambios
4. ✓ Stock actualizado de 45 a 60 unidades

### Ejemplo 3: Cambiar Categoría

1. Buscar producto por Código UPC: `012345678903`
2. Modificar campo "Categoría": `Periféricos`
3. Guardar cambios
4. ✓ Categoría actualizada de "Accesorios" a "Periféricos"

### Ejemplo 4: Modificar Múltiples Campos

1. Buscar producto por ID: `5`
2. Modificar:
   - "Nombre": `Monitor 27" LG UltraWide`
   - "Precio": `349.99`
   - "Stock Máximo": `40`
3. Guardar cambios
4. ✓ Tres campos actualizados simultáneamente

## Diagrama de Flujo

```
┌─────────────────────────┐
│  Clic en "Modificar     │
│  Producto" en menú      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Seleccionar método de  │
│  búsqueda:              │
│  • ID                   │
│  • Número Item          │
│  • Código UPC           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Ingresar valor         │
│  a buscar               │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  ¿Producto encontrado?  │
└────────┬────────┬───────┘
         │ NO     │ SÍ
         ▼        ▼
    ┌──────┐  ┌──────────────────┐
    │Error │  │ Mostrar datos    │
    └──────┘  │ actuales         │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Formulario con   │
              │ campos pre-      │
              │ llenados         │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Usuario modifica │
              │ uno o más campos │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Guardar Cambios  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Validar datos    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Actualizar       │
              │ producto         │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Actualizar vista │
              │ de productos     │
              └──────────────────┘
```

## Testing

Se proporciona un script de prueba: `test_modificar_producto.py`

Para ejecutarlo:
```bash
python test_modificar_producto.py
```

El script verifica:
- ✓ Búsqueda por ID
- ✓ Búsqueda por Número de Item
- ✓ Búsqueda por Código UPC
- ✓ Modificación de atributos
- ✓ Persistencia de cambios

## Notas Técnicas

### Métodos Utilizados

**En `gui.py`:**
- `modificar_producto()`: Abre el diálogo de búsqueda
- `abrir_dialogo_modificacion(producto)`: Muestra el formulario de edición

**En `models/inventario.py`:**
- `obtener_producto(id)`: Búsqueda por ID
- `obtener_producto_por_numero_item(numero_item)`: Búsqueda por número de item
- `obtener_producto_por_codigo_upc(codigo_upc)`: Búsqueda por código UPC
- `_invalidar_cache()`: Invalida el caché tras modificaciones

### Arquitectura

```
┌──────────────┐
│    GUI       │  ← modificar_producto()
│  (gui.py)    │  ← abrir_dialogo_modificacion()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Inventario  │  ← obtener_producto()
│ (inventario. │  ← obtener_producto_por_numero_item()
│     py)      │  ← obtener_producto_por_codigo_upc()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Producto   │  ← Atributos modificables
│ (producto.py)│
└──────────────┘
```

---

**Versión**: 2.0.0  
**Fecha**: Diciembre 2025  
**Autor**: Sistema de Gestión de Inventario Inteligente
