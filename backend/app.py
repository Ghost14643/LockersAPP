from dataBaseConnection import get_db

app, mysql = get_db()

# @app.route('/')
# def index():
#     return "TEST"

def dataCount():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM locker')
        result = cursor.fetchone()
        cursor.close()
        print(f"dddddddddddddddddddddd ", result)

dataCount()



if __name__ == '__main__':
    app.run(debug=True)
