from flask import current_app, request,redirect
from python.dataBaseConnection import get_db
app, mysql = get_db()


# def filtroLockerAlumno(runAlumno):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM reserva_alumno  where run",(runAlumno))
#     lockerAlumno = cursor.fetchall()
#     cursor.close()
#     return lockerAlumno if lockerAlumno is not None else None

#filtros de busqueda
def filtroEstado(idLocker):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombreEstadoLocker FROM locker l INNER JOIN estado_locker el ON l.estado_locker_idEstadoLocker = el.idEstadoLocker WHERE idLocker = %s  ",(idLocker,))
    estadoLocker = cursor.fetchall()
    cursor.close()
    return estadoLocker[0][0] if estadoLocker else current_app.page_not_found()

def filtroPiso(idLocker):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT pe.pisoCol FROM locker l
                   INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso
                   WHERE idLocker = %s  """,(idLocker,))
    pisoLocker = cursor.fetchall()
    cursor.close()
    return pisoLocker[0][0] if pisoLocker else current_app.page_not_found()

def filtroEdificio(idLocker):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT ei.letraEdificio FROM locker l
                INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso
                INNER JOIN edificio_instituto ei ON pe.edificio_instituto_idEdificioInstituto = ei.idEdificioInstituto
                WHERE idLocker = %s """,(idLocker,))
    edificioLocker = cursor.fetchall()
    cursor.close()
    return edificioLocker[0][0] if edificioLocker else current_app.page_not_found()


def escuela_lockerEstudiante(rutEstudiante, id_locker): #Valida si la escuela asignada al locker es igual al del estudiante
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT escuela_idEscuela FROM alumno a INNER JOIN carrera c ON a.carrera_idCarrera = c.idCarrera WHERE runAlumno = %s",(rutEstudiante,))
    idEscuelaAlumno = cursor.fetchone()
    cursor.execute("SELECT pisoEscuela_idEscuela FROM piso_edificio pe INNER JOIN locker l  ON l.piso_edificio_idPiso = pe.idPiso WHERE idLocker =  %s", (id_locker,))
    idEscuelaPiso = cursor.fetchone()
    cursor.close()
    if idEscuelaAlumno and idEscuelaPiso:
        return True if idEscuelaAlumno[0] == idEscuelaPiso[0] or idEscuelaPiso[0] is None else False
    return False #Retorna True o False si son iguales o no, asimismo si la escuela no retorna, representa que el locker es libre de esa restriccion 

def usuarioPatudo(runAlumno): #identifica si el usuario ya tiene un locker en uso
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT COUNT(*)
                    FROM reserva_alumno
                    WHERE alumno_runAlumno = %s 
                    AND fecha_fin = sysdate()
                    AND fecha_fin = (SELECT MAX(fecha_fin) FROM reserva_alumno)""",(runAlumno,))
    yaTieneLocker = cursor.fetchall()
    cursor.close()
    return yaTieneLocker[0][0] if yaTieneLocker else current_app.page_not_found()


def dispoCalendar(lockerId,start,end): #comprueba la disponibilidad por calendario
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT fecha_inicio , fecha_fin FROM reserva_alumno WHERE locker_idLocker= %s",(lockerId,))
    fechas = cursor.fetchone()
    bddStart = fechas[0].strftime("%Y-%m-%d") #Cambia el formato datetime a str para comparacion.
    bddEnd = fechas[1].strftime("%Y-%m-%d")
    cursor.close()
    if fechas:
        return True if bddStart <= start or bddEnd >= end or fechas is None else False #si esta dentro del rango, retornara True para entender que esta ocupado
    return False

def add_locker():
    numero = request.form['numero']
    piso = request.form['piso']
    estado = request.form['estado']
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO locker (numeroLocker, piso_edificio_idPiso, estado_locker_idEstadoLocker) VALUES (%s, %s, %s)", (numero, piso, estado))
    mysql.connection.commit()
    cursor.close()

    return redirect('/')
