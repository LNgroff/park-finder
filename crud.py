"""CRUD operations."""

from model import db, Park, User, Image, UserFavorite, Topic, connect_to_db


def create_user(email, password, username):
    """Create and return a new user."""

    user = User(email=email, password=password, username=username)

    db.session.add(user)
    db.session.commit()

    return user

def return_all_users():
    """Get list of all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Display user profile by user_id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Get user by username."""

    return User.query.filter(User.username == username).first()
    

def create_park(fullname, address, coordinates, url, description):
    """Create and return a new park."""

    park = Park(fullname=fullname, address=address, coordinates=coordinates, url=url, description=description)

    db.session.add(park)
    db.session.commit()

    return park

def return_all_parks():
    """Get list of all parks"""

    return Park.query.all()

def get_park_by_id(park_id):
    """Get park details by park_id."""

    return Park.query.get(park_id)

def get_park_by_state(state):
    """Get park details by state."""

    return Park.query.get(state)

# TODO: not sure how to do this one, but it's the lynch pin. Ask for help
def get_park_by_topic(topic_id):
    """Get park details by topic_id."""

    return Park.query.get(topic_id)


def get_park_by_topic(topic_name):
    """Get park details by topic_name."""

    return Park.query.get(topic_id)


def create_favorite(is_favorite, user, park):
    """Create and return a new favorite."""

    favorite = UserFavorite(is_favorite=is_favorite, user=user, park=park)

    db.session.add(favorite)
    db.session.commit()

    return favorite


if __name__ == '__main__':
    from server import app
    connect_to_db(app)



"""
TODO:

Create a search function that searches by topic and state.
    - If topic within list (for selecting multiple topics at once)
    - Will need lots of if statements with and/or
    - does this go here or in server?
Search by multiple states at once?
How do I search by multiple topics?
Can I combine some functions so there isn't a so many functions?


"""