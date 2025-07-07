import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import crear_conexion, verificar_estructura

class LoginApp:
    def __init__(self):
        # Verificar estructura de la BD al iniciar
        if not verificar_estructura():
            messagebox.showerror("Error", "La estructura de la base de datos no es válida")
            return
            
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x200")
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Widgets
        ttk.Label(self.root, text="Email:").pack(pady=5)  # Cambiado a Email para coincidir con BD
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        # Frame para los botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame, 
            text="Iniciar Sesión",
            command=self.validar_login
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Registrarse",
            command=self.abrir_ventana_registro
        ).pack(side=tk.LEFT, padx=5)
    
    def validar_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, Nombre_usuario FROM usuario WHERE Email = ? AND Contraseña = ?",
                    (email, password)
                )
                usuario = cursor.fetchone()
                
                if usuario:
                    self.root.destroy()
                    MainApp(usuario['id']).run()  # Pasamos el ID del usuario
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
    
    def abrir_ventana_registro(self):
        VentanaRegistro(self.root)
    
    def run(self):
        self.root.mainloop()

class VentanaRegistro:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro")
        self.ventana.geometry("350x250")
        
        # Campos del formulario
        ttk.Label(self.ventana, text="Nombre:").pack(pady=5)
        self.nombre_entry = ttk.Entry(self.ventana)
        self.nombre_entry.pack(pady=5, fill=tk.X, padx=10)
        
        ttk.Label(self.ventana, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self.ventana)
        self.email_entry.pack(pady=5, fill=tk.X, padx=10)
        
        ttk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self.ventana, show="*")
        self.password_entry.pack(pady=5, fill=tk.X, padx=10)
        
        ttk.Label(self.ventana, text="Confirmar Contraseña:").pack(pady=5)
        self.confirm_password_entry = ttk.Entry(self.ventana, show="*")
        self.confirm_password_entry.pack(pady=5, fill=tk.X, padx=10)
        
        # Botones
        btn_frame = ttk.Frame(self.ventana)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Registrar",
            command=self.registrar_usuario
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Cancelar",
            command=self.ventana.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def registrar_usuario(self):
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validaciones básicas
        if not all([nombre, email, password, confirm_password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuario (Nombre_usuario, Email, Contraseña) VALUES (?, ?, ?)",
                    (nombre, email, password)
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.ventana.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El email ya está registrado")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")

class MainApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión")
        self.root.geometry("1000x600")
        
        # Configurar interfaz
        self.setup_ui()
        self.cargar_productos()
    
    def setup_ui(self):
        # Barra de búsqueda
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(
            search_frame, 
            text="Buscar",
            command=self.buscar_productos
        ).pack(side=tk.LEFT)
        
        # Botones de acción
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=5)
        
        ttk.Button(
            action_frame, 
            text="Agregar Producto",
            command=self.mostrar_dialogo_agregar
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Modificar",
            command=self.modificar_producto
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Eliminar",
            command=self.eliminar_producto
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview con columnas según tu estructura
        self.tree = ttk.Treeview(
            self.root, 
            columns=("ID", "Producto", "Precio", "Stock", "Categoría", "Proveedor"), 
            show="headings"
        )
        
        # Configurar columnas
        columnas = {
            "ID": 50,
            "Producto": 200,
            "Precio": 100,
            "Stock": 80,
            "Categoría": 150,
            "Proveedor": 150
        }
        
        for col, width in columnas.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def cargar_productos(self):
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                query = """
                SELECT 
                    p.id_producto,
                    p.Producto,
                    p.Precio,
                    p.Cantidad,
                    c.nombre_categoria,
                    pr.Nombre_proveedor
                FROM products p
                LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                """
                cursor.execute(query)
                
                # Limpiar treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Insertar datos
                for producto in cursor.fetchall():
                    self.tree.insert("", tk.END, values=(
                        producto['id_producto'],
                        producto['Producto'],
                        f"${producto['Precio']}",
                        producto['Cantidad'],
                        producto['nombre_categoria'],
                        producto['Nombre_proveedor']
                    ))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar productos: {str(e)}")
    
    def buscar_productos(self):
        texto = self.search_entry.get()
        if not texto:
            self.cargar_productos()
            return
            
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                query = """
                SELECT 
                    p.id_producto,
                    p.Producto,
                    p.Precio,
                    p.Cantidad,
                    c.nombre_categoria,
                    pr.Nombre_proveedor
                FROM products p
                LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
                WHERE p.Producto LIKE ? OR c.nombre_categoria LIKE ? OR pr.Nombre_proveedor LIKE ?
                """
                cursor.execute(query, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
                
                # Limpiar y actualizar treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                for producto in cursor.fetchall():
                    self.tree.insert("", tk.END, values=(
                        producto['id_producto'],
                        producto['Producto'],
                        f"${producto['Precio']}",
                        producto['Cantidad'],
                        producto['nombre_categoria'],
                        producto['Nombre_proveedor']
                    ))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al buscar: {str(e)}")
    
    def mostrar_dialogo_agregar(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Producto")
        dialog.geometry("400x300")
        
        # Campos del formulario
        campos = [
            ("Producto", "producto"),
            ("Precio", "precio"),
            ("Cantidad", "cantidad"),
            ("ID Categoría (opcional)", "id_categoria"),
            ("ID Proveedor (opcional)", "id_proveedor")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entries[key] = ttk.Entry(dialog)
            entries[key].grid(row=i, column=1, padx=5, pady=5, sticky="we")
        
        def guardar():
            try:
                # Validar datos
                producto = entries['producto'].get()
                precio = float(entries['precio'].get())
                cantidad = int(entries['cantidad'].get())
                id_categoria = entries['id_categoria'].get() or None
                id_proveedor = entries['id_proveedor'].get() or None
                
                if not producto:
                    raise ValueError("El nombre del producto es obligatorio")
                
                with crear_conexion() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO products 
                        (Producto, Precio, Cantidad, id_categoria, id_proveedor)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (producto, precio, cantidad, id_categoria, id_proveedor)
                    )
                    
                    # Registrar movimiento
                    cursor.execute(
                        """
                        INSERT INTO movimientos 
                        (id_producto, tipo_movimiento, cantidad, id_usuario)
                        VALUES (?, 'ENTRADA', ?, ?)
                        """,
                        (cursor.lastrowid, cantidad, self.user_id)
                    )
                    
                    conn.commit()
                    self.cargar_productos()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo agregar el producto: {str(e)}")
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(
            row=len(campos), columnspan=2, pady=10)
        
        dialog.grid_columnconfigure(1, weight=1)
    
    def modificar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
            
        id_producto = self.tree.item(seleccion[0])['values'][0]
        
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM products WHERE id_producto = ?",
                    (id_producto,)
                )
                producto = cursor.fetchone()
                
                if not producto:
                    messagebox.showerror("Error", "Producto no encontrado")
                    return
                
                # Diálogo de modificación
                dialog = tk.Toplevel(self.root)
                dialog.title("Modificar Producto")
                dialog.geometry("400x300")
                
                campos = [
                    ("Producto", "producto", producto['Producto']),
                    ("Precio", "precio", producto['Precio']),
                    ("Cantidad", "cantidad", producto['Cantidad']),
                    ("ID Categoría", "id_categoria", producto['id_categoria'] or ""),
                    ("ID Proveedor", "id_proveedor", producto['id_proveedor'] or "")
                ]
                
                entries = {}
                for i, (label, key, value) in enumerate(campos):
                    ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
                    entries[key] = ttk.Entry(dialog)
                    entries[key].insert(0, str(value))
                    entries[key].grid(row=i, column=1, padx=5, pady=5, sticky="we")
                
                def actualizar():
                    try:
                        # Validar datos
                        producto_nombre = entries['producto'].get()
                        precio = float(entries['precio'].get())
                        cantidad = int(entries['cantidad'].get())
                        id_categoria = entries['id_categoria'].get() or None
                        id_proveedor = entries['id_proveedor'].get() or None
                        
                        if not producto_nombre:
                            raise ValueError("El nombre del producto es obligatorio")
                        
                        # Calcular diferencia de cantidad
                        diferencia = cantidad - producto['Cantidad']
                        tipo_movimiento = "ENTRADA" if diferencia > 0 else "SALIDA"
                        
                        with crear_conexion() as conn:
                            cursor = conn.cursor()
                            # Actualizar producto
                            cursor.execute(
                                """
                                UPDATE products SET
                                    Producto = ?,
                                    Precio = ?,
                                    Cantidad = ?,
                                    id_categoria = ?,
                                    id_proveedor = ?
                                WHERE id_producto = ?
                                """,
                                (producto_nombre, precio, cantidad, id_categoria, id_proveedor, id_producto)
                            )
                            
                            # Registrar movimiento si hay cambio en cantidad
                            if diferencia != 0:
                                cursor.execute(
                                    """
                                    INSERT INTO movimientos 
                                    (id_producto, tipo_movimiento, cantidad, id_usuario)
                                    VALUES (?, ?, ?, ?)
                                    """,
                                    (id_producto, tipo_movimiento, abs(diferencia), self.user_id)
                                )
                            
                            conn.commit()
                            self.cargar_productos()
                            dialog.destroy()
                            messagebox.showinfo("Éxito", "Producto actualizado")
                    
                    except ValueError as e:
                        messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")
                
                ttk.Button(dialog, text="Actualizar", command=actualizar).grid(
                    row=len(campos), columnspan=2, pady=10)
                
                dialog.grid_columnconfigure(1, weight=1)
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar el producto: {str(e)}")
    
    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
            
        id_producto = self.tree.item(seleccion[0])['values'][0]
        
        if not messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            return
            
        try:
            with crear_conexion() as conn:
                cursor = conn.cursor()
                
                # Registrar movimiento de baja
                cursor.execute(
                    """
                    INSERT INTO movimientos 
                    (id_producto, tipo_movimiento, cantidad, id_usuario)
                    SELECT id_producto, 'BAJA', Cantidad, ?
                    FROM products WHERE id_producto = ?
                    """,
                    (self.user_id, id_producto)
                )
                
                # Eliminar producto
                cursor.execute(
                    "DELETE FROM products WHERE id_producto = ?",
                    (id_producto,)
                )
                
                conn.commit()
                self.cargar_productos()
                messagebox.showinfo("Éxito", "Producto eliminado")
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    LoginApp().run()