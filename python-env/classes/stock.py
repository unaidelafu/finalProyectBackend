class stock:
    from classes import products as p
    def __init__(self, p, w_id, w_name, qty):
        self.p = p
        self.w_id = w_id
        self.w_name = w_name
        self.qty = qty


    #serialize to prepare for json

    def serialize(self):
        return {
            'id': self.p.id,
            'mp_id': self.p.mp_id, 
            'code': self.p.code,
            'name': self.p.name,
            'description': self.p.description,
            'size': self.p.size,
            'b_id': self.p.b_id,
            'b_name': self.p.b_name,
            'b_type_id': self.p.b_type_id,
            'b_type': self.p.b_type,
            'price': self.p.price,
            'img_url': self.p.img_url,            
            'w_id': self.w_id, 
            'w_name': self.w_name,
            'qty': self.qty,
        }