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
    direccion VARCHAR(200) NOT NULL
);