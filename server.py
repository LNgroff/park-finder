"""Server for park finder app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from model import connect_to_db
import crud
import os
import us
import secrets
from sqlalchemy import text
import json

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined

# OPT_TOPICS = ["Ancient Seas", "Animals", "Archeology", "Arctic", 
#         "Burial, Cemetery and Gravesite", "Canyons and Canyonlands",
#         "Caves, Caverns and Karst", "Coasts, Islands and Atolls", 
#         "Dams", "Dunes", "Estuaries and Mangroves", "Fire", 
#         "Foothills, Plains and Valleys", "Forests and Woodlands",
#         "Fossils and Paleontology", "Geology", "Geothermal", "Glaciers",
#         "Grasslands", "Groundwater", "Impact Craters", "Lakes", "Mountains",
#         "Natural Sounds", "Night Sky", "Oceans", "River and Riparian", 
#         "Rock Landscapes and Features", "Scenic Views", "The Tropics",
#         "Thickets and Shrublands", "Trails", "Volcanoes", "Waterfalls",
#         "Wetlands", "Wilderness"]

# with open("data/npsTopic.json") as n:
#     OPT_TOPICS = json.loads(n.read())


STATES = us.states.STATES_AND_TERRITORIES


@app.route('/')
def get_homepage():
    """Returns homepage."""

    if "username" in session:
        return redirect("/park_search")
    else:    
        return render_template("homepage.html")

# TODO: fix 
@app.route('/park_search')
def park_search():
    """Returns search page"""

    opt_topics = crud.return_all_topics()

    return render_template("park_search.html", topics=opt_topics, STATES=STATES)

# need to figure out how to limit box selection and return proper page.
# also include state selection.


@app.route('/search_results', methods = ["POST"])
def show_search_results():
    """View results of the search."""

    # get all the inputs from the user.
    topics = request.form.getlist("topic")
    fullstate = request.form.get("state")
    user_state = us.states.lookup(fullstate).abbr
    # print("*****", topics, "********")
    resulting_parks = {}
    final_parks = {}

    for topic in topics:
        # Gets park associated with each topic and appends to list for further parsing
        resulting_parks[topic] = crud.get_park_by_userstate(topic, user_state)
        print("*****", resulting_parks, "********")
    
    # for park in resulting_parks:
        # edit crud function/ create one that looks at park_id and state
    #     respark = crud.get_park_by_id(park.park_id)
    #     if respark.state == userstate:
    #         final_parks.append(respark)

    return render_template("search_results.html", 
                    parks=resulting_parks,
                    state=user_state)


@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    park = crud.get_park_by_id(park_id)
    image = crud.get_park_image(park_id)

    return render_template('park_details.html', park=park, image=image)

# Not a public facing route
@app.route('/all-users')
def show_all_users():
    """View all users."""

    users = crud.return_all_users()

    return render_template('all_users.html', users=users)

"""TODO: come back to this add to favorites route
needs to populate favorites page with user choice. Use a radio button on
park details page I think."""

# @app.route("/add_to_favorites/<park_id>")
# def add_to_favs(park_id):
#     if "favs" in session:
#         favs = session["favs"]
#     else:
#         favs = session["favs"] = {}
    
#     favs[park_id] = session.get(park_id)
#     flash("Your park was successfully added")

#     return redirect("/user_details")

"""Need to look at figure out populating the parks before I can do this part"""
# @app.route('/all-users/<user_id>')
# def user_details(user_id):
#     """Show details on specific user"""

#     user = crud.get_user_by_id(user_id)

#     parks_in_favs = []
#     favs = session["favs"]
    
#     for park_id in favs.items():
#         park = crud.get_by_park_id(park_id)
#         parks_in_favs.append(park)

#     # print(favs)


#     return render_template('user_details.html', 
#                             user=user,
#                             parks_in_favs=parks_in_favs)


@app.route('/users', methods = ['POST'] )
def register_user():
    """Get inputs from form"""

    email = request.form.get('email')
    password = request.form.get('password')
    uname = request.form.get('uname')
    user = crud.get_user_by_email(email)


    if user == None:
        crud.create_user(email, password, uname)
        flash('Account created! You can now log in.')
    else:    
        flash('Email already exists. Try again.')

    return redirect('/')

@app.route('/login', methods = ['POST'])
def log_in():
    """Gets input from log-in and checks to see if emails and passwords
    match."""

    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if (email == user.email) and password == user.password:
        session['user'] = user.user_id
        uname = user.uname
        flash(f'Welcome {uname}!')
        return redirect("/park_search")
    else:
        flash('Email and password do not match.')
        return redirect('/')
    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


"""
TODO:
Do I change parks_by_state.html to parks? so the page is used for 
multiple search types? I think yes.
Add a funtion for a user to add a park to favorites.


"""
