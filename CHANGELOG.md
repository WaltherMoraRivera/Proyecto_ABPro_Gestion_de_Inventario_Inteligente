# Registro de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [2.2.0] - 2025-12-16

### ✨ Características Añadidas

#### Exportar Base de Datos
- **Botón "💾 Exportar Base de Datos"** en la barra superior (a la izquierda de "Cargar Excel")
- **Exportación completa** de todos los productos actuales a archivo Excel
- **Formato compatible** con la función "Cargar Excel" para restaurar datos
- **Workflow completo**:
  1. Usuario carga datos con "Cargar Excel"
  2. Realiza modificaciones en la aplicación
  3. Exporta todo con "Exportar Base de Datos"
  4. Puede usar el archivo exportado en una nueva sesión

#### Funcionalidades Técnicas
- `exportar_base_datos()` en `gui.py`: Función completa de exportación
- Validación de inventario vacío antes de exportar
- Diálogo para seleccionar ubicación y nombre del archivo
- Todas las columnas incluidas: ID, Numero_Item, Codigo_UPC, BIN_Bodega, Nombre, Precio, Stock_Actual, Stock_Minimo, Stock_Maximo, Categoria
- Mensaje de confirmación con detalles de la exportación
- Manejo robusto de errores

### 📝 Archivos Modificados

#### `gui.py`
- Agregado botón "💾 Exportar Base de Datos" en título_frame (línea ~123)
- Nueva función `exportar_base_datos()` (~70 líneas)
- Exportación usando pandas.to_excel()

### 📚 Documentación Nueva

- **test_exportar_bd.py**: Script de pruebas que verifica:
  - Exportación de productos a Excel
  - Estructura correcta del archivo exportado
  - Compatibilidad con función "Cargar Excel"
  - Carga simulada del archivo exportado
  - ✓ Todas las pruebas pasan (5/5 productos exportados/cargados)

### 🔧 Archivos Actualizados

- **README.md**: 
  - Renombrada sección de "Carga Masiva desde Excel" a "Carga y Exportación de Datos"
  - Agregada subsección "Exportar Base de Datos" con características
  - Explicado workflow completo de carga → modificación → exportación

### 📊 Estadísticas de Cambios

- **Líneas de código añadidas**: ~70 en gui.py
- **Archivos nuevos**: 1 (test_exportar_bd.py)
- **Archivos modificados**: 2 (gui.py, README.md)
- **Botones nuevos**: 1 (Exportar Base de Datos)
- **Columnas exportadas**: 10

### 🎯 Casos de Uso

1. **Respaldo de datos**: Exportar inventario actual antes de cambios importantes
2. **Transferencia entre sesiones**: Guardar trabajo y continuar después
3. **Compartir datos**: Exportar y enviar archivo a otros usuarios
4. **Migración**: Mover datos entre instalaciones
5. **Auditoría**: Crear snapshots del estado del inventario

### ✅ Pruebas Realizadas

- ✓ Exportación de 5 productos exitosa
- ✓ Archivo contiene todas las 10 columnas necesarias
- ✓ Formato compatible verificado
- ✓ Carga del archivo exportado funciona correctamente
- ✓ Interfaz gráfica muestra botón correctamente
- ✓ Mensajes de error/éxito funcionan

---

## [2.1.0] - 2025-12-16

### ✨ Características Añadidas

#### Modificación de Productos Existentes
- **Opción "Modificar Producto" en el menú**: Nueva funcionalidad en la interfaz gráfica
- **Búsqueda flexible por tres métodos**:
  - Por ID del producto
  - Por Número de Item (6 dígitos)
  - Por Código UPC
- **Visualización completa de datos actuales**: Muestra todos los atributos del producto antes de modificar
- **Edición múltiple**: Permite modificar uno o varios atributos simultáneamente
- **Campos pre-llenados**: Todos los campos se cargan con los valores actuales
- **Validaciones robustas**:
  - Verificación de tipos de datos (ID entero, precio decimal, stock entero)
  - Stock no puede ser negativo
  - ID único (no puede cambiar a un ID existente)
  - Manejo de valores vacíos (mantiene valor original si el campo está en blanco)

#### Funcionalidades Técnicas
- `modificar_producto()` en `gui.py`: Diálogo de búsqueda con tres métodos
- `abrir_dialogo_modificacion(producto)` en `gui.py`: Formulario completo de edición
- Actualización automática del caché de matriz tras modificaciones
- Cambio de ID soportado (elimina producto con ID antiguo y crea nuevo)
- Actualización automática de la vista de productos tras modificar

