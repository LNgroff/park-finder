"""Models for park finder app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

### See to do list at end of file.

#  TODO: change the "ratings" in the postgresql
def connect_to_db(flask_app, db_uri='postgresql:///parks', echo=True):
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
                autoincrement = True,
                nullable = False)
    uname = db.Column(db.String,
                unique = True,
                nullable = False)
    email = db.Column(db.String,
                unique = True,
                nullable = False)
    password = db.Column(db.String,
                nullable = False)

    # favorite = a list of Favorite objects


    def __repr__(self):
        return f"""User user_id: {self.user_id}
                        uname: {self.uname}
                        email: {self.email}"""



class Park(db.Model):
    """A park"""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer,
                primary_key = True,
                autoincrement = True,
                nullable = False)
    fullname = db.Column(db.String,
                unique = True,
                nullable = False)
    park_code = db.Column(db.String,
                unique = True,
                nullable = False)
    state = db.Column(db.String)
    url = db.Column(db.String,
                unique = True,
                nullable = False)
    description = db.Column(db.String)

    # image = list of Image objects
    # topic = list of Topic objects
    # favorite = list of Favorite objects

    # is this right?
    topic = db.relationship("Topic", secondary='park_topics' , backref="parks")


    def __repr__(self):
        return f"""Park park_id: {self.park_id} 
                fullname: {self.fullname}
                park_code: {self.park_code}
                state: {self.state}
                url: {self.url}
                description: {self.description}"""


class Topic(db.Model):
    """A list of parks' topics"""

    __tablename__ = "topics"


    topic_id = db.Column(db.String,
                primary_key = True,
                nullable = False)
    topic_name = db.Column(db.String,
                unique = True,
                nullable = False)
    
    park = db.relationship("Park", secondary='park_topics' , backref="topics")

    def __repr__(self):
        return f"""Topic topic_id: {self.topic_id}
                topic_name: {self.topic_name}"""
                # park_id: {self.park_id}"""

class ParkTopic(db.Model):
    """Topics of a specific park."""

    __tablename__ = 'park_topics'

    pktopic_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer,
                        db.ForeignKey('parks.park_id'),
                        nullable=False)
    topic_id = db.Column(db.Integer,
                        db.ForeignKey('topics.topic_id'),
                        nullable=False)



    
    def __repr__(self):
        return f"""Park topics pktopic_id: {self.pktopic_id} 
                park_id: {self.park_id}
                topic_id: {self.topic_id}"""


class Image(db.Model):
    """Images of a park"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer,
                primary_key = True,
                autoincrement = True,
                nullable = False)
    park_id = db.Column(db.Integer,
                db.ForeignKey("parks.park_id"),
                nullable = False)
    url = db.Column(db.String,
                unique = True,
                nullable = False)
    
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
                autoincrement = True,
                nullable = False)
    park_id = db.Column(db.Integer,
                db.ForeignKey("parks.park_id"),
                nullable = False)
    user_id = db.Column(db.Integer,
                db.ForeignKey("users.user_id"),
                nullable = False)


    def __repr__(self):
        return f"""Favorite favorite_id: {self.favorite_id} 
                park_id: {self.park_id}
                user_id: {self.user_id}"""

    park = db.relationship('Park', backref='favorites')
    user = db.relationship('User', backref='favorites')




if __name__ == '__main__':
    from server import app

    connect_to_db(app)


"""
TODO:

"""