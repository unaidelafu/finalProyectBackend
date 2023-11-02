class Wharehouse:
      
      def __init__(self, id, name, location):
            self.id = id
            self.name =  name
            self.location = location

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'location': self.location
        }