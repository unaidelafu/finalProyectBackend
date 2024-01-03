class Incoming_header:
      
      def __init__(self, id, client_id, client, employee_id, 
                   employee, note_id, note, date_in, date_out, price, status_id, status):
            self.id = id
            self.client_id = client_id
            self.client =  client
            self.employee_id = employee_id
            self.employee =  employee
            self.note_id = note_id        
            self.note = note      
            self.date_in =  date_in
            self.date_out = date_out        
            self.price = price      
            self.status_id = status_id    
            self.status = status            

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'client_id': self.client_id,
            'client': self.client,
            'employee_id': self.employee_id,
            'employee': self.employee,
            'note_id': self.note_id,          
            'note': self.note,    
            'date_in': self.date_in,
            'date_out': self.date_out,
            'price': self.price,
            'status_id': self.status_id,           
            'status': self.status            
        }