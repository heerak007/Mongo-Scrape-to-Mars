from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB

@app.route("/")
def mainpage():

    infolist = db.ScrapedCollection.find_one()

    return render_template("index.html", infoList=infolist)

@app.route("/scrape")
def scrapeinfo():
    # call the scrape fucntion
    MarsInfo = scrape_mars.scrape()
    
    db.ScrapedCollection.drop()
    db.ScrapedCollection.insert_one(MarsInfo)

    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)