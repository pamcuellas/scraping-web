# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from dbconfig import dbname, dbuser, psswd, host, parameters


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# Or set inline
# mongodb+srv://mongorootuser:<password>@cluster0-mcbfw.mongodb.net/test?retryWrites=true&w=majority
connection_string ='mongodb+srv://' + dbuser + ':' + psswd + host + '/' + dbname + "?" + parameters 
mongo = PyMongo(app, uri=connection_string)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)