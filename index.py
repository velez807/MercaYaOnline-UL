from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/terminarRegistro.html')
def terminarRegistro():
    return render_template('terminarRegistro.html')

@app.route('/mercaya.html')
def mercaya():
    return render_template('mercaya.html')


if __name__ == '__main__':
    app.run(debug=True)