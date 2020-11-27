"""CRUD operations."""

from model import db, Park, User, Image, Favorite, Topic, ParkTopic, connect_to_db
from sqlalchemy import text


# USER FUNCTIONS
# TODO: used or unused? 👍🏻
def create_user(email, password, uname):
    """Create and return a new user."""

    user = User(email=email, password=password, uname=uname)

    db.session.add(user)
    db.session.commit()

    return user

# TODO: used or unused? 
def return_all_users():
    """Get list of all users"""

    return User.query.all()

# TODO: used or unused? 👍🏻
def get_user_by_id(user_id): 
    """Display user profile by user_id"""

    return User.query.get(user_id)

# TODO: used or unused? 👍🏻
def get_user_by_email(email):
    """Get user by email."""

    return User.query.filter(User.email == email).first()

# TODO: used or unused? 👎🏻
# unlikely to actually use
def get_user_by_uname(uname):
    """Get user by uname."""

    return User.query.filter(User.uname == uname).first()



# PARK FUNCTIONS

# TODO: used or unused? 👍🏻
def create_park(fullname, state, url, park_code, description):
    """Create and return a new park."""

    park = Park(fullname=fullname, 
                state=state, 
                park_url=url, 
                park_code=park_code,
                description=description)

    db.session.add(park)
    db.session.commit()

    return park


# TODO: used or unused? 👍🏻
def get_parktopic_image(topic_id, userstate):
    """Get parks by topic and state, include image"""

    park_image_state = db.session.query(Park, ParkTopic, Image)\
        .filter(Park.park_id == ParkTopic.park_id)\
        .filter(Park.park_id == Image.park_id)\
        .filter(Park.state.contains(userstate))\
        .filter(ParkTopic.topic_id == topic_id).all()

    # print(park_image_state)
    
    return [q._asdict() for q in park_image_state]

# TODO: used or unused? 👍🏻
def get_parktopic_image_nostate(topic_id):
    """Get park by topic_id but no state, include image."""

    park_image_nostate = db.session.query(Park, ParkTopic, Image)\
        .filter(Park.park_id == ParkTopic.park_id)\
        .filter(Park.park_id == Image.park_id)\
        .filter(ParkTopic.topic_id == topic_id).all()
    
    return [q._asdict() for q in park_image_nostate]

# TODO: used or unused? 👍🏻
def get_park_notopic_bystate(userstate):
    """Get park by state but no topic, include image."""

    park_image_nostate = db.session.query(Park, Image)\
        .filter(Park.state.contains(userstate))\
        .filter(Park.park_id == Image.park_id).all()
    
    return [q._asdict() for q in park_image_nostate]


# TODO: used or unused? 👍🏻
def get_park_by_id(park_id):
    """Get park details by park_id with image."""

    return db.session.query(Park, Image).join(Image)\
        .filter(Image.park_id == park_id).first()

# TODO: used or unused? 👍🏻
def get_parkimage_by_id(park_id):
    """Get park details by park_id with image."""

    # return db..session.query(Favorite, Park).join

    return Image.query.filter(Image.park_id == park_id).first()


# TODO: used or unused? 👎🏻
def get_park_by_park_code(park_code):
    """Get park details by park_code."""

    return Park.query.get(park_code)

# TODO: used or unused? 👎🏻
def get_park_by_state(state):
    """Get park details by state."""

    return Park.query.get(state)



#TOPIC FUNCTIONS

# TODO: used or unused? 👍🏻
def create_topic(topic_id, topic_name):

    topic = Topic(topic_id=topic_id, topic_name=topic_name)

    db.session.add(topic)
    db.session.commit()

    return topic

# TODO: used or unused? 
def return_all_topics():
    """Get list of all topics"""

    return Topic.query.all()
    

# TODO: used or unused?
def get_topic_by_name(name) :
    """Get topic by name"""

    return Topic.query.filter(Topic.topic_name==name).first()


# TODO: used or unused?
def get_topic_by_topic_id(topic_id):
    """get topic by topic_id"""

    return Topic.query.filter(Topic.topic_id == topic_id).first()



# FAVORITE FUNCTIONS

# TODO: used or unused? 👍🏻
def create_favorite(park_id, user_id):
    """Create and return a new favorite."""
    # do I need to change "user" here?

    favorite = Favorite(park_id=park_id,
                        user_id=user_id)

    db.session.add(favorite)
    db.session.commit()

    return favorite

# TODO: used or unused?
def get_user_favs(user_id) :
    """Get a dictionary of user favorites."""

    favorite_park = db.session.query(Park, Favorite, Image)\
        .filter(Park.park_id == Favorite.park_id)\
        .filter(Park.park_id == Image.park_id)\
        .filter(Favorite.user_id == user_id).all()

    return [q._asdict() for q in favorite_park]

def user_favs_by_park(user_id, park_id):
    """Get specific park from user favorites """

    return Favorite.query.filter(Favorite.user_id == user_id, Favorite.park_id == park_id).first()



# IMAGE FUNCTIONS    

# TODO: used or unused? 👍🏻
def create_image(park_id, image_url):
    """Create an image relating to a park"""

    image = Image(park_id=park_id, image_url=image_url)

    db.session.add(image)
    db.session.commit()

    return image

# TODO: used or unused? 👎🏻
def get_park_image(park_id): 
    """Get image for a park by park_id"""

    return Image.query.filter(Image.park_id == park_id).all()
    
    # images = db.session.query(Image)\
    #     .filter(Image.park_id == park_id).all()

    # return [q._asdict() for q in images]


# PARKTOPIC FUNCTIONS

# TODO: used or unused? 👍🏻
def add_topics_to_park(park, topic):

    park.topic.append(topic)

    db.session.commit()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)  


