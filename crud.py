"""CRUD operations."""

from model import db, Park, User, Image, Favorite, Topic, ParkTopic, connect_to_db


def create_user(email, password, uname):
    """Create and return a new user."""

    user = User(email=email, password=password, uname=uname)

    db.session.add(user)
    db.session.commit()

    return user

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

def create_topic(nps_id, name):

    topic = Topic(nps_id=nps_id, topic_name=name)

    db.session.add(topic)
    db.session.commit()

    return topic


def create_favorite(park_id, user_id):
    """Create and return a new favorite."""
    # do I need to change "user" here?

    favorite = Favorite(park_id=park_id,
                        user_id=user_id)

    db.session.add(favorite)
    db.session.commit()

    return favorite

def create_image(park_id, url):
    """Create an image relating to a park"""

    image = Image(park_id=park_id, url=url)

    db.session.add(image)
    db.session.commit

def return_all_users():
    """Get list of all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Display user profile by user_id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email."""

    return User.query.filter(User.email == email).first()

# unlikely to actually use
# def get_user_by_uname(uname):
#     """Get user by uname."""

#     return User.query.filter(User.uname == uname).first()

def get_topic_by_name(topic_name) :
    """Get topic by name"""

    return Topic.query.filter(topic_name).first()

def get_topic_by_id(topic_id):
    """get topic by topic_id"""

    return Topic.query.get(topic_id)

def get_topic_by_nps_id(nps_id):
    """get topic by nps_id"""

    return Topic.query.filter(Topic.nps_id == nps_id).first()


def get_park_image(park_id):
    """Get image for a park by park_id"""

    return Image.query.get(park_id)

def get_park_by_id(park_id):
    """Get park details by park_id."""

    return Park.query.get(park_id)

def get_park_by_park_code(park_code):
    """Get park details by park_code."""

    return Park.query.get(park_code)

def get_park_by_state(state):
    """Get park details by state."""

    return Park.query.get(state)

def get_park_by_nps_id(nps_id):
    """Get park nps by topic_id."""

    return Topic.query.get(nps_id)

def get_park_list_by_topic(topic_id):
    """Gets a list of of parks """
    #TODO Join along topic_id
    return db.session.query(Topic).join(ParkTopic).all()

def get_park_by_topic_name(topic_id):
    """Get park details by topic_name."""

    return ParkTopics.query.get(topic_id)





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