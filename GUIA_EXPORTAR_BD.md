# Guía de Uso: Exportar Base de Datos

## Descripción General

La funcionalidad **"Exportar Base de Datos"** permite guardar todos los productos actuales del inventario en un archivo Excel. Este archivo está completamente compatible con la función "Cargar Excel", lo que permite un workflow completo de exportación e importación de datos.

## Acceso a la Funcionalidad

**Ubicación**: Barra superior de la aplicación, botón **"💾 Exportar Base de Datos"** (a la izquierda del botón "Cargar Excel")

## Workflow Completo de Trabajo

```
┌─────────────────────────────────────────────────────────────┐
│  SESIÓN 1                                                   │
├─────────────────────────────────────────────────────────────┤
│  1. Cargar Excel con datos iniciales                        │
│     └─► Usar "📁 Cargar Excel"                             │
│                                                             │
│  2. Trabajar con los productos                              │
│     ├─► Agregar nuevos productos                           │
│     ├─► Modificar productos existentes                     │
│     ├─► Registrar entradas/salidas                         │
│     └─► Realizar cualquier cambio necesario                │
│                                                             │
│  3. Exportar todo el trabajo                                │
│     └─► Usar "💾 Exportar Base de Datos"                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    [Archivo Excel guardado]
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  SESIÓN 2 (Otro día, otra computadora, etc.)                │
├─────────────────────────────────────────────────────────────┤
│  1. Cargar el archivo exportado anteriormente               │
│     └─► Usar "📁 Cargar Excel"                             │
│                                                             │
│  2. Continuar trabajando desde donde quedó                  │
│     └─► Todos los datos se restauran exactamente           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Cómo Usar la Función

### Paso 1: Tener Productos en el Inventario

La función requiere que haya al menos un producto en el inventario. Puede:
- Cargar productos desde Excel
- Agregar productos manualmente
- Tener productos de sesiones anteriores

### Paso 2: Hacer Clic en "Exportar Base de Datos"

1. Localizar el botón **"💾 Exportar Base de Datos"** en la barra superior
2. Hacer clic en el botón
3. Se abrirá un diálogo para guardar el archivo

### Paso 3: Seleccionar Ubicación y Nombre

El diálogo de guardado permite:
- **Elegir la carpeta** donde guardar el archivo
- **Cambiar el nombre** del archivo (por defecto: `inventario_exportado.xlsx`)
- **Confirmar o cancelar** la operación

### Paso 4: Confirmación

Si la exportación es exitosa, aparecerá un mensaje mostrando:
- ✓ Nombre del archivo guardado
- ✓ Cantidad de productos exportados
- ✓ Nota sobre compatibilidad con "Cargar Excel"

**Ejemplo de mensaje:**
```
Base de datos exportada exitosamente.

Archivo: inventario_exportado.xlsx
Productos exportados: 15

