__author__ = 'Suraj'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from trip_planner.models import Restaurant, Base, City, User, Hotel, Attraction, \
    UserRestaurantAssociation, UserAttractionAssociation, UserHotelAssociation, UserCityAssociation

engine = create_engine('sqlite:///tripplanner.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a few dummy users
User1 = User(user_name="Robo Tourista", email="robotour@tripper.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(user_name="Vinnie Voyager", email='vinnvoya@tripper.com',
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

User3 = User(user_name="Tommy Traveller", email='tommtrav@tripper.com',
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User3)
session.commit()

# Create a few cities
City1 = City(city_name="New York", state="New York", country="USA")
session.add(City1)
a1 = UserCityAssociation(trip_log="New York, so many places to eat! So many things to see! Loved the trip!")
a1.user = User1
a2 = UserCityAssociation(trip_log="We went to Grimaldi's for lunch during our brief visit")
a2.user = User2
a3 = UserCityAssociation(trip_log="I went there just for the Indian food")
a3.user = User3
City1.travelers.append(a1)
City1.travelers.append(a2)
City1.travelers.append(a3)
session.commit()

City2 = City(city_name="Boston", state="Massachussetts", country="USA")
session.add(City2)
a4 = UserCityAssociation(trip_log="Lot of history in this place")
a4.user = User1
a5 = UserCityAssociation(trip_log="Not many Indian restaurants here")
a5.user = User3
City2.travelers.append(a4)
City2.travelers.append(a5)
session.commit()

City3 = City(city_name="Fort Lauderdale", state="Florida", country="USA")
session.add(City3)
a6 = UserCityAssociation(trip_log="Ah the beaches")
a6.user = User1
a7 = UserCityAssociation(trip_log="Too many old people")
a7.user = User2
City3.travelers.append(a6)
City3.travelers.append(a7)
session.commit()

City4 = City(city_name="Bangalore", state="Karnataka", country="India")
session.add(City4)
a8 = UserCityAssociation(trip_log="Tech crowd")
a8.user = User2
a9 = UserCityAssociation(trip_log="South Indian food!")
a9.user = User3
City4.travelers.append(a8)
City4.travelers.append(a9)
session.commit()

# Create a few Restaurants
Restaurant1 = Restaurant(restaurant_name="Grimaldi's Pizza", city_id=1)
session.add(Restaurant1)
assoc1 = UserRestaurantAssociation(review="NY style pizzas!", rating=5)
assoc1.user = User1
Restaurant1.customers.append(assoc1)
assoc2 = UserRestaurantAssociation(review="Didn't care much about the food, was in a rush, slow and crowded", rating=2)
assoc2.user = User2
Restaurant1.customers.append(assoc2)
session.commit()

Restaurant2 = Restaurant(restaurant_name="Saravana Bhavan", city_id=1)
session.add(Restaurant2)
assoc3 = UserRestaurantAssociation(review="I love south Indian food", rating=5)
assoc3.user = User3
Restaurant2.customers.append(assoc3)
session.commit()

Restaurant3 = Restaurant(restaurant_name="Kashmir", city_id=2)
session.add(Restaurant3)
assoc4 = UserRestaurantAssociation(review="Good Indian food", rating=4)
assoc4.user = User3
Restaurant3.customers.append(assoc4)
session.commit()

Restaurant4 = Restaurant(restaurant_name="Fugakyu", city_id=2)
session.add(Restaurant4)
assoc5 = UserRestaurantAssociation(review="I like sushi!", rating=5)
assoc5.user = User1
Restaurant4.customers.append(assoc5)
session.commit()

Restaurant5 = Restaurant(restaurant_name="It's all greek to me", city_id=3)
session.add(Restaurant5)
assoc6 = UserRestaurantAssociation(review="Good for a quick and cheap bite", rating=4)
assoc6.user = User1
Restaurant5.customers.append(assoc6)
session.commit()

Restaurant6 = Restaurant(restaurant_name="Thai Spice", city_id=3)
session.add(Restaurant6)
assoc7 = UserRestaurantAssociation(review="Great ambience, good food", rating=5)
assoc7.user = User1
assoc8 = UserRestaurantAssociation(review="Went for dinner, too expensive", rating=2)
assoc8.user = User2
Restaurant6.customers.append(assoc7)
Restaurant6.customers.append(assoc8)
session.commit()

Restaurant7 = Restaurant(restaurant_name="Indraprastha", city_id=4)
session.add(Restaurant7)
assoc9 = UserRestaurantAssociation(review="I love south Indian food!", rating=5)
assoc9.user = User3
Restaurant7.customers.append(assoc9)
session.commit()

Restaurant8 = Restaurant(restaurant_name="CTR", city_id=4)
session.add(Restaurant8)
assoc10 = UserRestaurantAssociation(review="Took too much time to get a table", rating=2)
assoc10.user = User2
assoc11 = UserRestaurantAssociation(review="Best dosa in town!", rating=5)
assoc11.user = User3
Restaurant8.customers.append(assoc10)
Restaurant8.customers.append(assoc11)
session.commit()

