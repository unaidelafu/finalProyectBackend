class Employee_type:
      
      def __init__(self, id, name, admin):
            self.id = id
            self.name =  name
            self.admin = admin

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'admin': self.admin
        }