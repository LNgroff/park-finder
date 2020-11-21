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

os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined


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


@app.route('/search_results', methods = ["POST"])
def show_search_results():
    """View results of the search."""

    # get all the inputs from the user.
    topics = request.form.getlist("topic")
    fullstate = request.form.get("state")

    # resulting_parks = set()
    # final_parks = []

    resulting_parks = {}
    final_parks = {}

    userstate = us.states.lookup(fullstate).abbr

    for topic in topics:
        # resulting_parks[topic] = crud.get_park_image_topic(topic, userstate)
        results = crud.get_parktopic_image(topic, userstate)
    image = results[0]['Image'].image_url

    return render_template("search_results.html", 
                    parks=results,
                    state=userstate,
                    image=image)

# NOTE: Ideally, each park is put in one of the lists or dictionaries above and that 
# is passes to the html. unfortunately I'm not sure how to do that properly. Need solution for if no park is found.

    # If the user selects a state but no topic:
"""    if topics == [] and fullstate != "noselection":

        userstate = us.states.lookup(fullstate).abbr
        results = crud.get_park_notopic_bystate(userstate)
        image = results[0]['Image'].image_url
        # resulting_parks.add(results).add(image)

    # if the user selects a state but no topic:
    elif fullstate == "no selection"  and topics != []:
        userstate = "none"
        
        for topic in topics:

            results = crud.get_parktopic_image_nostate(topic)
            resulting_parks[topic] = results
            # results = crud.get_parktopic_image_nostate(topic)
        image = results[0]['Image'].image_url
        # resulting_parks.add(results).add(image)

    else:
        userstate = us.states.lookup(fullstate).abbr

        for topic in topics:
            # resulting_parks[topic] = crud.get_park_image_topic(topic, userstate)
            results = crud.get_parktopic_image(topic, userstate)
            # image = results[0]['Image'].image_url
            
            for park in results:
                resulting_parks[topic] = park
                # image = results[0]['Image'].image_url
                # resulting_parks.add(image)"""
            
            # for park in results:
            #     resulting_parks[topic] = park

        # for park in resulting_parks:
        #     image = crud.get_park_image(park.park_id)
        #     final_parks.append(f"Park: park_name={park.fullname}, pic={image.url}, link={park.url}")


        # print("********", results[0]['Image'].image_url, "********")

    # return render_template("search_results.html", 
    #                 parks=results,
    #                 state=userstate,
    #                 image=image)


@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    park = crud.get_park_image(park_id)
    # image = crud.get_park_image(park_id)

    return render_template('park_details.html', park=park)

# Not a public facing route
@app.route('/all-users')
def show_all_users():
    """View all users."""

    users = crud.return_all_users()

    return render_template('all_users.html', users=users)

"""TODO: come back to this add to favorites route
needs to populate favorites page with user choice. Use a radio button on
park details page I think."""

@app.route("/parks/<park_id>/fav/save")
def add_to_favs(park_id):
    
    park = crud.get_park_by_id(park_id)
    # fav = session["fav"]

    if session["user"]:
        db_fav = crud.create_favorite(park, session["user"])
        flash("Park added!")
    else:
        flash("Log in to favorite park!")
    
    return redirect(f"/all-users/{session['user']}")

@app.route('/all-users/<user_id>')
def user_details(user_id):
    """Show details on specific user"""

    user = crud.get_user_by_id(user_id)

    parks_in_favs = []
    user_favs = crud.get_user_favs(user_id)
    
    for park_id in favs.items(): # is this correct syntax?
        park = crud.get_by_park_id(park_id)
        parks_in_favs.append(park)

    # print(favs)


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
