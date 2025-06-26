BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Categoria" (
	"id_categoria"	INTEGER,
	"nombre_categoria"	TEXT NOT NULL,
	PRIMARY KEY("id_categoria" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Productos" (
	"id_producto"	INTEGER,
	"id_proveedor"	INTEGER,
	"Producto"	TEXT NOT NULL,
	"id_categoria"	INTEGER,
	"Precio"	REAL,
	"Cantidad"	INTEGER,
	PRIMARY KEY("id_producto" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Proveedores" (
	"id_proveedor"	INTEGER,
	"nombre_proveedor"	TEXT NOT NULL,
	"telefono"	INTEGER,
	"email"	INTEGER,
	PRIMARY KEY("id_proveedor" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"id_usuario"	INTEGER,
	"Nombre_usuario"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Contraseña"	INTEGER NOT NULL,
	"Telefono"	NUMERIC NOT NULL,
	PRIMARY KEY("id_usuario" AUTOINCREMENT)
);
INSERT INTO "Categoria" VALUES (1,'Frutas');
INSERT INTO "Productos" VALUES (1,1,'Tomate',1,3.0,30);
INSERT INTO "Proveedores" VALUES (1,'Tobiascompany',1126366202,'tumacho@gmail.com');
COMMIT;
