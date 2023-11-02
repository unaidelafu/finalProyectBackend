class Customer:
      
      def __init__(self, id, sid, name_1, name_2, status):
            self.id = id
            self.sid = sid
            self.name_1 =  name_1
            self.name_2 = name_2
            self.status = status

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'sid': self.sid,
            'name_1': self.name_1,
            'name_2': self.name_2,
            'status': self.status
        }
      
