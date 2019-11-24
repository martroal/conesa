import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from forms import LoginForm, SaludarForm, RegistrarForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'tupu tamadre'

@app.route('/') #pagina de inicio
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

@app.route('/clientes') #tabla de clientes
def clientes():
    with open('templates/clientes.csv', encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file)
        return render_template('clientes.html',csv_reader=csv_reader)  

@app.route('/acerca', methods=['GET', 'POST']) #mi nombre aparace aqui
def acerca():
    return render_template("acerca.html")

@app.errorhandler(404) #erro kuatroserokuatro
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500) #weve got shit to deal with
def error_interno(e):
    return render_template('500.html'), 500

@app.route('/ingresar', methods=['GET', 'POST']) #ingrese su usuario dolor.huevo.0.1
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido al CRM de Conesa')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Por favor escribe bien, gracias')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

@app.route('/registrar', methods=['GET', 'POST']) #registrar usuario dolor.huevo.2.3
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado satisfactoriamente')
            return redirect(url_for('ingresar'))
        else:
            flash('las contrasenas no son iguales')
    return render_template('registrar.html', form=formulario)

@app.route('/cerrar_sesion', methods=['GET']) #chau
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('sesion_cerrada.html')
    else:
        return redirect(url_for('index'))

@app.route('/searchtest') #probando search by country
def searchtest():
    with open('templates/clientes.csv', encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file)
        return render_template('searchtest.html',csv_reader=csv_reader)   

@app.route('/searchtest2') #probando ESTE ES EL QUE SIRVEEE
def searchtest2():
    with open('templates/clientes.csv', encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file)
        return render_template('searchtest2.html',csv_reader=csv_reader)   


if __name__ == "__main__":
    app.run()
