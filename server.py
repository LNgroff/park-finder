"""Server for park finder app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from model import connect_to_db
import crud
import os
import us

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined

TOPICS = ["Ancient Seas", "Animals", "Archeology", "Arctic", 
        "Burial, Cemetery and Gravesite", "Canyons and Canyonlands",
        "Caves, Caverns and Karst", "Coasts, Islands and Atolls", 
        "Dams", "Dunes", "Estuaries and Mangroves", "Fire", 
        "Foothills, Plains and Valleys", "Forests and Woodlands",
        "Fossils and Paleontology", "Geology", "Geothermal", "Glaciers",
        "Grasslands", "Groundwater", "Impact Craters", "Lakes", "Mountains",
        "Natural Sounds", "Night Sky", "Oceans", "River and Riparian", 
        "Rock Landscapes and Features", "Scenic Views", "The Tropics",
        "Thickets and Shrublands", "Trails", "Volcanoes", "Waterfalls",
        "Wetlands", "Wilderness"]

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
def search_options():
    """Returns search page"""

    # location = request.form.args("state")

    # if location == "--":
    #     # location equals none, no argument passed.
    # else:
    #     location = us.states


    return render_template("park_search.html", TOPICS=TOPICS, STATES=STATES)

# need to figure out how to limit box selection and return proper page.
# also include state selection.


@app.route('/search_results', methods = ["POST"])
def show_search_results():
    """View results of the search."""

    # get all the inputs from the user.
    topics = request.form.getlist("topic")
    fullstate = request.form.get("state")
    state = us.states.lookup(fullstate).abbr

    """TODO: should this next piece go in seeds?"""
    # list to be used for api request if needed.
    topic_inputs =[]
    # list of parks for results = []
    # results = crud.get_park_SOMEVALUE
    
    for topic in topics:
        topic_result = crud.get_topic_by_name(topic)
        topic_result_id = topic_result.topic_id

        """ this is where I'd search a cache for parks. Psuedo code:
            
        if topic_result_id in cache: would this be topic result or park?
            for park in parks pertaining to topic:
                if park.state == state input from user:
                    list of parks.append(park)
        if topic not in cache make request:
            topic_iputs.append(topic_result_id)
            
            #this is on the wrong level.
            separator = "%2C"
            topic_url_input = separator.join(topic_url_input)   
            get request topicparks_url = f"https://developer.nps.gov/api/v1/topics/parks?id={topic_input}"
            parks_result = topicparks_url
                for park in parks_request:
                    crud.create_park(park[details]...)

            
    
            
        """


    """topic_url_input can be put into seeds's topicparks_url for 
    the get request
    """

    return render_template("search_results.html", 
                            parks=parks)

    """ 
    The following block of code works if a state is selected
    If no state is selected an attribute error occurs:
        'AttributeError: 'NoneType' object has no attribute 'abbr'"
    Have rewritten a number of ways. particularly with the return
    statement outside of the if else statement.
    """
    # if us.states.lookup(fullstate) == "no selection":
    #     return render_template("search_results.html", 
    #                     topics=topics,
    #                     state=fullstate)
    # else:
    #     state = (us.states.lookup(fullstate)).abbr
    #     return render_template("search_results.html", 
    #                             topics=topics,
    #                             state=state)
    """
    used as a test:
    return render_template("search_results.html", 
                        topics=topics,
                        state=state)
    """
"""
    TODO: parse through topics and grab arguments to use in request
    to API.

    I think I need something like this:
        >>> payload = {'name': 'hello', 'data': 'hello'}
        >>> r = requests.get("http://example.com/api/params", params=payload)
    And then the payload dictionary is topic:value and state:value.
    Would I need an if statement for two different requests based on
    whether topics or states are included?
"""
    # payload = {"topic_list" : json.dumps(topics)}

    

@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    park = crud.get_park_by_id(park_id)

    return render_template('park_details.html', park=park)

# Not a public facing route
@app.route('/all-users')
def show_all_users():
    """View all users."""

    users = crud.return_all_users()

    return render_template('all_users.html', users=users)

"""TODO: come back to this add to favorites route
needs to populate favorites page with user choice."""

# @app.route("/add_to_favorites/<park_id>")
# def add_to_favs(park_id):
#     if "favs" in session:
#         favs = session["favs"]
#     else:
#         favs = session["favs"] = {}
    
#     favs[park_id] = session.get(park_id)
#     flash("Your park was successfully added")

#     return redirect("/user_details")


@app.route('/all-users/<user_id>')
def user_details(user_id):
    """Show details on specific user"""

    user = crud.get_user_by_id(user_id)

    parks_in_favs = []
    favs = session["favs"]
    
    for park_id in favs.items():
        park = crud.get_by_park_id(park_id)
        parks_in_favs.append(park)

    print(favs)


    return render_template('user_details.html', 
                            user=user,
                            parks_in_favs=parks_in_favs)


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
        return render_template("/park_search")
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
