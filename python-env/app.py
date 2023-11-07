from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import mariadb
import logging
import os
from datetime import date

from db_files import database
from classes import API_response as ar
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

# flask
app = Flask(__name__)
ma=Marshmallow(app) 

# directory
basedir = os.path.abspath(os.path.dirname(__file__))

# logging config
logname = f"{basedir}\\logs\\{date.today()}_app.log"

# filemode='a'      add
# filemode='w'      write 
logging.basicConfig(filename= logname, filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')
#logging.INFO()

@app.route('/')

def hello():
    logging.info('Hello flask')
    return "Hey Flask"


def API_json_resp(message,obj):
    if("Error" not in str(message)): 
        if(obj is not None):       
            resp=[obj.serialize()] 
            retval = ar.API_response("OK",resp).serialize()
        else:
            retval = ar.API_response("OK","").serialize()
    else:
        retval = ar.API_response("ERROR",message).serialize()
        logging.error('%s', message)
    return  jsonify(retval)    


##   --   endpoints    --    ##

##      --- Customers ---       ##

## get all customers
@app.route('/customers', methods=["GET"])
def API_get_customers():

    customers = []
    customers = db.get_customers(None)
    customer_list=[customer.serialize() for customer in customers]  #serialize to prepare for json
    return jsonify(customer_list)

## get one customer
@app.route('/customer/<id>', methods=["GET"])
def API_get_customer(id):

    customers = []
    customers = db.get_customers(id)
    customer_list=[customer.serialize() for customer in customers]  #serialize to prepare for json
    return jsonify(customer_list)

## create a customer:
@app.route('/customer', methods=["POST"])
def API_add_customer():

    customer_resp = None
    retval = None
    message = ""

    sid = request.json['sid']
    name_1 = request.json['name_1']
    name_2 = request.json['name_2']
    new_customer = c.Customer(None,sid,name_1,name_2,None)

    message = db.create_customer(new_customer)
    if("Error" not in str(message)): 
        new_customer.id = message
        new_customer.status = 'ACTIVE'
    return API_json_resp(message,new_customer)

## update a customer:
@app.route("/customer/<id>", methods=["PUT"])
def API_update_customer(id):

    retval = None
    message = ""
    structure = None


    sid = request.json['sid']
    name1 = request.json['name_1']
    name2 = request.json['name_2']
    status = request.json['status']
    upd_customer = c.Customer(id,sid,name1,name2,status)

    message = db.update_customer(upd_customer)

    return API_json_resp(message,upd_customer)

## Delete one customer
@app.route("/customer/<id>", methods=["DELETE"])
def API_delete_customer(id):

    message = db.delete_customer(id)
    return API_json_resp(message,None)

##      --- Employees ---       ##

## get all employees
@app.route('/employees', methods=["GET"])
def API_get_employees():
    employees = []
    
    employees = db.get_employees(None)
    employee_list=[employee.serialize() for employee in employees]  #serialize to prepare for json

    return jsonify(employee_list)

## get one employee
@app.route('/employee/<id>', methods=["GET"])
def API_get_employee(id):

    employees = []
    employees = db.get_employees(id)
    employee_list=[employee.serialize() for employee in employees]  #serialize to prepare for json
    return jsonify(employee_list)

## create a employee:
@app.route('/employee', methods=["POST"])
def API_add_employee():

    employee_resp = None
    retval = None
    message = ""

    sid = request.json['sid']
    name_1 = request.json['name_1']
    name_2 = request.json['name_2']
    job = request.json['job']
    img_url = request.json['img_url']

    new_employee = em.Employee(None,sid,name_1,name_2,None,job,None,img_url)

    message = db.create_employee(new_employee)
    if("Error" not in str(message)): 
        new_employee.id = message
        new_employee.status = 'ACTIVE'
    return API_json_resp(message,new_employee)

## update a employee:
@app.route("/employee/<id>", methods=["PUT"])
def API_update_employee(id):

    retval = None
    message = ""
    structure = None


    sid = request.json['sid']
    name_1 = request.json['name_1']
    name_2 = request.json['name_2']
    job = request.json['job']
    status = request.json['status']
    img_url = request.json['img_url']
    upd_employee = em.Employee(id,sid,name_1,name_2,status,job,None,img_url)
#   ---
    message = db.update_employee(upd_employee)

    return API_json_resp(message,upd_employee)

## Delete one employee
@app.route("/employee/<id>", methods=["DELETE"])
def API_delete_employee(id):

    message = db.delete_employee(id)
    return API_json_resp(message,None)

##      --- Employee types ---       ##

## get all employee types
@app.route('/employee_types', methods=["GET"])
def API_get_employee_types():
    employee_types = []

    employee_types = db.get_employee_types()
    employee_type_list=[employee_type.serialize() for employee_type in employee_types]  #serialize to prepare for json

    return jsonify(employee_type_list)


##      --- Wharehouse ---       ##

## get all Wharehouses
@app.route('/wharehouses', methods=["GET"])
def API_get_wharehouses():
    wharehouses = []

    wharehouses = db.get_wharehouses()
    wharehouse_list=[wharehouse.serialize() for wharehouse in wharehouses]  #serialize to prepare for json

    return jsonify(wharehouse_list)

##      --- brands ---       ##

## get all Brands
@app.route('/brands', methods=["GET"])
def API_get_brands():
    brands = []

    brands = db.get_brands()
    brand_list=[brand.serialize() for brand in brands]  #serialize to prepare for json

    return jsonify(brand_list)

## Delete one employee
@app.route("/brand/<id>", methods=["DELETE"])
def API_delete_brand(id):

    message = db.delete_brand(id)
    return API_json_resp(message,None)

##      --- brand types ---       ## 

## get all brand types
@app.route('/brand_types', methods=["GET"])
def API_get_brand_types():
    brand_types = []

    brand_types = db.get_brands_types()
    brand_type_list=[brand_type.serialize() for brand_type in brand_types]  #serialize to prepare for json

    return jsonify(brand_type_list)

##      --- Products ---       ## 

## get all products
@app.route('/products', methods=["GET"])

def API_get_products_all():
    products = []

    products = db.get_products_all(None)
    products_list=[products.serialize() for products in products]  #serialize to prepare for json

    return jsonify(products_list)

## get one product
@app.route('/product/<id>', methods=["GET"])
def API_get_product_all(id):

    products = []
    products = db.get_products_all(id)
    products_list=[products.serialize() for products in products]  #serialize to prepare for json
    return jsonify(products_list)

## Delete one product
@app.route("/product/<id>", methods=["DELETE"])
def API_delete_product(id):

    message = db.delete_product(id)
    return API_json_resp(message,None)


if __name__ == '__main__':

    app.run(debug=True)
