from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

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
from classes import products as p
from classes import stock as s

# **********
# CONSTS
# **********

# ---- Database values and connection
host = "127.0.0.1"
port = 3306
user = "root"
password = "2bEvImI2"
db_name = "bike_workshop"

## host = "f80b6byii2vwv8cx.chr7pe7iynqr.eu-west-1.rds.amazonaws.com"
## port = 3306
## user = "u7l4ee66qbm07jcv"
## password = "aplc9ipz6oihonph"
## db_name = "upewp1i7wez74gbs"

#db_name = "devcamp_university_course"
conn_ok = False

db = database.DbLoader(host, port, user, password, db_name)

# ---------

# flask
app = Flask(__name__)
CORS(app)       #CORS to allow external use sending JSON messages
cors = CORS(app, resources={r"/*": {"origins": "*"}})   #allows origin of message form everywhere NOT SECURE!!
ma=Marshmallow(app) 
print(f"Starting the app...")
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

    sid = request.json['sid'].upper()
    name_1 = request.json['name_1'].capitalize() 
    name_2 = request.json['name_2'].capitalize()
    mail = request.json['mail'].lower()
    phone_num = request.json['phone_num']
    city = request.json['city'].capitalize() 

    new_customer = c.Customer(None,sid,name_1,name_2,mail,phone_num,city,None)

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


    sid = request.json['sid'].upper()
    name_1 = request.json['name_1'].capitalize() 
    name_2 = request.json['name_2'].capitalize()
    mail = request.json['mail'].lower()
    phone_num = request.json['phone_num']
    city = request.json['city'].capitalize() 
    status = request.json['status']

    upd_customer = c.Customer(id,sid,name_1,name_2,mail,phone_num,city,status)

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

    sid = request.json['sid'].upper()
    name_1 = request.json['name_1'].capitalize() 
    name_2 = request.json['name_2'].capitalize()
    mail = request.json['mail'].lower()
    phone_num = request.json['phone_num']       
    pswrd = request.json['pswrd']
    jobId = None
    job = request.json['job']
    img_url = request.json['img_url']

    new_employee = em.Employee(None,sid,name_1,name_2,mail,phone_num,pswrd,None,jobId,job,None,img_url)

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

    sid = request.json['sid'].upper()
    name_1 = request.json['name_1'].capitalize() 
    name_2 = request.json['name_2'].capitalize()
    mail = request.json['mail'].lower()
    phone_num = request.json['phone_num']    
    pswrd = request.json['pswrd']
    if pswrd =="":
        pswrd = None
    job = request.json['job']
    jobId = None
    status = request.json['status']
    img_url = request.json['img_url']
    upd_employee = em.Employee(id,sid,name_1,name_2,mail,phone_num,pswrd,status,jobId,job,None,img_url)
#   ---
    message = db.update_employee(upd_employee)

    return API_json_resp(message,upd_employee)

## update a employee pswrd: (NOT USING)

@app.route("/employee-pswrd/<id>", methods=["PUT"])
def API_update_employee_pswrd(id):

    retval = None
    message = ""
    structure = None

    sid = None
    name_1 = None
    name_2 = None
    mail = None
    phone_num = None    
    jobId = None
    job = None
    status = None
    img_url = None
    pswrd = request.json['pswrd']
    upd_employee = em.Employee(id,sid,name_1,name_2,mail,phone_num,pswrd,status,jobId,job,None,img_url)
#   ---
    message = db.update_employee_pswrd(upd_employee)

    return API_json_resp(message,upd_employee)

## Delete one employee
@app.route("/employee/<id>", methods=["DELETE"])
def API_delete_employee(id):

    message = db.delete_employee(id)
    return API_json_resp(message,None)


##      --- Employee login ---       
# ##
@app.route('/employee-login', methods=["PUT"])
def API_get_employee_login():
    employees = []
    
    id = None
    sid = request.json['sid']
    name_1 = None
    name_2 = None
    mail = None
    phone_num = None
    jobId = None
    job = None
    status = 'ACTIVE'
    img_url = None
    pswrd = request.json['pswrd']
    pswrd_employee = em.Employee(id,sid,name_1,name_2,mail,phone_num,pswrd,status,jobId,job,None,img_url)
    employees = db.check_employee_login(pswrd_employee)
    if(employees == []):
        employees.append(pswrd_employee)
    employee_list=[employee.serialize() for employee in employees]  #serialize to prepare for json

    return jsonify(employee_list)
