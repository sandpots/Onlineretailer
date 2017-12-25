from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.json_util import dumps
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__,static_url_path='')

app.config['MONGO_DBNAME'] = 'OnlineRetailer'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/OnlineRetailer'

mongo = PyMongo(app)


@app.route('/home',methods=['GET'])
def load_home_page():
	return app.send_static_file('Index.html')

@app.route('/search',methods=['GET'])
def load_search_page():
	return app.send_static_file('SearchRetailer.html')

@app.route('/Insert',methods=['GET'])
def load_insert_page():
	return app.send_static_file('Insert.html')

@app.route('/InsertRetailer',methods=['GET'])
def load_insert_Retailer_page():
	return app.send_static_file('InsertRetailer.html')

@app.route('/retailers',methods=['GET'])
def get_all_retailer():
	retldb = mongo.db.Retailer
	output =[]
	for retl in retldb.find():
		output.append(retl)
	return dumps(output)

@app.route('/findaretailer',methods=['POST'])
def get_retailer_zip():
	id = request.json['_id']
	retldb = mongo.db.Retailer
	output =[]
	result = retldb.find({"_id":id})
	for retl in result:
		output.append(retl)
		print(retl)
	return dumps(output)

@app.route('/insertretailer/',methods=['POST'])
def insert_retailer():
	retldb = mongo.db.Retailer
	Store_name = request.json['Store_name']
	Retailer_name = request.json['Retailer_name']
	phone = request.json['_id']
	zip = request.json['zip']
	retl_id = retldb.insert({"_id":phone, "Store_name" : Store_name,"Retailer_name" : Retailer_name,"zip" : zip})
	output = retldb.find_one({"_id":retl_id})
	return dumps(output)
	

@app.route('/insertproduct/',methods=['POST'])
def insert_product():
	retldb = mongo.db.Product
	Product_name = request.json['Product_name']
	Store_id = request.json['Store_id']
	product_qty = request.json['product_qty']
	prod_id = retldb.insert({"Product name" : Product_name,"Store_id" : Store_id,"product_qty" : product_qty})
	output = dumps(retldb.find({"Store_id":Store_id}))
	return output
	
@app.route('/deleteproduct/',methods=['POST'])
def delete_product():
	retldb = mongo.db.Product
	Product_id = request.json['Product_id']
	output =mongo.db.Product.delete({"_id":ObjectId(Product_id)})
	return output

	
@app.route('/insertcustomer/',methods=['POST'])
def insert_customer():
	retldb = mongo.db.Customer
	Customer_name = request.json['Customer name']
	phone = request.json['phone']
	zip = request.json['zip']
	cust_id = retldb.insert({"Customer name" : Customer_name,"phone" : phone,"zip" : zip})
	output = retldb.find_one({"_id":cust_id})
	return dumps(output)
	
@app.route('/findacustomer',methods=['POST'])
def get_customer_phone():
	phone = request.json['phone']
	retldb = mongo.db.Customer
	output =[]
	result = retldb.find({"phone":phone})
	for retl in result:
		output.append(retl)
	return dumps(output)	
	
@app.route('/removeacustomer',methods=['POST'])
def del_customer_phone():
	phone = request.json['phone']
	retldb = mongo.db.Customer
	output =[]
	result = retldb.remove({"phone":phone})
	for retl in result:
		output.append(retl)
	return dumps(output)
	
if __name__ == "__main__":
	app.run(host='0.0.0.0',port='5555')
