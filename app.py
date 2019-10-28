from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import jsonify

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), unique=False)
    item_description = db.Column(db.String(1000), unique=False)
    item_category = db.Column(db.String(30), unique=False)
    item_price = db.Column(db.Integer, unique=False)
    item_url = db.Column(db.String(1000), unique=False)

    def __init__(self, item_name, item_description, item_category, item_price, item_url):
        self.item_name = item_name
        self.item_description = item_description
        self.item_category = item_category
        self.item_price = item_price
        self.item_url = item_url

class ItemSchema(ma.Schema):
    class Meta: 
        fields = ('item_name', "item_description", "item_category", "item_price", "item_url")

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
    

if __name__ == '__main__':
    app.run(debug=True)