##      --- Employee types ---       ##

## get all employee types
@app.route('/employee-types', methods=["GET"])
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
@app.route('/brand-types', methods=["GET"])
def API_get_brand_types():
    brand_types = []

    brand_types = db.get_brands_types()
    brand_type_list=[brand_type.serialize() for brand_type in brand_types]  #serialize to prepare for json

    return jsonify(brand_type_list)

##      --- Products ---       ## 

## get all master products
@app.route('/master-products', methods=["GET"])

def API_get_master_products():
    products = []

    products = db.get_master_products()
    products_list=[products.serialize() for products in products]  #serialize to prepare for json

    return jsonify(products_list)

## Create master product
@app.route('/master-product', methods=["POST"])
def API_add_master_product():

    employee_resp = None
    retval = None
    message = ""
    mp_id = None
    code = request.json['code'].upper()
    name = request.json['name']
    description = None
    b_id = request.json['b_id']
    b_type_id = request.json['b_type_id']
    img_url = request.json['img_url']
    size = None
    price = request.json['price']

    new_product = p.product(None, mp_id, code, name, description, size, b_id, None, b_type_id, None, price, img_url)

    message = db.create_edit_master_product(new_product)
    if("Error" not in str(message)): 
        new_product.mp_id = message
    return API_json_resp(message,new_product)



##  Update Master product
@app.route('/master-product/<id>', methods=["PUT"])
def API_update_master_product(id):

    employee_resp = None
    retval = None
    message = ""
    mp_id = id
    code = request.json['code'].upper()
    name = request.json['name']
    description = None
    b_id = request.json['b_id']
    b_type_id = request.json['b_type_id']
    img_url = request.json['img_url']
    size = None
    price = request.json['price']

    updt_product = p.product(None, mp_id, code, name, description, size, b_id, None, b_type_id, None, price, img_url)

    message = db.create_edit_master_product(updt_product)

    return API_json_resp(message,updt_product)

## Delete one master product
@app.route("/master-product/<id>", methods=["DELETE"])
def API_delete_master_product(id):

    message = db.delete_master_product(id)
    return API_json_resp(message,None)


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

## create a product:
@app.route('/product', methods=["POST"])
def API_add_product():

    employee_resp = None
    retval = None
    message = ""

    #code = request.json['code'].upper()
    #name = request.json['name']
    mp_id = request.json['mp_id']
    description = request.json['description']    
    #b_type_id = request.json['b_type_id']
    #img_url = request.json['img_url']
    size = request.json['size'].upper()
    #price = request.json['price']
    wharehouse = request.json['wharehouse_id']
    qty = request.json['qty']

    new_product = p.product(None, mp_id, None, None, description, size, None, None, None, None, None, None)
    message = db.create_edit_product(new_product)

    if("Error" not in str(message)): 
        new_product.id = message
        new_product_stock = s.stock(new_product,wharehouse,None,qty)
        message = db.create_edit_stock(new_product_stock,message)        

    return API_json_resp(message,new_product)

## Update a product:
@app.route('/product/<id>', methods=["PUT"])
def API_update_product(id):

    employee_resp = None
    retval = None
    message = ""

    #code = request.json['code'].upper()
    #name = request.json['name']
    mp_id = request.json['mp_id']
    description = request.json['description']    
    #b_type_id = request.json['b_type_id']
    #img_url = request.json['img_url']
    size = request.json['size'].upper()
    #price = request.json['price']
    wharehouse = request.json['wharehouse_id']
    qty = request.json['qty']

    upd_product = p.product(int(id), int(mp_id), None, None, description, size, None, None, None, None, None, None)

    message = db.create_edit_product(upd_product)
    if("Error" not in str(message)): 
        upd_product.id = message
        upd_product_stock = s.stock(upd_product,wharehouse,None,qty)
        message = db.create_edit_stock(upd_product_stock,int(id))    
        
    return API_json_resp(message,upd_product)

## Delete one product
@app.route("/product/<id>", methods=["DELETE"])
def API_delete_product(id):

    message = db.delete_product(id)
    return API_json_resp(message,None)


## get one stock of mp
@app.route('/stock/<id>', methods=["GET"])
def API_get_product_stock(id):

    productsStock = []
    productsStock = db.get_stock(id)
    #print(f"Product stock: {productsStock}")
    products_list=[productStock.serialize() for productStock in productsStock]  #serialize to prepare for json
    return jsonify(products_list)

