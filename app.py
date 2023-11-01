from db_files import database
from python-env 
import sys
import mariadb


# **********
# CONSTS
# **********

host = "127.0.0.1"
port = 3306
user = "root"
password = "2bEvImI2"
db_name = "bike_workshop"
#db_name = "devcamp_university_course"

conn_ok = False

db = database.DbLoader(host, port, user, password, db_name)

try:
    db.connect()
    conn_ok = True
    db.get_customers()
    id = db.create_customers("P71872049","Elvira","Granja")
    if(id > 0):     
        print(f"Se ha introducido el valor: {id}")
    else:
        print(f"No se ha introducido ningun valor")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
