import os
import json
from random import choice, randint
from datetime import datetime

import model
import crud
import server

os.system('dropdb parks')
os.system('createdb parks')

model.connect_to_db(server.app)
model.db.create_all()

# This is what needs to change. I need to find a way to save/get data.
with open('data/parks.json') as f:
    park_data = json.loads(f.read())


parks_in_db = []
for park in park_data:

    db_park = crud.create_park(park['park_name'], park['description'], park['address'], park['url'], park['coordinates'])
    
    parks_in_db.append(db_park)

for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)
    
    for n in range(10):
        rand_park = choice(parks_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(score, user, rand_park)