### 📝 Archivos Modificados

#### `gui.py`
- Agregada opción "✏️ Modificar Producto" al menú principal (línea ~142)
- Nueva función `modificar_producto()`: Diálogo de búsqueda
- Nueva función `abrir_dialogo_modificacion(producto)`: Formulario de edición
- Aproximadamente 260 líneas de código añadidas

### 📚 Documentación Nueva

- **GUIA_MODIFICAR_PRODUCTO.md**: Guía completa con:
  - Proceso paso a paso de búsqueda y modificación
  - Explicación de cada campo editable
  - Validaciones y consideraciones importantes
  - 4 ejemplos prácticos de uso
  - Diagrama de flujo del proceso
  - Notas técnicas y arquitectura

- **test_modificar_producto.py**: Script de pruebas que verifica:
  - Búsqueda por ID (modifica precio)
  - Búsqueda por Número de Item (modifica stock)
  - Búsqueda por Código UPC (modifica categoría)
  - Persistencia de cambios
  - Todas las pruebas pasan exitosamente ✓

### 🔧 Archivos Actualizados

- **README.md**: 
  - Agregada funcionalidad "Modificar productos existentes" en sección de Funcionalidades
  - Actualizada lista de métodos de gestión de productos
  
- **INDICE_DOCUMENTACION.md**:
  - Nueva sección para GUIA_MODIFICAR_PRODUCTO.md
  - Agregado test_modificar_producto.py a Scripts y Utilidades
  - Actualizado mapa de navegación
  - Actualizada tabla de resumen

### 📊 Estadísticas de Cambios

- **Líneas de código añadidas**: ~260 en gui.py
- **Archivos nuevos**: 2 (guía + script de pruebas)
- **Archivos modificados**: 3 (gui.py, README.md, INDICE_DOCUMENTACION.md)
- **Funciones nuevas**: 2 (modificar_producto, abrir_dialogo_modificacion)
- **Documentación**: ~350 líneas en GUIA_MODIFICAR_PRODUCTO.md

### 🎯 Mejoras de Usabilidad

- **Interfaz intuitiva**: Proceso de dos pasos (buscar → modificar)
- **Campos pre-llenados**: El usuario ve inmediatamente los valores actuales
- **Flexibilidad**: Modifica solo lo necesario, el resto se mantiene
- **Mensajes claros**: Confirmaciones y errores descriptivos
- **Actualización automática**: La vista se refresca tras guardar cambios

---

## [2.0.0] - 2025-12-11

### 🎉 Características Principales Añadidas

#### Sistema BIN - Múltiples Ubicaciones de Bodega
- **Atributo BIN agregado**: Los productos ahora incluyen código de ubicación en bodega (formato: XXX/XXX/XXX)
- **Identificación única mejorada**: Combinación de (Número Item/UPC + BIN) para control granular
- **Stock por ubicación**: Cada entrada registra el stock en una ubicación específica
- **Stock total consolidado**: Cálculo automático sumando todas las ubicaciones

#### Métodos Nuevos en Inventario
- `obtener_producto_por_numero_item_y_bin()` - Busca producto en BIN específico
- `obtener_producto_por_codigo_upc_y_bin()` - Busca producto en BIN específico por UPC
- `obtener_stock_total_producto()` - Calcula stock total en todas las ubicaciones
- `obtener_bins_producto()` - Retorna diccionario {BIN: stock}
- `obtener_productos_agrupados()` - Agrupa productos mostrando todas sus ubicaciones

#### Interfaz Gráfica Mejorada
- **Vista agrupada de productos**: Muestra productos con stock total y desglose por BIN
- **Mapeo de BIN obligatorio**: Validación en carga desde Excel
- **Formulario actualizado**: Campo BIN agregado al agregar productos manualmente
- **Datos de ejemplo mejorados**: Incluye productos en múltiples ubicaciones

#### Carga desde Excel
- **Campo BIN añadido**: Mapeo obligatorio de la ubicación de bodega
- **Validación mejorada**: Verifica que BIN esté mapeado antes de cargar
- **Búsqueda actualizada**: Considera (Item/UPC + BIN) para identificar productos
- **Actualización granular**: Permite actualizar stock en BIN específico

### 📝 Archivos Modificados

#### `models/producto.py`
- Agregado atributo `bin` con valor por defecto "N/D"
- Actualizada documentación de clase
- Modificado `__str__()` para mostrar BIN

