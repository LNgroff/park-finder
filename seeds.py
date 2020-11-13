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

"""TODO: delete if loop for ids works.
topic_ids_only = "FB3641FE-67A3-4EC7-B9C4-0A0867776798,0D00073E-18C3-46E5-8727-2F87B112DDC6,
                    7F81A0CB-B91F-4896-B9A5-41BE9A54A27B,77B7EFDF-1A74-409C-8BA2-324EC919DB0E,
                    607D41B0-F830-4C07-A557-BCEF880A3929,BCE3ACBE-7871-495B-AEA3-5E19BC482405,
                    E25F3456-43ED-45DD-93BC-057F9B944F7A,46FC5CBD-9AD5-48F1-B4DA-1357031B1D2E,
                    DAAD7F5E-9112-45F2-9A27-DA51B639F27E,CDD8F34E-3BD4-425A-8264-4F0BA0DFBA38,
                    F79C1242-80FF-40F0-A0C1-5FFCBA172EC0,04A39AB8-DD02-432F-AE5F-BA1267D41A0D,
                    9F6A7003-59D6-4438-935F-760FD04C1073,41B1A0A3-11FF-4F55-9CB9-034A7E28B087,
                    F6D3A52E-608F-47D6-96DF-1FD64122A2FC,F0F97E32-2F29-41B4-AF98-9FBE8DAB36B1,
                    F16A7A2C-174D-4FD8-9203-8D8D8EAD644B,FBB14C45-1663-4714-9D28-B2B99874644D,
                    94262026-92F5-48E9-90EF-01CEAEFBA4FF,4BE01DC5-52E6-4F18-8C9A-B22D65965F6D,
                    66151063-AD2D-43C4-A385-5876B5AAD4F3,1CF1F6BB-A037-445B-8CF2-81428E50CE52,
                    101F4D51-F99D-45A6-BBB6-CD481E5FACED,F8C2FE93-DEB3-4B12-9A87-913E3E6B448D,
                    A7359FC4-DAD8-45F5-AF15-7FF62F816ED3,0E6D8503-CB65-467F-BCD6-C6D9E28A4E0B,
                    A155238F-0DD2-4610-9B87-05FCE1C59283,4244F489-6813-4B7A-9D0C-20CE098C8FFF,
                    9C9FCBB6-360B-4743-8155-6F9341CBE01B,CA07BC05-8FE3-4830-8041-14BC9B609A5F,
                    A86F34FB-BD6D-4D09-80CC-421B6113DF2E,5BE55D7F-BDB6-4E3D-AC35-2D8EBB974417,
                    90F8744F-CD10-4925-955C-064CB1A17EB0,5ED826E0-76BB-47BB-87DD-E081A72B0A04,
                    1365C347-952C-475A-B755-731DD523C195,B85866E2-0897-4000-9040-605CA335804F"
"""

with open('data/npsTopic.json') as f:
    topic_data = json.loads(f.read())

topics_in_db = []

# Loop through the topic dictionary to determine if they are available topics.
for topic in topics_data:
        # populate topic table
        db_topic = crud.create_topic(topic["id"], topic["name"])
        topics_in_db.append(db_topic)


ids_for_request = []

for topic in db_topic:
    ids_for_request.append(topic.nps_id)

""" Check indentation for this next part"""
id_list = ids_for_request.join(",")
    # url for request of parks using specific id pass the api key too
    topicparks_url = f"https://developer.nps.gov/api/v1/topics/parks?id={id_list}"

    # response object from URL
    topicparks_response = requests.get(topicparks_url)

    # converts the response object to a dictionary
    topicparks_dict = json.loads(topicparks_response.content)

topicparks_url = f"https://developer.nps.gov/api/v1/topics/parks?id={topic_ids_only}"
response = requests.get(topicparks_url)

with open('data/topicsParks.json','w') as fd:
    fd.write(response.content)

with open('data/topicParks.json') as f:
    topicPark_data = json.loads(f.read())

"""Ask about this part."""
parks_in_db = []
for topic in topicPark_data: # would this just be topic[park] 
    for parks in topic: # and then this line wouldn't be necessary?
        if parks[parkCode] not in db_park:
            db_park = crud.create_park(park['state'],
                            park['fullname'],
                            park['park_code'], 
                            park['url'])
                            # park['description'])
            parks_in_db.append(db_park)
        # TODO: Some parks have multiple states... How do I deal with that? do I need ANOTHER table?


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
