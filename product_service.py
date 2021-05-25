from product_model import ProductModel

class ProductService:
    def __init__(self):
        self.model= ProductModel()

    def get_all(self):
        return self.model.get_all_products()

    def get_by_product_id(self, product_id):
        return self.model.get_product_by_id(product_id)
    
    def create(self,product_name, product_brand, product_description, product_price, product_img):
        return self.model.create_product(product_name, product_brand, product_description, product_price, product_img)

    def update(self, product_id, product_name, product_brand, product_description, product_price, product_img):
        return self.model.update_product(product_id, product_name, product_brand, product_description, product_price, product_img)

    def delete(self, product_id):
        return self.model.delete_product(product_id)