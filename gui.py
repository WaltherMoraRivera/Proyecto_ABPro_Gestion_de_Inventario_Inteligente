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
from typing import Optional
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
            Producto(1, "Laptop HP 15", 899.99, 15, 5, 50, "Electrónica"),
            Producto(2, "Mouse Inalámbrico", 29.99, 45, 20, 100, "Accesorios"),
            Producto(3, "Teclado Mecánico", 79.99, 8, 10, 40, "Accesorios"),
            Producto(4, "Monitor 24\" LG", 249.99, 12, 5, 30, "Electrónica"),
            Producto(5, "Cable HDMI 2m", 14.99, 3, 30, 200, "Accesorios"),
            Producto(6, "Disco SSD 500GB", 69.99, 25, 15, 60, "Almacenamiento"),
            Producto(7, "Memoria USB 64GB", 12.99, 50, 25, 150, "Almacenamiento"),
            Producto(8, "Webcam HD", 49.99, 18, 10, 40, "Accesorios"),
            Producto(9, "Audífonos Bluetooth", 59.99, 22, 15, 50, "Audio"),
            Producto(10, "Cargador Universal", 24.99, 30, 20, 80, "Accesorios"),
        ]
        
        for producto in productos_ejemplo:
            self.inventario.agregar_producto(producto)
    
    def actualizar_vista_productos(self):
        """Actualiza la vista después de cambios en el inventario."""
        # Este método puede ser llamado para refrescar la vista actual
        pass
    
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
            
            # Mostrar información sobre el archivo cargado
            mensaje = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                     ARCHIVO EXCEL CARGADO                         ║
╚═══════════════════════════════════════════════════════════════════╝

📄 Archivo: {archivo.split('/')[-1]}
📊 Filas: {len(df)}
📋 Columnas: {', '.join(df.columns.tolist())}

Vista previa de los datos:
{df.head(10).to_string()}

═══════════════════════════════════════════════════════════════════

⚠️ NOTA: La funcionalidad de mapeo de columnas y carga automática
         del inventario se implementará según tus especificaciones.
         
Por ahora, el archivo ha sido leído correctamente y está listo
para ser procesado.

"""
            self.texto_contenido.delete(1.0, tk.END)
            self.texto_contenido.insert(1.0, mensaje)
            
            messagebox.showinfo(
                "Excel Cargado",
                f"Archivo cargado exitosamente.\n\n"
                f"Filas: {len(df)}\n"
                f"Columnas: {len(df.columns)}\n\n"
                f"Revise el área de trabajo para ver los detalles."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error al cargar Excel",
                f"No se pudo cargar el archivo:\n\n{str(e)}"
            )
    
    def ver_productos(self):
        """Muestra todos los productos del inventario."""
        self.texto_contenido.delete(1.0, tk.END)
        
        if not self.inventario.productos:
            self.texto_contenido.insert(1.0, "No hay productos en el inventario.")
            return
        
        contenido = """
╔═══════════════════════════════════════════════════════════════════╗
║                     LISTA DE PRODUCTOS                            ║
╚═══════════════════════════════════════════════════════════════════╝

"""
        for producto in self.inventario:
            contenido += f"\n{str(producto)}\n{'─' * 70}\n"
        
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
        dialog.geometry("450x400")
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
            ("Nombre:", "nombre"),
            ("Precio:", "precio"),
            ("Stock Inicial:", "stock"),
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
                nombre = entries['nombre'].get()
                precio = float(entries['precio'].get())
                stock = int(entries['stock'].get())
                minimo = int(entries['minimo'].get())
                maximo = int(entries['maximo'].get())
                categoria = entries['categoria'].get()
                
                producto = Producto(producto_id, nombre, precio, stock, minimo, maximo, categoria)
                
                if self.inventario.agregar_producto(producto):
                    messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado exitosamente.")
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
