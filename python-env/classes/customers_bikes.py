class Customer_bikes:
      
      def __init__(self, id, code, description, brand_id, brand, bike_type_id, bike_type, customer_id, customer,status):
            self.id = id
            self.code = code
            self.description =  description
            self.brand_id = brand_id
            self.brand =  brand
            self.bike_type_id = bike_type_id           
            self.bike_type = bike_type   
            self.customer_id = customer_id   
            self.customer = customer   
            self.status = status

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'code': self.code,
            'description': self.description,
            'brand_id': self.brand_id,
            'brand': self.brand,
            'bike_type_id': self.bike_type_id,          
            'bike_type': self.bike_type,    
            'customer_id': self.customer_id,     
            'customer': self.customer,   
            'status': self.status
        }