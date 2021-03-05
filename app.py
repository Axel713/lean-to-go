import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
