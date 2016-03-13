__author__ = 'Suraj'

from flask import Blueprint, render_template
from trip_planner.models import session, City, Hotel, Restaurant, Attraction, User

mod = Blueprint('general', __name__)

@mod.route('/')
def showMainPage():
    return render_template('general.html')


@mod.route('/cities')
def showCities():
    cities = session.query(City).all()
    return render_template('cities.html', cities=cities)


@mod.route('/hotels')
def showHotels():
    hotels = session.query(Hotel).all()
    return render_template('hotels.html', hotels=hotels)


@mod.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)
    # results = (session.query(Restaurant.id, Restaurant.restaurant_name, City.city_name,).join(City)).all()
    # return render_template('restaurants.html', results=results)

@mod.route('/attractions')
def showAttractions():
    attractions = session.query(Attraction).all()
    return render_template('attractions.html', attractions=attractions)
