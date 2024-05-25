from flask import Flask, render_template, redirect, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
#privet levan rogor xar? nichevo brat tavad
from utils import check_in_session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Nigger Jail"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    budget = db.Column(db.Integer)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Integer)
    name = db.Column(db.String(30))
    image = db.Column(db.String(500))



@app.route("/")
def products(): 
    return render_template("product.html", queryset = Product.query.all(), check_in_session = check_in_session)

@app.route("/products", methods=["POST"])
def add_products():
    name = request.form["name"]
    price = request.form["price"]
    image = request.files["image"]
    if image.filename == "":    
        return "No selected file"
    
    filename = "".join(image.filename.split())
    image.save(os.path.join("static", filename))
    full_path = os.path.join("static", filename)

    product = Product(name=name, price=price, image=full_path)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for("products"))



@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    print(role)
    if role == "Admin":
        user = User(username=username, password=password, is_admin=True)
    else:
        user = User(username=username, password=password, is_admin=False)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("login"))



@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = {'id': user.id, "is_admin": user.is_admin } 
        session.modified = True
        return redirect(url_for("products"))
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    del session["user"]
    session.modified = True
    return redirect(url_for("products"))



if "__main__" == __name__:
    with app.app_context():
        db.create_all()
    app.run(debug=True)
