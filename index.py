from itertools import product
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import time

#Servidor:
app = Flask(__name__)

#Base de datos:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

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


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    imagen = db.Column(db.String(300))
    precio = db.Column(db.String(80))
    categoria = db.Column(db.String(80))
    cantidad = db.Column(db.String(80))
    descripcion = db.Column(db.String(200))

#Rutas:
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/Regis', methods=['POST'])
def crearUsuario():
    nuevoUsuario = Usuario(nombre=request.form['nombre'], cedula=request.form['cedula'], correo=request.form['correo'], contrasena=request.form['contrasena'], tarjeta=request.form['tarjeta'], codigo=request.form['codigo'], fecha=request.form['fecha'], direccion=request.form['direccion'], telefono=request.form['telefono'])
    if nuevoUsuario.nombre == 'admin':
        return render_template('register.html', admin='Nombre de usuario incorrecto')
    if Usuario.query.filter_by(cedula=request.form['cedula']).first() is None:
        db.session.add(nuevoUsuario)
        db.session.commit()
        return render_template('Regis.html')
    else:
        return render_template('register.html', error='Ya hay un usuario registrado con esta cédula')
    

@app.route('/mercaya', methods=['POST', 'GET'])
def log():
    if request.method == 'POST':
        cedula = request.form['cedula']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(cedula=cedula, contrasena=contrasena).first()
        if usuario:
            return redirect(url_for('productos', idu=usuario.id))
        else:
            error = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error=error)
    else:
        aviso = 'Por motivos de seguridad vuelva a ingresar sus datos'
        return render_template('login.html', aviso=aviso)


@app.route('/mercaya/productos/<idu>')
def productos(idu):
    productos = Producto.query.all()
    usuario = Usuario.query.filter_by(id=idu).first()
    for producto in productos:
        if producto.cantidad < 0:
            producto.cantidad = producto.cantidad * -1
            db.session.commit()

    if usuario.cedula == 'admin':
        return render_template('admin.html', productos=productos, usuario=usuario)
    else:    
        return render_template('mercaya.html', usuario=usuario, productos=productos)


@app.route('/admin/AgregarProducto')
def aggproductos():
    return render_template('crearproducto.html')

@app.route('/Crear', methods=['POST', 'GET'])
def crearProducto():
    nuevoProducto = Producto(nombre=request.form['nombre'], imagen=request.form['imagen'], precio=request.form['precio'], categoria=request.form['categoria'], cantidad=request.form['cantidad'], descripcion=request.form['descripcion'])
    if Producto.query.filter_by(nombre=request.form['nombre']).first() is None:
        db.session.add(nuevoProducto)
        db.session.commit()
        return redirect(url_for('productos', idu=1))
    else:
        error = 'Ya se registro este producto'
        return render_template('crearproducto.html', error=error)

@app.route('/Eliminar/<id>', methods=['POST', 'GET'])
def deleteProducto(id):
    producto = Producto.query.filter_by(id=id).first()
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('productos', idu=1))

@app.route('/EditarProducto/<id>', methods=['POST', 'GET'])
def editProducto(id):
    producto = Producto.query.filter_by(id=id).first()
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.imagen = request.form['imagen']
        producto.precio = request.form['precio']
        producto.categoria = request.form['categoria']
        producto.cantidad = request.form['cantidad']
        producto.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('productos', idu=1))
    else:
        return render_template('editproducto.html', producto=producto)


@app.route('/perfil/<idu>', methods=['POST', 'GET'])
def perfil(idu):
    usuario = Usuario.query.filter_by(id=idu).first()
    if request.method == 'POST':
        return render_template('perfil.html', usuario=usuario)
    else:
        return render_template('perfil.html', usuario=usuario)

@app.route('/Mercaya/<id><idu>')
def reducirCantidad(id, idu):
    producto = Producto.query.filter_by(id=id).first()
    usuario = Usuario.query.filter_by(id=idu).first()
    if producto.cantidad >= 1:
        producto.cantidad = producto.cantidad - 1
        db.session.commit()
        time.sleep(3)
        return redirect(url_for('productos', idu=usuario.id))
    else:
        pass

@app.route('/Admin/Usuarios')
def verUsuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)




# Vea ni por el htpa vaya a borrar esto gvon
if __name__ == '__main__':
    app.run(debug=True)