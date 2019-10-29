from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)

heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ltgosiwrqvfkku:c07bc1c6da70457391a7715c22230b635272781d8a50857d59e61cec6adf03f8@ec2-54-83-202-132.compute-1.amazonaws.com:5432/dbfiqe07rppc5k"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=False)
    cart_item = db.Column(db.Integer(), unique=False)

    def __init__(self, user_id, cart_item):
        self.user_id = user_id
        self.cart_item = cart_item

class CartSchema(ma.Schema):
    class Meta: 
        fields = ("id", 'user_id', "cart_item")

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

@app.route("/addToCart", methods=["POST"])
def add_to_cart():
    user_id = request.json['user_id']
    cart_item = request.json['cart_item']
    new_cart_item = Users(user_id, cart_item)
    
    db.session.add(new_cart_item)
    db.session.commit()
    
    print(new_cart_item, request)
    cart_item = Users.query.get(new_cart_item.id)

    return cart_schema.jsonify(cart_item)

    #  item = Items.query.get(new_item.id)

    # return item_schema.jsonify(item)

@app.route("/getcart/<user_id>", methods=["GET"])
def get_cart_items(user_id):
    all_items = Users.query.get(user_id)
    result = carts_schema.dump(all_items)

    return carts_schema.jsonify(result)

@app.route("/getallcarts", methods=["GET"])
def get_all_carts():
    all_items = Users.query.all()
    print(request)
    result = carts_schema.dump(all_items)
    print(result)

    return carts_schema.jsonify(result)

@app.route("/removeitem/<id>", methods=["DELETE"])
def remove_from_cart(id):
    item = Users.query.get(id)
    db.session.delete(item)
    db.session.commit()

    all_items = Users.query.all()
    result = result = carts_schema.dump(all_items)
    return carts_schema.jsonify(result)

    

class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), unique=False)
    item_description = db.Column(db.String(250), unique=False)
    item_category = db.Column(db.String(30), unique=False)
    item_price = db.Column(db.Integer, unique=False)
    item_url = db.Column(db.String(250), unique=False)

    def __init__(self, item_name, item_description, item_category, item_price, item_url):
        self.item_name = item_name
        self.item_description = item_description
        self.item_category = item_category
        self.item_price = item_price
        self.item_url = item_url

class ItemSchema(ma.Schema):
    class Meta: 
        fields = ("id", 'item_name', "item_description", "item_category", "item_price", "item_url")

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)



@app.route("/getitems", methods=["GET"])
def get_items():
    all_items = Items.query.all()
    result = items_schema.dump(all_items)

    return items_schema.jsonify(result)

@app.route("/item/<id>", methods=["GET"])
def get_item(id):
    item = Items.query.get(id)
    return item_schema.jsonify(item)

@app.route("/additem", methods=["POST"])
def add_guide():
    item_name = request.json['item_name']
    item_description = request.json['item_description']
    item_category = request.json['item_category']
    item_price = request.json['item_price']
    item_url = request.json['item_url'] 

    new_item = Items(item_name, item_description, item_category, item_price, item_url)

    db.session.add(new_item)
    db.session.commit()

    item = Items.query.get(new_item.id)

    return item_schema.jsonify(item)

@app.route("/removesaved/<id>", methods=["DELETE"])
def remove_saved_item(id):
    item = Items.query.get(id)
    db.session.delete(item)
    db.session.commit()

    all_items = Items.query.all()
    result = result = items_schema.dump(all_items)
    return carts_schema.jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True)