from dataBaseConnection import get_db
app, mysql = get_db()
import qrcode
from cryptography.fernet import Fernet
import time
el = "--------------------------------------"
import mysql.connector

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jDXgT61EhWinGAx0Wy2H",
    database="lockersbd"
)
# @app.route('/')
# def index():
#     return "TEST"
# def crearKey():
#     key = Fernet.generate_key()

#     # Guarda la clave para su uso posterior
#     with open('secret.key', 'wb') as key_file:
#         key_file.write(key)
#     return key
# try:
#     #Carga la clave de la raiz del proyecto y lo almacena como constante
#     with open('secret.key', 'rb') as key_file:
#      key = key_file.read()
#      cipher = Fernet(key)

# except FileNotFoundError: #si no encuentra el archivo, creara uno nuevo
#     keyCreado=crearKey()
#     cipher = Fernet(keyCreado)
cursor = mysql.cursor()
runAlumno=21300379
cursor.execute("""SELECT secretKey , locker_idLocker, alumno_runAlumno, numeroLocker FROM reserva_alumno ra
INNER JOIN locker l ON ra.locker_idLocker = l.idLocker
WHERE
estadoReserva_idEstadoReserva = 1 AND
alumno_runAlumno = %s LIMIT 1 """ , (runAlumno,))
key = cursor.fetchone()
cursor.close()

# Cargar clave y almacenar en la raiz
# with open('secret.key', 'rb') as key_file:
#     key = key_file.read()
print(key[0])


cipher = Fernet(key[0])


# Datos a codificar
locker_id = 'locker1'

#creacion del token
token_data = f'{locker_id}:{runAlumno}:{int(time.time()) + 300}'  # Token expira en 5 minutos

# Cifra los datos
encrypted_data = cipher.encrypt(token_data.encode())

# Genera el código QR
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(runAlumno)
qr.add_data("|")
qr.add_data(encrypted_data)
print(encrypted_data)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')

# Guarda la imagen del código QR
img.save('qr_code.png')




def hash_test():
    import hashlib
    trans= hashlib.sha256(b"hola").hexdigest()
    print(trans)
    vuelve= hashlib.sha256(trans).hexdigest
    print(vuelve)




def dataCount():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'lockersbd'")
        temp = cursor.fetchall()
        print(el)
        print(f"La cantidad de tablas en la BDD es: ",temp[0][0])
        print(el)
        print()
        cursor.execute(
        """SELECT idLocker, numeroLocker, pe.pisoCol, ei.letraEdificio , estado_locker_idEstadoLocker
        FROM locker l 
        INNER JOIN piso_edificio pe ON l.piso_edificio_idPiso = pe.idPiso
        INNER JOIN edificio_instituto ei ON pe.edificio_instituto_idEdificioInstituto = ei.idEdificioInstituto""")
        temp = cursor.fetchall()

        print(f"id: ", temp[0][0])




        cursor.close()



# if __name__ == '__main__':
#     app.run(debug=True)