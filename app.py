from flask import render_template, request, session
from flask_cors import CORS
from python.dataBaseConnection import get_db  #conexión a la base de datos
import python.independ as independ
import python.rutasForm as rutasForm #importa blueprints de rutas con mayor complejidad
import xml.etree.ElementTree as ET  # Para cargar test.keyx

# Cargar la clave secreta desde secret.key
try:
    with open('secret.key', 'r') as file:
        app.secret_key = file.read().strip()  # Lee la clave y la asigna
except FileNotFoundError:
    print("Advertencia: El archivo 'secret.key' no se encontró. Usando clave predeterminada.")
    app.secret_key = 'claveMaestra'  # Valor predeterminado

# Si necesitas cargar el archivo test.keyx
try:
    tree = ET.parse('config/test.keyx')
    root = tree.getroot()
    key_data = root.find('.//Data').text  # Accede al valor dentro de <Data>
    print(f"Clave cargada desde test.keyx: {key_data}")
except (FileNotFoundError, ET.ParseError):
    print("Advertencia: El archivo 'test.keyx' no se encontró o está mal formado.")

# Aquí comienza tu código tal como estaba antes
app, mysql = get_db()

CORS(app)  # Habilitar CORS
app.secret_key = 'claveMaestra'  # Solo si no se pudo cargar desde el archivo

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/crear_edificio')
def crearEdificio():
    return render_template('crear_edificio.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para el formulario de login
app.register_blueprint(rutasForm.formLogin_bp)

# Ruta para cerrar sesión
app.register_blueprint(rutasForm.logout_bp)

# Ruta para crear el edificio
app.register_blueprint(rutasForm.creaEdificio_bp)

@app.route('/usuario-reserva')
def usuarioReserva():
    cursor = mysql.connection.cursor()
    cursor.execute(""" SELECT idLocker, numeroLocker, pe.pisoCol, ei.letraEdificio , estado_locker_idEstadoLocker
    FROM locker l 
    INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso
    INNER JOIN edificio_instituto ei ON pe.edificio_instituto_idEdificioInstituto = ei.idEdificioInstituto
   """)
    datos = cursor.fetchall()
    cursor.close()
    translated_data = []
    for locker in datos:
        idLocker, numeroLocker, pisoCol, letraEdificio, estado = locker
        if estado == 1:
            estado_texto = "Disponible"
        elif estado == 2:
            estado_texto = "Ocupado"
        elif estado == 3:
            estado_texto = "Con Problema"
        else:
            estado_texto = "Desconocido"
        translated_data.append((idLocker, numeroLocker, pisoCol, letraEdificio, estado_texto))
    return render_template('usuario-reserva.html', datos=translated_data)

# Métodos para filtrar en búsqueda
@app.route('/')
def index():
    # Verificamos si el usuario está logueado
    if not session.get('logged_in'):
        return render_template('home.html')  # Muestra home.html si no está logueado
    cursor = mysql.connection.cursor()

    # Recibir filtros desde el formulario
    estadoRequest = request.args.get('estado')
    piso = request.args.get('piso')
    edificio = request.args.get('edificio')
    # Construir la consulta con filtros
    cursor.execute("SELECT * FROM lockersbd.v_index")
    datos = cursor.fetchall()

    # Traducir el estado
    translated_data = []
    for locker in datos:
        idLocker, numeroLocker, pisoCol, letraEdificio, estado, alumno = locker

        # Aplicando los filtros :D
        if estadoRequest and independ.filtroEstado(idLocker) != estadoRequest:
            continue 

        if piso and str(independ.filtroPiso(idLocker)) != piso:
            continue 

        if edificio and independ.filtroEdificio(idLocker) != edificio:
            continue 

        # Traducir el estado del locker
        if estado == 1:
            estado_texto = "Disponible"
        elif estado == 2:
            estado_texto = "Ocupado"
        elif estado == 3:
            estado_texto = "Con Problema"
        else:
            estado_texto = "Desconocido"

        translated_data.append((idLocker, numeroLocker, pisoCol, letraEdificio, estado_texto))

    # Obtener opciones de edificios desde la base de datos e implementarlos en el label
    cursor.execute("SELECT DISTINCT pisoCol FROM lockersbd.piso_edificio")
    labelPiso = cursor.fetchall()
    cursor.execute("SELECT DISTINCT letraEdificio FROM edificio_instituto")
    labelEdificios = cursor.fetchall()
    cursor.close()
    return render_template('index.html', datos=translated_data, estado=estadoRequest, piso=piso, edificio=edificio, labelEdificios=labelEdificios, labelPiso=labelPiso)

# Nueva ruta para mostrar la reserva activa de un locker
@app.route('/reserva_activa/<int:locker_id>')
def reserva_activa(locker_id):
    cursor = mysql.connection.cursor()

    # Obtener los datos de la reserva activa del locker seleccionado
    query = """
        SELECT r.fecha_inicio, r.fecha_fin, a.pNombreAlumno, a.apPaternoAlumno, a.runAlumno
        FROM reserva_alumno r
        INNER JOIN alumno a ON r.alumno_runAlumno = a.runAlumno
        WHERE r.locker_idLocker = %s AND r.estadoReserva_idEstadoReserva = 1
    """
    cursor.execute(query, (locker_id,))
    reserva = cursor.fetchone()  # Asumimos que solo hay una reserva activa por locker

    cursor.close()

    if reserva:
        reserva_data = {
            'fecha_inicio': reserva[0],
            'fecha_fin': reserva[1],
            'nombre_alumno': reserva[2],
            'apellido_alumno': reserva[3],
            'run_alumno': reserva[4]
        }
        return render_template('reserva_activa.html', reserva=reserva_data)
    else:
        return f"No hay reservas activas para el locker con ID {locker_id}."

# Ruta para obtener los lockers en formato JSON
app.register_blueprint(rutasForm.lockerJson_bp)

# Ruta para mostrar la página de reserva
@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

# Ruta para reservar un locker
app.register_blueprint(rutasForm.formReserva_bp)

# Ruta para mostrar la página de cancelación
@app.route('/cancelacion')
def cancelacion():
    return render_template('cancelacion.html')

# Ruta para cancelar una reserva
app.register_blueprint(rutasForm.cancelReservation_bp)

if __name__ == '__main__':
    o = "1"  # Literal, esto solo sirve para que el terminal reconozca la variable
    if o == "1":
        app.run(debug=True)
    elif o == "2":
        app.run(host='0.0.0.0')
    else:
        print("Opción no válida. Por favor, elige 1 o 2.")
