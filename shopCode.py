from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
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
    description = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    environmental_impact = db.Column(db.Integer, nullable=False)

@app.route("/")
def home():
    sort_by = request.args.get('sort_by')  # Get the 'sort_by' parameter from the URL query string

    if sort_by == 'price':
        products = Product.query.order_by(asc(Product.price)).all()
    elif sort_by == 'name':
        products = Product.query.order_by(asc(Product.name)).all()
    elif sort_by == 'environmental_impact':
        products = Product.query.order_by(desc(Product.environmental_impact)).all()
    else:
        products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/checkout", methods=["POST","GET"])
def checkout():
    if request.method == "POST":
        name = request.form['names']
        cardnum = request.form['cardnum']
        if not name or not cardnum:
             error_message = "PLEASE ENTER YOUR DETAILS"
             return render_template('checkout.html', error_message=error_message)
        if not cardnum.isdigit() or len(cardnum) != 16:
            error_message = "INCORRECT CARD NUMBER"
            return render_template('checkout.html', error_message=error_message)
        return f"<h1>THANKYOU FOR YOUR PURCHASE</h1>"
    else:
        return render_template("checkout.html")
    

@app.route("/basketpage")
def basket():
    return render_template("basketpage.html")

@app.route("/product/<int:product_id>")
def item(product_id):
    product = Product.query.get(product_id)
    return render_template("item.html", product=product)



@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if db.session.query(Product).count ==0:
            mouse = Product(name='RGB Mouse',description='The wired RGB mouse is designed for precise and responsive tracking, featuring an optical sensor with adjustable DPI settings. It has a comfortable ergonomic shape for extended use and customizable RGB lighting effects. With programmable buttons and onboard memory, users can tailor their gaming or productivity needs. The mouse also offers smooth gliding with a durable and tangle-free wired connection.',  picture = 'images/mouse.jpg', price = 39.99, environmental_impact = 1)
            keyboard = Product(name='RGB Keyboard',description='The wired RGB keyboard features a standard layout with 104 keys and a durable wired connection for reliable performance. It offers customizable RGB backlighting with dynamic effects, allowing users to personalize their lighting preferences. It includes multimedia keys, anti-ghosting technology, and a comfortable ergonomic design, enhancing typing and gaming experiences.', picture = 'images/keyboard.jpg', price = 89.99, environmental_impact = 2)
            headset = Product(name='RGB Headset',description='The wired RGB gaming headset delivers immersive audio with 7.1 surround sound and a noise-canceling microphone for crystal-clear communication. It features customizable RGB lighting effects to match your gaming setup. The headset offers comfort with adjustable headband and cushioned ear cups. Its wired connection ensures lag-free audio and compatibility with various devices.', picture = 'images/headset.jpg', price = 99.99, environmental_impact = 3)
            speakers = Product(name='RGB Speakers',description='RGB speakers feature a wired connection for high-quality audio output. They provide dynamic RGB lighting effects that sync with your music or can be customized to match your mood or setup. With multiple connectivity options, including Bluetooth and auxiliary input, they offer versatile compatibility. The speakers also come with intuitive controls and a compact design that blends seamlessly into any environment.', picture = 'images/speaker.jpg', price = 149.99, environmental_impact = 4)
            db.session.add_all([mouse,keyboard,headset,speakers])
            db.session.commit()

    app.run(debug=True)