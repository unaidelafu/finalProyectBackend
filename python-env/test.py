from db_files import database
import sys
import mariadb
from classes import customers as c


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
    customers = db.get_customers()
    for customer in customers:
        print(customer.serialize(), customer.id, customer.sid, customer.name_1, customer.name_2, customer.status)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
