__author__ = 'Suraj'

from flask import Blueprint, render_template
from sqlalchemy import and_
from trip_planner.models import session, City, Hotel, Restaurant, Attraction, User, UserRestaurantAssociation, \
    UserAttractionAssociation, UserCityAssociation, UserHotelAssociation

mod = Blueprint('reviews', __name__, url_prefix='/reviews')

@mod.route('/restaurants/<int:restaurant_id>')
def show_restaurant_reviews(restaurant_id):
    reviews = session.query(UserRestaurantAssociation,
                            User.user_name,
                            UserRestaurantAssociation.review,
                            UserRestaurantAssociation.rating, User.id).\
        filter(and_(UserRestaurantAssociation.restaurant_id==restaurant_id,
                    User.id == UserRestaurantAssociation.user_id)).all()
    restaurant_name = session.query(Restaurant.restaurant_name).filter_by(id=restaurant_id).one()
    if restaurant_name:
        restaurant_name = restaurant_name[0]
    return render_template('reviews.html', name=restaurant_name, reviews=reviews)

@mod.route('/hotels/<int:hotel_id>')
def show_hotel_reviews(hotel_id):
    reviews = session.query(UserHotelAssociation,
                            User.user_name,
                            UserHotelAssociation.review,
                            UserHotelAssociation.rating, User.id).\
        filter(and_(UserHotelAssociation.hotel_id==hotel_id,
                    User.id == UserHotelAssociation.user_id)).all()
    hotel_name = session.query(Hotel.hotel_name).filter_by(id=hotel_id).one()
    if hotel_name:
        hotel_name = hotel_name[0]
    return render_template('reviews.html', name=hotel_name, reviews=reviews)

@mod.route('/attractions/<int:attraction_id>')
def show_attraction_reviews(attraction_id):
    reviews = session.query(UserAttractionAssociation,
                            User.user_name,
                            UserAttractionAssociation.review,
                            UserAttractionAssociation.rating, User.id).\
        filter(and_(UserAttractionAssociation.attraction_id==attraction_id,
                    User.id == UserAttractionAssociation.user_id)).all()
    attraction_name = session.query(Attraction.attraction_name).filter_by(id=attraction_id).one()
    if attraction_name:
        attraction_name = attraction_name[0]
    return render_template('reviews.html', name=attraction_name, reviews=reviews)

@mod.route('/cities/<int:city_id>')
def show_city_reviews(city_id):
    reviews = session.query(UserCityAssociation,
                            User.user_name,
                            UserCityAssociation.review,
                            UserCityAssociation.rating, User.id).\
        filter(and_(UserCityAssociation.hotel_id==city_id,
                    User.id == UserCityAssociation.user_id)).all()
    city_name = session.query(City.city_name).filter_by(id=city_id).one()
    if city_name:
        city_name = city_name[0]
    return render_template('reviews.html', name=city_name, reviews=reviews)

@mod.route('/users/<int:user_id>')
def show_user_contributions(user_id):
    user_name = session.query(User.user_name).filter_by(id=user_id).one()
    if user_name:
        user_name = user_name[0]
    city_reviews = session.query(UserCityAssociation,
                                 City.city_name,
                                 UserCityAssociation.review,
                                 UserCityAssociation.rating).\
        filter(and_(UserCityAssociation.user_id == user_id,
                    City.id == UserCityAssociation.city_id)).all()
    restaurant_reviews = session.query(UserRestaurantAssociation,
                                       Restaurant.restaurant_name,
                                       UserRestaurantAssociation.review,
                                       UserRestaurantAssociation.rating).\
        filter(and_(UserRestaurantAssociation.user_id == user_id,
                    Restaurant.id == UserRestaurantAssociation.restaurant_id)).all()
    attraction_reviews = session.query(UserAttractionAssociation,
                                       Attraction.attraction_name,
                                       UserAttractionAssociation.review,
                                       UserAttractionAssociation.rating).\
        filter(and_(UserAttractionAssociation.user_id == user_id,
                    Attraction.id == UserAttractionAssociation.attraction_id)).all()
    hotel_reviews = session.query(UserHotelAssociation,
                                  Hotel.hotel_name,
                                  UserHotelAssociation.review,
                                  UserHotelAssociation.rating).\
        filter(and_(UserHotelAssociation.user_id == user_id,
                    Hotel.id == UserHotelAssociation.hotel_id)).all()
    return render_template('user_contributions.html', city_reviews=city_reviews, restaurant_reviews=restaurant_reviews,
                           attraction_reviews=attraction_reviews, hotel_reviews=hotel_reviews, name=user_name)