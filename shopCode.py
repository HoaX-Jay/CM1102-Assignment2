from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] ='top secret!'
db_path = os.path.join(os.path.dirname(__file__), 'products.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False )
    description = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    environmental_impact = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products = products)

@app.route("/checkout", methods=["POST","GET"])
def checkout():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("user",usr=user))
    else:
        return render_template("checkout.html")

@app.route("/basket")
def basket():
    return render_template("basket.html")

@app.route("/product/<int:product_id>")
def item(product_id):
    print("Hello")
    product = Product.query.get(product_id)
    print("product ", product.id)
    return render_template("item.html", product=product)

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":

    

    with app.app_context():

        db.create_all()
        mouse = Product(name='RGB Mouse',description='Optical wired gaming mouse',  picture = 'images/mouse.jpg', price = 39.99, environmental_impact = "one")
        keyboard = Product(name='RGB Keyboard',description='Optical wired gaming keyboard', picture = 'images/keyboard.jpg', price = 89.99, environmental_impact = "two")
        headset = Product(name='RGB Headset',description='Wired gaming headset', picture = 'images/headset.jpg', price = 99.99, environmental_impact = "three")
        speakers = Product(name='RGB Speakers',description='Wired RGB speakers', picture = 'images/speaker.jpg', price = 149.99, environmental_impact = "four")



        db.session.add_all([mouse,keyboard,headset,speakers])
        db.session.commit()

    app.run(debug=True)