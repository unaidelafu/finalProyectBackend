class Status:
      
      def __init__(self, id, name):
            self.id = id
            self.name =  name

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }