# 📚 Índice de Documentación del Proyecto

Bienvenido al Sistema de Gestión de Inventario Inteligente. Esta guía te ayudará a navegar por toda la documentación disponible.

---

## 📖 Documentación Principal

### 1. [README.md](README.md) - **INICIO AQUÍ** ⭐
**Propósito**: Documentación principal del proyecto  
**Contenido**:
- Descripción general del sistema
- Estructura del proyecto
- Modelo matemático (álgebra lineal)
- Instalación y configuración
- Funcionalidades completas
- Guía de inicio rápido
- Ejemplos de uso

**Quién debe leerlo**: Todos los usuarios nuevos del proyecto

---

## 🎯 Guías de Usuario

### 2. [GUIA_CARGA_EXCEL.md](GUIA_CARGA_EXCEL.md)
**Propósito**: Guía completa para cargar inventario desde archivos Excel  
**Contenido**:
- Atributos del producto explicados
- Proceso paso a paso de mapeo de columnas
- Diferencia entre actualización y creación
- Casos de uso prácticos
- Opción "No cargar datos"
- Manejo de errores

**Cuándo usar**: Cuando necesites cargar o actualizar productos desde Excel

---

### 3. [GUIA_BIN.md](GUIA_BIN.md)
**Propósito**: Guía del sistema de ubicaciones de bodega (BIN)  
**Contenido**:
- Concepto de BIN y su formato (XXX/XXX/XXX)
- Productos en múltiples ubicaciones
- Stock por BIN vs. Stock Total
- Identificación única (Item/UPC + BIN)
- Métodos del sistema BIN
- Ejemplos de uso y flujos de trabajo
- Ventajas del sistema

**Cuándo usar**: Cuando trabajes con productos en múltiples bodegas

---

### 4. [GUIA_MODIFICAR_PRODUCTO.md](GUIA_MODIFICAR_PRODUCTO.md)
**Propósito**: Guía completa para buscar y modificar productos existentes  
**Contenido**:
- Tres métodos de búsqueda (ID, Número Item, Código UPC)
- Visualización de datos actuales
- Modificación de uno o varios atributos
- Campos pre-llenados con valores actuales
- Validaciones y consideraciones
- Ejemplos prácticos y casos de uso
- Diagrama de flujo del proceso

**Cuándo usar**: Cuando necesites editar información de productos existentes

---

### 5. [GUIA_EXPORTAR_BD.md](GUIA_EXPORTAR_BD.md) ✨ **NUEVO**
**Propósito**: Guía completa para exportar la base de datos a Excel  
**Contenido**:
- Workflow completo de trabajo (cargar → modificar → exportar → cargar)
- Estructura del archivo exportado (10 columnas)
- 6 casos de uso prácticos (respaldo, transferencia, auditoría, etc.)
- Compatibilidad con "Cargar Excel"
- Mejores prácticas y nomenclatura de archivos
- Solución de problemas
- Notas técnicas de implementación

**Cuándo usar**: Cuando necesites guardar el inventario completo o crear respaldos

---

## 🔧 Documentación Técnica

### 6. [RESUMEN_CAMBIOS.md](RESUMEN_CAMBIOS.md)
**Propósito**: Documentación técnica de la implementación inicial de carga desde Excel  
**Contenido**:
- Cambios en clases Producto e Inventario
- Nuevos atributos (numero_item, codigo_upc)
- Implementación del sistema de mapeo
- Archivos modificados y creados
- Detalles técnicos de implementación

**Quién debe leerlo**: Desarrolladores que quieran entender la arquitectura

---

### 7. [RESUMEN_CAMBIOS_BIN.md](RESUMEN_CAMBIOS_BIN.md)
**Propósito**: Documentación técnica completa del sistema BIN  
**Contenido**:
- Cambios en el modelo de datos
- Nuevos métodos implementados
- Lógica de identificación única
- Modificaciones en la interfaz gráfica
- Estadísticas de cambios
- Compatibilidad con versiones anteriores

**Quién debe leerlo**: Desarrolladores que trabajen con el sistema BIN

---

### 8. [CHANGELOG.md](CHANGELOG.md)
**Propósito**: Registro cronológico de todas las versiones y cambios  
**Contenido**:
- Historial de versiones (1.0.0, 1.1.0, 2.0.0, 2.1.0, 2.2.0, 2.3.0)
- Características añadidas por versión
- Archivos modificados en cada versión
- Tipos de cambios (Features, Fixes, Docs, etc.)

