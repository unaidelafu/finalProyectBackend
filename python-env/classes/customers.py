class Customer:
      
      def __init__(self, id, sid, name_1, name_2, mail, phone_num, city, status):
            self.id = id
            self.sid = sid
            self.name_1 =  name_1
            self.name_2 = name_2
            self.mail =  mail
            self.phone_num = phone_num        
            self.city = city      
            self.status = status

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'sid': self.sid,
            'name_1': self.name_1,
            'name_2': self.name_2,
            'mail': self.mail,
            'phone_num': self.phone_num,          
            'city': self.city,    
            'status': self.status
        }
      