Puede usar este archivo con la opción 'Cargar Excel'
para restaurar estos datos en una nueva sesión.
```

## Estructura del Archivo Exportado

El archivo Excel generado contiene **10 columnas** con toda la información de los productos:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **ID** | Identificador único del producto | 1 |
| **Numero_Item** | Código de 6 dígitos | 100001 |
| **Codigo_UPC** | Código de barras universal | 012345678901 |
| **BIN_Bodega** | Ubicación en bodega | 001/020/006 |
| **Nombre** | Nombre del producto | Laptop HP 15 |
| **Precio** | Precio unitario | 899.99 |
| **Stock_Actual** | Cantidad actual en inventario | 15 |
| **Stock_Minimo** | Stock mínimo permitido | 5 |
| **Stock_Maximo** | Stock máximo permitido | 50 |
| **Categoria** | Categoría del producto | Electrónica |

**Importante**: Los nombres de las columnas siguen exactamente el formato esperado por "Cargar Excel" con mapeo automático.

## Casos de Uso

### 1. Respaldo Periódico
**Situación**: Quiere guardar el estado actual del inventario como respaldo.

**Pasos**:
1. Hacer clic en "Exportar Base de Datos"
2. Guardar con nombre descriptivo: `inventario_backup_2025-12-16.xlsx`
3. Guardar en carpeta de respaldos

**Beneficio**: Puede restaurar el inventario a este punto en cualquier momento.

---

### 2. Fin de Jornada/Sesión
**Situación**: Ha trabajado todo el día agregando/modificando productos y necesita guardar el progreso.

**Pasos**:
1. Al finalizar el trabajo, exportar base de datos
2. Guardar como: `inventario_2025-12-16_final.xlsx`
3. Al día siguiente, cargar este archivo para continuar

**Beneficio**: No pierde ningún trabajo realizado.

---

### 3. Transferencia entre Computadoras
**Situación**: Trabajó en una computadora y necesita continuar en otra.

**Pasos**:
1. En la primera PC: Exportar base de datos
2. Transferir archivo (USB, correo, nube, etc.)
3. En la segunda PC: Cargar el archivo exportado

**Beneficio**: Movilidad total del trabajo.

---

### 4. Compartir Inventario
**Situación**: Necesita enviar el inventario actual a un colega o supervisor.

**Pasos**:
1. Exportar base de datos
2. Enviar el archivo Excel generado
3. El receptor puede abrirlo en Excel o cargarlo en la aplicación

**Beneficio**: Fácil compartición de datos.

---

### 5. Auditoría/Snapshots
**Situación**: Necesita mantener registros del estado del inventario en momentos específicos.

**Pasos**:
1. Al final de cada mes/semana, exportar base de datos
2. Guardar con fecha: `inventario_2025-12_cierre_mes.xlsx`
3. Mantener archivos históricos

**Beneficio**: Registro histórico para análisis y auditorías.

---

### 6. Migración de Datos
**Situación**: Necesita mover datos a una nueva instalación de la aplicación.

**Pasos**:
1. En instalación antigua: Exportar base de datos
2. Instalar aplicación en nuevo sistema
3. Cargar archivo exportado

**Beneficio**: Migración sin pérdida de datos.

---

## Compatibilidad con "Cargar Excel"

El archivo exportado está diseñado para ser **100% compatible** con la función "Cargar Excel":

✅ **Nombres de columnas correctos**: Coinciden exactamente con los esperados  
✅ **Formato de datos**: Tipos de datos correctos (números, texto)  
✅ **Estructura**: Una fila por producto, encabezados en primera fila  
✅ **Codificación**: Compatible con diferentes sistemas  
✅ **BIN incluido**: Mantiene la información de ubicaciones de bodega

### Flujo de Carga del Archivo Exportado

1. Abrir la aplicación
2. Clic en "📁 Cargar Excel"
3. Seleccionar el archivo previamente exportado
4. En el diálogo de mapeo:
   - Mapear `ID` → `ID`
   - Mapear `Numero_Item` → `Numero_Item`
   - Mapear `Codigo_UPC` → `Codigo_UPC`
   - Mapear `BIN_Bodega` → `BIN_Bodega`
   - Mapear las demás columnas según corresponda
5. Cargar datos
6. ✓ Todos los productos se restauran exactamente como estaban

## Validaciones y Manejo de Errores

### Validación: Inventario Vacío
**Situación**: No hay productos en el inventario.

**Comportamiento**:
```
⚠️ Sin Datos

No hay productos en el inventario para exportar.
```

**Solución**: Agregar o cargar productos antes de exportar.

---

### Validación: Error al Guardar
**Situación**: No se puede escribir el archivo (permisos, espacio, etc.).

**Comportamiento**:
```
❌ Error al Exportar

No se pudo exportar la base de datos:
[Mensaje de error específico]
```

**Soluciones**:
- Verificar permisos de escritura en la carpeta
- Verificar espacio disponible en disco
- Cerrar el archivo si está abierto en Excel
- Seleccionar otra ubicación

---

### Validación: Cancelación
**Situación**: Usuario cancela el diálogo de guardado.

**Comportamiento**: La función termina sin hacer nada, sin mensajes de error.

---

## Diferencias con "Agregar Producto" y "Modificar Producto"

| Función | Propósito | Alcance |
|---------|-----------|---------|
| **Agregar Producto** | Crear UN producto nuevo | 1 producto a la vez |
| **Modificar Producto** | Editar UN producto existente | 1 producto a la vez |
| **Exportar Base de Datos** | Guardar TODOS los productos | TODO el inventario |

**Exportar Base de Datos** es una operación masiva que guarda el estado completo del sistema.

## Formato Técnico del Archivo

### Características del Excel Generado

- **Formato**: `.xlsx` (Excel 2007+)
- **Hoja**: Nombre `Inventario`
- **Encabezados**: Primera fila
- **Índice**: No incluido (sin columna de números de fila)
- **Codificación**: UTF-8
- **Separadores**: Automáticos según Excel

### Ejemplo de Contenido

```
ID | Numero_Item | Codigo_UPC    | BIN_Bodega  | Nombre        | Precio | Stock_Actual | Stock_Minimo | Stock_Maximo | Categoria
---|-------------|---------------|-------------|---------------|--------|--------------|--------------|--------------|------------
1  | 100001      | 012345678901  | 001/020/006 | Laptop HP 15  | 899.99 | 15           | 5            | 50           | Electrónica
2  | 100001      | 012345678901  | 002/015/003 | Laptop HP 15  | 899.99 | 10           | 5            | 50           | Electrónica
3  | 100002      | 012345678902  | 001/020/007 | Mouse Wireless| 29.99  | 45           | 20           | 100          | Accesorios
```

## Mejores Prácticas

### 1. Nomenclatura de Archivos
Use nombres descriptivos que incluyan:
- Fecha: `inventario_2025-12-16.xlsx`
- Propósito: `inventario_backup_mensual.xlsx`
- Versión: `inventario_v2.xlsx`

### 2. Frecuencia de Exportación
Exporte regularmente:
- **Diariamente**: Si hay cambios frecuentes
- **Semanalmente**: Para inventarios estables
- **Antes de cambios importantes**: Prevención

### 3. Organización
Mantenga una estructura de carpetas:
```
/Respaldos_Inventario/
  ├─ 2025/
  │  ├─ Diciembre/
  │  │  ├─ inventario_2025-12-01.xlsx
  │  │  ├─ inventario_2025-12-15.xlsx
  │  │  └─ inventario_2025-12-31.xlsx
  │  └─ Noviembre/
  └─ Anteriores/
