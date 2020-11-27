"""Server for park finder app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from flask_login import (LoginManager, login_user, login_required,
                    logout_user, current_user)
from werkzeug.security import (generate_password_hash, check_password_hash)
from jinja2 import StrictUndefined
import os
import us
from sqlalchemy import text
import json

from model import connect_to_db
import crud


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)


STATES = us.states.STATES_AND_TERRITORIES


@app.route('/')
def get_homepage():
    """Returns homepage."""

    return render_template("homepage.html")


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

    resulting_parks = {}

    # If the user selects a state but no topic:
    if topics == [] and fullstate != "noselection":
        
        # convert state to postal code and perform search by state
        userstate = us.states.lookup(fullstate).abbr
        results = crud.get_park_notopic_bystate(userstate)
        
        # Loop through each park in results and get needed values
        # Store in resulting_parks dict
        for result in results:

                park = result["Park"]
                park_image = result["Image"]
                
                resulting_parks[park.park_id] = {"park_id" :  park.park_id,\
                    "image" : park_image.image_url, "fullname" : park.fullname}
                
        return render_template("search_results.html", 
                        parks=resulting_parks,
                        state=userstate)


    # if the user selects a state but no topic:
    elif fullstate == "no selection"  and topics != []:
        
        # Set the userstate to none, no conversion necessary
        userstate = "none"
        
        # Perform search for each topic chosen by user
        for topic in topics:
            results = crud.get_parktopic_image_nostate(topic)

            # Loop through each park in results and get needed values
            # Store in resulting_parks dict
            for result in results:

                    park = result["Park"]
                    park_image = result["Image"]
                    
                    resulting_parks[park.park_id] = {"park_id" :  park.park_id,\
                        "image" : park_image.image_url, "fullname" : park.fullname}
                    

        return render_template("search_results.html", 
                        parks=resulting_parks,
                        state=userstate)

    # If the user selects a state and topic:
    else:
        
        # Set user state to postal code abreviation
        userstate = us.states.lookup(fullstate).abbr

        for topic in topics:
            # resulting_parks[topic] = crud.get_park_image_topic(topic, userstate)
            results = crud.get_parktopic_image(topic, userstate)
            
            # Loop through each park in results and get needed values
            # Store in resulting_parks dict
            for result in results:

                park = result["Park"]
                park_image = result["Image"]
                
                resulting_parks[park.park_id] = {"park_id" :  park.park_id,\
                    "image" : park_image.image_url, "fullname" : park.fullname}

        return render_template("search_results.html", 
                        parks=resulting_parks,
                        state=userstate)

# TODO: Image gallery
@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    # gets park instance
    park = crud.get_park_by_id(park_id)
    
    # gets all images
    images = crud.get_park_image(park_id)

    return render_template('park_details.html', park=park, images=images)


# Not a public facing route, admin only? can delete?
# @app.route('/all-users')
# def show_all_users():
    # """View all users."""

    # users = crud.return_all_users()

    # return render_template("all_users.html", users=users)


@app.route("/parks/<park_id>/fav-save")
@login_required
def add_to_favs(park_id):
    
    # Get the park object to access the park_id
    park = crud.get_park_by_id(park_id)
    
    # If current user is logged in
    if current_user.is_authenticated:

        # Get instance of user fav for selected park
        user_favs = crud.user_favs_by_park(current_user.get_id(), park.Park.park_id)

        # If user has already saved the park, inform user.
        if user_favs:
            flash("You have already saved this park.")
            return redirect(f"/parks/{park.Park.park_id}")

        # Otherwise, create new fav for user.
        else:
            fav = crud.create_favorite(park.Park.park_id, current_user.get_id())
            flash("Park added!")
            
            return redirect(f"/user/{current_user.get_id()}")
    
    # If user is not logged in, ask to log in 
    else:
        flash("Log in to add park to favorites!")
    
        return redirect(f"/parks/{park.Park.park_id}")


@app.route('/user/<user_id>')
@login_required
def user_details(user_id):
    """Show user detail page with their saved parks"""

    # Get user to access user_id
    user = crud.get_user_by_id(user_id)

    # Create a dictionary for user favs
    user_favs = {}
    results = crud.get_user_favs(user_id)
    
    # Checks if user has saved and parks.
    if results == []:
        user_favs = "You do not have not saved any parks."
    
    # Set iterable dictionary of user favs
    else:
        for result in results:

            park = result["Park"]
            park_image = result["Image"]
            
            user_favs[park.park_id] = {"park_id" : park.park_id,\
                "image" : park_image.image_url, "fullname" : park.fullname}

        print('********', user_favs, '***********')


    return render_template('user_details.html', 
                            user=user,
                            parks=user_favs)


@app.route('/users', methods = ['POST'] )
def register_user():
    """Get inputs from Creat Account form"""

    # Get inputs from the create account form
    email = request.form.get('email')
    password = request.form.get('password')
    uname = request.form.get('uname')
    
    # Check that user entered all info and that it's correct info:
    if email and password and uname:

        # Get user by email from database
        user = crud.get_user_by_email(email)

        # Check that user doesn't already exist
        if user:
            # Let user know an account with that email already exists.
            flash('Email already exists. Try again.')
        
        else:    
            # TODO: somehow check valid email

            # Encrypt user password
            secure_password = generate_password_hash(password, method ="sha256")
            
            # Create new user
            crud.create_user(email, secure_password, uname)
            flash('Account created! You can now log in.')


    # Ask user to complete all fields
    else:
        flash('Please fill out all fields.')

    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    """"Flask user loader"""

    # Get user object with given id
    return crud.get_user_by_id(user_id)


@app.route('/login', methods = ['POST'])
def log_in():
    """Gets input from log-in and checks to see if emails and passwords
    match."""

    # Get email from log in form
    email = request.form.get('email')

    # Get user by email in database
    user = crud.get_user_by_email(email)

    # If user exists, check if passwords match, log in user or announce failure
    if user:

        if check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash(f'Logged in. Welcome {user.uname}!')
            
            return redirect("/park_search")
        else:
            flash('Email and password do not match. Try again.')
            return redirect('/')
    
    # Notify user that no email exists in system
    else: 
        flash("No account is associated with this email.")        
        return redirect('/')
    

@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    """Log a user out."""
        
    logout_user()
    flash("Logged out!")
    
    return redirect("/")




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

