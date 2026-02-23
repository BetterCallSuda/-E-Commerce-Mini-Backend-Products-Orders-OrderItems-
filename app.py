from flask import Flask
from models import db, User, Product, Order, OrderItem

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # ---------------------------
    # TEST DATA (Only runs once)
    # ---------------------------
    if not User.query.first():

        # Create User
        user1 = User(username="sudha", email="sudha@email.com")

        # Create Products
        product1 = Product(name="Laptop", price=1000, stock=10)
        product2 = Product(name="Mouse", price=50, stock=50)

        db.session.add_all([user1, product1, product2])
        db.session.commit()

        # Create Order
        order = Order(user=user1)

        item1 = OrderItem(order=order, product=product1, quantity=1)
        item2 = OrderItem(order=order, product=product2, quantity=2)

        db.session.add(order)
        db.session.commit()

        print("Database seeded successfully!")

@app.route("/")
def home():
    orders = Order.query.all()
    output = ""

    for order in orders:
        output += f"<h2>Order ID: {order.id}</h2>"
        output += f"<p>User: {order.user.username}</p>"
        output += f"<p>Total Price: {order.total_price}</p>"
        output += "<ul>"
        for item in order.items:
            output += f"<li>{item.product.name} - Quantity: {item.quantity}</li>"
        output += "</ul><hr>"

    return output


if __name__ == "__main__":
    app.run(debug=True)


