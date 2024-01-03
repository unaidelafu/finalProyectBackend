class Work_task:
      
      def __init__(self, id, name, time, price):
            self.id = id
            self.name =  name
            self.time = time
            self.price =  price            
      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'time': self.time, 
            'price': self.price            
        }