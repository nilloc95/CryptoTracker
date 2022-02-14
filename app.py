import json
from flask import Flask
from flask import render_template, request, redirect
from custom_tracker import customTracker 

stocksList = ['Tesla', 'GameStop', 'AMD', 'Apple', 'Facebook', 'Netflix', 'Microsoft', 'Nvidia', 'Oracle', 'Tesla', 'Twitter', 'Visa', 'Walmart']
listOfDogs = ['Golden', 'Doxin']

app = Flask(__name__)

@app.route('/')
async def home():
    data = await get_data('./data/crypto_count.json')
    return render_template('index.jinja2', data=data)


@app.route('/custom-tracker-example')
async def custom_tracker():
    data = await get_data('./data/custom_count.json')
    # data = [{'name': 'Twitter', 'count': 12}, {'name': 'Twitter', 'count': 6}, {'name': 'Twitter', 'count': 2}]
    print(data)
    return render_template('custom-tracker.jinja2', data=data)

@app.route('/custom-tracker-setup', methods=['POST', 'GET'])
def custom_tracker_setup():
    if request.method == 'POST':
        print('POST Request received')
        # print(request.form)
        subName = request.form['subName']
        customName = request.form['customName']
        trackedWords = request.form['trackedWords']
        trackedWords = trackedWords.splitlines()
        days = 1
        print(trackedWords)
        data = customTracker(subName, trackedWords, days)
        return render_template('custom-tracker-test.jinja2', data=data, subName=subName)
    else:
        return render_template('custom-tracker-setup.jinja2', listOfDogs=listOfDogs, stocksList=stocksList)

@app.route('/profile')
def profile_page():
    return render_template('profile.jinja2')


@app.route('/favorites')
def profile():
    return render_template('favorites.jinja2')


async def get_data(file):
    with open(file) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(debug=True)