**Cuándo usar**: Para ver qué ha cambiado entre versiones

---

## 🛠️ Scripts y Utilidades

### 9. [crear_excel_ejemplo.py](crear_excel_ejemplo.py)
**Propósito**: Script para generar archivo Excel de ejemplo  
**Uso**:
```bash
python crear_excel_ejemplo.py
```
**Genera**: `inventario_ejemplo.xlsx` con datos de prueba incluyendo:
- Productos con todos los atributos
- Ejemplos de productos en múltiples BINs
- Datos listos para probar el mapeo de columnas

---

### 9. [crear_excel_ejemplo.py](crear_excel_ejemplo.py)
**Propósito**: Script para generar archivo Excel de ejemplo  
**Uso**:
```bash
python crear_excel_ejemplo.py
```
**Genera**: `inventario_ejemplo.xlsx` con datos de prueba incluyendo:
- Productos con todos los atributos
- Ejemplos de productos en múltiples BINs
- Datos listos para probar el mapeo de columnas

---

### 10. [test_bin.py](test_bin.py)
**Propósito**: Script de pruebas del sistema BIN  
**Uso**:
```bash
python test_bin.py
```
**Verifica**:
- Creación de productos con BIN
- Cálculo de stock total
- Diccionario de ubicaciones
- Búsqueda por BIN específico
- Agrupación de productos

---

### 10. [test_bin.py](test_bin.py)
**Propósito**: Script de pruebas del sistema BIN  
**Uso**:
```bash
python test_bin.py
```
**Verifica**:
- Creación de productos con BIN
- Cálculo de stock total
- Diccionario de ubicaciones
- Búsqueda por BIN específico
- Agrupación de productos

---

### 11. [test_modificar_producto.py](test_modificar_producto.py)
**Propósito**: Script de pruebas para la funcionalidad de modificación de productos  
**Uso**:
```bash
python test_modificar_producto.py
```
**Verifica**:
- Búsqueda de productos por ID
- Búsqueda de productos por Número de Item
- Búsqueda de productos por Código UPC
- Modificación de atributos (precio, stock, categoría)
- Persistencia de cambios

---

### 11. [test_modificar_producto.py](test_modificar_producto.py)
**Propósito**: Script de pruebas para la funcionalidad de modificación de productos  
**Uso**:
```bash
python test_modificar_producto.py
```
**Verifica**:
- Búsqueda de productos por ID
- Búsqueda de productos por Número de Item
- Búsqueda de productos por Código UPC
- Modificación de atributos (precio, stock, categoría)
- Persistencia de cambios

---

### 12. [test_exportar_bd.py](test_exportar_bd.py)
**Propósito**: Script de pruebas para la funcionalidad de exportación de base de datos  
**Uso**:
```bash
python test_exportar_bd.py
```
**Verifica**:
- Exportación de productos a archivo Excel
- Estructura correcta del archivo exportado (10 columnas)
- Compatibilidad del formato con "Cargar Excel"
- Simulación de carga del archivo exportado
- Integridad de datos exportados/importados

**Genera**: `inventario_prueba_exportacion.xlsx` para validación

---

### 13. [test_purgar_bd.py](test_purgar_bd.py) ✨ **NUEVO**
**Propósito**: Script de pruebas para la funcionalidad de purgar base de datos  
**Uso**:
```bash
python test_purgar_bd.py
```
**Verifica**:
- Purga completa de todos los productos
- Inventario queda vacío después de purgar
- Permite agregar nuevos productos después de purgar
- No quedan rastros de productos antiguos
- Manejo correcto de inventario vacío
- Integridad del sistema después de purgar

**Escenarios probados**: 7 pruebas, todas pasan ✓

---

## 🗺️ Mapa de Navegación

### Para Usuarios Nuevos
1. Leer [README.md](README.md) completo
2. Ejecutar `python crear_excel_ejemplo.py`
3. Ejecutar `python gui.py`
4. Seguir [GUIA_CARGA_EXCEL.md](GUIA_CARGA_EXCEL.md) para cargar el ejemplo

### Para Gestión de Múltiples Bodegas
1. Leer [GUIA_BIN.md](GUIA_BIN.md)
2. Revisar ejemplos en `inventario_ejemplo.xlsx`
3. Ejecutar `python test_bin.py` para ver el sistema en acción

