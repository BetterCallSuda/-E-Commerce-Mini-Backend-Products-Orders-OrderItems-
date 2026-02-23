from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ---------------------------
# USER MODEL
# ---------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    orders = db.relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


# ---------------------------
# PRODUCT MODEL
# ---------------------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    order_items = db.relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }


# ---------------------------
# ORDER MODEL
# ---------------------------
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")

    items = db.relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id}>"

    @property
    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items)

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "total_price": self.total_price,
            "items": [item.to_dict() for item in self.items]
        }


# ---------------------------
# ORDER ITEM MODEL
# ---------------------------
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem Order:{self.order_id} Product:{self.product_id}>"

    def to_dict(self):
        return {
            "product": self.product.name,
            "quantity": self.quantity,
            "price_per_unit": self.product.price
        }


