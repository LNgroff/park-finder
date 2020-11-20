"""CRUD operations."""

from model import db, Park, User, Image, Favorite, Topic, ParkTopic, connect_to_db
from sqlalchemy import text

# TODO: used or unused? 👍🏻
def create_user(email, password, uname):
    """Create and return a new user."""

    user = User(email=email, password=password, uname=uname)

    db.session.add(user)
    db.session.commit()

    return user

# TODO: used or unused? 👍🏻
def create_park(fullname, state, url, park_code, description):
    """Create and return a new park."""

    park = Park(fullname=fullname, 
                state=state, 
                url=url, 
                park_code=park_code,
                description=description)

    db.session.add(park)
    db.session.commit()

    return park

# TODO: used or unused? 👍🏻
def create_topic(topic_id, topic_name):

    topic = Topic(topic_id=topic_id, topic_name=topic_name)

    db.session.add(topic)
    db.session.commit()

    return topic

# TODO: used or unused? 👍🏻
def create_favorite(park_id, user_id):
    """Create and return a new favorite."""
    # do I need to change "user" here?

    favorite = Favorite(park_id=park_id,
                        user_id=user_id)

    db.session.add(favorite)
    db.session.commit()

    return favorite

# TODO: used or unused? 👍🏻
def create_image(park_id, url):
    """Create an image relating to a park"""

    image = Image(park_id=park_id, url=url)

    db.session.add(image)
    db.session.commit()

    return image

# TODO: used or unused? 👍🏻
def add_topics_to_park(park, topic):

    park.topic.append(topic)
    
    db.session.commit()

# TODO: used or unused? 
def return_all_topics():
    """Get list of all topics"""

    return Topic.query.all()

# TODO: used or unused? 
def return_all_users():
    """Get list of all users"""

    return User.query.all()

# TODO: used or unused?
def get_user_by_id(user_id):
    """Display user profile by user_id"""

    return User.query.get(user_id)

# TODO: used or unused? 👍🏻
def get_user_by_email(email):
    """Get user by email."""

    return User.query.filter(User.email == email).first()

# unlikely to actually use
# def get_user_by_uname(uname):
#     """Get user by uname."""

#     return User.query.filter(User.uname == uname).first()

# TODO: used or unused?
def get_topic_by_name(name) :
    """Get topic by name"""

    return Topic.query.filter(Topic.topic_name==name).first()


# TODO: used or unused?
def get_topic_by_topic_id(topic_id):
    """get topic by topic_id"""

    return Topic.query.filter(Topic.topic_id == topic_id).first()

# TODO: used or unused? 👍🏻
def get_park_image(park_id): 
    """Get image for a park by park_id"""

    # return Image.query.filter(Image.park_id == park_id).first()
    return Park.query.join(Image).filter(Park.park_id==park_id).first()

# TODO: used or unused? 👍🏻
# NOTE: need to replicate for no state
def get_park_image_topic(topic_id, userstate):

    # NOTE: Parsable, no images.
    return Park.query.filter(Park.state.contains(userstate))\
        .join(ParkTopic).filter(ParkTopic.topic_id==topic_id)\
        .join(Image).filter(Image.park_id == Park.park_id).all()

    # NOTE: Parsable, no images.
    return Park.query.filter(Park.state.contains(userstate))\
        .join(Image).filter(Image.park_id == Park.park_id)\
        .join(ParkTopic).filter(ParkTopic.topic_id==topic_id).all()

    # NOTE: Parsable, no images.
    return Park.query.filter(Park.state.contains(userstate))\
        .join(ParkTopic).filter(ParkTopic.topic_id==topic_id)\
        .join(Image).all()

    # NOTE: Not parsable, includes images.
    return db.session.query(Park, ParkTopic, Image)\
        .filter(Park.park_id == ParkTopic.park_id)\
        .filter(Park.park_id == Image.park_id)\
        .filter(Park.state.contains(userstate))\
        .filter(ParkTopic.topic_id == topic_id)

# TODO: used or unused? 👍🏻
# NOTE: grabs image too.
def get_parks_by_topic_id_image_nostate(topic_id):
    """Get park details by topic_id."""

    return Park.query.join(ParkTopic).filter(ParkTopic.topic_id==topic_id)\
        .join(Image).filter(Image.park_id == Park.park_id).all()


# TODO: used or unused? 👍🏻
def get_park_by_id(park_id):
    """Get park details by park_id."""

    return Park.query.get(park_id)

# TODO: used or unused?
def get_park_by_park_code(park_code):
    """Get park details by park_code."""

    return Park.query.get(park_code)

# TODO: used or unused?
def get_park_by_state(state):
    """Get park details by state."""

    return Park.query.get(state)

# TODO: used or unused? 👍🏻
# NOTE: Currently being rewritten to include image above.
def get_parks_by_topic_id_nostate(topic_id):
    """Get park details by topic_id."""

    return Park.query.join(ParkTopic).filter(ParkTopic.topic_id==topic_id).all()

# TODO: used or unused? 👍🏻
# NOTE: Currently being rewritten to include image above.
def get_park_by_topic_and_userstate(topic_id, userstate):

    # return Park.query.filter(Park.park_id==park_id and Park.state==state)
    # return Park.query.join(ParkTopic).filter((Park.state== userstate and ParkTopic.topic_id== topic_id)).all()
    # return Park.query().filter(userstate == Park.state).join(ParkTopic).filter(ParkTopic.topic_id==topic_id).all()
    return Park.query.filter(Park.state.contains(userstate)).join(ParkTopic).filter(ParkTopic.topic_id==topic_id).all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)  



"""
TODO:

Create a search function that searches by topic and state.
    - If topic within list (for selecting multiple topics at once)
    - Will need lots of if statements with and/or
    - does this go here or in server?
Option to include earch by multiple states at once?
How do I search by multiple topics?
Can I combine some functions so there isn't a so many functions?


"""