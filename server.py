"""Server for park finder app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from flask_login import (LoginManager, login_user, login_required,
                    logout_user, current_user)
from werkzeug.security import (generate_password_hash, check_password_hash)
from urllib.parse import urlparse, urljoin
from jinja2 import StrictUndefined
import os
import us
from sqlalchemy import text
import json

from model import connect_to_db
import crud



app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY")
app.secret_key = "aJlHh;p'lBBTH,ULG1Ysli2OP%nOdwZV2^{aZO<8{%#5d{B9q#--|qG-JS}cP{I"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)


STATES = us.states.STATES_AND_TERRITORIES


@app.route('/')
def get_landing_page():
    """Returns landing."""
    
    image = crud.get_random_image()

    return render_template("landing.html", image=image)

@app.route('/home')
def get_homepage():
    """Returns homepage."""

    image = crud.get_image(158)

    return render_template("homepage.html", image=image)    
    

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
    # If the user makes no selection, ask them to.
    if topics == [] and fullstate == "no selection":

        flash("Please select at least one features or a state.")
        return redirect("/park_search")

    
    # If the user selects a state but no topic:
    if topics == [] and fullstate != "no selection":
        
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


@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    # gets park instance
    park = crud.get_park_by_id(park_id)
    
    # gets all images
    images = crud.get_park_image(park_id)

    topics = crud.get_parks_topics(park_id)

    return render_template('park_details.html', park=park, images=images, topics=topics)

@app.route('/images')
def get_images(park_id):
    """Get images for a specific park"""

    return crud.get_park_image(park_id)


# Not a public facing route, admin only? can delete?
# @app.route('/all-users')
# def show_all_users():
    # """View all users."""

    # users = crud.return_all_users()

    # return render_template("all_users.html", users=users)


@app.route("/parks/<park_id>/fav-save")
def add_to_favs(park_id):
    """Allows user to save a park to thier profile"""
    
    # Gets current page to reload
    referer = request.headers.get("Referer")
    
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
def user_details(user_id):
    """Show user detail page with their saved parks"""

    if current_user.is_authenticated:

        # Get user to access user_id
        user = crud.get_user_by_id(user_id)

        # Create a dictionary for user favs
        user_favs = {}
        results = crud.get_user_favs(user_id)
        
        # Checks if user has saved and parks.
        if results == []:
            user_favs = []
        
        # Set iterable dictionary of user favs
        else:
            for result in results:

                park = result["Park"]
                park_image = result["Image"]
                
                user_favs[park.park_id] = {"park_id" : park.park_id,\
                    "image" : park_image.image_url, "fullname" : park.fullname}


        return render_template('user_details.html', 
                                user=user,
                                parks=user_favs)
    else:
        flash("Please log in to view your favorite parks.")
        
        # Gets current page to reload
        referer = request.headers.get("Referer")
        return redirect(referer)


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

            # Encrypt user password
            secure_password = generate_password_hash(password, method ="sha256")
            
            # Create new user
            crud.create_user(email, secure_password, uname)
            flash('Account created! You can now log in.')


    # Ask user to complete all fields
    else:
        flash('Please fill out all fields.')

    # Gets current page to reload
    referer = request.headers.get("Referer")
    return redirect(referer)


@login_manager.user_loader
def load_user(user_id):
    """"Flask user loader"""

    # Get user object with given id
    return crud.get_user_by_id(user_id)


def is_safe_url(target):
    """Checks to see if url is safe."""
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc


@app.route('/login', methods = ['GET','POST'])
def log_in():
    """Gets input from log-in and checks to see if emails and passwords
    match."""

    #Gets current page to reload upon completion
    referer = request.headers.get("Referer")

    # Get email from log in form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check that user entered all info and that it's correct info:
    if email and password:

        # Get user by email in database
        user = crud.get_user_by_email(email)

        # If user exists, check if passwords match, log in user or announce failure
        if user:

            if check_password_hash(user.password, password):
                login_user(user)
                flash(f'Logged in. Welcome {user.uname}!')

                next = request.args.get('next')

                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or referer)

            else:
                flash('Email and password do not match. Try again.')
        
        # Notify user that no email exists in system
        else: 
            flash("No account is associated with this email, please register.")        

    # Ask user to complete all fields
    else:
        flash("Please fill out all fields.")
        
        
    return redirect(referer)


@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    """Log a user out."""

    logout_user()
    flash("Logged out!")
    

    return redirect('/home')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    

