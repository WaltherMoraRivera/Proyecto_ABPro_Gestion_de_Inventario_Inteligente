#!/usr/bin/env python3
"""
Interfaz Gráfica del Sistema de Gestión de Inventario Inteligente
==================================================================

Aplicación con interfaz gráfica usando tkinter que permite:
- Cargar inventario desde archivos Excel
- Gestionar productos en el inventario
- Registrar entradas y salidas de stock
- Ver alertas y estadísticas
- Generar reportes

Uso:
    python gui.py

Autor: Sistema de Gestión de Inventario
Versión: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pandas as pd
import numpy as np
from typing import Optional, Tuple
import sys

from models import Producto, Inventario
from logic import OperacionesMatriciales


class SistemaInventarioGUI:
    """
    Interfaz gráfica principal del sistema de inventario.
    
    Proporciona una interfaz visual moderna para gestionar
    el inventario utilizando operaciones de álgebra lineal.
    """
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica."""
        self.root = root
        self.root.title("Sistema de Gestión de Inventario Inteligente")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Inicializar el sistema de inventario
        self.inventario = Inventario()
        self.operaciones = OperacionesMatriciales(self.inventario)
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar datos de ejemplo
        self._cargar_datos_ejemplo()
        self.actualizar_vista_productos()
    
    def configurar_estilos(self):
        """Configura los estilos visuales de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        self.colores = {
            'primary': '#2196F3',
            'secondary': '#1976D2',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'dark': '#263238',
            'light': '#ECEFF1',
            'bg': '#FFFFFF'
        }
        
        # Estilo para botones
        style.configure('Primary.TButton',
                       background=self.colores['primary'],
                       foreground='white',
                       padding=10,
                       font=('Segoe UI', 10))
        
        style.configure('Success.TButton',
                       background=self.colores['success'],
                       foreground='white',
                       padding=10,
                       font=('Segoe UI', 10))
        
        # Estilo para labels
        style.configure('Title.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colores['dark'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colores['secondary'])
    
    def crear_interfaz(self):
        """Crea todos los componentes de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        titulo = ttk.Label(titulo_frame, 
                          text="📦 Sistema de Gestión de Inventario Inteligente",
                          style='Title.TLabel')
        titulo.pack(side=tk.LEFT)
        
        # Botón de cargar Excel
        btn_excel = ttk.Button(titulo_frame,
                              text="📁 Cargar Excel",
                              style='Success.TButton',
                              command=self.cargar_excel)
        btn_excel.pack(side=tk.RIGHT, padx=5)
        
        # Botón de exportar base de datos
        btn_exportar = ttk.Button(titulo_frame,
                                 text="💾 Exportar Base de Datos",
                                 style='Primary.TButton',
                                 command=self.exportar_base_datos)
        btn_exportar.pack(side=tk.RIGHT, padx=5)
        
        # Botón de purgar base de datos
        btn_purgar = ttk.Button(titulo_frame,
                               text="🗑️ Purgar Base de Datos",
                               command=self.purgar_base_datos)
        btn_purgar.pack(side=tk.RIGHT, padx=5)
        
        # Panel izquierdo (Menú de opciones)
        self.crear_panel_menu(main_frame)
        
        # Panel derecho (Área de contenido)
        self.crear_panel_contenido(main_frame)
    
    def crear_panel_menu(self, parent):
        """Crea el panel de menú con todas las opciones."""
        menu_frame = ttk.LabelFrame(parent, text="  Menú de Opciones  ", padding="10")
        menu_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Lista de opciones del menú
        opciones = [
            ("📋 Ver Todos los Productos", self.ver_productos),
            ("🔢 Ver Matriz de Inventario", self.ver_matriz),
            ("⚠️ Alertas de Stock Bajo", self.ver_alertas),
            ("➕ Registrar Entrada", self.registrar_entrada),
            ("➖ Registrar Salida", self.registrar_salida),
            ("📊 Ver Estadísticas", self.ver_estadisticas),
            ("📈 Reporte Completo", self.ver_reporte),
            ("📂 Análisis por Categoría", self.ver_analisis_categoria),
            ("➕ Agregar Producto", self.agregar_producto),
            ("✏️ Modificar Producto", self.modificar_producto),
        ]
        
        # Crear botones para cada opción
        for i, (texto, comando) in enumerate(opciones):
            btn = ttk.Button(menu_frame,
                           text=texto,
                           command=comando,
                           width=30)
            btn.grid(row=i, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Espaciador
        menu_frame.rowconfigure(len(opciones), weight=1)
        
        # Botón de salir al final
        btn_salir = ttk.Button(menu_frame,
                              text="🚪 Salir",
                              command=self.salir)
        btn_salir.grid(row=len(opciones)+1, column=0, pady=5, sticky=(tk.W, tk.E))
    
    def crear_panel_contenido(self, parent):
        """Crea el panel de contenido principal."""
        contenido_frame = ttk.LabelFrame(parent, text="  Área de Trabajo  ", padding="10")
        contenido_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        contenido_frame.columnconfigure(0, weight=1)
        contenido_frame.rowconfigure(0, weight=1)
        
        # Área de texto con scroll
        self.texto_contenido = scrolledtext.ScrolledText(
            contenido_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#F5F5F5',
            fg='#263238'
        )
        self.texto_contenido.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Mensaje de bienvenida
        self.mostrar_mensaje_bienvenida()
    
    def mostrar_mensaje_bienvenida(self):
        """Muestra el mensaje de bienvenida inicial."""
        mensaje = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🚀 BIENVENIDO AL SISTEMA DE GESTIÓN DE INVENTARIO INTELIGENTE  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

📌 Características:
   • Gestión de inventario con operaciones matriciales (NumPy/Pandas)
   • Carga de inventario desde archivos Excel
   • Alertas automáticas de stock bajo
   • Estadísticas y reportes en tiempo real
   • Análisis por categorías

💡 Instrucciones:
   1. Use el menú lateral para navegar entre las opciones
   2. Puede cargar un inventario desde Excel usando el botón superior
   3. Los datos de ejemplo ya están cargados para demostración

🎯 Para comenzar:
   • Seleccione una opción del menú lateral
   • O cargue su propio inventario desde Excel

═══════════════════════════════════════════════════════════════════

"""
        self.texto_contenido.delete(1.0, tk.END)
        self.texto_contenido.insert(1.0, mensaje)
    
    def _cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para demostración."""
        productos_ejemplo = [
            Producto(1, "Laptop HP 15", 899.990, 15, 5, 50, "Electrónica", "100001", "012345678901", "001/020/006"),
            Producto(2, "Laptop HP 15", 899.990, 10, 5, 50, "Electrónica", "100001", "012345678901", "002/015/003"),
            Producto(3, "Mouse Inalámbrico", 29.990, 45, 20, 100, "Accesorios", "100002", "012345678902", "001/020/007"),
            Producto(4, "Teclado Mecánico", 79.990, 8, 10, 40, "Accesorios", "100003", "012345678903", "001/020/008"),
            Producto(5, "Monitor 24\" LG", 249.990, 12, 5, 30, "Electrónica", "100004", "012345678904", "001/020/009"),
            Producto(6, "Cable HDMI 2m", 14.990, 3, 30, 200, "Accesorios", "100005", "012345678905", "003/010/001"),
            Producto(7, "Disco SSD 500GB", 69.990, 25, 15, 60, "Almacenamiento", "100006", "012345678906", "002/015/005"),
            Producto(8, "Memoria USB 64GB", 12.990, 50, 25, 150, "Almacenamiento", "100007", "012345678907", "002/015/006"),
            Producto(9, "Webcam HD", 49.099, 18, 10, 40, "Accesorios", "100008", "012345678908", "001/020/010"),
            Producto(10, "Audífonos Bluetooth", 59.990, 22, 15, 50, "Audio", "100009", "012345678909", "001/020/011"),
            Producto(11, "Cargador Universal", 24.990, 30, 20, 80, "Accesorios", "100010", "012345678910", "003/010/002"),
        ]
        
        for producto in productos_ejemplo:
            self.inventario.agregar_producto(producto)
    
    def actualizar_vista_productos(self):
        """Actualiza la vista después de cambios en el inventario."""
        # Limpiar el área de contenido
        self.texto_contenido.delete(1.0, tk.END)
        
        # Si no hay productos, mostrar mensaje de bienvenida
        if not self.inventario.productos:
            self.mostrar_mensaje_bienvenida()
        else:
            # Si hay productos, mostrar la lista actualizada
            self.ver_productos()
    
    # ==================== FUNCIONES DEL MENÚ ====================
    
    def cargar_excel(self):
        """Permite cargar un archivo Excel con inventario."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not archivo:
            return
        
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo)
            
            # Abrir diálogo de mapeo de columnas
            self.abrir_dialogo_mapeo_columnas(df, archivo)
            
        except Exception as e:
            messagebox.showerror(
                "Error al cargar Excel",
                f"No se pudo cargar el archivo:\n\n{str(e)}"
            )
    
    def exportar_base_datos(self):
        """Exporta todos los productos actuales a un archivo Excel."""
        if not self.inventario.productos:
            messagebox.showwarning(
                "Sin Datos",
                "No hay productos en el inventario para exportar."
            )
            return
        
        # Solicitar ubicación y nombre del archivo
        archivo = filedialog.asksaveasfilename(
            title="Guardar Base de Datos como Excel",
            defaultextension=".xlsx",
            filetypes=[
                ("Archivos Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ],
            initialfile="inventario_exportado.xlsx"
        )
        
        if not archivo:
            return
        
        try:
            # Crear lista de diccionarios con todos los productos
            datos_productos = []
            
            for producto in self.inventario.listar_productos():
                datos_productos.append({
                    'ID': producto.id,
                    'Numero_Item': producto.numero_item,
                    'Codigo_UPC': producto.codigo_upc,
                    'BIN_Bodega': producto.bin,
                    'Nombre': producto.nombre,
                    'Precio': producto.precio,
                    'Stock_Actual': producto.stock_actual,
                    'Stock_Minimo': producto.stock_minimo,
                    'Stock_Maximo': producto.stock_maximo,
                    'Categoria': producto.categoria
                })
            
            # Crear DataFrame
            df = pd.DataFrame(datos_productos)
            
            # Exportar a Excel
            df.to_excel(archivo, index=False, sheet_name='Inventario')
            
            messagebox.showinfo(
                "Exportación Exitosa",
                f"Base de datos exportada exitosamente.\n\n"
                f"Archivo: {archivo.split('/')[-1].split(chr(92))[-1]}\n"
                f"Productos exportados: {len(datos_productos)}\n\n"
                f"Puede usar este archivo con la opción 'Cargar Excel' "
                f"para restaurar estos datos en una nueva sesión."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error al Exportar",
                f"No se pudo exportar la base de datos:\n\n{str(e)}"
            )
    
    def purgar_base_datos(self):
        """Elimina todos los productos del inventario con confirmación de seguridad."""
        if not self.inventario.productos:
            messagebox.showinfo(
                "Inventario Vacío",
                "No hay productos en el inventario para purgar."
            )
            return
        
        # Contar productos actuales
        cantidad_productos = len(self.inventario.productos)
        
        # Primer nivel de confirmación
        respuesta = messagebox.askokcancel(
            "⚠️ ADVERTENCIA - Purgar Base de Datos",
            f"Esta acción ELIMINARÁ PERMANENTEMENTE todos los productos del inventario.\n\n"
            f"Productos actuales: {cantidad_productos}\n\n"
            f"⚠️ ESTA ACCIÓN NO SE PUEDE DESHACER ⚠️\n\n"
            f"Se recomienda usar 'Exportar Base de Datos' antes de purgar.\n\n"
            f"¿Desea continuar?"
        )
        
        if not respuesta:
            return
        
        # Segundo nivel de confirmación: Escribir "purgar"
        dialog = tk.Toplevel(self.root)
        dialog.title("Confirmar Purga de Base de Datos")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        
        # Título de advertencia
        titulo = ttk.Label(
            frame,
            text="🔴 CONFIRMACIÓN FINAL DE PURGA",
            font=('Segoe UI', 14, 'bold'),
            foreground='#F44336'
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Mensaje de confirmación
        mensaje = ttk.Label(
            frame,
            text=f"Se eliminarán {cantidad_productos} productos de forma PERMANENTE.\n\n"
                 f"Para confirmar esta acción, escriba la palabra:\n"
                 f"purgar\n\n"
                 f"(en minúsculas, sin espacios)",
            font=('Segoe UI', 10),
            justify=tk.CENTER
        )
        mensaje.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Campo de texto para confirmación
        ttk.Label(frame, text="Escriba 'purgar' para confirmar:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        confirmacion_entry = ttk.Entry(frame, width=30, font=('Segoe UI', 10))
        confirmacion_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        confirmacion_entry.focus()
        
        # Variable para controlar si se confirmó
        confirmado = {'valor': False}
        
        def confirmar_purga():
            """Verifica la palabra de confirmación y procede con la purga."""
            palabra = confirmacion_entry.get().strip()
            
            if palabra != "purgar":
                messagebox.showerror(
                    "Error de Confirmación",
                    f"La palabra ingresada '{palabra}' no es correcta.\n\n"
                    f"Debe escribir exactamente: purgar\n"
                    f"(en minúsculas, sin espacios)"
                )
                confirmacion_entry.delete(0, tk.END)
                confirmacion_entry.focus()
                return
            
            # Confirmación correcta, proceder con purga
            confirmado['valor'] = True
            dialog.destroy()
        
        def cancelar():
            """Cancela la operación de purga."""
            dialog.destroy()
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame,
            text="❌ Cancelar",
            command=cancelar
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Confirmar Purga",
            command=confirmar_purga
        ).pack(side=tk.LEFT, padx=5)
        
        # Esperar a que se cierre el diálogo
        dialog.wait_window()
        
        # Si no se confirmó, cancelar
        if not confirmado['valor']:
            messagebox.showinfo(
                "Purga Cancelada",
                "La operación de purga fue cancelada.\n\n"
                "No se eliminó ningún producto."
            )
            return
        
        # Proceder con la purga
        try:
            # Obtener lista de IDs antes de eliminar (para el mensaje)
            ids_eliminados = list(self.inventario.productos.keys())
            productos_eliminados = cantidad_productos
            
            # Eliminar todos los productos
            self.inventario.productos.clear()
            self.inventario._invalidar_cache()
            
            # Actualizar vista
            self.actualizar_vista_productos()
            self.mostrar_mensaje_bienvenida()
            
            # Mensaje de éxito
            messagebox.showinfo(
                "Purga Completada",
                f"✓ Base de datos purgada exitosamente.\n\n"
                f"Productos eliminados: {productos_eliminados}\n"
                f"Inventario actual: 0 productos\n\n"
                f"Puede cargar nuevos datos usando 'Cargar Excel'."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error al Purgar",
                f"Ocurrió un error durante la purga:\n\n{str(e)}"
            )
    
    def abrir_dialogo_mapeo_columnas(self, df: pd.DataFrame, archivo: str):
        """Abre un diálogo para mapear columnas del Excel a atributos de Producto."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Mapeo de Columnas - Carga de Excel")
        dialog.geometry("700x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_frame, 
                 text="Mapeo de Columnas del Archivo Excel",
                 style='Subtitle.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(main_frame,
                 text=f"Archivo: {archivo.split('/')[-1].split(chr(92))[-1]}",
                 font=('Segoe UI', 9)).grid(row=1, column=0, columnspan=2, pady=(0, 5))
        
        ttk.Label(main_frame,
                 text=f"Filas encontradas: {len(df)}",
                 font=('Segoe UI', 9)).grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # Crear frame con scroll para el mapeo
        canvas = tk.Canvas(main_frame, height=350)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Opciones de columnas del Excel + "No cargar datos"
        columnas_excel = ["No cargar datos"] + df.columns.tolist()
        
        # Atributos de Producto a mapear
        atributos = [
            ("ID del Producto", "id", True),
            ("Número Item (6 dígitos)", "numero_item", True),
            ("Código UPC", "codigo_upc", True),
            ("BIN (Ubicación Bodega)", "bin", True),
            ("Nombre", "nombre", False),
            ("Precio", "precio", False),
            ("Stock Actual", "stock_actual", False),
            ("Stock Mínimo", "stock_minimo", False),
            ("Stock Máximo", "stock_maximo", False),
            ("Categoría", "categoria", False),
        ]
        
        # Diccionario para almacenar los comboboxes
        mapeo_combos = {}
        
        # Crear encabezados
        ttk.Label(scrollable_frame, text="Atributo del Producto", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Label(scrollable_frame, text="Columna del Excel", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Crear comboboxes para cada atributo
        for i, (label, key, es_identificador) in enumerate(atributos, start=1):
            # Label del atributo
            label_text = f"{label} {'*' if es_identificador else ''}"
            ttk.Label(scrollable_frame, text=label_text).grid(
                row=i, column=0, padx=10, pady=5, sticky=tk.W
            )
            
            # Combobox para seleccionar columna
            combo = ttk.Combobox(scrollable_frame, values=columnas_excel, 
                               state="readonly", width=30)
            combo.set("No cargar datos")
            combo.grid(row=i, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
            
            mapeo_combos[key] = combo
        
        # Nota sobre identificadores
        ttk.Label(scrollable_frame,
                 text="* Al menos uno de los identificadores debe ser mapeado. BIN es REQUERIDO para identificar la ubicación.",
                 font=('Segoe UI', 8, 'italic'),
                 foreground='#666').grid(row=len(atributos)+1, column=0, columnspan=2, 
                                        padx=10, pady=10, sticky=tk.W)
        
        # Frame para botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        def procesar_carga():
            """Procesa la carga de datos según el mapeo configurado."""
            # Validar que al menos un identificador esté mapeado
            tiene_identificador = False
            for key in ['id', 'numero_item', 'codigo_upc']:
                if mapeo_combos[key].get() != "No cargar datos":
                    tiene_identificador = True
                    break
            
            if not tiene_identificador:
                messagebox.showerror(
                    "Error de Mapeo",
                    "Debe mapear al menos un identificador:\n- ID del Producto\n- Número Item\n- Código UPC"
                )
                return
            
            # Validar que BIN esté mapeado (es requerido para identificar ubicación)
            if mapeo_combos['bin'].get() == "No cargar datos":
                messagebox.showerror(
                    "Error de Mapeo",
                    "El atributo BIN (Ubicación Bodega) es REQUERIDO.\n\n"
                    "BIN identifica en qué bodega está el producto.\n"
                    "Debe mapear este campo para continuar."
                )
                return
            
            # Crear mapeo final
            mapeo = {}
            for key, combo in mapeo_combos.items():
                columna_seleccionada = combo.get()
                if columna_seleccionada != "No cargar datos":
                    mapeo[key] = columna_seleccionada
            
            # Procesar los datos
            exito, mensaje = self.procesar_datos_excel(df, mapeo)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                dialog.destroy()
                self.actualizar_vista_productos()
                self.ver_productos()
            else:
                messagebox.showerror("Error", mensaje)
        
        ttk.Button(btn_frame, text="Cargar Datos", 
                  command=procesar_carga, 
                  style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def procesar_datos_excel(self, df: pd.DataFrame, mapeo: dict) -> Tuple[bool, str]:
        """
        Procesa los datos del Excel y actualiza/agrega productos al inventario.
        
        Args:
            df: DataFrame con los datos del Excel
            mapeo: Diccionario que mapea atributos a columnas del Excel
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        productos_agregados = 0
        productos_actualizados = 0
        errores = []
        
        for idx, fila in df.iterrows():
            try:
                # Extraer valores según el mapeo
                datos_producto = {}
                
                # Procesar cada atributo mapeado
                for atributo, columna_excel in mapeo.items():
                    valor = fila[columna_excel]
                    
                    # Manejar valores NaN o vacíos
                    if pd.isna(valor) or (isinstance(valor, str) and valor.strip() == ""):
                        datos_producto[atributo] = "N/D"
                    else:
                        datos_producto[atributo] = valor
                
                # Determinar si el producto existe (considerando BIN)
                producto_existente = None
                bin_value = str(datos_producto.get('bin', 'N/D')) if datos_producto.get('bin') != "N/D" else "N/D"
                
                # Buscar por numero_item + BIN
                if 'numero_item' in datos_producto and datos_producto['numero_item'] != "N/D" and bin_value != "N/D":
                    producto_existente = self.inventario.obtener_producto_por_numero_item_y_bin(
                        str(datos_producto['numero_item']), bin_value
                    )
                
                # Si no se encontró, buscar por codigo_upc + BIN
                if not producto_existente and 'codigo_upc' in datos_producto and datos_producto['codigo_upc'] != "N/D" and bin_value != "N/D":
                    producto_existente = self.inventario.obtener_producto_por_codigo_upc_y_bin(
                        str(datos_producto['codigo_upc']), bin_value
                    )
                
                # Si no se encontró y no hay BIN, intentar buscar por id
                if not producto_existente and 'id' in datos_producto and datos_producto['id'] != "N/D":
                    try:
                        producto_existente = self.inventario.obtener_producto(int(datos_producto['id']))
                    except (ValueError, TypeError):
                        pass
                
                if producto_existente:
                    # Actualizar producto existente
                    self._actualizar_producto_existente(producto_existente, datos_producto, mapeo)
                    productos_actualizados += 1
                else:
                    # Crear nuevo producto
                    nuevo_producto = self._crear_nuevo_producto(datos_producto, mapeo)
                    if self.inventario.agregar_producto(nuevo_producto):
                        productos_agregados += 1
                    else:
                        errores.append(f"Fila {idx + 2}: No se pudo agregar el producto")
                        
            except Exception as e:
                errores.append(f"Fila {idx + 2}: {str(e)}")
        
        # Preparar mensaje final
        mensaje = f"Proceso completado:\n\n"
        mensaje += f"✓ Productos agregados: {productos_agregados}\n"
        mensaje += f"✓ Productos actualizados: {productos_actualizados}\n"
        
        if errores:
            mensaje += f"\n⚠ Errores encontrados: {len(errores)}\n"
            mensaje += "\n".join(errores[:5])  # Mostrar solo los primeros 5 errores
            if len(errores) > 5:
                mensaje += f"\n... y {len(errores) - 5} errores más"
        
        return True, mensaje
    
    def _actualizar_producto_existente(self, producto: Producto, datos: dict, mapeo: dict):
        """Actualiza un producto existente con los datos del Excel."""
        # Actualizar solo los atributos que fueron mapeados
        if 'nombre' in mapeo and 'nombre' in datos and datos['nombre'] != "N/D":
            producto.nombre = str(datos['nombre'])
        
        if 'precio' in mapeo and 'precio' in datos and datos['precio'] != "N/D":
            try:
                producto.precio = float(datos['precio'])
            except (ValueError, TypeError):
                pass
        
        if 'stock_actual' in mapeo and 'stock_actual' in datos and datos['stock_actual'] != "N/D":
            try:
                producto.stock_actual = int(datos['stock_actual'])
            except (ValueError, TypeError):
                pass
        
        if 'stock_minimo' in mapeo and 'stock_minimo' in datos and datos['stock_minimo'] != "N/D":
            try:
                producto.stock_minimo = int(datos['stock_minimo'])
            except (ValueError, TypeError):
                pass
        
        if 'stock_maximo' in mapeo and 'stock_maximo' in datos and datos['stock_maximo'] != "N/D":
            try:
                producto.stock_maximo = int(datos['stock_maximo'])
            except (ValueError, TypeError):
                pass
        
        if 'categoria' in mapeo and 'categoria' in datos and datos['categoria'] != "N/D":
            producto.categoria = str(datos['categoria'])
        
        if 'numero_item' in mapeo and 'numero_item' in datos and datos['numero_item'] != "N/D":
            producto.numero_item = str(datos['numero_item'])
        
        if 'codigo_upc' in mapeo and 'codigo_upc' in datos and datos['codigo_upc'] != "N/D":
            producto.codigo_upc = str(datos['codigo_upc'])
        
        if 'bin' in mapeo and 'bin' in datos and datos['bin'] != "N/D":
            producto.bin = str(datos['bin'])
        
        # Invalidar caché del inventario
        self.inventario.notificar_cambio_stock()
    
    def _crear_nuevo_producto(self, datos: dict, mapeo: dict) -> Producto:
        """Crea un nuevo producto con los datos del Excel."""
        # Generar un ID único si no se proporcionó
        if 'id' not in datos or datos['id'] == "N/D":
            # Generar ID basado en el máximo ID actual + 1
            max_id = max([p.id for p in self.inventario.productos.values()], default=0)
            producto_id = max_id + 1
        else:
            try:
                producto_id = int(datos['id'])
            except (ValueError, TypeError):
                max_id = max([p.id for p in self.inventario.productos.values()], default=0)
                producto_id = max_id + 1
        
        # Extraer valores con valores por defecto
        nombre = str(datos.get('nombre', 'N/D')) if datos.get('nombre') != "N/D" else "N/D"
        
        try:
            precio = float(datos.get('precio', 0.0)) if datos.get('precio') != "N/D" else 0.0
        except (ValueError, TypeError):
            precio = 0.0
        
        try:
            stock_actual = int(datos.get('stock_actual', 0)) if datos.get('stock_actual') != "N/D" else 0
        except (ValueError, TypeError):
            stock_actual = 0
        
        try:
            stock_minimo = int(datos.get('stock_minimo', 10)) if datos.get('stock_minimo') != "N/D" else 10
        except (ValueError, TypeError):
            stock_minimo = 10
        
        try:
            stock_maximo = int(datos.get('stock_maximo', 100)) if datos.get('stock_maximo') != "N/D" else 100
        except (ValueError, TypeError):
            stock_maximo = 100
        
        categoria = str(datos.get('categoria', 'N/D')) if datos.get('categoria') != "N/D" else "N/D"
        numero_item = str(datos.get('numero_item', 'N/D')) if datos.get('numero_item') != "N/D" else "N/D"
        codigo_upc = str(datos.get('codigo_upc', 'N/D')) if datos.get('codigo_upc') != "N/D" else "N/D"
        bin_location = str(datos.get('bin', 'N/D')) if datos.get('bin') != "N/D" else "N/D"
        
        return Producto(
            id=producto_id,
            nombre=nombre,
            precio=precio,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            categoria=categoria,
            numero_item=numero_item,
            codigo_upc=codigo_upc,
            bin=bin_location
        )
    
    def ver_productos(self):
        """Muestra todos los productos del inventario agrupados por item."""
        self.texto_contenido.delete(1.0, tk.END)
        
        if not self.inventario.productos:
            self.texto_contenido.insert(1.0, "No hay productos en el inventario.")
            return
        
        # Obtener productos agrupados
        agrupados = self.inventario.obtener_productos_agrupados()
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     LISTA DE PRODUCTOS                            ║
║            (Agrupados por Item con Stock por Bodega)              ║
╚═══════════════════════════════════════════════════════════════════╝

"""
        for identificador, productos in agrupados.items():
            # Obtener información del primer producto (datos comunes)
            primer_producto = productos[0]
            
            # Calcular stock total
            stock_total = sum(p.stock_actual for p in productos)
            
            contenido += f"\n{'═' * 70}\n"
            contenido += f"📦 {primer_producto.nombre} (Núm. Item: {primer_producto.numero_item})\n"
            contenido += f"   UPC: {primer_producto.codigo_upc} | Precio: ${primer_producto.precio:.2f}\n"
            contenido += f"   Categoría: {primer_producto.categoria}\n"
            contenido += f"   📊 STOCK TOTAL: {stock_total} unidades\n"
            contenido += f"\n   Desglose por Bodega (BIN):\n"
            
            for producto in productos:
                estado = "⚠️" if producto.necesita_reabastecimiento() else "✓"
                contenido += f"     {estado} BIN {producto.bin}: {producto.stock_actual} unidades "
                contenido += f"(ID: {producto.id}, Min: {producto.stock_minimo}, Max: {producto.stock_maximo})\n"
            
            contenido += f"{'─' * 70}\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def ver_matriz(self):
        """Muestra la representación matricial del inventario."""
        self.texto_contenido.delete(1.0, tk.END)
        
        matriz = self.inventario.obtener_matriz_inventario()
        
        if matriz.size == 0:
            self.texto_contenido.insert(1.0, "No hay productos en el inventario.")
            return
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     MATRIZ DE INVENTARIO                          ║
╚═══════════════════════════════════════════════════════════════════╝

Representación matricial I (n × 5):
Columnas: [ID, Precio, Stock, Mínimo, Máximo]

"""
        # Crear tabla formateada
        encabezados = ["ID", "Precio", "Stock", "Mínimo", "Máximo"]
        contenido += f"{'Fila':>5} | " + " | ".join(f"{h:>10}" for h in encabezados) + "\n"
        contenido += "─" * 70 + "\n"
        
        for i, fila in enumerate(matriz):
            contenido += f"{i:>5} | " + " | ".join(f"{v:>10.2f}" for v in fila) + "\n"
        
        contenido += f"\n\nDimensiones de la matriz: {matriz.shape}\n"
        contenido += f"Tipo de datos: {matriz.dtype}\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def ver_alertas(self):
        """Muestra los productos que necesitan reabastecimiento."""
        self.texto_contenido.delete(1.0, tk.END)
        
        vector_alertas = self.operaciones.calcular_alertas_stock_bajo()
        productos_alerta = self.operaciones.obtener_productos_alerta()
        sugerencias = self.operaciones.calcular_cantidad_reabastecimiento()
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     ALERTAS DE STOCK BAJO                         ║
╚═══════════════════════════════════════════════════════════════════╝

"""
        contenido += f"Vector de alertas (booleano): {vector_alertas}\n"
        contenido += f"Total de alertas: {np.sum(vector_alertas)}\n\n"
        
        if not productos_alerta:
            contenido += "✓ Todos los productos tienen stock suficiente.\n"
        else:
            contenido += "⚠️  PRODUCTOS QUE REQUIEREN REABASTECIMIENTO:\n"
            contenido += "─" * 70 + "\n\n"
            
            productos_lista = self.inventario.listar_productos()
            for i, producto in enumerate(productos_lista):
                if vector_alertas[i]:
                    contenido += f"• {producto.nombre} (ID: {producto.id})\n"
                    contenido += f"  Stock actual: {producto.stock_actual}\n"
                    contenido += f"  Stock mínimo: {producto.stock_minimo}\n"
                    contenido += f"  Sugerencia de compra: {sugerencias[i]} unidades\n\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def registrar_entrada(self):
        """Abre un diálogo para registrar entrada de productos."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Registrar Entrada de Productos")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ID del producto
        ttk.Label(frame, text="ID del Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_entry = ttk.Entry(frame, width=30)
        id_entry.grid(row=0, column=1, pady=5)
        
        # Cantidad
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cantidad_entry = ttk.Entry(frame, width=30)
        cantidad_entry.grid(row=1, column=1, pady=5)
        
        def confirmar():
            try:
                producto_id = int(id_entry.get())
                cantidad = int(cantidad_entry.get())
                
                exito, mensaje = self.operaciones.registrar_entrada(producto_id, cantidad)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    dialog.destroy()
                    self.actualizar_vista_productos()
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Confirmar", command=confirmar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def registrar_salida(self):
        """Abre un diálogo para registrar salida de productos."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Registrar Salida de Productos")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ID del producto
        ttk.Label(frame, text="ID del Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_entry = ttk.Entry(frame, width=30)
        id_entry.grid(row=0, column=1, pady=5)
        
        # Cantidad
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cantidad_entry = ttk.Entry(frame, width=30)
        cantidad_entry.grid(row=1, column=1, pady=5)
        
        def confirmar():
            try:
                producto_id = int(id_entry.get())
                cantidad = int(cantidad_entry.get())
                
                exito, mensaje = self.operaciones.registrar_salida(producto_id, cantidad)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    dialog.destroy()
                    self.actualizar_vista_productos()
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Confirmar", command=confirmar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def ver_estadisticas(self):
        """Muestra estadísticas del inventario."""
        self.texto_contenido.delete(1.0, tk.END)
        
        stats = self.operaciones.calcular_estadisticas()
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     ESTADÍSTICAS DEL INVENTARIO                   ║
╚═══════════════════════════════════════════════════════════════════╝

📊 MÉTRICAS CALCULADAS MEDIANTE ÁLGEBRA LINEAL:

"""
        contenido += f"  Total de productos:        {stats['total_productos']}\n"
        contenido += f"  Total de unidades:         {stats['total_unidades']}\n"
        contenido += f"  Valor total:               ${stats['valor_total']:,.2f}\n"
        contenido += f"  Productos con alerta:      {stats['productos_alerta']}\n"
        contenido += f"  Porcentaje con alerta:     {stats['porcentaje_alerta']:.1f}%\n"
        contenido += f"  Stock promedio:            {stats['stock_promedio']:.1f} unidades\n"
        contenido += f"  Precio promedio:           ${stats['precio_promedio']:.2f}\n"
        contenido += f"  Valor promedio por prod.:  ${stats['valor_promedio']:.2f}\n"
        
        contenido += "\n\n📐 VECTORES EXTRAÍDOS DE LA MATRIZ:\n\n"
        contenido += f"  Vector de stock:   {self.operaciones.obtener_vector_stock()}\n"
        contenido += f"  Vector de precios: {self.operaciones.obtener_vector_precios()}\n"
        contenido += f"  Vector de valores: {self.operaciones.calcular_vector_valores()}\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def ver_reporte(self):
        """Muestra el reporte completo como DataFrame."""
        self.texto_contenido.delete(1.0, tk.END)
        
        df = self.operaciones.generar_reporte_dataframe()
        
        if df.empty:
            self.texto_contenido.insert(1.0, "No hay datos para mostrar.")
            return
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     REPORTE COMPLETO (DataFrame)                  ║
╚═══════════════════════════════════════════════════════════════════╝

"""
        contenido += df.to_string(index=False)
        contenido += "\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def ver_analisis_categoria(self):
        """Muestra el análisis agrupado por categoría."""
        self.texto_contenido.delete(1.0, tk.END)
        
        df = self.operaciones.analisis_por_categoria()
        
        if df.empty:
            self.texto_contenido.insert(1.0, "No hay datos para mostrar.")
            return
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     ANÁLISIS POR CATEGORÍA                        ║
╚═══════════════════════════════════════════════════════════════════╝

"""
        contenido += df.to_string()
        contenido += "\n"
        
        self.texto_contenido.insert(1.0, contenido)
    
    def agregar_producto(self):
        """Abre un diálogo para agregar un nuevo producto."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Producto")
        dialog.geometry("450x550")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos del formulario
        campos = [
            ("ID del Producto:", "id"),
            ("Número Item (6 dígitos):", "numero_item"),
            ("Código UPC:", "codigo_upc"),
            ("BIN (Ej: 001/020/006):", "bin"),
            ("Nombre:", "nombre"),
            ("Precio:", "precio"),
            ("Stock Actual:", "stock"),
            ("Stock Mínimo:", "minimo"),
            ("Stock Máximo:", "maximo"),
            ("Categoría:", "categoria"),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entries[key] = entry
        
        def confirmar():
            try:
                producto_id = int(entries['id'].get())
                numero_item = entries['numero_item'].get().strip() or "N/D"
                codigo_upc = entries['codigo_upc'].get().strip() or "N/D"
                bin_location = entries['bin'].get().strip() or "N/D"
                nombre = entries['nombre'].get()
                precio = float(entries['precio'].get())
                stock = int(entries['stock'].get())
                minimo = int(entries['minimo'].get())
                maximo = int(entries['maximo'].get())
                categoria = entries['categoria'].get()
                
                producto = Producto(producto_id, nombre, precio, stock, minimo, maximo, 
                                  categoria, numero_item, codigo_upc, bin_location)
                
                if self.inventario.agregar_producto(producto):
                    messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado exitosamente en BIN {bin_location}.")
                    dialog.destroy()
                    self.actualizar_vista_productos()
                else:
                    messagebox.showerror("Error", f"Ya existe un producto con ID {producto_id}.")
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Confirmar", command=confirmar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def modificar_producto(self):
        """Abre un diálogo para buscar y modificar un producto existente."""
        # Primer diálogo: seleccionar método de búsqueda
        dialog_busqueda = tk.Toplevel(self.root)
        dialog_busqueda.title("Buscar Producto para Modificar")
        dialog_busqueda.geometry("450x300")
        dialog_busqueda.transient(self.root)
        dialog_busqueda.grab_set()
        
        # Centrar el diálogo
        dialog_busqueda.update_idletasks()
        x = (dialog_busqueda.winfo_screenwidth() // 2) - (dialog_busqueda.winfo_width() // 2)
        y = (dialog_busqueda.winfo_screenheight() // 2) - (dialog_busqueda.winfo_height() // 2)
        dialog_busqueda.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog_busqueda, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(frame, text="Buscar Producto", style='Subtitle.TLabel').grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )
        
        # Método de búsqueda
        ttk.Label(frame, text="Buscar por:").grid(row=1, column=0, sticky=tk.W, pady=5)
        metodo_var = tk.StringVar(value="id")
        
        metodos_frame = ttk.Frame(frame)
        metodos_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(metodos_frame, text="ID", variable=metodo_var, value="id").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(metodos_frame, text="Número Item", variable=metodo_var, value="numero_item").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(metodos_frame, text="Código UPC", variable=metodo_var, value="codigo_upc").pack(side=tk.LEFT, padx=5)
        
        # Campo de búsqueda
        ttk.Label(frame, text="Valor:").grid(row=2, column=0, sticky=tk.W, pady=5)
        busqueda_entry = ttk.Entry(frame, width=30)
        busqueda_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Información
        info_label = ttk.Label(
            frame,
            text="Ingrese el valor del identificador para buscar el producto.",
            font=('Segoe UI', 9, 'italic'),
            foreground='#666'
        )
        info_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        def buscar_y_modificar():
            """Busca el producto y abre el diálogo de modificación."""
            metodo = metodo_var.get()
            valor = busqueda_entry.get().strip()
            
            if not valor:
                messagebox.showerror("Error", "Debe ingresar un valor para buscar.")
                return
            
            # Buscar el producto según el método seleccionado
            producto = None
            
            if metodo == "id":
                try:
                    producto_id = int(valor)
                    producto = self.inventario.obtener_producto(producto_id)
                except ValueError:
                    messagebox.showerror("Error", "El ID debe ser un número entero.")
                    return
            elif metodo == "numero_item":
                producto = self.inventario.obtener_producto_por_numero_item(valor)
            elif metodo == "codigo_upc":
                producto = self.inventario.obtener_producto_por_codigo_upc(valor)
            
            if producto is None:
                messagebox.showerror(
                    "Producto no encontrado",
                    f"No se encontró ningún producto con {metodo.replace('_', ' ').title()}: {valor}"
                )
                return
            
            # Cerrar diálogo de búsqueda y abrir diálogo de modificación
            dialog_busqueda.destroy()
            self.abrir_dialogo_modificacion(producto)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Buscar", command=buscar_y_modificar, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog_busqueda.destroy).pack(side=tk.LEFT, padx=5)
    
    def abrir_dialogo_modificacion(self, producto: Producto):
        """Abre el diálogo para modificar los atributos de un producto."""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Modificar Producto - {producto.nombre}")
        dialog.geometry("550x780")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        
        # Título
        ttk.Label(
            main_frame,
            text=f"Modificar Producto",
            style='Subtitle.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Información del producto actual
        info_frame = ttk.LabelFrame(main_frame, text="  Datos Actuales  ", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_text = f"""ID: {producto.id}
Número Item: {producto.numero_item}
Código UPC: {producto.codigo_upc}
BIN: {producto.bin}
Nombre: {producto.nombre}
Precio: ${producto.precio:.2f}
Stock Actual: {producto.stock_actual}
Stock Mínimo: {producto.stock_minimo}
Stock Máximo: {producto.stock_maximo}
Categoría: {producto.categoria}"""
        
        ttk.Label(info_frame, text=info_text, font=('Consolas', 9)).pack(anchor=tk.W)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Título para nuevos valores
        ttk.Label(
            main_frame,
            text="Nuevos Valores (deje en blanco para mantener el valor actual):",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Campos editables
        campos = [
            ("ID del Producto:", "id", str(producto.id)),
            ("Número Item (6 dígitos):", "numero_item", producto.numero_item),
            ("Código UPC:", "codigo_upc", producto.codigo_upc),
            ("BIN (Ej: 001/020/006):", "bin", producto.bin),
            ("Nombre:", "nombre", producto.nombre),
            ("Precio:", "precio", str(producto.precio)),
            ("Stock Actual:", "stock", str(producto.stock_actual)),
            ("Stock Mínimo:", "minimo", str(producto.stock_minimo)),
            ("Stock Máximo:", "maximo", str(producto.stock_maximo)),
            ("Categoría:", "categoria", producto.categoria),
        ]
        
        entries = {}
        row_offset = 4
        
        for i, (label, key, valor_actual) in enumerate(campos):
            ttk.Label(main_frame, text=label).grid(
                row=row_offset + i, column=0, sticky=tk.W, pady=5
            )
            entry = ttk.Entry(main_frame, width=35)
            entry.grid(row=row_offset + i, column=1, pady=5, sticky=(tk.W, tk.E))
            entry.insert(0, valor_actual)  # Pre-llenar con valor actual
            entries[key] = entry
        
        # Nota informativa
        nota_frame = ttk.Frame(main_frame)
        nota_frame.grid(row=row_offset + len(campos), column=0, columnspan=2, pady=15)
        
        ttk.Label(
            nota_frame,
            text="💡 Los campos están pre-llenados con los valores actuales.\nModifique solo los que desee cambiar.",
            font=('Segoe UI', 9, 'italic'),
            foreground='#2196F3'
        ).pack()
        
        def confirmar_modificacion():
            """Aplica las modificaciones al producto."""
            try:
                # Obtener valores (mantener originales si el campo está vacío)
                nuevo_id = int(entries['id'].get().strip() or producto.id)
                nuevo_numero_item = entries['numero_item'].get().strip() or producto.numero_item
                nuevo_codigo_upc = entries['codigo_upc'].get().strip() or producto.codigo_upc
                nuevo_bin = entries['bin'].get().strip() or producto.bin
                nuevo_nombre = entries['nombre'].get().strip() or producto.nombre
                nuevo_precio = float(entries['precio'].get().strip() or producto.precio)
                nuevo_stock = int(entries['stock'].get().strip() or producto.stock_actual)
                nuevo_minimo = int(entries['minimo'].get().strip() or producto.stock_minimo)
                nuevo_maximo = int(entries['maximo'].get().strip() or producto.stock_maximo)
                nueva_categoria = entries['categoria'].get().strip() or producto.categoria
                
                # Validar que el stock no sea negativo
                if nuevo_stock < 0:
                    messagebox.showerror("Error", "El stock no puede ser negativo.")
                    return
                
                # Si se cambió el ID, verificar que no exista otro producto con ese ID
                if nuevo_id != producto.id and self.inventario.obtener_producto(nuevo_id) is not None:
                    messagebox.showerror(
                        "Error",
                        f"Ya existe un producto con ID {nuevo_id}.\nNo se puede cambiar el ID a uno existente."
                    )
                    return
                
                # Aplicar cambios
                # Si cambió el ID, necesitamos eliminar el antiguo y crear uno nuevo
                if nuevo_id != producto.id:
                    self.inventario.eliminar_producto(producto.id)
                    producto.id = nuevo_id
                    self.inventario.productos[nuevo_id] = producto
                
                # Actualizar atributos
                producto.numero_item = nuevo_numero_item
                producto.codigo_upc = nuevo_codigo_upc
                producto.bin = nuevo_bin
                producto.nombre = nuevo_nombre
                producto.precio = nuevo_precio
                producto.stock_actual = nuevo_stock
                producto.stock_minimo = nuevo_minimo
                producto.stock_maximo = nuevo_maximo
                producto.categoria = nueva_categoria
                
                # Invalidar caché
                self.inventario._invalidar_cache()
                
                messagebox.showinfo(
                    "Éxito",
                    f"Producto '{producto.nombre}' modificado exitosamente."
                )
                dialog.destroy()
                self.actualizar_vista_productos()
                self.ver_productos()
                
            except ValueError as e:
                messagebox.showerror(
                    "Error de Validación",
                    f"Datos inválidos. Verifique que:\n" +
                    f"- ID sea un número entero\n" +
                    f"- Precio sea un número decimal\n" +
                    f"- Stock, Mínimo y Máximo sean números enteros\n\n" +
                    f"Error: {str(e)}"
                )
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row_offset + len(campos) + 1, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame,
            text="💾 Guardar Cambios",
            command=confirmar_modificacion,
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="❌ Cancelar",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def salir(self):
        """Cierra la aplicación."""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.quit()


def main():
    """Función principal de entrada."""
    root = tk.Tk()
    app = SistemaInventarioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