### Para Modificar Productos Existentes
1. Leer [GUIA_MODIFICAR_PRODUCTO.md](GUIA_MODIFICAR_PRODUCTO.md)
2. Ejecutar `python test_modificar_producto.py` para ver ejemplos
3. Usar la opción "✏️ Modificar Producto" en la GUI

### Para Exportar/Respaldar Datos
1. Cargar o trabajar con productos en la aplicación
2. Hacer clic en "💾 Exportar Base de Datos" en la barra superior
3. Guardar el archivo Excel generado
4. Usar el archivo exportado con "Cargar Excel" en futuras sesiones
5. Ejecutar `python test_exportar_bd.py` para ver el proceso de exportación

### Para Limpiar/Reiniciar Inventario
1. **⚠️ PRECAUCIÓN**: Esta acción elimina TODOS los productos permanentemente
2. Se recomienda usar "💾 Exportar Base de Datos" antes de purgar
3. Hacer clic en "🗑️ Purgar Base de Datos" en la barra superior
4. Confirmar en el diálogo de advertencia
5. Escribir "purgar" en el campo de confirmación
6. Ejecutar `python test_purgar_bd.py` para ver el proceso de purga

### Para Desarrolladores
1. [README.md](README.md) - Arquitectura general
2. [RESUMEN_CAMBIOS.md](RESUMEN_CAMBIOS.md) - Implementación carga Excel
3. [RESUMEN_CAMBIOS_BIN.md](RESUMEN_CAMBIOS_BIN.md) - Implementación BIN
4. [CHANGELOG.md](CHANGELOG.md) - Historial completo

---

## 📊 Resumen por Tipo de Documento

| Tipo | Archivos | Propósito |
|------|----------|-----------|
| **Principal** | README.md | Documentación general y punto de entrada |
| **Guías de Usuario** | GUIA_CARGA_EXCEL.md<br>GUIA_BIN.md<br>GUIA_MODIFICAR_PRODUCTO.md<br>GUIA_EXPORTAR_BD.md | Instrucciones paso a paso |
| **Técnica** | RESUMEN_CAMBIOS.md<br>RESUMEN_CAMBIOS_BIN.md | Detalles de implementación |
| **Historial** | CHANGELOG.md | Registro de versiones |
| **Scripts** | crear_excel_ejemplo.py<br>test_bin.py<br>test_modificar_producto.py<br>test_exportar_bd.py<br>test_purgar_bd.py | Utilidades y pruebas |

---

## 🎯 Casos de Uso - ¿Qué Documento Leer?

### "Quiero empezar a usar el sistema"
→ [README.md](README.md) sección "Inicio Rápido"

### "Necesito cargar productos desde Excel"
→ [GUIA_CARGA_EXCEL.md](GUIA_CARGA_EXCEL.md)

### "Tengo productos en varias bodegas"
→ [GUIA_BIN.md](GUIA_BIN.md)

### "Quiero entender cómo funciona internamente"
→ [RESUMEN_CAMBIOS_BIN.md](RESUMEN_CAMBIOS_BIN.md)

### "¿Qué cambió en la última versión?"
→ [CHANGELOG.md](CHANGELOG.md)

### "Necesito datos de ejemplo para probar"
→ Ejecutar `python crear_excel_ejemplo.py`

---

## 📞 Recursos Adicionales

- **Código Fuente**: Ver carpetas `models/`, `logic/`, `tests/`
- **Interfaz Gráfica**: `gui.py`
- **Aplicación Consola**: `main.py`
- **Dependencias**: [requirements.txt](requirements.txt)

---

## 🚀 Inicio Rápido (TL;DR)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Generar datos de ejemplo
python crear_excel_ejemplo.py

# 3. Ejecutar aplicación
python gui.py

# 4. Cargar Excel y explorar funcionalidades
```

**Documentación recomendada**: [README.md](README.md) → [GUIA_BIN.md](GUIA_BIN.md)

---

## ✅ Lista de Verificación para Nuevos Usuarios

- [ ] Leer README.md
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Generar Excel de ejemplo (`python crear_excel_ejemplo.py`)
- [ ] Ejecutar aplicación (`python gui.py`)
- [ ] Cargar el Excel de ejemplo
- [ ] Ver productos agrupados
- [ ] Leer GUIA_BIN.md para entender múltiples ubicaciones
- [ ] Explorar las diferentes opciones del menú

---

**Última actualización**: Diciembre 11, 2025  
**Versión del proyecto**: 2.0.0
