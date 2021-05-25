from flask import Flask,request,jsonify
from product_service import ProductService

app = Flask(__name__)
service=ProductService()



@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Header']="Content-Type,Access-Control-Allow-Header,,"
    response.headers['Access-Control-Allow-Methods']="POST,GET,PUT,DELETE"
    return response

@app.route('/products',methods=['GET'])
def get_all_products():
    return jsonify(service.get_all())

@app.route('/products/<product_id>',methods=['GET'])
def get_product_by_id(product_id):
    return jsonify(service.get_by_product_id(product_id))

@app.route('/products',methods=['POST'])
def save_user():
    product_details = request.get_json()
    product_name = product_details["product_name"]
    product_brand = product_details["product_brand"]
    product_description = product_details["product_description"]
    product_price = product_details["product_price"]
    product_img = product_details["product_img"]
    return jsonify(service.create(product_name, product_brand, product_description, product_price, product_img))
          
    
@app.route('/products/<product_id>',methods=['PUT'])
def update_user_by_id(product_id):
    product_details = request.get_json()
    #product_id = product_details["product_id"]
    product_name = product_details["product_name"]
    product_brand = product_details["product_brand"]
    product_description = product_details["product_description"]
    product_price = product_details["product_price"]
    product_img = product_details["product_img"]
    return jsonify(service.update(product_id, product_name, product_brand, product_description, product_price, product_img))

@app.route('/products/<product_id>',methods=['DELETE'])
def delete_user_by_id(product_id):
    return jsonify(service.delete(product_id))


    
if __name__ == "__main__" :
    app.run(debug=True,port=5000)