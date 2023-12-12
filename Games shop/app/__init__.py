from flask import Flask, render_template, request, redirect
from .forms import RegistrationForm, AddGameForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from datetime import datetime
from flask_caching import Cache

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, default="")
    email = db.Column(db.String(50), nullable=False, unique=True)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), db.ForeignKey("user.id"))
    price = db.Column(db.Integer, db.ForeignKey("post.id"))


@app.route("/admin", methods=["GET", "POST"])
def form():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect("/main_page")
    return render_template("form.html", form=form)


@app.route("/post/<int:id>", methods=["GET", "POST"])
@login_required
def page_2(id):
    p = Games.query.get(id)
    comments = Games.query.filter_by(post=id)
    form = AddGameForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        games = Games(name=name, description=description, price=price)
        db.session.add(games)
        db.session.commit()
        return redirect("/post")
    return render_template("addgames.html", post=p)


@app.route('/add_to_cart/<int:game_id>')
def add_to_cart(games_id):
    return redirect("/main_page")


@app.route('/cart')
def cart():
    return render_template('cart.html')