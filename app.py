import json
import time
from flask import Flask
from flask import render_template, request, redirect
from custom_tracker import customTracker 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

stocksList = ['Tesla', 'GameStop', 'AMD', 'Apple', 'Facebook', 'Netflix', 'Microsoft', 'Nvidia', 'Oracle', 'Tesla', 'Twitter', 'Visa', 'Walmart']
listOfDogs = ['Golden', 'Doxin']

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://collingilmore:Buddy20201995!!@cluster0.04dxl.mongodb.net/mydb?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route('/')
async def home():
    data = await get_data('./data/crypto_count.json')
    collection = mongo.db.ScrapedData
    post = collection.find_one(ObjectId('6233b1caa4a549ff574fcd27'))
    return render_template('index.jinja2', data=post)


@app.route('/custom-tracker-example')
async def custom_tracker():
    data = await get_data('./data/custom_count.json')
    return render_template('custom-tracker.jinja2', data=data)

@app.route('/custom-tracker-setup', methods=['POST', 'GET'])
async def custom_tracker_setup():
    if request.method == 'POST':
        scraped_data = mongo.db.ScrapedData
        print('POST Request received')
        # print(request.form)
        subName = request.form['subName']
        customName = request.form['customName']
        trackedWords = request.form['trackedWords']
        trackedWords = trackedWords.splitlines()
        days = 1
        print(trackedWords)
        data = customTracker(subName, trackedWords, days)
        post = formatPost(data, customName, subName)
        print(post)

        scraped_data.insert_one({'post': post})

        return render_template('custom-tracker-test.jinja2', data=data, subName=subName)
    else:
        print('get request')
        listOfWords = await generateWords()
        return render_template('custom-tracker-setup.jinja2',listOfWords=listOfWords)

@app.route('/getWords')
async def getWords():
    retDict = {}
    retDict['words'] = await generateWords()
    return retDict

@app.route('/customTrackers')
def profile_page():
    collection = mongo.db.ScrapedData
    trackers = collection.find()

    return render_template('customTrackers.jinja2', trackers=trackers)

@app.route('/customTracker/<ObjectId:id>')
def customTracker_page(id):
    collection = mongo.db.ScrapedData
    post = collection.find_one(id)
    return render_template('customTracker.jinja2', post=post)


async def get_data(file):
    with open(file) as f:
        data = json.load(f)
    return data

async def generateWords():
    with open('./services/word_generator/number.txt', 'w') as number_file:
        number_file.write("100")
    time.sleep(1)
    with open('./services/word_generator/random_words.txt', 'r') as word_file:
        lines = word_file.read().splitlines()
        print(len(lines))
    return lines

def formatPost(data, customName, subName):
    post = {
        'subName': subName,
        'customName': customName,
        'data': data
    }
    return post

if __name__ == '__main__':
    app.run(debug=True)
