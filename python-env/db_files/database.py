# Module Imports
import mariadb
import sys
from classes import customers as c
from classes import employees as em
from classes import employee_types as emt
from classes import wharehouses as w
from classes import brands as b
from classes import brand_types as bt


class DbLoader:

    # Constructor
    def __init__(self, host, port, user, password, db_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = None

    # Abre la conexion con la db
    def connect(self):

        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name

        )

        #self.conn.autocommit(True)

    # Cierra la conexion con la db
    def disconnect(self):
        self.conn.close()

    def get_cursor(self):
        return self.conn.cursor()

    #aqui es donde comenzariamos a usar sentencias

    # customers:

    def get_customers(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT c_id, c_sid, c_name_1, c_name_2, c_status FROM customers WHERE c_id>=?",
                (1,))
            # Print Result-set
            for (id, sid, name1, name2, status) in cur:
                resultlist.append(c.Customer(id, sid, name1, name2, status))
                print(f"First Name: {name2}, Last Name: {name1}, with dni: {sid}")

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()
        return resultlist
    
    def create_customers(self, customer):
        cur = None
        query = "INSERT INTO customers (c_sid,c_name_1,c_name_2) VALUES (%s, %s, %s)"
        #query = f"INSERT INTO customers (c_sid,c_name_1,c_name_2) VALUES ('{sid}', '{name1}', '{name2}')"
        values = (customer.sid, customer.name_1, customer.name_2)
        id = 0
        try:
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            id = cur.lastrowid
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()
        return id
        
    # Employees

    def get_employees(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """select e.e_id, e.e_sid, e.e_name, e.e_surname, e.e_status, et.et_name , et.et_admin 
                from employees e 
                inner join employees_types et 
                on e.e_type_id = et.et_id 
                where 1""")
            # Print Result-set
            for (id,sid, name1, name2, status, job, admin) in cur:
                resultlist.append(em.Employee(id, sid, name1, name2, status, job, admin))
                #print(f"First Name: {e_name}, Last Name: {e_surname}, with dni: {e_sid}")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()        

        return resultlist
    # Employees types

    def get_employees_types(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """select et_id, et_name, et_admin 
                from employees_types
                where 1""")
            # Print Result-set
            for (id, name, admin ) in cur:
                resultlist.append(emt.Employee_type(id, name, admin))
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()                
        return resultlist
    #Wharehouse

    def get_wharehouses(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """select w_id, w_name, w_location 
                from wharehouses
                where 1""")
            # Print Result-set
            for (id, name, admin) in cur:
                resultlist.append(w.Wharehouse(id, name, admin))
                #print(f"Name: {w_name}, admin: {w_location}")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()   
        return resultlist
    #brands
    def get_brands(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """select b_id, b_name
                from brands
                where 1""")
            # Print Result-set
            for (id, name) in cur:
                resultlist.append(b.Brand(id, name))

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()       
        return resultlist
    #brand types  

    def get_brands_types(self):
        cur = None
        resultlist = []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """select bt_id, bt_type
                from brands_types
                where 1""")
            # Print Result-set
            for (id, name) in cur:
                resultlist.append(bt.Brand_type(id, name))
                
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()   
        return resultlist      

    #products - master product - brands - brand types

    def get_product_all(self):
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(
                """ select p.p_id, p.p_description, p.p_size, 
                    mp.mp_product_code, mp.mp_product_name, mp.mp_price, mp.mp_img_url, 
                    b.b_name, bt.bt_type  
                    from product p 
                    inner join master_product mp 
                    on p.p_mp_id = mp.mp_id 
                    inner join brands b 
                    on mp.mp_brand_id = b.b_id 
                    inner join brands_types bt 
                    on mp.mp_bt_id = bt.bt_id 
                    where 1 """)
            # Print Result-set  Resultado
            for (p_id, p_description) in cur:
                print(f"Name: {p_description}, admin: {p_id}")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:
            if cur is not None:
                cur.close()    