__author__ = 'Suraj'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class UserCityAssociation(Base):
    __tablename__ = 'user_city_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'), primary_key=True)
    user = relationship("User", back_populates="cities")
    city = relationship("City", back_populates="travelers")
    review = Column(String(400))
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <=5'))


class UserRestaurantAssociation(Base):
    __tablename__ = 'user_restaurant_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), primary_key=True)
    user = relationship("User", back_populates="restaurants")
    restaurant = relationship("Restaurant", back_populates="customers")
    review = Column(String(400))
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <=5'))


class UserHotelAssociation(Base):
    __tablename__ = 'user_hotel_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True)
    user = relationship("User", back_populates="hotels")
    hotel = relationship("Hotel", back_populates="guests")
    review = Column(String(400))
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <=5'))


class UserAttractionAssociation(Base):
    __tablename__ = 'user_attraction_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), primary_key=True)
    user = relationship("User", back_populates="attractions")
    attraction = relationship("Attraction", back_populates="visitors")
    review = Column(String(400))
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <=5'))


class User(Base):
    __tablename__ = 'user'

    user_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(30), nullable=False)
    picture = Column(String(300), nullable=True)
    cities = relationship("UserCityAssociation", back_populates="user")
    restaurants = relationship("UserRestaurantAssociation", back_populates="user")
    hotels = relationship("UserHotelAssociation", back_populates="user")
    attractions = relationship("UserAttractionAssociation", back_populates="user")

    @property
    def number_of_reviews(self):
        return len(self.cities) + len(self.restaurants) + len(self.hotels) + len(self.attractions)

    @property
    def serialize(self):
        return {
            'user_name': self.user_name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
            'cities': self.cities,
            'restaurants': self.restaurants,
            'hotels': self.hotels,
            'attractions': self.attractions
        }


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    travelers = relationship("UserCityAssociation", back_populates="city")
    restaurants = relationship("Restaurant", back_populates="city")
    hotels = relationship("Hotel", back_populates="city")
    attractions = relationship("Attraction", back_populates="city")

    @property
    def serialize(self):
        return {
            'city_name': self.city_name,
            'id': self.id,
            'state': self.state,
            'country': self.country,
            'travelers': self.travelers
        }


class Restaurant(Base):
    __tablename__ = 'restaurant'

    restaurant_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    customers = relationship("UserRestaurantAssociation", back_populates="restaurant")
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City")

    @property
    def rating(self):
        return session.query(func.avg(UserRestaurantAssociation.rating)).filter_by(restaurant_id=self.id).one()[0]

    @property
    def number_of_customers(self):
        return len(self.customers)

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'restaurant_name': self.restaurant_name,
            'id': self.id,
            'number_of_customers': self.number_of_customers,
            'city_id': self.city_id,
            'rating': self.rating
        }


class Hotel(Base):
    __tablename__ = 'hotel'

    hotel_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City")
    guests = relationship("UserHotelAssociation", back_populates="hotel")

    @property
    def serialize(self):
        return {
            'hotel_name': self.hotel_name,
            'id': self.id,
            'guests': self.guests,
            'rating': self.rating,
            'city_id': self.city_id
        }


class Attraction(Base):
    __tablename__ = 'attraction'

    id = Column(Integer, primary_key=True)
    attraction_name = Column(String(80), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City")
    visitors = relationship("UserAttractionAssociation", back_populates="attraction")

    @property
    def serialize(self):
        return {
            'attraction_name': self.attraction_name,
            'id': self.id,
            'rating': self.rating,
            'visitors': self.visitors,
            'city_id': self.city_id
        }


### insert at the end of the file ###
engine = create_engine('sqlite:///tripplanner.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()