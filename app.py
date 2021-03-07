import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Database configuration/Get database name
app.config["MONGODB_NAME"] = os.environ.get("MONGO_DBNAME")
# Database configuration/Get database string
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Flask configuration/Get secret key
app.secret_key = os.environ.get("SECRET_KEY")
# Database configuration/Pymongo instance
mongo = PyMongo(app)


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.pdca_tasks.find()
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # if username already exists, return to register page to try again
        if existing_user:
            flash("Username not available")
            return render_template(url_for("register"))

        # if username not taken, add to db
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # set user in session
        session["user"] = request.form.get("username").lower()
        flash("Registration complete!")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
