import tkinter as tk
from tkinter import ttk, messagebox

def cerrar_aplicacion(ventana_lista, ventana_login):
    ventana_lista.destroy()
    ventana_login.destroy()

def mostrar_lista(ventana_login):
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Items")
    ventana_lista.geometry("600x400")
    
    # Configura el cierre para terminar la aplicación
    ventana_lista.protocol("WM_DELETE_WINDOW", 
                          lambda: cerrar_aplicacion(ventana_lista, ventana_login))
    
    frame = ttk.Frame(ventana_lista, padding=20)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Barra de búsqueda
    ttk.Label(frame, text="Buscar:").pack(pady=5)
    entry_busqueda = ttk.Entry(frame, width=40)
    entry_busqueda.pack(pady=5)
    
    # Lista (Treeview)
    columnas = ("ID", "Nombre", "Categoría")
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    # Datos de ejemplo
    items = [
        ("1", "Laptop", "Electrónicos"),
        ("2", "Libro", "Educación"),
        ("3", "Mouse", "Electrónicos")
    ]
    
    for item in items:
        tree.insert("", tk.END, values=item)
    
    tree.pack(pady=10, fill=tk.BOTH, expand=True)
    
    # Frame para botones
    frame_botones = ttk.Frame(frame)
    frame_botones.pack(pady=10)
    
    btn_agregar = ttk.Button(frame_botones, text="Agregar", 
                            command=lambda: agregar_item(tree))
    btn_agregar.pack(side=tk.LEFT, padx=5)
    
    btn_borrar = ttk.Button(frame_botones, text="Borrar", 
                           command=lambda: borrar_item(tree))
    btn_borrar.pack(side=tk.LEFT, padx=5)

# Funciones para los botones (pendientes de implementar)
def agregar_item(tree):
    messagebox.showinfo("Agregar", "Aquí irá la lógica para agregar ítems a la lista")

def borrar_item(tree):
    seleccionado = tree.selection()
    if seleccionado:
        tree.delete(seleccionado)
    else:
        messagebox.showwarning("Advertencia", "Selecciona un ítem para borrar")