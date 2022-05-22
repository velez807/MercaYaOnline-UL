class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    cedula = db.Column(db.String(80), unique=True)
    correo = db.Column(db.String(120))
    contrasena = db.Column(db.String(80))
    tarjeta = db.Column(db.String(80))
    codigo = db.Column(db.String(80))
    fecha = db.Column(db.String(80))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(80))
    compras = db.column(db.Integer)

-- crear tabla con los datos de arriba

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(80) NOT NULL,
    cedula VARCHAR(80) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    contrasena VARCHAR(80) NOT NULL,
    tarjeta VARCHAR(80) NOT NULL,
    codigo VARCHAR(80) NOT NULL,
    fecha VARCHAR(80) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    imagen = db.Column(db.String(300))
    precio = db.Column(db.String(80))
    categoria = db.Column(db.String(80))
    cantidad = db.column(db.Integer)
    descripcion = db.Column(db.String(200))

-- crear tabla con los datos de arriba

CREATE TABLE producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    imagen TEXT NOT NULL,
    precio TEXT NOT NULL,
    categoria TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    descripcion TEXT NOT NULL
);
