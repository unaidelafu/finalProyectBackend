class Incoming_line:
      
      def __init__(self, id, ih_id, bike_id, bike_code, bike_desc, 
                   work_id, work_desc, product_id, product_desc, employee_id, 
                   employee_sid, time_start, time_end, note_id, note, status_id, status):
            self.id = id
            self.ih_id = ih_id
            self.bike_id =  bike_id
            self.bike_code = bike_code
            self.bike_desc =  bike_desc
            self.work_id = work_id
            self.work_desc =  work_desc                                          
            self.product_id = product_id      
            self.product_desc =  product_desc
            self.employee_id = employee_id
            self.employee_sid =  employee_sid           
            self.time_start = time_start        
            self.time_end = time_end   
            self.note_id = note_id
            self.note = note
            self.status_id = status_id    
            self.status = status            

      #serialize to prepare for json

      def serialize(self):
        return {
             
            'id': self.id,
            'ih_id': self.ih_id,
            'bike_id':  self.bike_id,
            'bike_code': self.bike_code,
            'bike_desc':  self.bike_desc,
            'work_id': self.work_id,
            'work_desc':  self.work_desc,                                          
            'product_id': self.product_id,      
            'product_desc':  self.product_desc,
            'employee_id': self.employee_id,
            'employee_sid':  self.employee_sid,
            'time_start': self.time_start,  
            'time_end': self.time_end,   
            'note_id': self.note_id,
            'note': self.note,
            'status_id': self.status_id,
            'status': self.status               
        }