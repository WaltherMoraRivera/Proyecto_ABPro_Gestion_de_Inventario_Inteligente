# Registro de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

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
