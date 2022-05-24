from array import array
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random, time

# Servidor:
app = Flask(__name__)
app.secret_key = "arquitectura"

# Base de datos:
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
    carrito = db.column(db.String(1000))


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    codigo = db.Column(db.String(255), unique=True)
    imagen = db.Column(db.String(300))
    precio = db.Column(db.String(80))
    categoria = db.Column(db.String(80))
    cantidad = db.Column(db.String(80))
    descripcion = db.Column(db.String(200))


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


# Rutas:
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
    nuevoUsuario = Usuario(nombre=request.form['nombre'], cedula=request.form['cedula'], correo=request.form['correo'], contrasena=request.form['contrasena'],
                           tarjeta=request.form['tarjeta'], codigo=request.form['codigo'], fecha=request.form['fecha'], direccion=request.form['direccion'], telefono=request.form['telefono'])
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
        usuario = Usuario.query.filter_by(
            cedula=cedula, contrasena=contrasena).first()
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


@app.route('/Admin/Usuarios')
def verUsuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/admin/AgregarProducto')
def aggproductos():
    return render_template('crearproducto.html')


@app.route('/Crear', methods=['POST', 'GET'])
def crearProducto():
    nuevoProducto = Producto(nombre=request.form['nombre'], imagen=request.form['imagen'], precio=request.form['precio'], codigo=request.form['codigo'],
                             categoria=request.form['categoria'], cantidad=request.form['cantidad'], descripcion=request.form['descripcion'])
    if Producto.query.filter_by(nombre=request.form['nombre']).first() is None and Producto.query.filter_by(codigo=request.form['codigo']).first() is None:
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
        producto.codigo = request.form['codigo']
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


# ese malparido carrito:

@app.route('/agregarCarrito/<idu>', methods=['POST'])
def agregarCarrito(idu):

    try:
        cantidadC = int(request.form['cantidadC'])
        _codigo = request.form['code']

        if cantidadC and _codigo and request.method == 'POST':
            producto = Producto.query.filter_by(codigo=_codigo).first()

            itemArray = {producto.codigo: {'nombre': producto.nombre, 'codigo': producto.codigo, 'imagen': producto.imagen, 'precio': producto.precio, 'cantidad': cantidadC, 'descripcion': producto.descripcion, 'precioTotal': producto.precio * cantidadC}}

            precioCarrito = 0
            cantidadCarrito = 0

            session.modified = True
            if 'cart_item' in session:
                if producto.codigo in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if key == producto.codigo:
                            cantidadAntigua = session['cart_item'][key]['cantidad']
                            cantidadTotal = cantidadAntigua + cantidadC
                            session['cart_item'][key]['cantidad'] = cantidadTotal
                            session['cart_item'][key]['precioTotal'] = cantidadTotal * producto.precio
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    cantidadIndividual = int(session['cart_item'][key]['cantidad'])
                    precioIndividual = float(session['cart_item'][key]['precioTotal'])
                    cantidadCarrito = cantidadCarrito + cantidadIndividual
                    precioCarrito = precioCarrito + precioIndividual

            else:
                session['cart_item'] = itemArray
                cantidadCarrito = cantidadCarrito + cantidadC
                precioCarrito = precioCarrito + (producto.precio * cantidadC)

            session['cantidadCarrito'] = cantidadCarrito
            session['precioCarrito'] = precioCarrito

            producto.cantidad = producto.cantidad - cantidadC
            db.session.commit()
            return redirect(url_for('productos', idu=idu))
        else:
            return render_template('admin.html', errorC='Error al agregar producto')

    except ValueError as err:
        pass 


@app.route('/vaciar/<idu>')
def vaciarCarrito(idu):
    session.clear()
    return redirect(url_for('carrito', idu=idu))


@app.route('/Mercaya/Carrito/<idu>', methods=['POST', 'GET'])
def carrito(idu):
    usuario = Usuario.query.filter_by(id=idu).first()
    return render_template('carrito.html', usuario=usuario)


@app.route('/quitar/<idu>/<string:code>')
def quitarProducto(code, idu):
    precioCarrito = 0
    cantidadCarrito = 0
    session.modified = True

    cantidad = session['cart_item'][code]['cantidad']
    producto = Producto.query.filter_by(codigo=code).first()

    for item in session['cart_item'].items():
        if item[0] == code:
            session['cart_item'].pop(item[0], None)
            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    cantidadIndividual = int(
                        session['cart_item'][key]['cantidad'])
                    precioIndividual = float(
                        session['cart_item'][key]['precioTotal'])
                    cantidadCarrito = cantidadCarrito + cantidadIndividual
                    precioCarrito = precioCarrito + precioIndividual
            break
    
    if cantidadCarrito == 0:
        session.clear()
        
    else:
        session['cantidadCarrito'] = cantidadCarrito
        session['precioCarrito'] = precioCarrito

    producto.cantidad = producto.cantidad + cantidad
    db.session.commit()
    return redirect(url_for('carrito', idu=idu))

@app.route('/comprar/<idu>', methods=['POST', 'GET'])
def comprar(idu):
    usuario = Usuario.query.filter_by(id=idu).first()
    numero = random.randint(10000, 99999)
    tarjeta = str(usuario.tarjeta)
    codigo = str(usuario.codigo)
    time.sleep(3)
    if len(tarjeta) == 16 and len(codigo) == 3:
        return render_template('factura.html', usuario=usuario, numero=numero)
    else:
        return render_template('carrito.html', usuario=usuario, errorP='Tu método de pago ha sido rechazado')


@app.route('/Mercaya/Perfil/MétodoPago/<idu>', methods=['POST', 'GET'])
def metodoPago(idu):
    usuario = Usuario.query.filter_by(id=idu).first()
    if request.method == 'POST':
        tarjeta = request.form['tarjeta']
        codigo = request.form['codigo']
        fecha = request.form['fecha']
        if len(tarjeta) == 16 and len(codigo) == 3:
            usuario.tarjeta = tarjeta
            usuario.codigo = codigo
            usuario.fecha = fecha
            db.session.commit()
            return render_template('perfil.html', usuario=usuario, mensaje='Tu método de pago ha sido actualizado')
        else:
            return render_template('metodopago.html', usuario=usuario, error='Tarjeta o código inválidos')
    else:
        return render_template('metodopago.html', usuario=usuario)



# Vea ni por el htpa vaya a borrar esto gvon
if __name__ == '__main__':
    app.run(debug=True)
