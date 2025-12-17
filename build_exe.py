"""
Script para construir el ejecutable del Sistema de Gestión de Inventario Inteligente.
Usa PyInstaller para crear un ejecutable standalone de Windows.
"""

import PyInstaller.__main__
import os

# Obtener directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir el ejecutable
PyInstaller.__main__.run([
    'gui.py',                           # Script principal
    '--name=GestionInventario',         # Nombre del ejecutable
    '--onefile',                        # Un solo archivo ejecutable
    '--windowed',                       # Sin ventana de consola
    '--icon=c:\\Users\\Walther\\Downloads\\inventario.ico',  # Icono personalizado
    '--add-data=models;models',         # Incluir carpeta models
    '--add-data=logic;logic',           # Incluir carpeta logic
    '--hidden-import=pandas',           # Importación oculta de pandas
    '--hidden-import=numpy',            # Importación oculta de numpy
    '--hidden-import=openpyxl',         # Importación oculta de openpyxl
    '--hidden-import=tkinter',          # Importación oculta de tkinter
    '--hidden-import=tkinter.ttk',      # Importación oculta de ttk
    '--hidden-import=tkinter.messagebox',  # Importación oculta de messagebox
    '--hidden-import=tkinter.filedialog',  # Importación oculta de filedialog
    '--collect-all=pandas',             # Recolectar todos los archivos de pandas
    '--collect-all=openpyxl',           # Recolectar todos los archivos de openpyxl
    '--noconfirm',                      # Sobrescribir sin confirmar
    '--clean',                          # Limpiar caché y archivos temporales
])

print("\n" + "="*80)
print("✅ EJECUTABLE CREADO EXITOSAMENTE")
print("="*80)
print(f"\n📁 Ubicación: {os.path.join(current_dir, 'dist', 'GestionInventario.exe')}")
print("\n🎯 Para ejecutar:")
print("   1. Navega a la carpeta 'dist'")
print("   2. Ejecuta 'GestionInventario.exe'")
print("\n⚠️ Notas importantes:")
print("   • El ejecutable es standalone (no requiere Python instalado)")
print("   • Incluye todas las dependencias necesarias")
print("   • Puede tardar unos segundos en iniciar la primera vez")
print("   • Para cargar Excel, debe estar en formato .xlsx o .xls")
print("\n" + "="*80)
