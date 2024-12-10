import cv2
from pyzbar.pyzbar import decode
from cryptography.fernet import Fernet
import time
#vista flask para mejor simulacion
import mysql.connector

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jDXgT61EhWinGAx0Wy2H",
    database="lockersbd"
)   

 
# Cargar clave y almacenar en la raiz
# with open('secret.key', 'rb') as key_file:
#     key = key_file.read()








# Simular que el locker se abrio
def open_locker(locker_id, runEstudiante):
    cursor = mysql.cursor()
    cursor.execute("""INSERT INTO
                   `lockersbd`.`registro_lockers` (`idLocker`, `RunAlumno`, `fechaIngreso`, `horaIngreso`)
                    VALUES (%s, %s, CURRENT_DATE, CURRENT_TIME); """ , (locker_id, runEstudiante,))
    mysql.commit()
    cursor.close()
    print(f"Locker {locker_id} del estudiante {runEstudiante} abierto")

# inicio de la camara
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al acceder a la cámara")
        break

    datosDecodificados = decode(frame)
    for obj in datosDecodificados:
        runAlumno = obj.data[:8]
        datosEncriptados = obj.data[9:]
        
        try:
            
            cursor = mysql.cursor()
            cursor.execute("""SELECT secretKey , locker_idLocker, numeroLocker FROM reserva_alumno ra
            INNER JOIN locker l ON ra.locker_idLocker = l.idLocker
            WHERE
            estadoReserva_idEstadoReserva = 1 AND
            alumno_runAlumno = %s LIMIT 1 """ , (runAlumno,))
            data = cursor.fetchone()
            cursor.close()
            cipher = Fernet(data[0])


            datosDecifrados = cipher.decrypt(datosEncriptados).decode('utf-8')
            locker_id,runEstudiante, tiempoExpirado = datosDecifrados.split(':')
            tiempoExpirado = int(tiempoExpirado)
            sysdate = int(time.time())
            #cursor = mysql.connection.cursor()
            # cursor.execute("""SELECT *
            #                 FROM lockersbd.reserva_alumno
            #                 WHERE locker_idLocker = %s AND estadoReserva_idEstadoReserva = 1 AND alumno_runAlumno = %s
            #                 ORDER BY fecha_fin DESC
            #                 LIMIT 1;""",(locker_id, runEstudiante,))
            if sysdate < tiempoExpirado:
                open_locker(data[1], runAlumno)
                print("Token válido")
                exit()
            else:
                print("Token expirado")
        except Exception as e:
            print("Código QR no válido", e)


#Muestra la vista previa de la camara
    cv2.imshow("vista camara :D",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




# import cv2
# from pyzbar.pyzbar import decode
# from cryptography.fernet import Fernet
# # Carga la clave de cifrado
# with open('secret.key', 'rb') as key_file:
#     key = key_file.read()
# cipher = Fernet(key)
# # Carga y decodifica la imagen del código QR
# img = cv2.imread('qr_code.png')
# decoded_objects = decode(img)
# for obj in decoded_objects:
#     encrypted_data = obj.data
# # Descifra los datos
# decrypted_data = cipher.decrypt(encrypted_data)
# print(decrypted_data.decode())
# # Carga la imagen del código QR
# def escanear_qr():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         decoded_objects = decode(frame)
#         for obj in decoded_objects:
#             print(obj.data.decode())
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
# escanear_qr()




# if __name__ == '__main__':
#     o = "1" #literal esto solo sirve para que el terminal reconozca la variable kajskajsdasa
#     if o == "1":
#         app.run(debug=True)
#     elif o == "2":
#         app.run(host='0.0.0.0')
#     else:
#         print("Opción no válida. Por favor, elige 1 o 2.")