#### `models/inventario.py`
- 5 métodos nuevos para gestión de BINs
- Actualizado `actualizar_o_agregar_producto()` para considerar BIN
- Actualizado `obtener_dataframe()` para incluir columna BIN

#### `gui.py`
- Rediseñada función `ver_productos()` con agrupación y stock total
- Actualizado `abrir_dialogo_mapeo_columnas()` con campo BIN
- Modificado `procesar_datos_excel()` para búsqueda por BIN
- Actualizado `agregar_producto()` con campo BIN
- Actualizado `_cargar_datos_ejemplo()` con BINs

#### `crear_excel_ejemplo.py`
- Nueva columna `BIN_Bodega`
- Ejemplo de producto duplicado en diferentes BINs (Router WiFi 6)

### 📚 Documentación Nueva

- **GUIA_BIN.md**: Guía completa del sistema de ubicaciones BIN
- **RESUMEN_CAMBIOS_BIN.md**: Documentación técnica de la implementación
- **test_bin.py**: Script de pruebas del sistema BIN

### 🔧 Archivos Actualizados

- **README.md**: Completamente actualizado con nueva información del sistema BIN
- **requirements.txt**: Añadidos comentarios y organización mejorada

---

## [1.1.0] - 2025-12-11

### ✨ Características Añadidas

#### Carga desde Excel
- **Mapeo personalizado de columnas**: Interfaz visual para seleccionar qué columnas del Excel corresponden a cada atributo
- **Opción "No cargar datos"**: Permite carga parcial de información
- **Actualización inteligente**: Detecta productos existentes y actualiza solo campos mapeados
- **Creación automática**: Agrega productos nuevos con valores por defecto para campos no mapeados

#### Nuevos Atributos en Producto
- `numero_item` (str): Número de item de 6 dígitos, identificador único
- `codigo_upc` (str): Código UPC, identificador único

#### Métodos Nuevos en Inventario
- `obtener_producto_por_numero_item()` - Busca producto por número de item
- `obtener_producto_por_codigo_upc()` - Busca producto por código UPC
- `actualizar_o_agregar_producto()` - Determina si actualizar o crear producto

### 📝 Archivos Modificados

- `models/producto.py`: Agregados atributos numero_item y codigo_upc
- `models/inventario.py`: Métodos de búsqueda y actualización
- `gui.py`: Sistema completo de mapeo y carga desde Excel

### 📚 Documentación Nueva

- **GUIA_CARGA_EXCEL.md**: Guía detallada de carga desde Excel
- **crear_excel_ejemplo.py**: Generador de archivo Excel de prueba
- **RESUMEN_CAMBIOS.md**: Documentación técnica de cambios

---

## [1.0.0] - Versión Inicial

### 🎯 Características Principales

#### Sistema Base
- Representación vectorial de productos usando NumPy
- Representación matricial del inventario
- Operaciones de álgebra lineal para cálculos eficientes

#### Clases Principales
- **Producto**: Modelo de producto con representación vectorial
- **Inventario**: Gestión de múltiples productos con operaciones matriciales
- **OperacionesMatriciales**: Lógica de negocio con álgebra lineal

#### Funcionalidades
- Agregar/eliminar productos
- Registrar entradas y salidas de inventario
- Sistema de alertas de stock bajo
- Cálculo de valor total del inventario
- Estadísticas y reportes con Pandas
- Análisis por categoría

#### Interfaz Gráfica
- Aplicación tkinter con diseño moderno
- Menú lateral de opciones
- Vista de productos, matriz, alertas
- Diálogos para entradas/salidas
- Estadísticas y reportes visuales

#### Documentación
- README.md completo
- Código documentado con docstrings
- Estructura de proyecto clara

---

## Tipos de Cambios

- **✨ Características Añadidas**: Nuevas funcionalidades
- **🔧 Cambios**: Modificaciones en funcionalidades existentes
- **🐛 Correcciones**: Corrección de errores
- **📝 Documentación**: Cambios solo en documentación
- **🔥 Eliminados**: Características eliminadas
- **⚡ Rendimiento**: Mejoras de rendimiento
- **🔒 Seguridad**: Correcciones de seguridad

---

## Enlaces

- [Repositorio](https://github.com/WaltherMoraRivera/Proyecto_ABPro_Gestion_de_Inventario_Inteligente)
- [Reportar Issues](https://github.com/WaltherMoraRivera/Proyecto_ABPro_Gestion_de_Inventario_Inteligente/issues)
