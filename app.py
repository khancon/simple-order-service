from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)

@app.route('/')
def index():
    return "Welcome to the Order Service API. Use /orders to get or add orders."

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": order.id, "product_id": order.product_id, "quantity": order.quantity} for order in orders])

@app.route('/orders', methods=['POST'])
def add_order():
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    new_order = Order(product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"id": new_order.id, "product_id": new_order.product_id, "quantity": new_order.quantity}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003)
