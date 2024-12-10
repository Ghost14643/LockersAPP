from flask import render_template, request, redirect, session
from flask_cors import CORS
from python.dataBaseConnection import get_db  #conexión a la base de datos

app, mysql = get_db()
CORS(app)  # Habilitar CORS
app.secret_key = 'claveMaestra'


@app.route('/crear_edificio')
def crearEdificio():
    return render_template('crear_edificio.html')



# Ruta para el formulario de login
@app.route('/formLogin', methods=['POST'])
def formLogin():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form['email']
        password = request.form['password']

        # Consultar la base de datos para verificar el usuario y la contraseña
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM alumno WHERE emailAlumno = %s AND contrasenAlumno = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Guardar los datos del usuario en la sesión
            session['logged_in'] = True
            session['user_id'] = user[0]  # Guarda el ID del usuario (ajusta según tu base de datos)
            session['email'] = email

            return redirect('/')
        else:
            mensaje = "Usuario o contraseña incorrectos"
            return render_template('login.html', mensaje=mensaje)
        


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Elimina los datos de la sesión para cerrar la sesión del usuario
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect('/login')


@app.route('/usuario-reserva')
def usuarioReserva():
    return render_template('usuario-reserva.html')
