from flask import Flask, render_template, request, session, escape, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/search")
def search():
    nickname = request.args.get("nickname")
    
    user = Users.query.filter_by(username=nickname).first()

    if user:
        return user.username

    return "El nombre de usuario no existe."

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(username=request.form["username"], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Te registraste satifactoriamente.", "success")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            flash("Hola " + user.username, "success")
            return render_template("home.html")
            #return "Abriste sesión correctamente."
        flash("Datos incorrectos, verifique y vuelva a intentarlo.", "success")

    return render_template("login.html")

@app.route("/home")
def home():
    if "username" in session:
        flash("Hola " + session["username"], "success")
        #return "Tu eres %s" % escape(session["username"])
    else:
        flash("Primero debse iniciar sesion", "success")
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop("username", None)

    return "Cerraste sesión correctamente"

app.secret_key = "54321"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
