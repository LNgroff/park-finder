"""Models for park finder app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creating tables

#  TODO: change the "ratings" in the postgresql
def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """A user"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer,
                primary_key = True,
                autoincrement = True)
    username = db.Column(db.String,
                unique = True)
    email = db.Column(db.String,
                unique = True)
    password db.Column(db.String)

    def __repr__(self):
        return f"""User user_id: {self.user_id}
                        username: {self.username}
                        email: {self.email}"""



class Park(db.Model):
    """A park"""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer,
                primary_key = True,
                autoincrement = True)
    park_name = db.Column(db.String,
                unique = True)
    address = db.Column(db.String,
                unique = True)
    coordinates = db.Column(db.Integer)
    url = db.Column(db.String,
                unique = True)
    description = db.Column(db.String)


    def __repr__(self):
        return f"""Park park_id: {self.park_id} 
                name: {self.name}
                address: {self.address}
                coordinates: {self.coordinates}
                url: {self.url}
                description: {self.description}"""

class Image(db.Model):
    """Images of a park"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    park_id = db.Column(db.Integer,
                    db.ForeignKey("parks.park_id"))
    url = db.Column(db.String,
                unique = True)
    
    park = db.relationship('Park', backref='images')

    def __repr__(self):
        return f"""Image image_id: {self.image_id} 
                park_id: {self.park_id}
                url: {self.url}
                park: {self.park}"""


class Favorite(db.Model):
    """A list of user's favorites"""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    park_id = db.Column(db.Integer,
                    db.ForeignKey("parks.park_id"))
    user_id = db.Column(db.Integer,
                    db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"""Favorite favorite_id: {self.favorite_id} 
                park_id: {self.park_id}
                user_id: {self.user_id}"""

    park = db.relationship('Park', backref='favorites')
    user = db.relationship('User', backref='favorites')


class Topics(db.Model):
    """A list of parks' topics"""

    __tablename__ = "topics"


    topic_id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    topic_name = db.Column(db.String,
                    unique = True)
    park_id db.Column(db.Integer,
                    db.ForeignKey("parks.park_id"))
    user_id = db.Column(db.Integer,
                    db.ForeignKey("users.user_id"))
    
    park = db.relationship('Park', backref='topics')
    user = db.relationship('User', backref='topics')
    

    def __repr__(self):
        return f"""Topic topic_id: {self.topic_id} 
                topic_name: {self.topic_name}
                park_id: {self.park_id}
                user_id: {self.user_id}"""

