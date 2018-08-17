from flask import Flask, render_template, redirect, url_for
import pymongo
import scrape_mars

app = Flask(__name__)

#connecting to mongo, and initializing the database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB

@app.route("/")
def mainpage():
    #searching in mongo db for collection
    infolist = db.ScrapedCollection.find_one()
    #at initial start, ther will be no data, hence initializing with null
    if not infolist:
        infolist = {
            "news_title":None,
            "news_p":None,
            "featured_image_url":None,
            "mars_weather":None,
            "html_table":None,
            "hemisphere_image_urls":[None, None, None, None]
        }
    #flask is rendering html template, with variable infolist
    return render_template("index.html", infoList=infolist)
    
@app.route("/scrape")
def scrapeinfo():
    # call the scrape fucntion from scrape_mars.py
    MarsInfo = scrape_mars.scrape()

    #add the imformation to the mongo database
    db.ScrapedCollection.drop()
    db.ScrapedCollection.insert_one(MarsInfo)

    return redirect(url_for('mainpage'))


if __name__ == "__main__":
    app.run(debug=True)