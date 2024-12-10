from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__, template_folder='../templates' ,static_folder= '../static') 
# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jDXgT61EhWinGAx0Wy2H' 
app.config['MYSQL_DB'] = 'lockersbd' 
mysql = MySQL(app)
def get_db():
    return app, mysql