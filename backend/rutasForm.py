from flask import Blueprint, render_template, request, session, redirect, jsonify, flash
from python.dataBaseConnection import get_db
import python.independ as independ
#ESTE ES UN MODULO PARA GUARDAR RUTAS SIN TEMPLATE REGISTRADO
app, mysql = get_db()
#Blueprints para redireccionar
formLogin_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
lockerJson_bp = Blueprint('lockerJson', __name__)
formReserva_bp = Blueprint('formReserva', __name__)
cancelReservation_bp = Blueprint('cancelReservation', __name__)
creaEdificio_bp = Blueprint('creaEdificio', __name__)

@formLogin_bp.route('/formLogin', methods=['POST'])
def formLogin():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form['email']
        password = request.form['password']

        # Consultar la base de datos para verificar el usuario y la contraseña
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM alumno WHERE emailAlumno = %s AND contrasenAlumno = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Guardar los datos del usuario en la sesión
            session['logged_in'] = True
            session['user_id'] = user[0]  # Guarda el ID del usuario (ajusta según tu base de datos)
            session['email'] = email
            return redirect('/')
        else:
            mensaje = "Usuario o contraseña incorrectos"
            return render_template('login.html', mensaje=mensaje)

@logout_bp.route('/logout')
def logout():
    # Elimina los datos de la sesión para cerrar la sesión del usuario
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect('/login')


@lockerJson_bp.route('/api/lockers', methods=['GET'])
def get_lockers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idLocker, numeroLocker, pe.pisoCol , piso_edificio_idPiso ,estado_locker_idEstadoLocker FROM locker l INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso")
    datos = cursor.fetchall()
    
    # Traducir el estado
    translated_data = []

    for locker in datos:
        edificio = locker[3]
        if edificio == 1:
            estado_edificio = "Y"
        elif edificio == 2:
            estado_edificio = "W"
        elif edificio == 3:
            estado_edificio = "Z"
        else:
            estado_edificio = "???"


    for locker in datos:
        estado = locker[4]  # estado_locker_idEstadoLocker
        if estado == 1:
            estado_texto = "Disponible"
        elif estado == 2:
            estado_texto = "Ocupado"
        elif estado == 3:
            estado_texto = "Con Problema"
        else:
            estado_texto = "Desconocido"

        translated_data.append({
            'id': locker[0],
            'numero': locker[1],
            'piso': locker[2],
            'edificio': estado_edificio,
            'estado': estado_texto
        })

    cursor.close()
    return jsonify(translated_data)

@formReserva_bp.route('/reserve', methods=['POST'])
def reserve_locker():
    #try:
        numLocker = request.form['numeroLocker']
        pisoLocker = request.form['piso']
        edificio_Locker = request.form['edificio']
        rut_estudiante = session['user_id']  # utiliza el run de usuario iniciado
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        estado = '1'
        tipo_reserva = '1'
        cursor = mysql.connection.cursor()
        
        # Verificar si el locker existe y está disponible
        cursor.execute(
            """SELECT idLocker , estado_locker_idEstadoLocker
            FROM locker l 
            INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso
            WHERE l.numeroLocker = %s AND pisoCol = %s AND pe.edificio_instituto_idEdificioInstituto = %s""", (numLocker, pisoLocker, edificio_Locker)
        )
        
        locker = cursor.fetchone()
        if locker:          
            locker_id = locker[0]  # Extraer el idLocker de la primera tupla
            #print(dispoCalendar(locker_id,start_date,end_date))
            # Llamada a escuela_estudiante con ambos parámetros
            if independ.escuela_lockerEstudiante(rut_estudiante, locker_id):
                if locker[1] == 1:  # Verifica si el locker está disponible
                    cursor.execute(
                        """INSERT INTO reserva_alumno 
                        (fecha_inicio, fecha_fin, locker_idLocker, alumno_runAlumno, estadoReserva_idEstadoReserva, reserva_idReserva) 
                        VALUES (%s, %s, %s, %s, %s, %s)""", (start_date, end_date, locker_id, rut_estudiante, estado, tipo_reserva)
                    )
                    mysql.connection.commit()
                    return redirect('/')  # Redirige al índice después de reservar
                elif locker[1] == 2:
                    flash("El locker solicitado no está disponible.", "error")
                else:
                    flash("El locker solicitado no existe.", "error")
            else:
                flash("El locker seleccionado pertenece a otra escuela, escoja otro.", "error")
        else:
            flash("El locker solicitado no existe.", "error")

        cursor.close()
        return redirect('/reserva')

    # except Exception as e:
    #     # Manejo de errores de base de datos u otros problemas
    #     mysql.connection.rollback()
    #     flash(f"Error al reservar el locker: {str(e)}", "error")
    #return redirect('/reserva')

@cancelReservation_bp.route('/cancel', methods=['POST'])
def cancel_reservation():
    idReserva = request.form['idReserva']
    rutAdmin = request.form['rutAdmin']
    observacion = request.form['observacion']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO `lockersbd`.`cancelacion_reserva` (`administrador_runAdministrador`, `reserva_alumno_idReservaAlumno`, `observacion`) VALUES (%s , %s , %s)" , (rutAdmin, idReserva ,  observacion)) 
    mysql.connection.commit()
    cursor.close()
    return redirect('/')  # Redirige al índice después de cancelar

@creaEdificio_bp.route('/creaEdificio', methods=['POST'])
def nuevoEdificio():
    nombre = request.form['nombre']
    numero_pisos = request.form['numero_pisos']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO `lockersbd`.`edificio_instituto` (`letraEdificio`) VALUES (%s)", (nombre,))
    if numero_pisos:
        cursor.execute("SELECT idEdificioInstituto FROM lockersbd.edificio_instituto WHERE letraEdificio = %s" ,(nombre,))
        newEdificioId  = cursor.fetchone()
        cursor.execute("CALL p_crearPiso(%s, %s)", (numero_pisos, newEdificioId[0]))
    mysql.connection.commit()
    cursor.close()

    return redirect('/')