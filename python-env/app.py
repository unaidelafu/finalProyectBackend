from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import mariadb
import os

from db_files import database

# **********
# CONSTS
# **********

# ---- Database values and connection
host = "127.0.0.1"
port = 3306
user = "root"
password = "2bEvImI2"
db_name = "bike_workshop"
#db_name = "devcamp_university_course"
conn_ok = False

db = database.DbLoader(host, port, user, password, db_name)

# ---------


app = Flask(__name__)
ma=Marshmallow(app)

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')

def hello():
    return "Hey Flask"


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('sid','name1')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


#endpoints

##create a customer:
@app.route('/customer', methods=["POST"])
def add_customer():
    sid = request.json['sid']
    name1 = request.json['name1']
    name2 = request.json['name2']
    try:
        db.connect()
        conn_ok = True
        guideId = db.create_customers(sid,name1,name2)
        if(guideId > 0):     
            print(f"Se ha introducido el valor: {guideId}")
        else:
            print(f"No se ha introducido ningun valor")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")    

    return customer_schema.jsonify((guideId,"OK"))

if __name__ == '__main__':

    app.run(debug=True)
