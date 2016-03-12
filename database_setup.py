__author__ = 'Suraj'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Table, CheckConstraint

Base = declarative_base()

user_city_association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('city_id', Integer, ForeignKey('city.id'))
)

class UserRestaurantAssociation(Base):

    __tablename__ = 'user_restaurant_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), primary_key=True)
    user = relationship("User", back_populates="restaurants")
    restaurant = relationship("Restaurant", back_populates="customers")


class UserHotelAssociation(Base):

    __tablename__ = 'user_hotel_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True)
    user = relationship("User", back_populates="hotels")
    hotel = relationship("Hotel", back_populates="guests")


class UserAttractionAssociation(Base):

    __tablename__ = 'user_attraction_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), primary_key=True)
    user = relationship("User", back_populates="attractions")
    attraction = relationship("Attraction", back_populates="visitors")


class User(Base):

    __tablename__ = 'user'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(30), nullable=False)
    picture = Column(String(300), nullable=True)
    cities = relationship(
        "City",
        secondary=user_city_association_table,
        back_populates="users")
    restaurants = relationship("UserRestaurantAssociation", back_populates="user")
    hotels = relationship("UserHotelAssociation", back_populates="user")
    attractions = relationship("UserAttractionAssociation", back_populates="user")

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
            'email' : self.email,
            'picture' : self.picture,
            'cities' : self.cities,
            'restaurants' : self.restaurants,
            'hotels' : self.hotels,
            'attractions' : self.attractions
        }


class City(Base):

    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    users = relationship(
        "User",
        secondary=user_city_association_table,
        back_populates="cities")

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
            'state' : self.state,
            'country' : self.country,
            'users' : self.users
        }


class Restaurant(Base):

    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    customers = relationship("UserRestaurantAssociation", back_populates="restaurant")
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <=5'))

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

       return {
           'name' : self.name,
           'id' : self.id,
           'customers' : self.customers,
           'city_id' : self.city_id,
           'rating' : self.rating
       }


class Hotel(Base):

    __tablename__ = 'hotel'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    guests = relationship("UserHotelAssociation", back_populates="hotel")
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <= 5'))

    @property
    def serialize(self):

        return {
            'name' : self.name,
            'id' : self.id,
            'guests' : self.guests,
            'rating' : self.rating,
            'city_id' : self.city_id
        }


class Attraction(Base):

    __tablename__ = 'attraction'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <= 5'))
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    visitors = relationship("UserAttractionAssociation", back_populates="attraction")

    @property
    def serialize(self):

        return {
            'name' : self.name,
            'id' : self.id,
            'rating' : self.rating,
            'visitors' : self.visitors,
            'city_id' : self.city_id
        }


### insert at the end of the file ###
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.create_all(engine)