import os
import json
from random import choice, randint
from datetime import datetime
import us

import model
import crud
import server

os.system('dropdb parks')
os.system('createdb parks')

model.connect_to_db(server.app)
model.db.create_all()



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

topics_in_db = []

# Loop through the topic dictionary to determine if they are available topics.
for topic in topics_dict:
    if topic['name'] in finder_topics:

        # populate topic table
        db_topic = crud.create_topic(topic['id'], topic['name'])
        topics_in_db.append(db_topic)


topic_id = topic["topic_id"]

park_url = f"https://developer.nps.gov/api/v1/topics/parks?q={topic_id}

park_response = requests.get()


parks_in_db = []
for park in park_data:

    db_park = crud.create_park(park['park_name'], 
                            park['description'], 
                            park['state'], 
                            park['url'], 
                            park['coordinates'])
    
    parks_in_db.append(db_park)

for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)
    
    # for n in range(10):
    #     rand_park = choice(parks_in_db)
    #     score = randint(1, 5)

    #     rating = crud.create_rating(score, user, rand_park)
"""
Do I approach this similar to the pokemon berries problem listed below?
Is there a better approach to going about this?
Do I leave the data here, do I put it in a file?

jQuery.ajax({
    url: 'https://pokeapi.co/api/v2/berry/',
    type: 'GET',
    dataType: 'json',
    success: function(data){
        
        // console.log(data); // for testing
        let nameArray = data.results
        //console.log(nameArray)

        // looping through each item of the array and
        // getting the first value (the name)
        for (let name of nameArray) {
            let berry = name.name
            // console.log(name.name); // for testing
            $('#berries').append(berry + ", ");
            
            };

        }
    
});
"""