```

### 4. Verificación Post-Exportación
Después de exportar:
1. ✓ Verificar que el archivo se creó
2. ✓ Comprobar el tamaño del archivo (no está vacío)
3. ✓ Abrir en Excel para validar contenido
4. ✓ Opcional: Cargar en otra instancia de la app para verificar

### 5. Respaldos Múltiples
- Mantenga al menos 3 versiones históricas
- Guarde copias en diferentes ubicaciones
- Considere respaldos en la nube

## Solución de Problemas

### Problema: "No hay productos en el inventario para exportar"
**Causa**: El inventario está vacío.  
**Solución**: Cargar o agregar productos primero.

---

### Problema: El archivo exportado no se puede cargar
**Causa**: Archivo corrupto o dañado.  
**Solución**: 
1. Exportar nuevamente
2. Verificar que Excel puede abrir el archivo
3. Revisar que tiene las 10 columnas esperadas

---

### Problema: Falta información en el archivo exportado
**Causa**: Productos con atributos vacíos o "N/D".  
**Solución**: Los valores "N/D" se exportan tal cual, son válidos.

---

### Problema: El archivo es demasiado grande
**Causa**: Muchos productos en el inventario.  
**Solución**: 
1. Normal para inventarios grandes
2. Considere exportar por categorías (futura funcionalidad)
3. Comprimir el archivo .xlsx en .zip para transferencia

---

## Testing

Se incluye un script de pruebas: `test_exportar_bd.py`

**Para ejecutarlo**:
```bash
python test_exportar_bd.py
```

**El script verifica**:
- ✓ Exportación exitosa de productos
- ✓ Archivo contiene 10 columnas correctas
- ✓ Compatibilidad con "Cargar Excel"
- ✓ Carga simulada funciona
- ✓ Integridad de datos exportados/importados

## Notas Técnicas

### Implementación

**Archivo**: `gui.py`  
**Función**: `exportar_base_datos()`  
**Ubicación botón**: Línea ~123 en `titulo_frame`

**Librerías usadas**:
- `pandas`: Para crear DataFrame y exportar a Excel
- `tkinter.filedialog`: Para diálogo de guardar archivo
- `tkinter.messagebox`: Para mensajes de confirmación/error

**Código simplificado**:
```python
def exportar_base_datos(self):
    # 1. Validar que hay productos
    if not self.inventario.productos:
        return
    
    # 2. Solicitar ubicación de guardado
    archivo = filedialog.asksaveasfilename(...)
    
    # 3. Crear lista de diccionarios con datos
    datos = [{'ID': p.id, 'Nombre': p.nombre, ...} for p in productos]
    
    # 4. Crear DataFrame y exportar
    df = pd.DataFrame(datos)
    df.to_excel(archivo, index=False)
    
    # 5. Confirmar éxito
    messagebox.showinfo("Éxito", ...)
```

### Formato de Datos

```python
datos_productos = [{
    'ID': int,
    'Numero_Item': str,
    'Codigo_UPC': str,
    'BIN_Bodega': str,
    'Nombre': str,
    'Precio': float,
    'Stock_Actual': int,
    'Stock_Minimo': int,
    'Stock_Maximo': int,
    'Categoria': str
}]
```

---

**Versión**: 2.2.0  
**Fecha**: Diciembre 2025  
**Autor**: Sistema de Gestión de Inventario Inteligente
