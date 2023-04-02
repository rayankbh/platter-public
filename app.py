from flask import Flask, render_template, request
import re
import requests
import random
from random import choice


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

#zip code validation (5 digit number)
def postalValid(zipcode):
    if not re.match(r"^\d{5}(-\d{4})?$", zipcode.strip()):
        return False
    return True


# Define a route for handling the form submission
@app.route('/', methods=['POST'])
def submit_zipcode():
    zipcode = request.form['zip']
    if postalValid(zipcode):
        # question page if the zipcode is valid
        return render_template('quiz.html', zipcode=zipcode)
    else:
        # error if the zipcode is invalid
        return render_template('error.html', message='Invalid zipcode')


YELP_API_KEY = 'XXXXXXXXX'
YELP_API_BASE_URL = 'https://api.yelp.com/v3/businesses/search'


def search_restaurants(category, location, limit=40):
    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}',
    }
    params = {
        'term': category,
        'location': location,
        'limit': limit,
    }

    response = requests.get(
        YELP_API_BASE_URL, headers=headers, params=params)
    businesses = response.json().get('businesses', [])

    # Filter restaurants with a rating of 3.5 or higher
    high_rated_businesses = [
        business for business in businesses if business['rating'] >= 3]

    # Randomly select 5 restaurants
    random_businesses = random.sample(
        high_rated_businesses, min(5, len(high_rated_businesses)))

    return random_businesses


@app.route('/results', methods=['POST'])
def get_restaurants():
    zipcode = request.form['zip']
    category = request.form.get('category', None)
    random_pick = request.form.get('random', None)

    if random_pick:
        categories = ['italian', 'chinese', 'mexican', 'indian', 'japanese', 'sushi', 'thai', 'korean', 'pizza', 'burgers', 'seafood']
        category = choice(categories)

    businesses = search_restaurants(category, zipcode)

    if random_pick:
        selected_restaurant = choice(businesses) if businesses else None
        return render_template('random_restaurant.html', restaurant=selected_restaurant, category= category)

    return render_template('results.html', restaurants=businesses)



if __name__ == '__main__':
    app.run(port=5500, debug=True)
