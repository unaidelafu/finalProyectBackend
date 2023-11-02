from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import mariadb
import os

from db_files import database
from classes import customers as c
from classes import employees as em
from classes import employee_types as emt
from classes import wharehouses as w
from classes import brands as b
from classes import brand_types as bt

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
def API_add_customer():
    customer_resp = None
    sid = request.json['sid']
    name1 = request.json['name1']
    name2 = request.json['name2']
    new_customer = c.Customer(None,sid,name1,name2,None)
    try:
        db.connect()
        conn_ok = True
        guideId = db.create_customers(new_customer)
        if(guideId > 0):     
            customer_resp=[new_customer.serialize()]
            print(f"Se ha introducido el valor: {guideId}")
        else:
            print(f"No se ha introducido ningun valor")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")    

    return jsonify(customer_resp)


## get all customers
@app.route('/customers', methods=["GET"])
def API_get_customers():
    customers = []
    try:
        db.connect()
        conn_ok = True
        customers = db.get_customers()
        customer_list=[customer.serialize() for customer in customers]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(customer_list)





## get all employees
@app.route('/employees', methods=["GET"])
def API_get_employees():
    employees = []
    try:
        db.connect()
        conn_ok = True
        employees = db.get_employees()
        employee_list=[employee.serialize() for employee in employees]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(employee_list)


## get all employee types
@app.route('/employee_types', methods=["GET"])
def API_get_employee_types():
    employee_types = []
    try:
        db.connect()
        conn_ok = True
        employee_types = db.get_employees_types()
        employee_type_list=[employee_type.serialize() for employee_type in employee_types]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(employee_type_list)

## get all Wharehouses
@app.route('/wharehouses', methods=["GET"])
def API_get_wharehouses():
    wharehouses = []
    try:
        db.connect()
        conn_ok = True
        wharehouses = db.get_wharehouses()
        wharehouse_list=[wharehouse.serialize() for wharehouse in wharehouses]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(wharehouse_list)

## get all Brands
@app.route('/brands', methods=["GET"])
def API_get_brands():
    brands = []
    try:
        db.connect()
        conn_ok = True
        brands = db.get_brands()
        brand_list=[brand.serialize() for brand in brands]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(brand_list)

## get all brand types
@app.route('/brand_types', methods=["GET"])
def API_get_brand_types():
    brand_types = []
    try:
        db.connect()
        conn_ok = True
        brand_types = db.get_brands_types()
        brand_type_list=[brand_type.serialize() for brand_type in brand_types]  #serialize to prepare for json

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    return jsonify(brand_type_list)




if __name__ == '__main__':

    app.run(debug=True)