## Delete one stock of mp
@app.route('/stock/<id>/<w_id>', methods=["DELETE"])
def API_delete_stock_product(id,w_id):
    #wharehouse = request.json['wharehouse_id']    
    product_stock = s.stock(None,w_id,None,None)
    message = db.delete_stock_product(id, product_stock)
    return API_json_resp(message,None)


## get status
@app.route('/status', methods=["GET"])
def API_get_status():
    statuses = []

    statuses = db.get_status()
    status_list=[status.serialize() for status in statuses]  #serialize to prepare for json

    return jsonify(status_list)

## get bike_types
@app.route('/bike_types', methods=["GET"])
def API_get_bike_types():
    bike_types = []

    bike_types = db.get_bike_types()
    bike_types_list=[bike_type.serialize() for bike_type in bike_types]  #serialize to prepare for json

    return jsonify(bike_types_list)

## get work_tasks
@app.route('/work_tasks', methods=["GET"])
def API_get_work_tasks():
    work_tasks = []

    work_tasks = db.get_work_tasks()
    work_tasks_list=[work_task.serialize() for work_task in work_tasks]  #serialize to prepare for json

    return jsonify(work_tasks_list)

## get all customers_bikes
@app.route('/customers_bikes', methods=["GET"])
def API_get_customers_bikes():
    customers_bikes = []

    customers_bikes = db.get_customers_bikes(None, None)
    customers_bikes_list=[customer_bike.serialize() for customer_bike in customers_bikes]  #serialize to prepare for json

    return jsonify(customers_bikes_list)

## get customer_bike    cb_id
@app.route('/customer_bike/<id>', methods=["GET"])
def API_get_customer_bike(id):
    customer_bike = []

    customer_bike = db.get_customers_bikes(id, None)
    customer_bike_list=[bike.serialize() for bike in customer_bike]  #serialize to prepare for json

    return jsonify(customer_bike_list)

## get customer_bikes    cb_c_id
@app.route('/customer_bikes/<id>', methods=["GET"])
def API_get_customer_bikes(id):
    customer_bikes = []

    customer_bikes = db.get_customers_bikes(None, id)
    customer_bikes_list=[bike.serialize() for bike in customer_bikes]  #serialize to prepare for json

    return jsonify(customer_bikes_list)

## get incoming Header  
@app.route('/incoming_header/<id>', methods=["GET"])
def API_get_incoming_header(id):
    incoming_headers = []

    incoming_headers = db.get_incoming_headers(id, None)
    incoming_headers_list=[incoming_header.serialize() for incoming_header in incoming_headers]  #serialize to prepare for json

    return jsonify(incoming_headers_list)
## get incoming headers status
@app.route('/incoming_headers/<status>', methods=["GET"])
def API_get_incoming_headers(status):
    incoming_headers = []

    incoming_headers = db.get_incoming_headers(None, status)
    incoming_headers_list=[incoming_header.serialize() for incoming_header in incoming_headers]  #serialize to prepare for json

    return jsonify(incoming_headers_list)

## get incoming line  
@app.route('/incoming_line/<id>', methods=["GET"])
def API_get_incoming_line(id):
    incoming_lines = []

    incoming_lines = db.get_incoming_lines(id, None, None)
    incoming_line_list=[incoming_line.serialize() for incoming_line in incoming_lines]  #serialize to prepare for json

    return jsonify(incoming_line_list)
## get incoming lines status
@app.route('/incoming_lines/<status>', methods=["GET"])
def API_get_incoming_lines(status):
    incoming_lines = []

    incoming_lines = db.get_incoming_lines(None, None, status)
    incoming_line_list=[incoming_line.serialize() for incoming_line in incoming_lines]  #serialize to prepare for json

    return jsonify(incoming_line_list)

## get incoming lines h_id
@app.route('/incoming_lines_header/<id>', methods=["GET"])
def API_get_incoming_lines_header(id):
    incoming_lines = []

    incoming_lines = db.get_incoming_lines(None, id, None)
    incoming_line_list=[incoming_line.serialize() for incoming_line in incoming_lines]  #serialize to prepare for json

    return jsonify(incoming_line_list)

if __name__ == '__main__':

    app.run(debug=True)
