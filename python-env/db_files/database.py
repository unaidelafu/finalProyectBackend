# Module Imports
import mariadb
import sys
from classes import customers as c
from classes import employees as em
from classes import employee_types as emt
from classes import wharehouses as w
from classes import brands as b
from classes import brand_types as bt
from classes import products as p
from classes import stock as s


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

    ##      --- Customers ---       ##

    def get_customers(self,id):
        
        cur = None      
        resultlist = []
        wherecon = " WHERE 1"
        if id is not None:
            wherecon = f" WHERE c_id = {id}"
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                """SELECT c_id, c_sid, c_name_1, c_name_2, c_mail, c_phone_num, c_city, c_status FROM customers""" 
                + wherecon + """ ORDER BY c_city, c_name_1, c_name_2 """ )
            
            # Print Result-set
            for (id, sid, name1, name2, mail, phone_num, city, status) in cur:
                resultlist.append(c.Customer(id, sid, name1, name2, mail, phone_num, city, status))
                #print(f"First Name: {name2}, Last Name: {name1}, with dni: {sid}")

        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return resultlist
    
    def create_customer(self, customer):

        cur = None
        retval = None

        query = "INSERT INTO customers (c_sid, c_name_1, c_name_2, c_mail, c_phone_num, c_city) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (customer.sid, customer.name_1, customer.name_2, customer.mail, customer.phone_num, customer.city)
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            retval = cur.lastrowid
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval


    def update_customer(self, customer):
        
        cur = None
        retval = ""

        query = """UPDATE customers
	                SET c_sid= %s, c_name_1= %s, c_name_2= %s, c_mail= %s, c_phone_num= %s, c_city= %s, c_status= %s
	                WHERE c_id= %s;""" 
        values = (customer.sid, customer.name_1, customer.name_2, customer.mail, customer.phone_num, customer.city,
                  customer.status,customer.id)
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect
        return retval


    def delete_customer(self,id):
        
        cur = None
        retval = ""
        query = f"DELETE FROM customers WHERE c_id= {id} "
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval    

    ##      --- Employees ---       ##

    def get_employees(self, id):

        cur = None
        resultlist = []
        wherecon = " WHERE 1"
        if id is not None:
            wherecon = f" WHERE e.e_id = {id}"
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                f"""select e.e_id, e.e_sid, e.e_name, e.e_surname, e.e_mail, e.e_phone_num, e.e_pswrd, e.e_status, et.et_id, et.et_name, et.et_admin, e.e_img_url 
                from employees e 
                inner join employees_types et 
                on e.e_type_id = et.et_id {wherecon} 
                ORDER BY e.e_status='ACTIVE', et.et_name, e.e_name, e.e_surname""")
            # Print Result-set
            for (id,sid, name1, name2,mail, phone_num, pswrd, status, jobId, job, admin,img_url) in cur:
                resultlist.append(em.Employee(id, sid, name1, name2, mail, phone_num, pswrd, status, jobId, job, admin, img_url))
                #print(f"First Name: {e_name}, Last Name: {e_surname}, with dni: {e_sid}")
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()        

        return resultlist
    
    def create_employee(self, employee):

        cur = None
        retval = None
        #Asumiendo que de la app se envia el id del job_type
        query = """INSERT INTO  employees (e_sid,e_name, e_surname, e_mail, e_phone_num, e_pswrd,e_type_id,e_img_url)
            VALUES (%s,%s,%s,%s,%s, password(%s),%s,%s);"""
        #query = f"INSERT INTO customers (c_sid,c_name_1,c_name_2) VALUES ('{sid}', '{name1}', '{name2}')"
        #job, admin,img_url
        values = (employee.sid, employee.name_1, employee.name_2, employee.mail, employee.phone_num, employee.pswrd, employee.job,employee.img_url)
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            retval = cur.lastrowid
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval

    def delete_employee(self,id):
        
        cur = None
        retval = ""
        query = f"DELETE FROM employees WHERE e_id= {id} "
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval    
    
    def update_employee(self, employee):
        
        cur = None
        retval = ""
        passQuery =""
        if(employee.pswrd!= None):
            passQuery = f" e_pswrd = password('{employee.pswrd}'),"
        
        query = """UPDATE employees
	                SET e_sid= %s, e_name= %s, e_surname= %s, e_mail = %s, e_phone_num = %s,""" + passQuery + """ e_type_id= %s,
                     e_status= %s, e_img_url= %s
	                WHERE e_id= %s;"""
        values = (employee.sid, employee.name_1, employee.name_2, employee.mail, employee.phone_num, employee.job,
                  employee.status,employee.img_url,employee.id)
        #id = 0
        #print(f"Query : {query}")
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect
        return retval

 
    ##      --- Employee Login ---       ##
    def check_employee_login(self, employee):

        cur = None
        resultlist = []
        query = """select e.e_id, e.e_sid, e.e_name, e.e_surname, e.e_mail, e.e_phone_num, e.e_pswrd, e.e_status, et.et_id, et.et_name, et.et_admin, e.e_img_url 
                from employees e 
                inner join employees_types et 
                on e.e_type_id = et.et_id 
                WHERE e.e_sid = %s and e.e_pswrd = password(%s) 
                and e.e_status = %s"""
        values = (employee.sid, employee.pswrd, employee.status)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            # Print Result-set
            for (id,sid, name1, name2, mail, phone_num, pswrd, status, jobId, job,admin,img_url) in cur:
                resultlist.append(em.Employee(id, sid, name1, name2, mail, phone_num, pswrd, status, jobId, job, admin, img_url))
                #print(f"First Name: {e_name}, Last Name: {e_surname}, with dni: {e_sid}")
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()        

        return resultlist

    ##      --- Employee Password ---       ##
    
    def update_employee_pswrd(self, employee):

        cur = None
        retval = ""

        query = """UPDATE employees
	                SET e_pswrd = password(%s)
	                WHERE e_id= %s;"""
        values = (employee.pswrd, employee.id)
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect
        return retval   

    ##      --- Employee types ---       ##
             
    def get_employee_types(self):
        cur = None
        resultlist = []
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                """select et_id, et_name, et_admin 
                from employees_types
                where 1""")
            # Print Result-set
            for (id, name, admin ) in cur:
                resultlist.append(emt.Employee_type(id, name, admin))
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()                
        return resultlist
    ##      --- Wharehouse ---       ##

    def get_wharehouses(self):
        cur = None
        resultlist = []
        try:
            self.connect()
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
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()   
        return resultlist
    ##      --- brands ---       ##
    def get_brands(self):
        cur = None
        resultlist = []
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                """select b_id, b_name
                from brands
                where 1 ORDER BY b_name""")
            # Print Result-set
            for (id, name) in cur:
                resultlist.append(b.Brand(id, name))

        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()       
        return resultlist

    def delete_brand(self,id):
        
        cur = None
        retval = ""
        query = f"DELETE FROM brands WHERE b_id= {id} "
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval      
    
    ##      --- brand types ---       ##  

    def get_brands_types(self):
        cur = None
        resultlist = []
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                """select bt_id, bt_type
                from brands_types
                where 1 ORDER BY bt_type""")
            # Print Result-set
            for (id, name) in cur:
                resultlist.append(bt.Brand_type(id, name))
                
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()   
        return resultlist      

    ##      --- products - master product - brands - brand types ---       ##
    def get_master_products(self):
        cur = None
        resultlist = []
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                f""" Select mp.mp_id, mp.mp_product_code, mp.mp_product_name, 
                    b.b_id, b.b_name, bt.bt_id, bt.bt_type, mp.mp_price, mp.mp_img_url  
                    from master_product mp 
                    inner join brands b 
                    on mp.mp_brand_id = b.b_id 
                    inner join brands_types bt 
                    on mp.mp_bt_id = bt.bt_id  WHERE 1 
                    order by bt.bt_type, mp.mp_product_code, mp.mp_product_name""")
            # Print Result-set  Resultado
            for (mp_id, code, name, b_id, b_name, b_type_id, b_type, price, img_url) in cur:
                resultlist.append(p.product(None, mp_id, code, name, None, None, b_id, b_name,b_type_id, b_type, price, img_url))

        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()       
        return resultlist       

    def create_edit_master_product(self, product):
        cur = None
        retval = None

        if(product.mp_id == None):
            query = """INSERT INTO master_product (mp_product_code, mp_product_name, mp_brand_id, mp_bt_id, mp_price, mp_img_url)
                VALUES (%s,%s,%s,%s,%s,%s);"""
            values = (product.code, product.name, product.b_id, product.b_type_id, product.price, product.img_url)
        else:
            query = """UPDATE  master_product SET mp_product_code = %s, mp_product_name = %s,
                    mp_brand_id = %s, mp_bt_id = %s, mp_price = %s, mp_img_url = %s
                    WHERE mp_id = %s"""
            values = (product.code, product.name, product.b_id, product.b_type_id, product.price, product.img_url, product.mp_id)           
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            if(product.mp_id == None):
                retval = cur.lastrowid
            else:
                retval = product.mp_id
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval

    def delete_master_product(self,id):
        #las foren keys saltaran si queda algun product
        cur = None
        retval = ""
        query = f"DELETE FROM master_product WHERE mp_id= {id} "
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval  

    def get_products_all(self, mp_id):
        cur = None
        resultlist = []
        wherecon = " WHERE 1"
        if mp_id is not None:
            wherecon = f" WHERE mp.mp_id = {mp_id}"
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                f""" Select p.p_id,mp.mp_id, mp.mp_product_code, mp.mp_product_name, 
                    p.p_description, p.p_size, b.b_id,
                    b.b_name, bt.bt_id, bt.bt_type, mp.mp_price, mp.mp_img_url  
                    from product p 
                    inner join master_product mp 
                    on p.p_mp_id = mp.mp_id 
                    inner join brands b 
                    on mp.mp_brand_id = b.b_id 
                    inner join brands_types bt 
                    on mp.mp_bt_id = bt.bt_id {wherecon} 
                    order by mp.mp_product_code, mp.mp_product_name, p.p_description, FIELD(p.p_size, 'XS', 'S', 'M', 'L', 'XL')""")
            # Print Result-set  Resultado
            for (p_id, mp_id, code, name, description, size, b_id, b_name, b_type_id, b_type, price, img_url) in cur:
                resultlist.append(p.product(p_id, mp_id, code, name, description, size, b_id, b_name,b_type_id, b_type, price, img_url))
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()    
        return resultlist
    
    def get_product_id(self, product):
        cur1 = None
        checkedId = None
        wherecon = ""            
        try:
            self.connect()
            cur1 = self.conn.cursor()
            query = f""" Select p_id, p_mp_id 
                    from product 
                    WHERE p_mp_id = {product.mp_id} and p_description = '{product.description}'
                    and p_size = '{product.size}'"""
            #print(f"Query : {query}")
            cur1.execute(
                f""" Select p_id, p_mp_id 
                    from product 
                    WHERE p_mp_id = {product.mp_id} and p_description = '{product.description}'
                    and p_size = '{product.size}'""")
            # Print Result-set  Resultado
            for (p_id,p_mp_id) in cur1:
                checkedId = p_id
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur1 is not None:
                cur1.close()    
        return checkedId
      
    def create_edit_product(self, product):
        cur = None
        retval = None
        idCheck = None

        if(product.id == None):
            #check if exist

            idCheck = self.get_product_id(product)
            if(idCheck != None):
                product.id = idCheck

            query = """INSERT INTO  product (p_mp_id, p_description, p_size)
                VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE p_mp_id = p_mp_id"""
            values = (product.mp_id, product.description, product.size)              
        else:
            query = """UPDATE  product SET p_mp_id = %s, p_description = %s,
                    p_size = %s WHERE p_id = %s"""
            values = (product.mp_id, product.description, product.size, product.id)                        
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid
            if(product.id == None):
                retval = cur.lastrowid
            else:
                retval = product.id
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval


    def create_edit_stock(self,stock,id):
        
        cur = None
        retval = None

        query = """INSERT INTO stock (s_w_id, s_p_id, s_qty) VALUES (%s,%s,%s)
        ON DUPLICATE KEY UPDATE s_qty = %s"""        

        values = (stock.w_id, id, stock.qty, stock.qty)                  
        #id = 0
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query,values)
            self.conn.commit() 
            #id = cur.lastrowid

            retval = cur.lastrowid

            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval

    def create_edit_product_old(self, product, p_id):
 
        cur = None
        retval = None
        resultlist = []
        mp_id = 0
        #check if master product exists.

        query = f"SELECT mp_id, mp_product_code from master_product where mp_product_code = '{product.code}' LIMIT 1"
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            for (id, code) in cur:
                mp_id = id
            print(f"mp ID: {mp_id}")
            if mp_id > 0:
                #Update changes
                query = """UPDATE  master_product 
                    SET mp_product_name = %s, mp_brand_id = %s,
                    mp_bt_id = %s, mp_price = %s, mp_img_url = %s
                    WHERE mp_product_code = %s"""
                values = (product.name, product.b_id, product.b_type_id, product.price, product.img_url,product.code)
                cur.execute(query,values)
                #---self.conn.commit()  
            else:
                #Create master product, get mp_id,
                query = """INSERT INTO  master_product (mp_product_code, mp_product_name, mp_brand_id,
                mp_bt_id, mp_price, mp_img_url)
                VALUES (%s,%s,%s,%s,%s,%s);"""
                values = (product.code, product.name, product.b_id, product.b_type_id, product.price, product.img_url)
                cur.execute(query,values)
                #---self.conn.commit() 
                mp_id = cur.lastrowid
            if p_id < 1:                
                # insert product
                query = """INSERT INTO  product (p_mp_id, p_description, p_size)
                VALUES (%s,%s,%s);"""
                values = (mp_id, product.description, product.size)   
                cur.execute(query,values)
                self.conn.commit() 
                #id = cur.lastrowid
                retval = cur.lastrowid    
            else:
                query = """UPDATE  product SET p_mp_id = %s, p_description = %s, p_size = %s
                WHERE p_id = %s"""
                values = (mp_id, product.description, product.size, p_id) 
                cur.execute(query,values)
                self.conn.commit() 
                #id = cur.lastrowid
                retval = p_id                   

        
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()
            self.disconnect()
        return retval
 
    def get_stock(self, mp_id):
        cur = None
        resultlist = []
        wherecon = " WHERE 1"
        productVar = None
        if mp_id is not None:
            wherecon = f" WHERE mp.mp_id = {mp_id}"
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(
                f""" Select p.p_id,mp.mp_id, mp.mp_product_code, mp.mp_product_name, 
                    p.p_description, p.p_size, b.b_id,
                    b.b_name, bt.bt_id, bt.bt_type, mp.mp_price, mp.mp_img_url, s.s_w_id, w.w_name, s.s_qty  
                    from stock s
                    inner join wharehouses w 
                    on w.w_id = s.s_w_id 
                    inner join product p 
                    on s_p_id = p_id
                    inner join master_product mp 
                    on p.p_mp_id = mp.mp_id 
                    inner join brands b 
                    on mp.mp_brand_id = b.b_id 
                    inner join brands_types bt 
                    on mp.mp_bt_id = bt.bt_id {wherecon} 
                    order by w.w_name, mp.mp_product_code, mp.mp_product_name, p.p_description, FIELD(p.p_size, 'XS', 'S', 'M', 'L', 'XL')""")
            # Print Result-set  Resultado
            for (p_id, mp_id, code, name, description, size, b_id, b_name, b_type_id, b_type, price, img_url, w_id, w_name, s_qty) in cur:
                productVar = p.product(p_id, mp_id, code, name, description, size, b_id, b_name,b_type_id, b_type, price, img_url)
                resultlist.append(s.stock(productVar,w_id, w_name, s_qty))               
        except mariadb.Error as e:
            print(f"Error - MariaDB : {e}")
        finally:
            if cur is not None:
                cur.close()    
        return resultlist     
    
    def delete_product(self,id):
        
        cur = None
        retval = ""
        query = f"DELETE FROM stock WHERE s_p_id= {id} "
        query2 = f"DELETE FROM product WHERE p_id= {id} "
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            cur.execute(query2)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval  

    def delete_stock_product(self,id,stock):
        
        cur = None
        retval = ""
        query = f"DELETE FROM stock WHERE s_p_id= {id} and s_w_id = {stock.w_id}"
        #values = (id)
        try:
            self.connect()
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit() 
            
        except mariadb.Error as e:
            self.conn.rollback()
            print(f"Error - MariaDB : {e}")
            retval = f"Error - MariaDB : {e}"
        finally:
            if cur is not None:
                cur.close()  
            self.disconnect()
        return retval      