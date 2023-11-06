class API_response:
    def __init__(self, status, message):
        self.status = status
        self.message =  message

      #serialize to prepare for json

    def serialize(self):
        return {
            'status': self.status, 
            'message': self.message
        }