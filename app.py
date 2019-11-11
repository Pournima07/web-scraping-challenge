from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask (__name__)

mongo = PyMongo(app,uri="mongodb://localhost:27017/scrape_mars")

@app.route("/")
def homepage():
	mars_listing_data = mongo.db.mars_listings.find_one()
	if mars_listing_data:
		return render_template('index.html', mars_listing = mars_listing_data )
	else:
		return redirect("/scrape",code =302)


@app.route('/scrape')
def scraper():

	mars_listings = mongo.db.mars_listings
	scraped_data = scrape_mars.scrape()
	mars_listings.update({}, scraped_data, upsert=True)
	return redirect("/",code =302)
	

if __name__ == "__main__":
	app.run (debug=False)
