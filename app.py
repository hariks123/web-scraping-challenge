from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars_data.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    
    mars = mongo.db.mars_data
    mdata = scrape_mars.scrape()
    print(mdata)
    #mars.insert_one(mdata)
    mars.update({}, mdata, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
