from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# creat instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up a mongo connection
mongo = PyMongo(app)

# create route that renders index.html and finds documents from mongo
@app.route("/")
def home():

    # Find data
    info = mongo.db.collections.find()

    # return template and data
    return render_template("index.html", info=info)


# Route that will trigger scape funtions
@app.route("/scrape")
def scrape():

    #Run scraped function
    mars_1 = mission_to_mars(1).scrape_nasa()
    mars_2 = mission_to_mars(1).scrape_image()
    mars_3 = mission_to_mars(1).scrape_tweets()
    mars_4 = mission_to_mars(1).scrape_table()
    mars_5 = mission_to_mars(1).scrape_hemi()

    # Store results into a dictionary
    info = {
        "Title": mars_1["Article_title"],
        "Text": mars_1["Article_text"],
        "Featured Image URL": mars_2["featured_image_url"],
        "Weather": mars_3["mars_weather"],
        "Data Table": mars_4["Data_table"],
        "Hemisphere Images": mars_5["Hemisphere_images"]
    }

    # Insert info into database
    mongo.db.collection.insert_one(info)

    # Redirect back to homepage
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)