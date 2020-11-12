import os
import json
from random import choice, randint
from datetime import datetime
import us

import model
import crud
import server

# TODO: Do I want to drop it every time?
os.system('dropdb parks')
os.system('createdb parks')

# TODO: Is this different too?
model.connect_to_db(server.app)
model.db.create_all()


with open('data/npsTopic.json') as f:
    topic_data = json.loads(f.read())

topics_in_db = []

# Loop through the topic dictionary to determine if they are available topics.
for topic in topics_data:
    if topic['name'] in finder_topics:

        # populate topic table
        db_topic = crud.create_topic(topic['id'], topic['name'])
        topics_in_db.append(db_topic)

"""

Now I think I need to use those for get requests to populate parks.


# url for request for all possible topics.
topics_url = 'https://developer.nps.gov/api/v1/topics/'

# Response object from URL
topics_response = requests.get(topic_url)

# Converts the response objecto to a dictionary
topics_dict = json.loads(topics_response.content)

# Set of available topics:
finder_topics = set(["Ancient Seas", "Animals", "Archeology", "Arctic", 
        "Burial, Cemetery and Gravesite", "Canyons and Canyonlands",
        "Caves, Caverns and Karst", "Coasts, Islands and Atolls", 
        "Dams", "Dunes", "Estuaries and Mangroves", "Fire", 
        "Foothills, Plains and Valleys", "Forests and Woodlands",
        "Fossils and Paleontology", "Geology", "Geothermal", "Glaciers",
        "Grasslands", "Groundwater", "Impact Craters", "Lakes", "Mountains",
        "Natural Sounds", "Night Sky", "Oceans", "River and Riparian", 
        "Rock Landscapes and Features", "Scenic Views", "The Tropics",
        "Thickets and Shrublands", "Trails", "Volcanoes", "Waterfalls",
        "Wetlands", "Wilderness"])
"""


"""
# TODO: this changes, where does this come from??  
populating parks will need to be done case by case. Do I put a crud
function here? A crud function that gets a park by topic id
and then use that response to populate the parks table?

"""


topic_id = topic["topic_id"]

# url for request of parks using specific id
topicparks_url = f"https://developer.nps.gov/api/v1/topics/parks?id={topic_id}"

# response object from URL
topicparks_response = requests.get(topicparks_url)

# converts the response object to a dictionary
topicparks_dict = json.loads(topicparks_response.content)

parks_in_db = []

# TODO: how do I save these in a cache? Like a session?
for park in topicparks_dict:
    # TODO: if no decription, is that okay? how does that work?
    # TODO: Some parks have multiple states... How do I deal with that?
    db_park = crud.create_park(park['state'],
                            park['fullname'],
                            park['park_code'], 
                            park['url'])
                            # park['description'])
    
    parks_in_db.append(db_park)


"""
In order to populate images, I need to get the first image from the park
result. Would this be correct? And nest this under the above for loop?
Would I do something similar for state then? with an if loop?


for Park.park_code in db_park:
    parkget = f""https://developer.nps.gov/api/v1/parks?parkCode={Park.park_code}
    db_image = crud.create_image(Park.park_id, parkget[url])


"""


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)
    
    # for n in range(10):
    #     rand_park = choice(parks_in_db)
    #     score = randint(1, 5)

    #     rating = crud.create_rating(score, user, rand_park)
