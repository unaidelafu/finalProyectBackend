class product:

    def __init__(self, id, code, name, description, size, b_id, b_name, b_type_id, b_type, price, img_url):
        self.id = id
        self.code = code
        self.name =  name
        self.description = description
        self.size = size
        self.b_id = b_id
        self.b_name = b_name
        self.b_type_id = b_type_id
        self.b_type = b_type
        self.price = price
        self.img_url = img_url

    #serialize to prepare for json

    def serialize(self):
        return {
            'id': self.id, 
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'b_id': self.b_id,
            'b_name': self.b_name,
            'b_type_id': self.b_type_id,
            'b_type': self.b_type,
            'price': self.price,
            'img_url': self.img_url
        }