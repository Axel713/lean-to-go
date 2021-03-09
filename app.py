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
    tasks = list(mongo.db.pdca_tasks.find())
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
# register new user
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
        flash("Registration Complete!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # verify hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # if provided password does not match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # if provided username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # extracts the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    # verifies user's session (cookie) exists
    if session["user"]:
        return render_template("profile.html", username=username)

    # if user's session not found (cookie) return to login page
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have successfully logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add a task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        # sets "is_ongoing" variable on if truthy in form element
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        # build task dictionary from form
        task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        mongo.db.pdca_tasks.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_tasks"))

    # get categories from db
    categories = mongo.db.categories.find()
    return render_template("add_task.html", categories=categories)


# Edit a task
@app.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = mongo.db.pdca_tasks.find_one({"_id": ObjectId(task_id)})

    # get categories from db
    categories = mongo.db.categories.find()
    return render_template("edit_task.html", task=task, categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
