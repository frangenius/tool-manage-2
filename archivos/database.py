import sqlite3
from sqlite3 import Error



def crear_conexion():
    """Crear conexión a tu base de datos existente"""
    try:
        conexion = sqlite3.connect('control_stock.db')
        conexion.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        return conexion
    except Error as e:
        raise Exception(f"Error al conectar a la base de datos: {e}")