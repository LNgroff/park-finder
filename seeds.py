import os
import json
from random import choice, randint
from datetime import datetime
import us
from werkzeug.security import (generate_password_hash, check_password_hash)


import model
import crud
import server



os.system("dropdb parks")
os.system("createdb parks")


model.connect_to_db(server.app)
model.db.create_all()

# API_KEY = os.environ.get("API_KEY")

# request_url = f"https://developer.nps.gov/api/v1/parks?&api_key={{API_KEY}}"
# parks_response = request.get(request_url)

# with open("data/AllParks.json","w") as fd:
#     fd.write(parks_response.content)


# with open("data/parks.json") as f:
#     park_data = json.loads(f.read())

with open("data/allParks.json") as f:
    park_data = json.loads(f.read())

parks_in_db = []
topics_in_db = []
images_in_db = []
topics_dict = {}


with open("data/npsTopic.json") as n:
    topic_data = json.loads(n.read())

# populates topics in db
for topic in topic_data:
  
    topics_dict[topic["id"]] = crud.create_topic(topic["id"], topic["name"])

# populates parks in db
for park in park_data["data"]:
    db_park = crud.create_park(park["fullName"],
                park["states"],
                park["url"],
                park["parkCode"],
                park["description"])

    parks_in_db.append(db_park)

    # connects parks to topics
    for topic in park["topics"]:
        
        # Looking to see if the topic["id"] is in the local topic["nps"]
        if topic["id"] in topics_dict:

            db_topic = crud.add_topics_to_park(db_park, topics_dict[topic["id"]])

            topics_in_db.append(db_topic)

    # populates images in db
    for image in park["images"]:

        # if image == park["images"][0]:
        #     db_image = crud.create_image(db_park.park_id, image["url"])
        #     images_in_db.append(db_image)
        
        db_image = crud.create_image(db_park.park_id, image["url"])
        images_in_db.append(db_image)


# Test users
for n in range(10):
    email = f"user{n}@test.com"
    password = generate_password_hash(f"test{n}", method="sha256")
    uname = f"bob{n}"

    user = crud.create_user(email, password, uname)
    
