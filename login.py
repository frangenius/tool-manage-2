import tkinter as tk
from tkinter import ttk, messagebox
import lista  # Importa la pantalla de lista

def verificar_login(ventana, entry_usuario, entry_contraseña):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    if usuario == "admin" and contraseña == "1234":
        ventana.withdraw()  # Oculta el login
        lista.mostrar_lista(ventana)  # Abre la pantalla de lista
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def mostrar_login():
    ventana = tk.Tk()
    ventana.title("Login")
    ventana.geometry("300x200")
    ventana.resizable(False, False)
    
    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True)
    
    # Widgets
    ttk.Label(frame, text="Usuario:").pack(pady=5)
    entry_usuario = ttk.Entry(frame)
    entry_usuario.pack(pady=5)
    
    ttk.Label(frame, text="Contraseña:").pack(pady=5)
    entry_contraseña = ttk.Entry(frame, show="*")
    entry_contraseña.pack(pady=5)
    
    btn_login = ttk.Button(frame, text="Iniciar Sesión",
                          command=lambda: verificar_login(ventana, entry_usuario, entry_contraseña))
    btn_login.pack(pady=15)
    
    ventana.mainloop()