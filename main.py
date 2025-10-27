from flask import Flask, render_template, \
    request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.secret_key = "test"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User: {self.name}"

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    is_complated = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task: {self.task} | User: {self.user_id}"


@app.route("/")
def index():
    name = session.get("name")
    if not name:
        return redirect(url_for("login"))
    return render_template("index.html", ism=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form.get("login")
        password = request.form.get("password")
        user = Users.query.filter_by(login=login, password=password).first()
        if user:
            session['name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        ism = request.form.get("ism")
        login = request.form.get("login")
        password = request.form.get("password")
        if not ism and not login and not password:
            return redirect(url_for("register"))
        try:
            user = Users(name=ism, login=login, password=password)
            db.session.add(user)
            db.session.commit()
            session['name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        except:
            print("xato")
            return redirect(url_for("register"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
