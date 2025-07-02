import tkinter as tk
from tkinter import ttk, messagebox

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x200")
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Widgets
        ttk.Label(self.root, text="Usuario:").pack(pady=5)
        self.usuario_entry = ttk.Entry(self.root)
        self.usuario_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(
            self.root, 
            text="Iniciar Sesión",
            command=self.validar_login
        ).pack(pady=10)
        
        ttk.Button(
            self.root, 
            text="Registrarse",
            command=self.abrir_registro
        ).pack(pady=5)
    
    def validar_login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        
        # Credenciales de prueba
        if usuario == "admin" and password == "123":
            self.root.destroy()  # Cierra la ventana de login
            app = MainApp()     # Abre la aplicación principal
            app.run()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def abrir_registro(self):
        RegistroApp(self.root)
    
    def run(self):
        self.root.mainloop()

class RegistroApp:
    def __init__(self, ventana_padre):
        self.ventana = tk.Toplevel(ventana_padre)
        self.ventana.title("Registro")
        self.ventana.geometry("300x250")
        
        # Widgets
        ttk.Label(self.ventana, text="Nombre:").pack(pady=5)
        self.nombre_entry = ttk.Entry(self.ventana)
        self.nombre_entry.pack(pady=5)
        
        ttk.Label(self.ventana, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self.ventana)
        self.email_entry.pack(pady=5)
        
        ttk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self.ventana, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(
            self.ventana, 
            text="Guardar",
            command=self.guardar_registro
        ).pack(pady=20)
    
    def guardar_registro(self):
        # Aquí iría la lógica para guardar en la base de datos
        messagebox.showinfo("Éxito", "Registro guardado (simulado)")
        self.ventana.destroy()

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión")
        self.root.geometry("800x600")
        
        # Datos simulados (en una app real vendrían de una BD)
        self.datos = [
            {"id": 1, "nombre": "Producto 1", "precio": 100, "stock": 10},
            {"id": 2, "nombre": "Producto 2", "precio": 200, "stock": 5},
            {"id": 3, "nombre": "Producto 3", "precio": 150, "stock": 8},
            {"id": 4, "nombre": "Producto 4", "precio": 300, "stock": 3},
            {"id": 5, "nombre": "Producto 5", "precio": 250, "stock": 7},
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame para la barra de búsqueda
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(
            search_frame, 
            text="Buscar",
            command=self.buscar_datos
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame para los botones de acción
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Button(
            button_frame, 
            text="Agregar",
            command=self.agregar_item
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Modificar",
            command=self.modificar_item
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Eliminar",
            command=self.eliminar_item
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar los datos
        self.tree = ttk.Treeview(
            self.root, 
            columns=("id", "nombre", "precio", "stock"), 
            show="headings"
        )
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=200)
        self.tree.column("precio", width=100)
        self.tree.column("stock", width=100)
        
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Cargar datos iniciales
        self.actualizar_lista()
    
    def actualizar_lista(self, datos=None):
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar los datos
        data = datos if datos else self.datos
        for item in data:
            self.tree.insert("", tk.END, values=(
                item["id"], 
                item["nombre"], 
                f"${item['precio']}", 
                item["stock"]
            ))
    
    def buscar_datos(self):
        texto_busqueda = self.search_entry.get().lower()
        if not texto_busqueda:
            self.actualizar_lista()
            return
        
        resultados = [
            item for item in self.datos 
            if texto_busqueda in item["nombre"].lower()
        ]
        self.actualizar_lista(resultados)
    
    def agregar_item(self):
        # Crear ventana de diálogo para agregar
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Producto")
        dialog.geometry("300x250")
        
        # Widgets
        ttk.Label(dialog, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(dialog)
        nombre_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Precio:").pack(pady=5)
        precio_entry = ttk.Entry(dialog)
        precio_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.pack(pady=5)
        
        def guardar():
            # Validar y guardar el nuevo item
            try:
                nuevo_id = max(item["id"] for item in self.datos) + 1
                nuevo_item = {
                    "id": nuevo_id,
                    "nombre": nombre_entry.get(),
                    "precio": float(precio_entry.get()),
                    "stock": int(stock_entry.get())
                }
                self.datos.append(nuevo_item)
                self.actualizar_lista()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")
        
        ttk.Button(
            dialog, 
            text="Guardar",
            command=guardar
        ).pack(pady=20)
    
    def modificar_item(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un item para modificar")
            return
        
        # Obtener datos del item seleccionado
        item_id = self.tree.item(seleccion[0])["values"][0]
        item = next((x for x in self.datos if x["id"] == item_id), None)
        
        if not item:
            return
        
        # Crear ventana de diálogo para modificar
        dialog = tk.Toplevel(self.root)
        dialog.title("Modificar Producto")
        dialog.geometry("300x250")
        
        # Widgets con valores actuales
        ttk.Label(dialog, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(dialog)
        nombre_entry.insert(0, item["nombre"])
        nombre_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Precio:").pack(pady=5)
        precio_entry = ttk.Entry(dialog)
        precio_entry.insert(0, str(item["precio"]))
        precio_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.insert(0, str(item["stock"]))
        stock_entry.pack(pady=5)
        
        def actualizar():
            # Validar y actualizar el item
            try:
                item["nombre"] = nombre_entry.get()
                item["precio"] = float(precio_entry.get())
                item["stock"] = int(stock_entry.get())
                self.actualizar_lista()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Producto modificado correctamente")
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")
        
        ttk.Button(
            dialog, 
            text="Actualizar",
            command=actualizar
        ).pack(pady=20)
    
    def eliminar_item(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un item para eliminar")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este item?"):
            return
        
        # Obtener y eliminar el item
        item_id = self.tree.item(seleccion[0])["values"][0]
        self.datos = [x for x in self.datos if x["id"] != item_id]
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()