from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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
    nuevoUsuario = Usuario(nombre=request.form['nombre'], cedula=request.form['cedula'], correo=request.form['correo'], contrasena=request.form['contrasena'], tarjeta=request.form['tarjeta'], codigo=request.form['codigo'], fecha=request.form['fecha'], direccion=request.form['direccion'])
    db.session.add(nuevoUsuario)
    db.session.commit()
    return render_template('Regis.html')

if __name__ == '__main__':
    app.run(debug=True)